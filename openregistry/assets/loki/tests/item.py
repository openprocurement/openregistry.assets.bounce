# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.api.tests.base import snitch

from openregistry.assets.loki.tests.base import (
    AssetContentWebTest
)
from openprocurement.api.tests.blanks.json_data import test_loki_item_data
from openregistry.assets.loki.tests.blanks.item import (
    create_item_resource,
    patch_item
)

class AssetItemResourceTest(AssetContentWebTest):
    initial_item_data = deepcopy(test_loki_item_data)
    test_create_item_resource = snitch(create_item_resource)
    test_patch_item_resource = snitch(patch_item)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetItemResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')