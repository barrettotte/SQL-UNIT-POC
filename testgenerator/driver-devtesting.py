# Test driver while developing

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

    #gen.removeTestById(1, 2)
    #gen.removeCollectionById(1)
    #gen.removeTestById(0, 2)
    #gen.removeTestById(0, 3)

    gen.removeAllTests(3)
    #gen.removeTestById(0,2)
    #gen.removeCollectionById(3)

if __name__=='__main__': main()
