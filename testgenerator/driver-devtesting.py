# Test driver while developing

import json, sys
import utils, testgenerator

def main():
    config = utils.readJson("./config.dev.json")
    gen = testgenerator.TestGenerator(config)

    mockTest1 = {"name": "sometest_DEMO", "description": "This is a test"}
    mockTest2 = {"name": "another_test", "description": "This is another test"}
    mockCollection1 = {
        "name": "WASD", 
        "description": "This is a generated collection",
        "config": {
            "server": "QWERTY",
            "dialect": "DB2",
            "keep-results": 100,
            "fail-threshold": 0,
            "measure-performance": "true",
            "record-results": "true",
            "generate-report": "true",
            "allow-stored-procedures": "false"
        }
    }

    gen.addTest(0, mockTest1)
    gen.addCollection(mockCollection1)
    gen.addTest(1, mockTest2)

    #gen.removeTest(1, 2)
    #gen.removeCollection(1)
    #gen.removeTest(0, 2)
    #gen.removeTest(0, 3)

    gen.removeAllTests(3)
    #gen.removeTest(0,2)
    #gen.removeCollection(3)

if __name__=='__main__': main()
