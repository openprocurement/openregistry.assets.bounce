# -*- coding: utf-8 -*-
from datetime import timedelta
from copy import deepcopy

from openregistry.assets.core.utils import (
    get_now,
    calculate_business_date
)

from openregistry.assets.bounce.models import (
    Asset,
    Period
)
from openregistry.assets.bounce.tests.base import (
    check_patch_status_200
)


def create_decision(self):
    self.app.authorization = ('Basic', ('broker', ''))

    decision_data = deepcopy(self.initial_decision_data)

    response = self.app.get('/{}'.format(self.resource_id))
    old_decs_count = len(response.json['data'].get('decisions', []))
    self.assertEqual(response.json['data']['status'], 'draft')

    decision_data.update({
        'relatedItem': '1' * 32
    })
    response = self.app.post_json(
        '/{}/decisions'.format(self.resource_id),
        {"data": decision_data},
        headers=self.access_header
    )
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.json['data']['decisionDate'], decision_data['decisionDate'])
    self.assertEqual(response.json['data']['decisionID'], decision_data['decisionID'])
    self.assertEqual(response.json['data']['decisionOf'], 'asset')
    self.assertNotIn('relatedItem', response.json['data'])

    response = self.app.get('/{}'.format(self.resource_id))
    present_decs_count = len(response.json['data'].get('decisions', []))
    self.assertEqual(old_decs_count + 1, present_decs_count)


def patch_decision(self):
    self.app.authorization = ('Basic', ('broker', ''))
    self.initial_status = 'draft'
    self.create_resource()

    decision_data = {'title': 'Some Title'}
    response = self.app.patch_json(
        '/{}/decisions/{}'.format(self.resource_id, self.decision_id),
        params={'data': decision_data},
        headers=self.access_header
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['id'], self.decision_id)
    self.assertEqual(response.json['data']['title'], decision_data['title'])


def create_or_patch_decision_in_not_allowed_status(self):
    self.app.authorization = ('Basic', ('broker', ''))
    self.initial_status = 'draft'
    self.create_resource()

    check_patch_status_200(self, self.resource_id, 'pending', self.access_header)

    self.app.authorization = ('Basic', ('concierge', ''))
    check_patch_status_200(self, self.resource_id, 'verification', self.access_header)

    self.app.authorization = ('Basic', ('broker', ''))
    decision_data = {
        'decisionDate': get_now().isoformat(),
        'decisionID': 'decisionLotID'
    }
    response = self.app.post_json(
        '/{}/decisions'.format(self.resource_id),
        {"data": decision_data},
        headers=self.access_header,
        status=403
    )
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(
        response.json['errors'][0]['description'],
        'Can\'t update decisions in current (verification) asset status'
    )

    response = self.app.patch_json(
        '/{}/decisions/{}'.format(self.resource_id, self.decision_id),
        {"data": decision_data},
        headers=self.access_header,
        status=403
    )
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(
        response.json['errors'][0]['description'],
        'Can\'t update decisions in current (verification) asset status'
    )


def patch_decisions_with_lot_by_broker(self):
    self.app.authorization = ('Basic', ('broker', ''))
    self.initial_status = 'draft'
    self.create_resource(with_decisions=False)

    decision_data = [
        {
            'decisionID': 'decID',
            'decisionDate': get_now().isoformat()
        },
        {
            'decisionID': 'decID2',
            'decisionDate': get_now().isoformat()
        }
    ]
    decision_data = {
        'decisions': decision_data
    }

    response = self.app.patch_json(
        '/{}'.format(self.resource_id),
        params={'data': decision_data},
        headers=self.access_header
    )
    self.assertNotIn('decisions', response.json)


def create_decisions_with_asset(self):
    data = deepcopy(self.initial_data)
    decision_1 = {'id': '1' * 32,  'decisionID': 'decID',  'decisionDate': get_now().isoformat()}
    decision_2 = deepcopy(decision_1)
    decision_2['id'] = '2' * 32
    data['decisions'] = [
       decision_1, decision_2
    ]
    response = self.app.post_json('/', params={'data': data})
    decision_1['decisionOf'] = 'asset'
    decision_2['decisionOf'] = 'asset'

    self.assertEqual(response.status, '201 Created')
    self.assertEqual(len(response.json['data']['decisions']), 2)
    self.assertEqual(response.json['data']['decisions'][0], decision_1)
    self.assertEqual(response.json['data']['decisions'][1], decision_2)

    del decision_1['decisionOf']
    del decision_2['decisionOf']

    decision_2['id'] = '1' * 32
    data['decisions'] = [
       decision_1, decision_2
    ]
    response = self.app.post_json('/', params={'data': data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(
        response.json['errors'][0]['description'][0],
        u'Decision id should be unique for all decisions'
    )
