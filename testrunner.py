# Runs all tests located in test folder

import os
import utils
from glob import glob


class TestRunner():
    
    def __init__(self, config):
        utils.log("Test Runner initialized.")
        self.config = config
        self.collectionsPath = config["test-collections"]

    def before(self, collectionName):
        utils.log("Configuring Test Runner")
        fileTargets = [".sql", "-expected.json", "-actual.json", "-config.json"]
        self.targetCollection = collectionName
        #print(collectionFolders)

        self.collections = {"collections": []}
        for folder in glob(self.collectionsPath + "\\*\\"):
            collection = {"name": utils.getSplitLast(folder, "\\", 1), "path": utils.getCwd() + folder, "tests": []}
            for testfolder in glob(folder + "*\\"):
                test = {"name": utils.getSplitLast(testfolder, "\\", 1), "path": utils.getCwd() + testfolder, "files": []}
                collection["tests"].append(test)
                for file in glob(testfolder + "*.*"):
                    filename = utils.getSplitLast(file, "\\")
                    for target in fileTargets:
                        if filename == utils.getSplitLast(test["path"], "\\", 1) + target:
                            utils.log("Found " + test["path"] +  filename)       
            self.collections["collections"].append(collection)

    def run(self):
        utils.log("Running test set [" + self.targetCollection + "]")
        print(self.collections)

    def after(self):
        utils.log("Test Runner finished.")


def main():
    runner = TestRunner(utils.readJson(utils.getCwd() + "\\config.json"))
    collectionName = "WASD" # TODO shell script passing set name
    runner.before(collectionName)
    #runner.run()
    #runner.after()

if __name__=='__main__': main()