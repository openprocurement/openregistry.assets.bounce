# -*- coding: utf-8 -*-
import os
from copy import deepcopy

from openregistry.assets.core.tests.base import (
    BaseAssetWebTest as BaseAWT, #snitch
    connection_mock_config,
    MOCK_CONFIG as BASE_MOCK_CONFIG,
    AssetTransferWebTest as AssetTWT
)
from json_data import test_asset_bounce_data
from openregistry.assets.bounce.tests.fixtures import PARTIAL_MOCK_CONFIG


MOCK_CONFIG = connection_mock_config(PARTIAL_MOCK_CONFIG,
                                     base=BASE_MOCK_CONFIG,
                                     connector=('plugins', 'api', 'plugins',
                                                'assets.core', 'plugins'))


class BaseAssetWebTest(BaseAWT):
    initial_auth = ('Basic', ('broker', ''))
    relative_to = os.path.dirname(__file__)
    mock_config = MOCK_CONFIG

    def setUp(self):
        self.initial_data = deepcopy(test_asset_bounce_data)
        super(BaseAssetWebTest, self).setUp()


class AssetTransferWebTest(AssetTWT):
    initial_auth = ('Basic', ('broker', ''))
    relative_to = os.path.dirname(__file__)
    mock_config = MOCK_CONFIG

    def setUp(self):
        self.initial_data = deepcopy(test_asset_bounce_data)
        super(AssetTransferWebTest, self).setUp()


class AssetContentWebTest(BaseAssetWebTest):
    init = True
    initial_status = 'pending'
    mock_config = MOCK_CONFIG
