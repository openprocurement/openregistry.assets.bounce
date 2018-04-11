# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.api.constants import IS_SCHEMAS_PROPERTIES_ENABLED_LOKI


def create_item_resource(self):
    response = self.app.post_json('/{}/items'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_item_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    item_id = response.json["data"]['id']
    self.assertIn(item_id, response.headers['Location'])
    self.assertEqual(self.initial_item_data['description'], response.json["data"]["description"])
    self.assertEqual(self.initial_item_data['quantity'], response.json["data"]["quantity"])
    self.assertEqual(self.initial_item_data['address'], response.json["data"]["address"])


def patch_item(self):
    response = self.app.post_json('/{}/items'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_item_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    item_id = response.json["data"]['id']
    self.assertIn(item_id, response.headers['Location'])
    self.assertEqual(self.initial_item_data['description'], response.json["data"]["description"])
    self.assertEqual(self.initial_item_data['quantity'], response.json["data"]["quantity"])
    self.assertEqual(self.initial_item_data['address'], response.json["data"]["address"])

    response = self.app.patch_json('/{}/items/{}'.format(self.resource_id, item_id),
        headers=self.access_header, params={
            "data": {
                "description": "new item description",
                "registrationDetails": self.initial_item_data['registrationDetails'],
                "unit": self.initial_item_data['unit'],
                "address": self.initial_item_data['address'],
                "quantity": self.initial_item_data['quantity'],
                "classification": self.initial_item_data['classification'],
            }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(item_id, response.json["data"]["id"])
    self.assertEqual(response.json["data"]["description"], 'new item description')


def create_item_resource_invalid(self):
    pass


def patch_item_resource_invalid(self):
    pass


def list_item_resource(self):
    pass


@unittest.skipIf(not IS_SCHEMAS_PROPERTIES_ENABLED_LOKI, "not supported now")
def create_loki_with_item_schemas(self):
    asset = self.create_resource()

    response = self.app.post_json('/{}/items'.format(asset['id']), {'data': self.initial_item_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    response = response.json['data']
    self.assertEqual(response['schema_properties']['properties'], self.initial_item_data['schema_properties']['properties'])
    self.assertEqual(response['schema_properties']['code'][0:2], self.initial_item_data['schema_properties']['code'][:2])
    self.assertEqual(response['description'], self.initial_item_data['description'])
    self.assertEqual(response['classification'], self.initial_item_data['classification'])
    self.assertEqual(response['additionalClassifications'], self.initial_item_data['additionalClassifications'])
    self.assertEqual(response['address'], self.initial_item_data['address'])
    self.assertEqual(response['id'], self.initial_item_data['id'])
    self.assertEqual(response['unit'], self.initial_item_data['unit'])
    self.assertEqual(response['quantity'], self.initial_item_data['quantity'])


@unittest.skipIf(not IS_SCHEMAS_PROPERTIES_ENABLED_LOKI, "not supported now")
def bad_item_schemas_code(self):
    asset = self.create_resource()

    bad_initial_data = deepcopy(self.initial_item_data)
    bad_initial_data['classification']['id'] = "42124210-6"
    response = self.app.post_json('/{}/items'.format(asset['id']), {'data': bad_initial_data},status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'],
                     [{
                         "location": "body",
                         "name": "item",
                         "description": [
                             {u"schema_properties": [u"classification id mismatch with schema_properties code"]},
                         ]
                     }])


@unittest.skipIf(not IS_SCHEMAS_PROPERTIES_ENABLED_LOKI, "not supported now")
def delete_item_schema(self):
    asset = self.create_resource()

    response = self.app.post_json('/{}/items'.format(asset['id']), {'data': self.initial_item_data})
    item_id = response.json["data"]['id']
    self.assertEqual(response.status, '201 Created')
    resource = response.json['data']
    self.resource_token = response.json['access']['token']
    self.access_header = {'X-Access-Token': str(response.json['access']['token'])}
    self.resource_id = resource['id']
    status = resource['status']
    self.set_status(self.initial_status)

    updated_item_data = deepcopy(self.initial_item_data)
    updated_item_data['schema_properties'] = None
    response = self.app.patch_json('/{}/items/{}?access_token={}'.format(
                            self.resource_id, item_id, self.resource_token),
                            headers=self.access_header,
                            params={'data': updated_item_data})
    # TODO add schema props delete
    # self.assertEqual(response.json['data']['schema_properties'], None)
