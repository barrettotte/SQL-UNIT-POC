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

def createFolderIne(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def printList(l):
    for elem in l:
        print(str(elem))

def printDict(d):
    for key, val in d.items():
        print(key + " --- " + str(val))

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

def printCliError(msg, showHelp=True):
    if showHelp:
        msg += " Use -h flag for more information."
    log(msg, "ERROR", False)

def isValidArg(arg, argList, key):
    for a in argList:
        if arg == a[key]:
            return True
    printCliError(key + " [" + arg + "] not found")
    return False

def printArgList(argList, keys, separator=" --- ", prefix="   "):
    for arg in argList:
        print(prefix + arg[keys[0]] + separator + arg[keys[1]])

def log(msg, msgType="INFO", writeFile=True):
    print("[" + msgType + "] " + msg)
    #TODO write to file

def makePrompt(basePrompt, choices, inType, spaces, default):
    prompt = (" " * spaces) + basePrompt
    if len(choices) > 0:
       prompt += " [choices=" + "|".join(choices) + "]"
    if default != "": # TODO if not default --test
       prompt += " [default=" + str(default) + "]"
    prompt += " : "
    return prompt

def getInputInt(x, inType):
    try:
        x = int(x)
        if "+" in inType and x < 0:
            log("Input must be a positive integer", "ERROR", False)
        else:
            return x
    except ValueError:
        log("Input must be an integer.", "ERROR", False)
    return ""

def strToBool(inp):
    if inp == "true" or inp == "false":
        return inp
    return "true" if inp.lower() == "y" else "false"

def getInput(prompt, choices=[], inType="str", spaces=3, default=""):
    choices = choices if (inType != "bool") else ["Y","N"]
    prompt = makePrompt(prompt, choices, inType, spaces, default)
    inp = ""
    try:
        while inp == "": # TODO while not input --test
            x = input(prompt).strip()
            if x == "": # TODO if not x --test
               inp = default
            elif "int" in inType:
                inp = getInputInt(x, inType)
            elif (inType == "str" and len(choices) > 0) or inType == "bool":
                inp = x if choiceIsValid(x, choices) else ""
            else:
                inp = x
    except KeyboardInterrupt:
        print("")
        fatalError("Keyboard interrupt occurred.", False)
        exit()
    if inType == "bool":
        inp = strToBool(inp)
    return inp

def choiceIsValid(x, sList):
    for s in sList:
        if x.lower() == s.lower():
            return True
    log("Input not valid, must be [" + "|".join(sList) + "]", "ERROR", False)
    return False

def getFoldersAsDict(root):
    collectionDirs = {}
    for d in os.listdir(root):
        collectionDirs[d] = []
        for sd in os.listdir(os.path.join(root, d)):
            collectionDirs[d].append(sd)
    return collectionDirs


# TODO util for searching/handling if file/dir is duplicate name
# TODO util for simple log, print to console + write to text file
# TODO util for getting timestamp - getTimestamp(formatSpecifier)