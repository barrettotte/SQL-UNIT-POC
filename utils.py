# Utilities


import json, os


def readJson(filePath):
    # TODO: file not found exception handling
    with open(filePath, 'r') as jsonFile:
        data = json.load(jsonFile)
    return data

def writeJson(filePath, data):
    writeFile(filePath, getPrettyJson(data))

def writeFile(filePath, buffer):
    # TODO: exception handling
    with open(filePath, 'w') as f:
        f.write(buffer)

def createFolderIne(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def printList(list):
    for elem in list:
        print(elem)

def getPrettyJson(jsonRaw, sort=False):
    return json.dumps(jsonRaw, indent=4, sort_keys=sort)