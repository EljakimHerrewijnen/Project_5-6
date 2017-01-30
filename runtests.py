import os
import sys
import unittest
import tests.HTMLTestRunner
from tests.test_user_addressDAO import TestUserAddress, TestClass
from tests.test_helpers import TestHelper
from tests.test_endpoint import TestEndpointProducts, TestEndpointAuthentication, TestEndpointAccount
#import all classes to test here ^^^

# def htmlgenerator(classnames):
#     suites_list = []
#     for test_class in classnames:
#         suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
#         suites_list.append(suite)

#     big_suite = unittest.TestSuite(suites_list)
#     loader = unittest.TestLoader()
#     htmlfile = open('app/static/views/unittest-result-view.html', 'w') #path to html
#     runner = tests.HTMLTestRunner.HTMLTestRunner(stream=htmlfile, verbosity=2, title='Test report')
#     runner.run(big_suite)

def results(classnames):
    suites_list = []
    for test_class in classnames:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)
    test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    result2 = test_runner.run(big_suite)
    sys.exit(not result2.wasSuccessful())

if __name__ == '__main__':
    test_classes_to_run = [TestUserAddress, TestHelper, TestEndpointProducts, TestEndpointAuthentication, TestEndpointAccount]

    #htmlgenerator(test_classes_to_run)
    results(test_classes_to_run)    