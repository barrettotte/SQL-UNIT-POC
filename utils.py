# Utilities

import json, os, shutil


def getCwd():
    return os.path.dirname(__file__)

def readJson(filePath):
    try:
        with open(filePath, 'r') as jsonFile:
            data = json.load(jsonFile)
    except FileNotFoundError:
        fatalError("File [" + filePath + "] could not be found.")
    return data

def log(msg, msgType="INFO", writeFile=True):
    print("[" + msgType + "] " + msg)
    #TODO write to file
    
def fatalError(msg, writeFile=True):
    log(msg, "FATAL", writeFile)
    exit()

def writeJson(filePath, data, sort=False):
    writeFile(filePath, getPrettyJson(data))

def writeFile(filePath, buffer):
    try:
        with open(filePath, 'w') as f:
            f.write(buffer)
    except Exception:
        log("File [" + filePath + "] could not be written.", "ERROR")

def printList(l):
    for elem in l:
        print(str(elem))

def printDict(d):
    for key, val in d.items():
        print(key + " --- " + str(val))

def getPrettyJson(jsonRaw, sort=False):
    return json.dumps(jsonRaw, indent=4, sort_keys=sort)

def printKeyVal(key, val):
    return "{" + str(key) + ": " + str(val) + "}"

def getFoldersAsDict(root):
    dirs = {}
    for d in os.listdir(root):
        dirs[d] = []
        for sd in os.listdir(os.path.join(root, d)):
            dirs[d].append(sd)
    return dirs

def getSplitLast(s, delim, offset=0):
    spl = s.split(delim)
    return spl[len(spl) - (1 + offset)]