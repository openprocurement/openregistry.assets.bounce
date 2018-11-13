# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.assets.core.tests.base import snitch

from openregistry.assets.core.tests.blanks.mixins import (
    BaseAssetResourceTestMixin, ResourceTestMixin
)

from openregistry.assets.bounce.models import Asset as AssetBounce
from openregistry.assets.bounce.tests.base import (
    test_asset_bounce_data, BaseAssetWebTest, #snitch
)
from openregistry.assets.bounce.tests.json_data import (
    test_loki_item_data,
    test_decision_data
)

from openregistry.assets.bounce.tests.blanks.asset import (
    administrator_change_complete_status,
    administrator_change_delete_status,
    asset_concierge_patch,
    change_active_asset,
    change_pending_asset,
    change_verification_asset,
    create_asset_with_items,
    dateModified_resource,
    patch_asset,
    patch_decimal_item_quantity,
    rectificationPeriod_autocreation,
    rectificationPeriod_endDate_remove,
)


class BounceAssetResourceTestMixin(BaseAssetResourceTestMixin):
    test_09_asset_concierge_patch = snitch(asset_concierge_patch)


class AssetBounceResourceTest(BaseAssetWebTest, ResourceTestMixin, BounceAssetResourceTestMixin):
    asset_model = AssetBounce
    docservice = True
    initial_data = test_asset_bounce_data
    initial_item_data = deepcopy(test_loki_item_data)
    initial_decision_data = deepcopy(test_decision_data)
    initial_status = 'pending'
    precision = 4

    test_05_dateModified_resource = snitch(dateModified_resource)
    test_08_patch_asset = snitch(patch_asset)
    test_10_administrator_change_delete_status = snitch(administrator_change_delete_status)
    test_11_administrator_change_complete_status = snitch(administrator_change_complete_status)
    test_13_check_pending_asset = snitch(change_pending_asset)
    test_14_check_verification_asset = snitch(change_verification_asset)
    test_15_check_active_asset = snitch(change_active_asset)
    test_19_patch_decimal_with_items = snitch(patch_decimal_item_quantity)
    test_create_asset_with_items = snitch(create_asset_with_items)
    test_rectificationPeriod_autocreation = snitch(rectificationPeriod_autocreation)
    test_rectificationPeriod_endDate_remove = snitch(rectificationPeriod_endDate_remove)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetBounceResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
