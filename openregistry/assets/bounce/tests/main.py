# -*- coding: utf-8 -*-

import unittest

from openregistry.assets.bounce.tests import (
    asset,
    document,
    transferring,
    related_processes,
    migration,
)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(asset.suite())
    tests.addTest(document.suite())
    tests.addTest(migration.suite())
    tests.addTest(transferring.suite())
    tests.addTest(related_processes.suite())
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
