import pyodbc, utils
from glob import glob


class SQLTestRunner():
    

    def __init__(self, config, target):
        utils.log("SQL Test Runner initializing", init=True)
        # TODO exception handling for suites path
        self.config = config
        self.suitesPath = utils.getCwd() + "\\" + config["test-suites"]
        self.target = target
        self.currentDbConfig = {}
        self.testResults = []


    def execute(self):
        self.setUp()
        self.run()
        self.tearDown()


    def setUp(self):
        utils.log("SQL Test Runner using directory [" + self.suitesPath + "]")
        utils.createFolderIne(self.suitesPath)
        self.suites = self.loadSuites(self.suitesPath) # Not optimal loading all, but its POC
        self.targetSuite = utils.getElemByKey(self.target, "name", self.suites)
        utils.log("SQL Test Runner targeted with suite [" + self.targetSuite["name"] + "]")
        
        self.connection = pyodbc.connect(self.getConnectDetails())
        utils.log("Initializing SQLUnit_Wrapper Stored Procedure")
        self.connection.autocommit = False
        self.connection.cursor().execute(("".join(utils.readFile("../wrapper.sql"))))
        self.connection.commit()


    def run(self):
        if self.targetSuite:
            testLen = len(self.targetSuite["tests"])
            utils.log("Running suite [" + self.targetSuite["name"] + "] with " + str(testLen) + " test(s)")
            for idx, test in enumerate(self.targetSuite["tests"]):
                utils.log("Running test " + ("[" + test["name"] + "] ").ljust(30) + "(" + str(idx+1) + " of " + str(testLen) + ")", pref=" "*3)
                sqlDef = utils.getElemByKey(test["name"] + ".sql", "name", test["files"])
                fileDefs = self.getTestFiles(test)
                utils.log("Reading files", pref=" "*6)
                results = self.runSQLTest(fileDefs)
                
                utils.log("\n" + utils.getPrettyJson(results)) # TODO TEMP

                self.evaluateResults(results, fileDefs)

        else:
            utils.log("Test suite [" + self.targetSuite["name"] + "] could not be found.", "ERROR")


    def tearDown(self):
        self.connection.cursor().execute("DROP PROCEDURE [dbo].[SQLUnit_Wrapper]")
        self.connection.commit()
        self.connection.close()
        utils.log("SQL Test Runner finished")

    
    def evaluateResults(self, results, fileDefs):
        pass # TODO


    # TODO TRY/CATCH with PYODBC Exception, fail 'gracefully' -- teardown
    def runSQLTest(self, fileDefs):
        utils.log("Executing [" + fileDefs["sql"]["name"] + "]", pref=" "*6)    
        sql = ("".join(utils.readFile(fileDefs["sql"]["path"]))).replace("'", "&!SQ!&").replace("\n","&!NL!&")
        columnDefs = []
        for col in utils.readJson(fileDefs["expected"]["path"])["columns"]:
            columnDefs.append(col["name"] + " " + col["type"])
        params = (sql, ("|,|".join(columnDefs)+"|,|"))
        wrappedSQL = "{ CALL SQLUnit_Wrapper (@SQL_STRING=?, @RES_COLS=?) }"
        cursor = self.connection.cursor().execute(wrappedSQL, params)

        resCols = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(resCols, row)))
        self.connection.commit()
        return results
        

    def getTestFiles(self, test):
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
        utils.writeJson("./loaded.json", suites)
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
