# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import timedelta

from openregistry.assets.core.tests.base import create_blacklist
from openregistry.assets.core.tests.blanks.json_data import test_loki_item_data
from openregistry.assets.core.constants import STATUS_CHANGES, ASSET_STATUSES

from openregistry.assets.core.models import (
    Period
)
from openregistry.assets.bounce.tests.base import (
    check_patch_status_200,
    check_patch_status_403
)

from openregistry.assets.core.utils import (
    get_now,
    calculate_business_date
)
# AssetResourceTest


def add_cancellationDetails_document(self, asset):
    # Add cancellationDetails document
    test_document_data = {
        # 'url': self.generate_docservice_url(),
        'title': u'укр.doc',
        'hash': 'md5:' + '0' * 32,
        'format': 'application/msword',
        'documentType': 'cancellationDetails'
    }
    test_document_data['url'] = self.generate_docservice_url()

    response = self.app.post_json('/{}/documents'.format(asset['id']),
                                  headers=self.access_header,
                                  params={'data': test_document_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])
    self.assertEqual(u'укр.doc', response.json["data"]["title"])
    self.assertIn('Signature=', response.json["data"]["url"])
    self.assertIn('KeyID=', response.json["data"]["url"])
    self.assertNotIn('Expires=', response.json["data"]["url"])
    key = response.json["data"]["url"].split('/')[-1].split('?')[0]
    tender = self.db.get(self.resource_id)
    self.assertIn(key, tender['documents'][-1]["url"])
    self.assertIn('Signature=', tender['documents'][-1]["url"])
    self.assertIn('KeyID=', tender['documents'][-1]["url"])
    self.assertNotIn('Expires=', tender['documents'][-1]["url"])


def patch_asset(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()
    dateModified = asset.pop('dateModified')

    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'title': ' PATCHED'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']['dateModified'], dateModified)

    asset = self.create_resource()
    self.set_status('draft')

    # Move status from Draft to Active
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'active'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (draft) status")

    # Move status from Draft to Deleted
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'deleted'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (draft) status")

    # Move status from Draft to Complete
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'complete'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (draft) status")

    # Move status from Draft to Pending
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')

    # Move status from Pending to Draft
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'draft'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't switch asset to draft status")

    # Move status from Pending to Active
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'active'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

    # Move status from Pending to Complete
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'complete'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

    # Move status from Pending to Deleted 403
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'deleted'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'][0]['description'],
                    u"You can set deleted status "
                    u"only when asset have at least one document with \'cancellationDetails\' documentType")

    add_cancellationDetails_document(self, asset)


    # Move status from Pending to Deleted
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'deleted'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'deleted')

    # Move status from Deleted to Draft
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'draft'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")

    # Move status from Deleted to Pending
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'pending'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")

    # Move status from Deleted to Active
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'active'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")

    # Move status from Deleted to Complete
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'complete'}},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")


def simple_add_asset(self):

    u = self.asset_model(self.initial_data)
    u.assetID = "UA-X"

    assert u.id is None
    assert u.rev is None

    u.store(self.db)

    assert u.id is not None
    assert u.rev is not None

    fromdb = self.db.get(u.id)

    assert u.assetID == fromdb['assetID']
    assert u.doc_type == "Asset"

    u.delete_instance(self.db)


# Asset workflow test
ROLES = ['asset_owner', 'Administrator', 'concierge', 'convoy']
STATUS_BLACKLIST = create_blacklist(STATUS_CHANGES, ASSET_STATUSES, ROLES)


def create_asset_with_items(self):
    data = deepcopy(self.initial_data)
    data['items'] = [deepcopy(test_loki_item_data)]

    response = self.app.post_json('/', params={'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('id', response.json['data']['items'][0])
    self.assertEqual(response.json['data']['items'][0]['unit'], data['items'][0]['unit'])
    self.assertEqual(response.json['data']['items'][0]['classification'], data['items'][0]['classification'])
    self.assertEqual(response.json['data']['items'][0]['address'], data['items'][0]['address'])
    self.assertEqual(response.json['data']['items'][0]['quantity'], data['items'][0]['quantity'])
    self.assertEqual(response.json['data']['items'][0]['additionalClassifications'], data['items'][0]['additionalClassifications'])


    del data['items'][0]['unit']

    response = self.app.post_json('/', params={'data': data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['description'][0]['unit'], ['This field is required.'])


def dateModified_resource(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.post_json('/', {'data': self.initial_data})
    self.assertEqual(response.status, '201 Created')
    resource = response.json['data']
    token = str(response.json['access']['token'])
    dateModified = resource['dateModified']

    response = self.app.get('/{}'.format(resource['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['dateModified'], dateModified)

    # Add decision
    response = self.app.get('/{}'.format(resource['id']))
    old_decs_count = len(response.json['data'].get('decisions', []))

    decision_data = {
        'decisionDate': get_now().isoformat(),
        'decisionID': 'decisionLotID'
    }
    response = self.app.post_json(
        '/{}/decisions'.format(resource['id']),
        {"data": decision_data},
        headers={'X-Access-Token': token}
    )
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.json['data']['decisionDate'], decision_data['decisionDate'])
    self.assertEqual(response.json['data']['decisionID'], decision_data['decisionID'])

    response = self.app.get('/{}'.format(resource['id']))
    present_decs_count = len(response.json['data'].get('decisions', []))
    self.assertEqual(old_decs_count + 1, present_decs_count)
    resource = response.json['data']

    response = self.app.patch_json('/{}'.format(resource['id']),
        headers={'X-Access-Token': token}, params={
            'data': {'status': 'pending'}
    })
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')

    self.assertNotEqual(response.json['data']['dateModified'], dateModified)
    resource = response.json['data']
    dateModified = resource['dateModified']

    response = self.app.get('/{}'.format(resource['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], resource)
    self.assertEqual(response.json['data']['dateModified'], dateModified)


def change_pending_asset(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_resource()


    self.app.authorization = ('Basic', ('convoy', ''))

    # Move from 'pending' to one of blacklist status
    for status in STATUS_BLACKLIST['pending']['convoy']:
        check_patch_status_403(self, asset['id'], status)


    self.app.authorization = ('Basic', ('broker', ''))

    # Move from 'pending' to one of blacklist status
    for status in STATUS_BLACKLIST['pending']['asset_owner']:
        check_patch_status_403(self, asset['id'], status, self.access_header)

    # Move from 'pending' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending', self.access_header)

    # Add cancellationDetails document
    add_cancellationDetails_document(self, asset)

    # Move from 'pending' to 'deleted' status
    check_patch_status_200(self, asset['id'], 'deleted', self.access_header)


    asset = self.create_resource()

    # Add cancellationDetails document
    add_cancellationDetails_document(self, asset)


    self.app.authorization = ('Basic', ('administrator', ''))

    # Move from 'pending' to one of blacklist status
    for status in STATUS_BLACKLIST['pending']['Administrator']:
        check_patch_status_403(self, asset['id'], status)

    # Move from 'pending' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, asset['id'], 'verification')

    # Move from 'verification' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'deleted' status
    check_patch_status_200(self, asset['id'], 'deleted')


    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()


    self.app.authorization = ('Basic', ('concierge', ''))

    # Move from 'pending' to one of blacklist status
    for status in STATUS_BLACKLIST['pending']['concierge']:
        check_patch_status_403(self, asset['id'], status)

    # Move from 'pending' to 'pending' status
    check_patch_status_200(self, asset['id'], 'pending')

    # Move from 'pending' to 'verification' status
    check_patch_status_200(self, asset['id'], 'verification')


    self.app.authorization = ('Basic', ('broker', ''))
    data = deepcopy(self.initial_data)
    data['status'] = 'draft'
    data['items'] = []
    response = self.app.post_json('/', params={'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'draft')
    self.assertNotIn('items', response.json['data'])
    asset = response.json['data']
    token = response.json['access']['token']
    access_header = {'X-Access-Token': str(token)}

    response = self.app.patch_json('/{}'.format(asset['id']), params={'data': {'status': 'pending'}}, headers=access_header, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(
        response.json['errors'][0]['description'],
        'You cannot switch the asset status from draft to pending unless at least one item has been added.'
    )

    response = self.app.post_json('/{}/items'.format(asset['id']),
                                  headers=access_header,
                                  params={'data': self.initial_item_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.patch_json('/{}'.format(asset['id']), params={'data': {'status': 'pending'}}, headers=access_header, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(
        response.json['errors'][0]['description'],
        'You cannot switch the asset status from draft to pending unless at least one decision has been added.'
    )

    response = self.app.post_json('/{}/decisions'.format(asset['id']),
                                  headers=access_header,
                                  params={'data': self.initial_decision_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.patch_json('/{}'.format(asset['id']), params={'data': {'status': 'pending'}}, headers=access_header)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')
    self.assertEqual(len(response.json['data']['items']), 1)


def administrator_change_delete_status(self):
    response = self.app.get('/')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_resource()

    response = self.app.get('/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], asset)

    add_cancellationDetails_document(self, asset)


    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'pending'}}
    )
    self.assertEqual(response.status, '200 OK')


    response = self.app.patch_json(
        '/{}'.format(asset['id']),
        {'data': {'status': 'deleted'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json('/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")


def patch_decimal_item_quantity(self):
    """ Testing different decimal quantity (decimal_numbers) at the root and items of assets."""
    precision = self.precision if hasattr(self, 'precision') else 3
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


    for quantity in [3, '3', 7.658, '7.658', 2.3355, '2.3355']:
        item_data = deepcopy(self.initial_item_data)
        item_data['quantity'] = quantity
        response = self.app.patch_json('/{}/items/{}'.format(asset['id'], item_id),
                                       headers=self.access_header,
                                       params={'data': item_data})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')

        response = self.app.get('/{}/items/{}'.format(asset['id'], item_id),
                                       headers=self.access_header,
                                       params={'data': item_data})

        self.assertNotIsInstance(response.json['data']['quantity'], basestring)
        rounded_quantity = round(float(quantity), precision)
        self.assertEqual(response.json['data']['quantity'], rounded_quantity)


def rectificationPeriod_workflow(self):
    rectificationPeriod = Period()
    rectificationPeriod.startDate = get_now() - timedelta(3)
    rectificationPeriod.endDate = calculate_business_date(rectificationPeriod.startDate,
                                                          timedelta(1),
                                                          None)

    asset = self.create_resource()

    response = self.app.get('/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['id'], asset['id'])

    # Change rectification period in db
    fromdb = self.db.get(asset['id'])
    fromdb = self.asset_model(fromdb)

    fromdb.status = 'pending'
    fromdb.rectificationPeriod = rectificationPeriod
    fromdb = fromdb.store(self.db)

    self.assertEqual(fromdb.id, asset['id'])

    response = self.app.get('/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['id'], asset['id'])

    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'title': ' PATCHED'}})
    self.assertNotEqual(response.json['data']['title'], 'PATCHED')
    self.assertEqual(asset['title'], response.json['data']['title'])

    add_cancellationDetails_document(self, asset)
    check_patch_status_200(self, asset['id'], 'deleted', self.access_header)
