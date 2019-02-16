# Utilities

import json, os, shutil

def readJson(filePath):
    # TODO file not found exception handling
    with open(filePath, 'r') as jsonFile:
        data = json.load(jsonFile)
    return data

def writeJson(filePath, data, sort=False):
    writeFile(filePath, getPrettyJson(data))

def writeFile(filePath, buffer):
    # TODO exception handling
    with open(filePath, 'w') as f:
        f.write(buffer)

def createFolderIne(folder):
    # TODO handle duplicate directory names
    if not os.path.exists(folder):
        os.makedirs(folder)

def printList(list):
    # TODO List comp. or lamda?
    for elem in list:
        print(str(elem))

def getPrettyJson(jsonRaw, sort=False):
    return json.dumps(jsonRaw, indent=4, sort_keys=sort)

def getIncrementedId(collection, key="id"):
    return collection[len(collection)-1][key] + 1 if len(collection) > 0 else 1

def keyvalStr(key, val):
    return "{" + str(key) + ": " + str(val) + "}"

def sanitizeFilename(filename):
    # TODO regex invalid chars
    return filename.replace(" ", "")

def getElemById(collection, elemId, key="id"):
    # TODO List comp. or lamda?
    for elem in collection:
        if elem[key] == elemId:
           return elem
    return ""

def regenerateIds(collection, key="id"):
    for i, elem in enumerate(collection):
        elem[key] = i

def deleteDirectory(directoryPath):
    shutil.rmtree(directoryPath)

       


# TODO util for searching/handling if file/dir is duplicate name
# TODO util for simple error logging - errorLog(msg)
# TODO util for getting timestamp - getTimestamp(formatSpecifier)
# TODO util for handling duplicate names in list