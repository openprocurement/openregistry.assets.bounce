# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.assets.core.tests.base import snitch

from openregistry.assets.bounce.tests.base import (
    AssetContentWebTest
)
from openregistry.assets.core.tests.blanks.json_data import test_loki_item_data
from openregistry.assets.bounce.tests.blanks.item import (
    create_item_resource,
    patch_item,
    create_bounce_with_item_schemas,
    bad_item_schemas_code,
    delete_item_schema,
    item_listing,
    rectificationPeriod_item_workflow
)

class AssetItemResourceTest(AssetContentWebTest):
    initial_item_data = deepcopy(test_loki_item_data)
    test_create_item_resource = snitch(create_item_resource)
    test_patch_item_resource = snitch(patch_item)
    test_item_listing = snitch(item_listing)
    # test_create_bounce_with_item_schemas = snitch(create_bounce_with_item_schemas)
    # test_bad_item_schemas_code = snitch(bad_item_schemas_code)
    # test_delete_item_schema = snitch(delete_item_schema)
    test_rectificaionPeriod_item_workflow = snitch(rectificationPeriod_item_workflow)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetItemResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
