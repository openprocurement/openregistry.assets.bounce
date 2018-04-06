# -*- coding: utf-8 -*-

from openprocurement.api.tests.base import create_blacklist
from openregistry.assets.core.constants import STATUS_CHANGES, ASSET_STATUSES

from uuid import uuid4

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

    # Move status from Pending to Deleted 422
    response = self.app.patch_json('/{}'.format(asset['id']),
                                   headers=self.access_header,
                                   params={'data': {'status': 'deleted'}},
                                   status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'][0]['description'][0],
                    u"You can set deleted status"
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
