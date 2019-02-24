import pyodbc, utils
from glob import glob


class SQLTestRunner():
    

    def __init__(self, config, target):
        utils.log("SQL Test Runner initializing", init=True)
        # TODO exception handling for collections path
        self.config = config
        self.collectionsPath = utils.getCwd() + "\\" + config["test-collections"]
        self.target = target
        self.currentDbConfig = {}
        self.testResults = []


    def execute(self):
        self.setUp()
        self.run()
        self.tearDown()


    def setUp(self):
        utils.log("SQL Test Runner using directory [" + self.collectionsPath + "]")
        utils.createFolderIne(self.collectionsPath)
        self.collections = self.loadCollections(self.collectionsPath) # Not optimal loading all, but its POC
        self.targetCollection = utils.getElemByKey(self.target, "name", self.collections)
        utils.log("SQL Test Runner targeted with collection [" + self.targetCollection["name"] + "]")
        self.connection = pyodbc.connect(self.getConnectDetails())


    def run(self):
        if self.targetCollection:
            testLen = len(self.targetCollection["tests"])
            utils.log("Running collection [" + self.targetCollection["name"] + "] with " + str(testLen) + " test(s)")
            idx = 1
            for test in self.targetCollection["tests"]:
                utils.log("Running test " + ("[" + test["name"] + "] ").ljust(30) + "(" + str(idx) + " of " + str(testLen) + ")", pref=" "*3)
                idx += 1
                sqlDef = utils.getElemByKey(test["name"] + ".sql", "name", test["files"])
                if sqlDef:
                    utils.log("Reading [" + sqlDef["name"] + "]", pref=" "*6)
                    sql = "".join(utils.readFile(sqlDef["path"]))
                    utils.log("Executing [" + sqlDef["name"] + "]", pref=" "*6)
                    cursor = self.connection.cursor().execute(getWrappedSql(sql))
                    for row in cursor.fetchall():
                        print(row)
        else:
            utils.log("Test collection [" + self.targetCollection["name"] + "] could not be found.", "ERROR")


    def tearDown(self):
        utils.log("SQL Test Runner finished")


    def getWrappedSQl(self, sql):
        dialect = self.currentDbConfig["dialect"]
        if dialect == "MSSQL":
            prefix = ""
        else:
            utils.fatalError("Dialect for [" + dialect + "] not supported.")


    def loadCollections(self, path):
        utils.log("Loading all test files")
        colls = []
        # TODO Make this pythonic. quad for loop? in python? seriously? do you know how to code?
        for folder in glob(path + "\\*\\"):
            collName = utils.getSplitLast(folder, "\\", 1)
            collection = {"name": collName, "path": folder, "config": folder + collName + ".config.json", "tests": []}
            for testFolder in glob(folder + "*\\"):
                test = {"name": utils.getSplitLast(testFolder, "\\", 1), "path": testFolder, "files": []}
                collection["tests"].append(test)
                for file in glob(testFolder + "*.*"):
                    filename = utils.getSplitLast(file, "\\")
                    for target in [".sql", "-expected.json", "-actual.json", "-config.json"]:
                        if filename == utils.getSplitLast(test["path"], "\\", 1) + target:
                            test["files"].append({"name": filename, "path": file})
            colls.append(collection)
        utils.log("Found " + str(len(colls)) + " collection(s) in [" + path + "]")
        utils.writeJson("./loaded.json", colls)
        return colls
    

    def getConnectDetails(self, dbConfig):
        dbConfig = utils.readJson(self.targetCollection["config"])["database-config"]
        utils.log("Creating database connection to [" + dbConfig["server"] + "\\" + dbConfig["database"] + "]")
        self.currentDbConfig = dbConfig
        return (";".join([
            "DRIVER={ODBC Driver 13 for SQL Server}",
            "SERVER=" + dbConfig["server"],
            "DATABASE=" + dbConfig["database"],
            "Trusted_Connection=yes"
        ])) + ";"
