import os
import unittest
import sys


if __name__ == '__main__':
    sys.path.append(os.getcwd())

    from elysium import config
    from elysium.tests.test_backends.test_postgresql.test_config import db_config
    config.update(db_config)

    testsuite = unittest.TestLoader().discover('./elysium/tests')
    result = unittest.TextTestRunner(verbosity=1).run(testsuite)
    sys.exit(not result.wasSuccessful())
