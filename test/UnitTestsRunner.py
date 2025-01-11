import os
import unittest
import sys
from distutils.util import strtobool
from unittest import TextTestRunner, TestResult

"""
This procedure deletes Cythonized files and discovers and runs all other (RawPythons) unittests.
It includes or excludes integration tests based on the parameter it receives from outside.
For all types of Cythonized tests, see CythonizedTests. The raw Python test versions of Cythonized ones are also tested here. Use this for py files, and the other for pyx files.
By default, integration tests are disabled.
"""

#region Colored
GREEN = "\033[32m"      #Solution without 3rd party: https://stackoverflow.com/questions/37340049/how-do-i-print-colored-output-to-the-terminal-in-python/37340245
BLUE = "\033[34m"
YELLOW = "\033[33m"     #color codes: https://www.instructables.com/Printing-Colored-Text-in-Python-Without-Any-Module/
ENDC = "\033[m"
RED = "\033[31m"
def printgr(msg:str):
    """
    Prints in green.
    :param msg:
    :return:
    """
    print(GREEN + msg + ENDC)
def toYellow():
    print(YELLOW)
def toBlue():
    print(BLUE)
def toGreen():
    print(GREEN)
def toRed():
    print(RED)
def toDefault():
    print(ENDC)
#endregion

def PrintTestResults(result, suiteName:str, includesIntegrations:bool, beepIfAnyError:bool=True):
    """
    Reports the unittest runner output to the screen with colors.
    :param result:
    :param suiteName:
    :param includesIntegrations:
    :return:
    """
    print("\n\n\n--------TEST RESULTS (" + suiteName + ")--------------")
    if result.wasSuccessful():
        toGreen()
        print("->TESTS PASSED (" + suiteName + ")")
        print(result)
    else:
        toRed()
        print("->THERE ARE FAILED TESTS ( " + suiteName + ")")
        print(result)

    toYellow()  #warnings
    if(not includesIntegrations):
        print("Skipping integration tests (" + suiteName + ")")
    toDefault()

if __name__ == "__main__":

    #STEPS
    """
    1) To find test files, __init__.py must be added to each folder. Including subfolders. It must be in all folders up to the top.
    2) It doesn't work while Cython's pyd and c files are present. So delete them before running the tests and then recompile them. It gives an import error saying "Is this module globally installed?". See CythonizedTests.
    3) If this process is slow, many files may contain open imports and open operations without being hidden in the main method. Pay attention to those open references for Python performance.
    4) Whether unittest.main() is placed in the main block of the file or not does not affect the global test. It is for connecting to tests instead of the normal main while debugging locally.
    5) If the file has both main and unittest, unit tests are called before mains because of unittest.main(). You can leave the mains disabled. Or you can try converting mains to tests. Or you can expect the tests to run first and then the mains.
    """

    #Paths
    from pathlib import Path
    currentDirectory = os.getcwd()
    print("Current Directory: " + currentDirectory)
    if(currentDirectory.endswith("test")):
        start_dir = Path(currentDirectory).parent.joinpath("src")
    else:
        start_dir = Path(currentDirectory).joinpath("src")
    print("Source Directory: ", start_dir)

    #Args
    skipIntegrationsArg:bool = True if sys.argv.__len__() <= 1 else bool(strtobool(sys.argv[1]))
    failFast:bool = False if sys.argv.__len__() <= 2 else bool(strtobool(sys.argv[2]))      #It is useful to give this when calling from a batch file.
    skipIntegrationsEff:bool = skipIntegrationsArg
    toBlue()
    print("SkipIntegrations: " + str(skipIntegrationsEff))
    print("FailFast: " + str(failFast))
    toDefault()

    #Load tests
    #https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory
    loader = unittest.TestLoader()
    s = str(start_dir)
    suite = loader.discover(start_dir=s, pattern="*.py", top_level_dir=s)       #all py files. no cython support in this state. Cythonized ones should use a separate *Tests.py file. see setup.py. Note: Files with (-) in their names cannot be discovered.

    #region exclude special folders
    toRed()
    for t in suite._tests:
        if(len(t._tests))>0:
            try:        #not every testsuite is iterable.
                for _testclass in t._tests:
                    for _testcase in _testclass:
                        if(str(_testcase._testMethodName).startswith("test_integration_") and skipIntegrationsEff):
                            _testclass._tests.remove(_testcase)  #We only ignore that testcase method.
                            print("Integration test method skipped: '" + _testcase._testMethodName + "'")
            except Exception as ex:
                pass
                #print(ex)      #We expect a not iterable error. Open if there is another error.
    toDefault()
    #endregion

    #Run all
    runner = TextTestRunner(verbosity=5, failfast=failFast)         #if failfast is true, it exits at the first error
    result:TestResult = runner.run(suite)

    #Report
    PrintTestResults(result, "Tests", not skipIntegrationsEff)

    # Exit with a non-zero status code if any test fails
    if not result.wasSuccessful():
        sys.exit(1)