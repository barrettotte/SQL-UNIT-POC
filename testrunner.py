import pyodbc, utils, time
from glob import glob


class SQLTestRunner():
    

    def __init__(self, config, target):
        utils.log("SQL Test Runner initializing", init=True)
        self.config = config
        self.suitesPath = config["test-suites"]
        self.target = target
        self.currentDbConfig = {}
        self.testResults = []


    def execute(self):
        self.setUp()
        self.run()
        self.tearDown()


    def setUp(self):
        utils.log("SQL Test Runner using directory [" + self.suitesPath + "]")
        self.suites = self.loadSuites(self.suitesPath) # Not optimal loading all, but its POC
        self.targetSuite = utils.getElemByKey(self.target, "name", self.suites)
        if self.targetSuite:
            utils.log("SQL Test Runner targeted with suite [" + self.targetSuite["name"] + "]")
            try:
                utils.log("Initializing SQLUnit_Wrapper Stored Procedure")
                self.connection = pyodbc.connect(self.getConnectDetails())
                self.connection.autocommit = False
                self.connection.cursor().execute(("".join(utils.readFile("./wrapper.sql"))))
                self.connection.commit()
            except:
                utils.log("Could not initialize stored procedure", "ERROR")
        else:
            utils.log("Could not find [" + self.target + "]", "ERROR")
            exit()


    def run(self):
        passedTests = []
        suiteTime = time.time()
        if self.targetSuite:
            testLen = len(self.targetSuite["tests"])
            utils.log("Running suite [" + self.targetSuite["name"] + "] with " + str(testLen) + " test(s)")

            for idx, test in enumerate(self.targetSuite["tests"]):
                startTime = time.time()
                utils.log("Running test " + ("[" + test["name"] + "] ").ljust(30) + "(" + str(idx+1) + " of " + str(testLen) + ")", pref=" "*3)
                fileDefs = self.getTestFiles(test)
                results = self.runSQLTest(fileDefs)
                endTime = time.time()
                expected = utils.readJson(fileDefs["expected"]["path"])
                passed = self.evaluateResults(results, expected)
                if expected["success"] == "false" and not passed:
                    passed = True
                passedTests.append(passed)
                utils.log("Test execution in " + str(round(((endTime-startTime)*1000), 4)) + " ms", pref=" "*6)

            suiteResults = {
                "name": self.targetSuite["name"],
                "total": len(passedTests),
                "passed": passedTests.count(True),
                "time": round(((time.time()-suiteTime)*1000), 4),
                "tests": self.targetSuite["tests"]
            }
            utils.log("Results: " + str(suiteResults["passed"]) + " of " + str(suiteResults["total"]) + " test(s) passed")
            utils.log("Suite execution in " + str(suiteResults["time"]) + " ms")
            utils.createFolderIne(self.config["results-output"])
            utils.writeJson(self.config["results-output"] + self.targetSuite["name"] + ".results.json", suiteResults)
        else:
            utils.log("Test suite [" + self.targetSuite["name"] + "] could not be found.", "ERROR")


    def tearDown(self):
        utils.log("Cleaning up database and connection")
        try:
            self.connection.cursor().execute("DROP PROCEDURE [dbo].[SQLUnit_Wrapper]")
            self.connection.commit()
        except pyodbc.Error:
            utils.log("Database cleanup failed", "ERROR")
        self.connection.close()
        utils.log("SQL Test Runner finished")

    
    def evaluateResults(self, actualArr, expectedJson):
        pref = " "*6
        try:
            for idx, expected in enumerate(expectedJson["rows"]):
                for k, v in expected.items():
                    if "__SQLUnit_FAILED__" in actualArr[idx] or expected[k] != actualArr[idx][k]:
                        utils.log("Test Failed", pref="X" + pref)
                        return False
        except:
            utils.log("Evaluation exception", "ERROR", pref=pref)
            utils.log("Test Failed", pref="X" + pref[:-1])
            return False
        utils.log("Test Passed", pref=pref)
        return True


    def runSQLTest(self, fileDefs):
        utils.log("Executing [" + fileDefs["sql"]["name"] + "]", pref=" "*6)    
        sql = ("".join(utils.readFile(fileDefs["sql"]["path"]))).replace("'", "&!SQ!&").replace("\n","&!NL!&")
        columnDefs = []
        for col in utils.readJson(fileDefs["expected"]["path"])["columns"]:
            columnDefs.append(col["name"] + " " + col["type"])
        params = (sql, ("|,|".join(columnDefs)+"|,|"))
        wrappedSQL = "{ CALL SQLUnit_Wrapper (@SQL_STRING=?, @RES_COLS=?) }"
        results = []
        try:
            cursor = self.connection.cursor().execute(wrappedSQL, params)
            resCols = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                results.append(dict(zip(resCols, row)))
            self.connection.commit()
        except pyodbc.Error:
            utils.log("SQL Query failed", pref=" "*6)
        utils.writeJson(fileDefs["actual"]["path"], results)
        return results
        

    def getTestFiles(self, test):
        utils.log("Reading files", pref=" "*6)
        return {
            "sql": utils.getElemByKey(test["name"] + ".sql", "name", test["files"]),
            "expected": utils.getElemByKey(test["name"] + ".expected.json", "name", test["files"]),
            "actual": utils.getElemByKey(test["name"] + ".actual.json", "name", test["files"])
        }


    def loadSuites(self, path):
        utils.log("Loading all test files")
        suites = []
        # TODO Make this pythonic. quad for loop? in python? seriously? do you know how to code?
        for folder in glob(path + "\\*\\"):
            suiteName = utils.getSplitLast(folder, "\\", 1)
            suite = {"name": suiteName, "path": folder, "config": folder + suiteName + ".config.json", "tests": []}
            for testFolder in glob(folder + "*\\"):
                test = {"name": utils.getSplitLast(testFolder, "\\", 1), "path": testFolder, "files": []}
                suite["tests"].append(test)
                for file in glob(testFolder + "*.*"):
                    filename = utils.getSplitLast(file, "\\")
                    for target in [".sql", ".expected.json", ".actual.json", ".config.json"]:
                        if filename == utils.getSplitLast(test["path"], "\\", 1) + target:
                            test["files"].append({"name": filename, "path": file})
            suites.append(suite)
        utils.log("Found " + str(len(suites)) + " suite(s) in [" + path + "]")
        return suites
    

    def getConnectDetails(self):
        dbConfig = utils.readJson(self.targetSuite["config"])["database-config"]
        utils.log("Creating database connection to [" + dbConfig["server"] + "\\" + dbConfig["database"] + "]")
        self.currentDbConfig = dbConfig
        return (";".join([
            "DRIVER={ODBC Driver 13 for SQL Server}",
            "SERVER=" + dbConfig["server"],
            "DATABASE=" + dbConfig["database"],
            "Trusted_Connection=yes"
        ])) + ";"
