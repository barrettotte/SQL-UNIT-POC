# Driver


import json
import utils, testgenerator


def main():
    config = utils.readJson("./config.dev.json")
    gen = testgenerator.TestGenerator(config)

    collectionIdx = 0
    mockTest = { "name": "sometest_DEMO", "description": "This is a test" }

    gen.addTest(collectionIdx, mockTest)

if __name__=='__main__': main()