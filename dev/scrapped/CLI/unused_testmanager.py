# Generate Test Collections/Tests and configure Test Manager

import utils

class TestManager:

    def __init__(self, config):
        try:
            self.config = config
            self.testManagerJson = utils.readJson(config["test-manager"])
            self.collections = self.testManagerJson["test-collections"]
            utils.createFolderIne(config["test-folder"])
        except Exception:
            print("[FATAL] Test Manager could not be initialized.")
            exit()

    def createTest(self, inputData, collection):
        sanitName = utils.sanitizeFilename(inputData["name"])
        return {
            "id": utils.getIncrementedId(collection["tests"]),
            "name": sanitName,
            "description": inputData["description"]
        }
    
    def createCollection(self, inputData):
        return {
            "id": utils.getIncrementedId(self.collections),
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
        utils.writeFile(testFolder + "/" + test["name"] + ".sql", "-- Generated with SQL-Unit --")
        utils.writeFile(testFolder + "/" + test["name"] + "-expected.json", "{}")
        utils.writeFile(testFolder + "/" + test["name"] + "-actual.json", "{}")

    def addTest(self, collectionId, inputData):
        collection = utils.getElemById(self.collections, collectionId)
        test = self.createTest(inputData, collection)
        out = "Adding test " + utils.keyvalStr(test["id"], test["name"])
        utils.log(out + " to test collection " + utils.keyvalStr(collection["id"], collection["name"]))
        collection["tests"].append(test)
        self.refreshJson()
        self.writeTestFiles(collection, test)

    def addCollection(self, inputData):
        collection = self.createCollection(inputData)
        utils.log("Adding collection " + utils.keyvalStr(collection["id"], collection["name"]))
        self.collections.append(collection)
        self.refreshJson()
    
    def getDefaultCollectionConfig(self, collectName):
        return {
            "name": collectName,
            "description": collectName,
            "config": self.config["collection-defaults"]
        }

    def removeTestById(self, collectionId, testId):
        collection = utils.getElemById(self.collections, collectionId)
        test = self.getTestById(collectionId, testId)
        if test != "":
            out = "Removing test " + utils.keyvalStr(test["id"], test["name"])
            utils.log(out + " from test collection " + utils.keyvalStr(collection["id"], collection["name"]))
            collection["tests"].remove(test)
            self.refreshJson()
            utils.deleteDirectory(self.config["test-folder"] + "/" + collection["name"] + "/" + test["name"])

    def removeCollectionById(self, collectionId):
        collection = self.getCollectionById(collectionId)
        if collection != "":
            utils.log("Removing collection " + utils.keyvalStr(collection["id"], collection["name"]))
            self.collections.remove(collection)
            self.refreshJson()
            utils.deleteDirectory(self.config["test-folder"] + "/" + collection["name"])
    
    def removeCollectionByName(self, collectionName):
        collection = self.getCollectionByName(collectionName)
        if collection != "":
            self.removeCollectionById(collection["id"])
        else:
            utils.log("Collection [" + collectionName + "] not found.")
    
    def removeTestByName(self, collectionName, testName):
        collection = self.getCollectionByName(collectionName)
        if collection != "":
            test = utils.getElemById(collection["tests"], testName, "name")
            if test != "":
                self.removeTestById(collection["id"], test["id"])
            else:
                utils.log("Test [" + testName + "] not found in collection [" + collectionName + "]")    
        else:
            utils.log("Collection [" + collectionName + "] not found.")
    
    def getCollectionById(self, collectionId):
        return utils.getElemById(self.collections, collectionId)
    
    def getTestById(self, collectionId, testId):
        return utils.getElemById(self.getCollectionById(collectionId), testId)

    def getCollectionByName(self, collectionName):
        collection = utils.getElemById(self.collections, collectionName, "name")
        if collection != "":
            return collection
        else:
            utils.log("Collection [" + collectionName + "] not found.")
        return ""
    
    def getTestByName(self, collectionName, testName):
        collection = self.getCollectionByName(collectionName)
        if collection != "":
            test = utils.getElemById(collection["tests"], testName, "name")
            if test != "":
                return test
            else:
                utils.log("Test [" + testName + "] not found in collection [" + collectionName + "]")    

    def refreshJson(self):
        for collection in self.collections:
            utils.regenerateIds(collection["tests"])
        utils.regenerateIds(self.collections)
        utils.writeJson(self.config["test-manager"], self.testManagerJson)
        self.refreshCollections()

    def refreshCollections(self):
        collectionFolders = utils.getFoldersAsDict(self.config["test-folder"])
        names = self.getCollectionNames()
        for key, val in collectionFolders.items():
            if key in names:
                print(key)
            else:
                self.addCollection(self.getDefaultCollectionConfig(key))
        collectionsJson = self.testManagerJson["test-collections"]
        for collection in collectionsJson:
            print(collection)
            # check if in JSON, but not a folder -- remove from JSON

            # +-------------------------------------+
            # | !!!!!!!! DEV STOPPED HERE !!!!!!!!! |
            # +-------------------------------------+


    def removeAllCollections(self):
        self.testCollections.clear()
        self.refreshJson()
    
    def removeAllTests(self, collectionIdx):
        utils.getElemById(self.collections, collectionIdx)["tests"].clear()
        self.refreshJson()

    def getCollections(self):
        return self.testCollections
    
    def getCollectionNames(self):
        names = []
        for collection in self.collections:
            names.append(collection["name"])
        return names


# TODO Handle duplicate naming/deleting for collections+tests
# TODO Stats function for returning info on test/collection count
# TODO Create any missing files/folders when refreshing