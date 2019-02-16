# Generate Test Collections and Tests for SQL-Unit

import os, sys, json
import utils

class TestGenerator:

    def __init__(self, config):
        # TODO If exception in init, exit
        print("Test Generator created.")
        self.config = config
        self.testManagerJson = utils.readJson(config["test-manager"])
        self.testCollections = self.testManagerJson["test-collections"]
        utils.createFolderIne(config["test-folder"])

    def createTest(self, inputData, collection):
        sanitName = utils.sanitizeFilename(inputData["name"])
        return {
            "id": utils.getIncrementedId(collection["tests"]),
            "type": "test",
            "name": sanitName,
            "description": inputData["description"],
            "sql": sanitName + ".sql",
            "expected": sanitName + "-expected.json",
            "actual": sanitName + "-actual.json"
        }
    
    def createCollection(self, inputData):
        return {
            "id": utils.getIncrementedId(self.testCollections),
            "type": "collection",
            "name": utils.sanitizeFilename(inputData["name"]),
            "description": inputData["description"],
            "config": inputData["config"],
            "tests": []
        }

    def getTestFolderName(self, collection, test):
        return self.config["test-folder"] + "/" + collection["name"] + "/" + test["name"]
    
    def writeTestFiles(self, collection, test):
        testFolder = self.getTestFolderName(collection, test)
        utils.createFolderIne(testFolder)
        utils.writeFile(testFolder + "/" + test["sql"], "-- Generated with SQL-Unit --")
        utils.writeFile(testFolder + "/" + test["expected"], "{}")
        utils.writeFile(testFolder + "/" + test["actual"], "{}")

    def addTest(self, collectionIdx, inputData):
        targetCollection = utils.getElemById(self.testCollections, collectionIdx)
        newTest = self.createTest(inputData, targetCollection)
        out = "[INFO] Adding test " + utils.keyvalStr(newTest["id"], newTest["name"])
        print(out + " to test collection " + utils.keyvalStr(targetCollection["id"], targetCollection["name"]))
        targetCollection["tests"].append(newTest)
        self.refreshJson()
        self.writeTestFiles(targetCollection, newTest)

    def addCollection(self, inputData):
        newCollection = self.createCollection(inputData)
        print("[INFO] Adding collection " + utils.keyvalStr(newCollection["id"], newCollection["name"]))
        self.testCollections.append(newCollection)
        self.refreshJson()

    def removeTest(self, collectionIdx, testIdx):
        targetCollection = utils.getElemById(self.testCollections, collectionIdx)
        tests = targetCollection["tests"]
        targetTest = utils.getElemById(tests, testIdx)
        if targetTest != "":
            out = "[INFO] Removing test " + utils.keyvalStr(targetTest["id"], targetTest["name"])
            print(out + " from test collection " + utils.keyvalStr(targetCollection["id"], targetCollection["name"]))
            tests.remove(utils.getElemById(tests, testIdx))
            self.refreshJson()
            utils.deleteDirectory(self.config["test-folder"] + "/" + targetCollection["name"] + "/" + targetTest["name"])

    def removeCollection(self, collectionIdx):
        targetCollection = utils.getElemById(self.testCollections, collectionIdx)
        if targetCollection != "":
            print("[INFO] Removing collection " + utils.keyvalStr(targetCollection["id"], targetCollection["name"]))
            self.testCollections.remove(utils.getElemById(self.testCollections, collectionIdx))
            self.refreshJson()
            utils.deleteDirectory(self.config["test-folder"] + "/" + targetCollection["name"])
    
    def refreshJson(self):
        for collection in self.testCollections:
            utils.regenerateIds(collection["tests"])
        utils.regenerateIds(self.testCollections)
        utils.writeJson(self.config["test-manager"], self.testManagerJson)

    def removeAllCollections(self):
        self.testCollections.clear()
        self.refreshJson()
    
    def removeAllTests(self, collectionIdx):
        utils.getElemById(self.testCollections, collectionIdx)["tests"].clear()
        self.refreshJson()


# TODO Handle duplicate naming/deleting for collections+tests
# TODO Stats function for returning info on test/collection count