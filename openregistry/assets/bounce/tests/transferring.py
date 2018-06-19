# -*- coding: utf-8 -*-
import unittest

from openregistry.assets.bounce.tests.base import AssetTransferWebTest
from openregistry.assets.core.tests.plugins.transferring.mixins import AssetOwnershipChangeTestCaseMixin

class AssetOwnershipChangeTest(AssetTransferWebTest,
                               AssetOwnershipChangeTestCaseMixin):
    second_owner = 'broker3'
    test_owner = 'broker3t'
    invalid_owner = 'broker1'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetOwnershipChangeTest))
    return suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
