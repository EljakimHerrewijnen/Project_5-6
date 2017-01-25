import os
import unittest
import HTMLTestRunner
#import all classes to test here ^^^

if __name__ == '__main__':
    loader = unittest.TestLoader()
    #Create new test suites to test.
    #To run multiple suites you have to create one suite combining all suites.
    finalsuite = unittest.TestSuite(loader.loadTestsFromTestCase(#Load class here))
    htmlfile = open('static/views/unittest.html', 'w') #path to html
    runner = HTMLTestRunner.HTMLTestRunner(stream=htmlfile, verbosity=2, title='Test report')
    runner.run(finalsuite) #Run the suites here