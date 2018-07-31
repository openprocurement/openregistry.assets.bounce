# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.assets.core.tests.base import snitch

from openregistry.assets.bounce.tests.base import (
    AssetContentWebTest
)
from openregistry.assets.bounce.tests.json_data import test_decision_data
from openregistry.assets.bounce.tests.blanks.decision import (
    create_decision,
    patch_decision,
    patch_decisions_with_lot_by_broker,
    rectificationPeriod_decision_workflow,
    create_or_patch_decision_in_not_allowed_status,
    create_decisions_with_asset
)


class LotDecisionResourceTest(AssetContentWebTest):
    initial_status = 'draft'
    initial_decision_data = deepcopy(test_decision_data)

    test_create_decision = snitch(create_decision)
    test_patch_decision = snitch(patch_decision)
    test_patch_decisions_with_lot_by_broker = snitch(patch_decisions_with_lot_by_broker)
    test_rectificationPeriod_decision_workflow = snitch(rectificationPeriod_decision_workflow)
    test_create_or_patch_decision_in_not_allowed_status = snitch(create_or_patch_decision_in_not_allowed_status)
    test_create_decisions_with_asset = snitch(create_decisions_with_asset)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LotDecisionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
