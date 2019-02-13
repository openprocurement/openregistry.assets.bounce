# -*- coding: utf-8 -*-
import os
from copy import deepcopy
from functools import partial

from openregistry.assets.core.utils import (
    get_now,
    read_json,
)
from openregistry.assets.core.tests.base import (
    BaseAssetWebTest as BaseAWT, #snitch
    connection_mock_config,
    MOCK_CONFIG as BASE_MOCK_CONFIG,
    AssetTransferWebTest as AssetTWT
)
from json_data import test_asset_bounce_data
from openregistry.assets.bounce.tests.fixtures import PARTIAL_MOCK_CONFIG
from openregistry.assets.bounce.constants import SNAPSHOTS_DIR


MOCK_CONFIG = connection_mock_config(PARTIAL_MOCK_CONFIG,
                                     base=BASE_MOCK_CONFIG,
                                     connector=('plugins', 'api', 'plugins',
                                                'assets.core', 'plugins'))

get_snapshot = partial(read_json, file_dir=SNAPSHOTS_DIR)


def check_patch_status_200(self, asset_id, asset_status, headers=None, extra_data={}):
    patch_data = {'status': asset_status}
    patch_data = patch_data.update(extra_data) or patch_data
    response = self.app.patch_json(
        '/{}'.format(asset_id),
        params={'data': patch_data},
        headers=headers
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], patch_data['status'])
    for field, value in extra_data.items():
        self.assertEqual(response.json['data'][field], value)
    return response


def check_patch_status_403(self, asset_id, asset_status, headers=None):
    response = self.app.patch_json(
        '/{}'.format(asset_id),
        params={'data': {'status': asset_status}},
        headers=headers,
        status=403
    )
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    return response


class BaseAssetWebTest(BaseAWT):
    initial_auth = ('Basic', ('broker', ''))
    relative_to = os.path.dirname(__file__)
    mock_config = MOCK_CONFIG

    def setUp(self):
        self.initial_data = deepcopy(test_asset_bounce_data)
        super(BaseAssetWebTest, self).setUp()

    def create_resource(self, extra=None, auth=None, with_decisions=True):
        resource = super(BaseAssetWebTest, self).create_resource(extra, auth)
        if with_decisions:
            current_status = resource['status']

            self.set_status('pending')
            response = self.app.get('/{}'.format(self.resource_id))
            old_decs_count = len(response.json['data'].get('decisions', []))

            decision_data = {
                'decisionDate': get_now().isoformat(),
                'decisionID': 'decisionLotID'
            }
            response = self.app.post_json(
                '/{}/decisions'.format(self.resource_id),
                {"data": decision_data},
                headers=self.access_header
            )
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.json['data']['decisionDate'], decision_data['decisionDate'])
            self.assertEqual(response.json['data']['decisionID'], decision_data['decisionID'])
            self.decision_id = response.json['data']['id']

            self.set_status(current_status)

            response = self.app.get('/{}'.format(self.resource_id))
            present_decs_count = len(response.json['data'].get('decisions', []))
            self.assertEqual(old_decs_count + 1, present_decs_count)
            resource = response.json['data']

        return resource


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
