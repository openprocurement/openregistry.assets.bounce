# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy
from datetime import timedelta

from openregistry.assets.core.utils import get_now, calculate_business_date
from openregistry.assets.core.models import (
    Period
)
from openregistry.assets.bounce.models import Asset


def item_listing(self):
    response = self.app.get('/{}/items'.format(self.resource_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), len(self.initial_data['items']))

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

    response = self.app.get('/{}/items'.format(self.resource_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), len(self.initial_data['items']) + 1)


def update_items_in_forbidden(self):
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

    data = self.initial_item_data
    data['quantity'] = 99.9999
    for status in self.forbidden_item_statuses_modification:
        self.set_status(status)
        response = self.app.patch_json('/{}/items/{}'.format(self.resource_id, item_id),
            headers=self.access_header, params={
                "data": data}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"],
                         "Can't update or create item in current ({}) {} status".format(status, self.resource_name[:-1]))

    for status in self.forbidden_item_statuses_modification:
        self.set_status(status)
        response = self.app.post_json('/{}/items'.format(self.resource_id),
            headers=self.access_header, params={
                "data": self.initial_item_data
            }, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"],
                         "Can't update or create item in current ({}) {} status".format(status, self.resource_name[:-1]))


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

    # Test partial update
    response = self.app.patch_json('/{}/items/{}'.format(self.resource_id, item_id),
        headers=self.access_header, params={
            "data": {
                "description": "partial item update",
                "additionalClassifications": []
            }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(item_id, response.json["data"]["id"])
    self.assertEqual(response.json["data"]["description"], 'partial item update')
    self.assertNotIn('additionalClassifications', response.json['data'])


def create_item_resource_invalid(self):
    pass


def patch_item_resource_invalid(self):
    pass


def list_item_resource(self):
    pass


def create_bounce_with_item_schemas(self):
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


def rectificationPeriod_item_workflow(self):
    rectificationPeriod = Period()
    rectificationPeriod.startDate = get_now() - timedelta(3)
    rectificationPeriod.endDate = calculate_business_date(rectificationPeriod.startDate,
                                                          timedelta(1),
                                                          None)

    asset = self.create_resource()

    response = self.app.post_json('/{}/items'.format(asset['id']),
                                  headers=self.access_header,
                                  params={'data': self.initial_item_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    item_id = response.json["data"]['id']
    self.assertIn(item_id, response.headers['Location'])
    self.assertEqual(self.initial_item_data['description'], response.json["data"]["description"])
    self.assertEqual(self.initial_item_data['quantity'], response.json["data"]["quantity"])
    self.assertEqual(self.initial_item_data['address'], response.json["data"]["address"])
    item_id = response.json['data']['id']

    response = self.app.get('/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['id'], asset['id'])

    # Change rectification period in db
    fromdb = self.db.get(asset['id'])
    fromdb = Asset(fromdb)

    fromdb.status = 'pending'
    fromdb.rectificationPeriod = rectificationPeriod
    fromdb = fromdb.store(self.db)

    self.assertEqual(fromdb.id, asset['id'])

    response = self.app.get('/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['id'], asset['id'])

    response = self.app.post_json('/{}/items'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': self.initial_item_data},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]['description'], 'You can\'t change items after rectification period')


    self.assertEqual(response.json['errors'][0]['description'], 'You can\'t change items after rectification period')
    response = self.app.patch_json('/{}/items/{}'.format(asset['id'], item_id),
                                   headers=self.access_header,
                                   params={'data': self.initial_item_data},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]['description'], 'You can\'t change items after rectification period')




