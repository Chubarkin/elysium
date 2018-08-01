import os
import unittest
import sys

from elysium import config
from elysium.tests.test_backends.test_postgresql.test_config import db_config

if __name__ == '__main__':
    sys.path.append(os.getcwd())

    config.update(db_config)

    testsuite = unittest.TestLoader().discover('./elysium/tests')
    result = unittest.TextTestRunner(verbosity=1).run(testsuite)
    sys.exit(not result.wasSuccessful())
