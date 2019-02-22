# Driver for unit testing SQL

import utils
from testrunner import TestRunner

def main():
    # TODO configPath + collectionName pass in via shell script
    configPath = utils.readJson(utils.getCwd() + "\\config.json")
    collectionName = "WASD"
    runner = TestRunner(configPath, collectionName)
    runner.before()
    runner.run()
    runner.after()

if __name__=='__main__': main()