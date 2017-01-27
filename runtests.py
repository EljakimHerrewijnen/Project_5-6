import os
import sys
import unittest
import tests.HTMLTestRunner
from tests.test_user_addressDAO import TestUserAddress
#import all classes to test here ^^^

def htmlgenerator():
    loader = unittest.TestLoader()

    #Create new test suites to test.
    #To run multiple suites you have to create one suite combining all suites.
    finalsuite = unittest.TestSuite(loader.loadTestsFromTestCase(TestUserAddress))

    htmlfile = open('app/static/views/unittest-result-view.html', 'w') #path to html
    runner = tests.HTMLTestRunner.HTMLTestRunner(stream=htmlfile, verbosity=2, title='Test report')
    result = runner.run(finalsuite) #Run the suites here

def results():
    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUserAddress)
    test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    result2 = test_runner.run(test_suite)
    sys.exit(not result2.wasSuccessful())

if __name__ == '__main__':
    htmlgenerator()
    results()
    
    