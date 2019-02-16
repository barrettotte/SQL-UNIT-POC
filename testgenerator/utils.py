# Utilities

import json
import os
import shutil


def getCwd():
    return os.path.dirname(__file__)


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


def printCliError(msg, showHelp=True):
    out = "[ERROR] " + msg
    if showHelp:
        out += " Use -h flag for more information."
    print(out)


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


def makePrompt(basePrompt, choices, inType, spaces, default):
    prompt = (" " * spaces) + basePrompt
    if len(choices) > 0:
       prompt += " [choices=" + "|".join(choices) + "]"
    if default != "":
       prompt += " [default=" + str(default) + "]"
    prompt += " : "
    return prompt


def getInputInt(x, inType):
    try:
        x = int(x)
        if "+" in inType and x < 0:
            printCliError("Input must be a positive integer", showHelp=False)
        else:
            return x
    except ValueError:
        printCliError("Input must be an integer.", showHelp=False)
    return ""


def getInput(prompt, choices=[], inType="str", spaces=3, default=""):
    choices = choices if (inType != "bool") else ["Y","N"]
    prompt = makePrompt(prompt, choices, inType, spaces, default)
    inp = ""
    try:
        while inp == "":
            x = input(prompt).strip()
            if x == "":
               inp = default
            elif "int" in inType:
                inp = getInputInt(x, inType)
            elif (inType == "str" and len(choices) > 0) or inType == "bool":
                inp = x if choiceIsValid(x, choices) else ""
            else:
                inp = x
    except KeyboardInterrupt:
        print("")
        printCliError("Keyboard interrupt occurred. Exiting program.", showHelp=False)
        exit()
    if inType == "bool":
        inp = "true" if inp.lower() == "y" else "false"
    return inp


def choiceIsValid(x, sList):
   for s in sList:
      if x.lower() == s.lower():
        return True
   printCliError("Input not valid, must be [" + "|".join(sList) + "]", showHelp=False)
   return False


# TODO util for searching/handling if file/dir is duplicate name
# TODO util for simple log, print to console + write to text file
# TODO util for getting timestamp - getTimestamp(formatSpecifier)
# TODO util for handling duplicate names in list
