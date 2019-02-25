import json, os, shutil, datetime

def getCwd():
    return os.path.dirname(__file__)

def readJson(path):
    data = {}
    if ".json" in path:
        try:
            with open(path, 'r') as jsonFile:
                data = json.load(jsonFile)
        except FileNotFoundError:
            fatalError("File [" + path + "] could not be found.")
    else:
        log(path + " is not a JSON file. ", "ERROR")
    return data

def readFile(path):
    try:
        with open(path, 'r') as f:
            return f.readlines();
    except FileNotFoundError:
        fatalError("File [" + path + "] could not be found.")
    return ""

def writeJson(path, data, sort=False):
    if ".json" in path:
        writeFile(path, getPrettyJson(data))
    else:
        log(path + " is not a JSON file.", "ERROR")

def writeFile(path, buffer):
    try:
        with open(path, 'w') as f:
            f.write(buffer)
    except Exception:
        log("File [" + path + "] could not be written.", "ERROR")

def log(msg, msgType="INFO", path=".\\log.txt", writeFile=True, init=False, pref=""):
    msg = "[" + msgType.ljust(6) + getTimestamp() + "] " + pref + msg
    try:
        if init and os.path.exists(path): 
            os.remove(path)
        with open(path, "a+") as f:
            f.write(msg + "\n")
    except Exception as e:
        print("[ERROR] Could not write to log")
        print(e)
    print(msg)
    
def fatalError(msg, writeFile=True):
    log(msg, "FATAL", writeFile)
    exit()

def getTimestamp():
    return str(datetime.datetime.now())

def printList(l):
    for elem in l:
        print(str(elem))

def printDict(d):
    for key, val in d.items():
        print(key + " --- " + str(val))

def printKeyVal(key, val):
    return "{" + str(key) + ": " + str(val) + "}"

def getPrettyJson(jsonRaw, sort=False):
    return json.dumps(jsonRaw, indent=4, sort_keys=sort)

def getFoldersAsDict(root):
    dirs = {}
    for d in os.listdir(root):
        dirs[d] = []
        for sd in os.listdir(os.path.join(root, d)):
            dirs[d].append(sd)
    return dirs

def getSplitLast(s, delim, offset=0):
    return str(s).split(delim)[(-offset)-1]

def findDictInList(l, targetVal, targetKey):
    for elem in l:
        if elem[targetKey] == targetVal:
           return elem
    return ""

def createFolderIne(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def getElemByKey(target, key, collection):
    # TODO List comp. or lamda?
    for elem in collection:
        if elem[key] == target:
            return elem
    return ""
