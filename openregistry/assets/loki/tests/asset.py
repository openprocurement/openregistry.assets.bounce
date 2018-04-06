# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.api.tests.base import snitch
from openprocurement.api.tests.blanks.mixins import ResourceTestMixin

from openregistry.assets.core.tests.blanks.asset import patch_decimal_item_quantity
from openregistry.assets.core.tests.blanks.mixins import AssetResourceTestMixin

from openregistry.assets.loki.models import Asset as AssetLoki
from openregistry.assets.loki.tests.base import (
    test_asset_loki_data, BaseAssetWebTest
)
from openprocurement.api.constants import IS_SCHEMAS_PROPERTIES_ENABLED_LOKI
from openregistry.assets.loki.tests.blanks.asset import (
    patch_asset,
    change_pending_asset,
    administrator_change_delete_status
)


class AssetCompoundResourceTest(BaseAssetWebTest, ResourceTestMixin, AssetResourceTestMixin):
    asset_model = AssetLoki
    docservice = True
    initial_data = test_asset_loki_data
    initial_status = 'pending'
    precision = 4

    test_08_patch_asset = snitch(patch_asset)
    test_10_administrator_change_delete_status = snitch(administrator_change_delete_status)
    test_13_check_pending_asset = snitch(change_pending_asset)
    test_19_patch_decimal_witt_items = snitch(patch_decimal_item_quantity)

    @unittest.skipIf(not IS_SCHEMAS_PROPERTIES_ENABLED_LOKI,
                     "not supported now")
    def test_create_compount_with_item_schemas(self):
        response = self.app.post_json('/', {'data': test_asset_loki_data})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        response = response.json['data']
        self.assertEqual(response['items'][0]['schema_properties']['properties'], test_asset_loki_data['items'][0]['schema_properties']['properties'])
        self.assertEqual(response['items'][0]['schema_properties']['code'][0:2], test_asset_loki_data['items'][0]['schema_properties']['code'][:2])
        self.assertEqual(response['items'][0]['description'], test_asset_loki_data['items'][0]['description'])
        self.assertEqual(response['items'][0]['classification'], test_asset_loki_data['items'][0]['classification'])
        self.assertEqual(response['items'][0]['additionalClassifications'], test_asset_loki_data['items'][0]['additionalClassifications'])
        self.assertEqual(response['items'][0]['address'], test_asset_loki_data['items'][0]['address'])
        self.assertEqual(response['items'][0]['id'], test_asset_loki_data['items'][0]['id'])
        self.assertEqual(response['items'][0]['unit'], test_asset_loki_data['items'][0]['unit'])
        self.assertEqual(response['items'][0]['quantity'], test_asset_loki_data['items'][0]['quantity'])

    @unittest.skipIf(not IS_SCHEMAS_PROPERTIES_ENABLED_LOKI,
                     "not supported now")
    def test_bad_item_schemas_code(self):
        bad_initial_data = deepcopy(test_asset_loki_data)
        bad_initial_data['items'][0]['classification']['id'] = "42124210-6"
        response = self.app.post_json('/', {'data': bad_initial_data},status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'],
                         [{
                             "location": "body",
                             "name": "items",
                             "description": [
                                 {u"schema_properties": [u"classification id mismatch with schema_properties code"]},
                                 {u"schema_properties": [u"classification id mismatch with schema_properties code"]},
                             ]
                         }])

    @unittest.skipIf(not IS_SCHEMAS_PROPERTIES_ENABLED_LOKI,
                     "not supported now")
    def test_delete_item_schema(self):
        response = self.app.post_json('/', {'data': test_asset_loki_data})
        self.assertEqual(response.status, '201 Created')
        resource = response.json['data']
        self.resource_token = response.json['access']['token']
        self.access_header = {'X-Access-Token': str(response.json['access']['token'])}
        self.resource_id = resource['id']
        status = resource['status']
        self.set_status(self.initial_status)

        response = self.app.patch_json('/{}?access_token={}'.format(
                                self.resource_id, self.resource_token),
                                headers=self.access_header,
                                params={'data': {"items": [{'schema_properties': None}, {'schema_properties': None}]}})
        # TODO add schema props delete
        # self.assertEqual(response.json['data']['items'][0]['schema_properties'], None)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetCompoundResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
