# Generate Test Collections and Tests for SQL-Unit


import os, sys, json
import utils


class TestGenerator:

    def __init__(self, config):
        print("Test Generator created.")
        self.config = config
        self.testManagerJson = utils.readJson(config["test-manager"])
        self.testCollections = self.testManagerJson["test-collections"]
        utils.createFolderIne(config["test-folder"])

    def createTest(self, inp, collection):
        sanitName = inp["name"].replace(" ", "") # TODO Make sure filename has no invalid characters (regex?)
        return {
            "id": len(collection["tests"]),
            "name": sanitName,
            "description": inp["description"],
            "sql": sanitName + ".sql",
            "expected": sanitName + "-expected.json",
            "actual": sanitName + "-actual.json"
        }
    
    def writeTestFiles(self, test, collection):
        testFolder = self.config["test-folder"] + "/" + collection["name"]
        utils.createFolderIne(testFolder)
        utils.writeFile(testFolder + "/" + test["sql"], "-- Generated with SQL-Unit --")
        utils.writeFile(testFolder + "/" + test["expected"], "{}")
        utils.writeFile(testFolder + "/" + test["actual"], "{}")

    def addTest(self, collectionIdx, test):
        targetCollection = self.testCollections[collectionIdx]
        newTest = self.createTest(test, targetCollection)
        targetCollection["tests"].append(newTest)
        utils.writeJson(self.config["test-manager"], self.testManagerJson)
        self.writeTestFiles(newTest, targetCollection)
        print("[SUCCESS] Added test [" + newTest["name"] + "] to collection [" + targetCollection["name"] + "]")

    def addCollection(self):
        print("[TODO] Adding new test collection")

    def removeTest(self):
        print("[TODO] Removing a test")

    def removeCollection(self):
        print("[TODO] Removing a test collection")
