import os
import unittest
import sys

if __name__ == '__main__':
    sys.path.append(os.getcwd())
    testsuite = unittest.TestLoader().discover('./elysium/tests')
    result = unittest.TextTestRunner(verbosity=1).run(testsuite)
    sys.exit(not result.wasSuccessful())
