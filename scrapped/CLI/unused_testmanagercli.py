# CLI for Test Manager

import os, sys
import utils, testmanager

class TestManagerCli:
    
    def __init__(self, args, configpath):
        if len(args) == 1: args.append("-h")
        self.args = args
        self.config = utils.readJson(configpath)
        self.cmds = self.config["commands"]
        self.flags = self.config["flags"]
        self.tm = testmanager.TestManager(self.config)

    def printHelp(self, cmd):
        print("FORMAT ->  [COMMAND] [FLAG] [ARG1] ... [ARGN]")
        print("COMMANDS:")
        utils.printArgList(self.cmds, ["command","desc"])
        print("FLAGS:")
        utils.printArgList(self.flags, ["flag","desc"])

    def printInfo(self, cmd):
        info = self.config["info"]
        for i in info: print(i + ": " + info[i])

    def printVersion(self, cmd):
        print("version: " + self.config["info"]["version"])

    def refreshJson(self, cmd):
        self.tm.refreshJson()
    
    def debugFunc(self, cmd):
        utils.log("Debug function called")
        self.tm.refreshCollections()

    def getFuncDict(self):
        return {
            "-h": self.printHelp,
            "-f": self.refreshJson, 
            "-i": self.printInfo,
            "-j": self.genJson, 
            "-l": self.printList,
            "-r": self.removeSingle,
            "-s": self.genSingle, 
            "-t": self.genText, 
            "-v": self.printVersion,
            "-x": self.genXml,
            "-debug": self.debugFunc
        }

    def genSingle(self, cmd):
        collectName = self.args[3]
        if self.args[1] == "test":
            testName = self.args[4]
            utils.log("Generating test [" + testName + "] in collection [" + collectName + "]")
            collections = self.tm.getCollections()
            if utils.getElemById(collections, collectName, "name") == "":
                utils.log("Collection [" + collectName + "] not found. Generating new collection.")
                self.tm.addCollection(self.configureCollection(collectName))
            self.tm.addTest(utils.getElemById(collections, collectName, "name")["id"], self.configureTest(testName))
        elif self.args[1] == "collection":
            self.tm.addCollection(self.configureCollection(collectName))
    
    def removeSingle(self, cmd):
        collectName = self.args[3]
        if self.args[1] == "test":
            self.tm.removeTestByName(collectName, self.args[4]) 
        elif self.args[1] == "collection":
            self.tm.removeCollectionByName(collectName)

    def configureTest(self, testName):
        utils.log("Configuring test [" + testName + "]")
        return {"name": testName, "description": utils.getInput("Test description", default=testName)}
    
    def configureCollection(self, collectName):
        utils.log("Configuring collection [" + collectName + "]")
        defaults = self.tm.getDefaultCollectionConfig(collectName)
        return {
            "name": collectName,
            "description": utils.getInput("Collection description", default=collectName),
            "config": { # TODO Can this be looped over ?
                "server": utils.getInput("Server Name", default=defaults["server"]),
                "dialect": utils.getInput("SQL Dialect", choices=["MSSQL","DB2"], default=defaults["dialect"]),
                "keep-results": utils.getInput("Result sets to store", inType="int+", default=defaults["keep-results"]),
                "fail-threshold": utils.getInput("Fail threshold", inType="int+", default=defaults["fail-threshold"]),
                "measure-performance": utils.getInput("Measure Performance?", inType="bool", default=defaults["measure-performance"]),
                "record-results": utils.getInput("Record Results?", inType="bool", default=defaults["record-results"]),
                "generate-report": utils.getInput("Generate Reports?", inType="bool", default=defaults["generate-report"]),
                "allow-stored-procedures": utils.getInput("Allow Stored Procedures?", inType="bool", default=defaults["allow-stored-procedures"])
            }
        }

    def printList(self, cmd):
        if self.args[1] == "test":
            collection = self.tm.getCollectionByName(self.args[3])
            print("collection: " + utils.keyvalStr(collection["id"], collection["name"]))
            for test in collection["tests"]:
                print("   test: " + utils.keyvalStr(test["id"], test["name"]))
        elif self.args[1] == "collection":
            print("All collections: ")
            for coll in self.tm.getCollections():
                print("   collection: " + utils.keyvalStr(coll["id"], coll["name"]))

    def genJson(self):
        # TODO
        return

    def genText(self):
        # TODO
        return

    def genXml(self):
        # TODO
        return

    def processArgs(self):
        try:
            cmd = self.args[1].lower()
            flag = self.args[2].lower()
            if utils.isValidArg(flag, self.flags, "flag") and utils.isValidArg(cmd, self.cmds, "command"):
                self.tm.refreshJson()
                self.getFuncDict()[flag](cmd)
        except IndexError:
            if len(self.args) == 2 and self.args[1].lower() in ["-f","-h","-i","-v", "-debug"]:
                self.getFuncDict()[self.args[1].lower()]("")
            else:
                utils.printCliError("Not enough arguments")

def main():
    TestManagerCli(sys.argv, "./config.json").processArgs()


if __name__=='__main__': main()