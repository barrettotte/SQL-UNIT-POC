from testrunner import SQLTestRunner
import utils
import unittest, shutil, os


class BasicTest(unittest.TestCase):
    
    def setUp(self):
        self.target = "BARRETT_TEST"
        addTests = ["WASD", "QWERTY", "ASDF"]
        addFiles = [".sql", "-expected.json", "-actual.json"]
        self.config = utils.readJson("..\\_configs\\SQL-UNIT-POC-Config.json")
        self.runner = SQLTestRunner(self.config, self.target)
        self.setupMockSuite(addTests, addFiles)

    def setupMockSuite(self, addTests, addFiles):
        self.rootFolder = utils.getCwd() + "\\" + self.config["test-suites"]
        self.mockSuitePath = self.rootFolder + "\\" + self.target
        self.testPaths = {}
        for test in addTests:
            self.testPaths[test] = self.mockSuitePath + "\\" + test
            utils.createFolderIne(self.testPaths[test])
            for file in addFiles:
                utils.writeFile(self.testPaths[test] + "\\" + test + file, "")
    
    def test_init(self):
        self.assertIsInstance(self.runner, SQLTestRunner)
        self.assertTrue(os.path.exists(self.mockSuitePath))
        self.assertEqual(3, len(os.listdir(self.mockSuitePath))) # 3 tests in suite
        for tp in self.testPaths:
            self.assertEqual(3, len(os.listdir(self.mockSuitePath + "\\" + tp))) # 3 files / test
    
    def tearDown(self):
        shutil.rmtree(self.mockSuitePath)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(BasicTest("test_init"))
    return suite

def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == "__main__": main()