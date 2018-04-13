# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.api.tests.base import snitch
from openprocurement.api.tests.blanks.mixins import ResourceTestMixin

from openregistry.assets.core.tests.blanks.mixins import AssetResourceTestMixin
from openregistry.assets.core.tests.blanks.asset import patch_decimal_item_quantity
from openregistry.assets.core.tests.blanks.mixins import (
    AssetResourceTestMixin, ResourceTestMixin
)

from openregistry.assets.loki.models import Asset as AssetLoki
from openregistry.assets.loki.tests.base import (
    test_asset_loki_data, BaseAssetWebTest, #snitch
)
from openregistry.assets.loki.tests.json_data import test_loki_item_data

from openregistry.assets.loki.tests.blanks.asset import (
    patch_asset,
    change_pending_asset,
    administrator_change_delete_status,
    patch_decimal_item_quantity,
    rectificationPeriod_workflow
)


class AssetLokiResourceTest(BaseAssetWebTest, ResourceTestMixin, AssetResourceTestMixin):
    asset_model = AssetLoki
    docservice = True
    initial_data = test_asset_loki_data
    initial_item_data = deepcopy(test_loki_item_data)
    initial_status = 'pending'
    precision = 4

    test_08_patch_asset = snitch(patch_asset)
    test_10_administrator_change_delete_status = snitch(administrator_change_delete_status)
    test_13_check_pending_asset = snitch(change_pending_asset)
    test_19_patch_decimal_with_items = snitch(patch_decimal_item_quantity)
    test_rectificationPeriod_workflow = snitch(rectificationPeriod_workflow)

def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetLokiResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
