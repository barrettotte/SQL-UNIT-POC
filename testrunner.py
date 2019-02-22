# Runs all tests located in test folder

import pyodbc, utils
from glob import glob


class TestRunner():
    

    def __init__(self, config, target):
        utils.log("Test Runner initialized with target collection [" + target + "]", init=True)
        self.config = config
        # TODO make collectionsPath absolute, folder find try/except
        self.collectionsPath = utils.getCwd() + "\\" + config["test-collections"]
        self.targetCollection = target
        self.testResults = []


    # Gather all test-collection folders, test folders, and test files
    def before(self):
        utils.log("Creating database connection")
        ## TODO Create/Configure DB Connection
        utils.log("Loading test files")

        # TODO Make this more pythonic, quad for loop? in python? seriously?
        self.collections = {"collections": []}
        for folder in glob(self.collectionsPath + "\\*\\"):
            collection = {"name": utils.getSplitLast(folder, "\\", 1), "path": folder, "tests": []}
            for testFolder in glob(folder + "*\\"):
                test = {"name": utils.getSplitLast(testFolder, "\\", 1), "path": testFolder, "files": []}
                collection["tests"].append(test)
                for file in glob(testFolder + "*.*"):
                    filename = utils.getSplitLast(file, "\\")
                    for target in [".sql", "-expected.json", "-actual.json", "-config.json"]:
                        if filename == utils.getSplitLast(test["path"], "\\", 1) + target:
                            #utils.log("Found " + test["path"] +  filename)
                            test["files"].append({"name": filename, "path": file})
            self.collections["collections"].append(collection)
        utils.log("Found " + str(len(self.collections["collections"])) + " collection(s)")
        utils.writeJson("./loaded-tests.json", self.collections)


    def run(self):
        collection = utils.findDictInList(self.collections["collections"], self.targetCollection, "name")
        testLen = len(collection["tests"])
        utils.log("Running collection [" + self.targetCollection + "] with " + str(testLen) + " test(s)")

        #print(utils.getPrettyJson(self.collections)) #TODO debug remove
        #print(utils.getPrettyJson(collection)) #TODO debug remove
        idx = 1
        for test in collection["tests"]:
            utils.log("Running test [" + test["name"] + "] " + "(" + str(idx) + " of " + str(testLen) + ")")
            idx += 1
            #for file in test["files"]:
            #    print("   " + file["name"])

            # TODO Execute SQL in wrapper function


    def after(self):
        utils.log("Test Runner finished.")
        # TODO Evaluate test results

