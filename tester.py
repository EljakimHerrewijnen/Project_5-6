from tests.adminDAOTest import AdminDAOTest

def Test():
    testing = AdminDAOTest()
    testing.setUp()
    successfulTest = False

    for i in range(0, 5):
        successfulTest = testing.TestAdmin()

        if not(successfulTest):
            print("F")
            return

        print("P", end = "")
    print("\n\nTest Successful!!")

Test()
