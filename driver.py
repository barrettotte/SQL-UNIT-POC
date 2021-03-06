# Driver for unit testing SQL

import utils, sys
from testrunner import SQLTestRunner

def main():
    args = sys.argv
    if len(args) == 2:
        configPath = utils.readJson(".\\SQLUnit.config.json")
        SQLTestRunner(configPath, args[1]).execute()
    else:
        msg = "Too many arguments given." if len(args) > 2 else "No arguments given"
        utils.log(msg + "  <collection>", "ERROR", writeFile=False)
    

if __name__=='__main__': main()