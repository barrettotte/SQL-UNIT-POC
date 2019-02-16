# Driver for TestGenerator

import sys
import utils, testgenerator

class CliObj:
    
    def __init__(self, args):
        self.args = args
        self.helpData = utils.readJson(utils.getCwd() + "\cli-config.json")
        self.cmds = self.helpData["commands"]
        self.flags = self.helpData["flags"]

    def printHelp(self, cmd):
        print("FORMAT ->  [COMMAND] [FLAG] [ARG1] ... [ARGN]")
        print("COMMANDS:")
        utils.printArgList(self.cmds, ["command","desc"])
        print("FLAGS:")
        utils.printArgList(self.flags, ["flag","desc"])

    def printInfo(self, cmd):
        info = self.helpData["info"]
        for i in info: print(i + ": " + info[i])

    def printVersion(self, cmd):
        print("version: " + self.helpData["info"]["version"])

    def getFuncDict(self):
        return {
            "-h": self.printHelp, 
            "-i": self.printInfo,
            "-j": self.genJson, 
            "-l": self.printList,
            "-r": self.removeSingle,
            "-s": self.genSingle, 
            "-t": self.genText, 
            "-v": self.printVersion,
            "-x": self.genXml
        }

    def genSingle(self, cmd):
        collectName = self.args[3]
        if self.args[1] == "test":
            testName = self.args[4]
            utils.log("Generating test [" + testName + "] in collection [" + collectName + "]")
            collections = self.gen.getCollections()
            if utils.getElemById(collections, collectName, "name") == "":
                utils.log("Collection [" + collectName + "] not found. Generating new collection.")
                self.gen.addCollection(self.configureCollection(collectName))
            self.gen.addTest(utils.getElemById(collections, collectName, "name")["id"], self.configureTest(testName))
        elif self.args[1] == "collection":
            self.gen.addCollection(self.configureCollection(collectName))
    
    def removeSingle(self, cmd):
        collectName = self.args[3]
        if self.args[1] == "test":
            self.gen.removeTestByName(collectName, self.args[4]) 
        elif self.args[1] == "collection":
            self.gen.removeCollectionByName(collectName)

    def configureTest(self, testName):
        utils.log("Configuring test [" + testName + "]")
        return {"name": testName, "description": utils.getInput("Test description", default=testName)}
    
    def configureCollection(self, collectName):
        utils.log("Configuring collection [" + collectName + "]")
        return {
            "name": collectName,
            "description": utils.getInput("Collection description", default=collectName),
            "config": {
                "server": utils.getInput("Server Name"),
                "dialect": utils.getInput("SQL Dialect", choices=["MSSQL","DB2"], default="MSSQL"),
                "keep-results": utils.getInput("Result sets to store", inType="int+", default=25),
                "fail-threshold": utils.getInput("Fail threshold", inType="int+", default=0),
                "measure-performance": utils.getInput("Measure Performance?", inType="bool", default="Y"),
                "record-results": utils.getInput("Record Results?", inType="bool", default="Y"),
                "generate-report": utils.getInput("Generate Reports?", inType="bool", default="Y"),
                "allow-stored-procedures": utils.getInput("Allow Stored Procedures?", inType="bool", default="Y")
            }
        }

    def printList(self, cmd):
        if self.args[1] == "test":
            collection = self.gen.getCollectionByName(self.args[3])
            print("collection: " + utils.keyvalStr(collection["id"], collection["name"]))
            for test in collection["tests"]:
                print("   test: " + utils.keyvalStr(test["id"], test["name"]))
        elif self.args[1] == "collection":
            print("All collections: ")
            for coll in self.gen.getCollections():
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
                self.gen = testgenerator.TestGenerator(utils.readJson("./config.dev.json"))
                self.getFuncDict()[flag](cmd)
        except IndexError:
            if len(self.args) == 2 and self.args[1].lower() in ["-h","-i","-v"]:
                self.getFuncDict()[self.args[1].lower()]("")
            else:
                utils.printCliError("Not enough arguments")

def main():
    args = sys.argv
    if len(args) == 1:
        args.append("-h")
    cli = CliObj(args)
    cli.processArgs()


if __name__=='__main__': main()
