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


def rectificationPeriod_decision_workflow(self):
    rectificationPeriod = Period()
    rectificationPeriod.startDate = get_now() - timedelta(3)
    rectificationPeriod.endDate = calculate_business_date(rectificationPeriod.startDate,
                                                          timedelta(1),
                                                          None)

    self.create_resource()
    response = self.app.get('/{}'.format(self.resource_id))
    lot = response.json['data']

    self.set_status('pending')

    response = self.app.post_json('/{}/decisions'.format(lot['id']),
                                  headers=self.access_header,
                                  params={'data': self.initial_decision_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    decision_id = response.json["data"]['id']
    self.assertIn(decision_id, response.headers['Location'])
    self.assertEqual(self.initial_decision_data['decisionID'], response.json["data"]["decisionID"])
    self.assertEqual(self.initial_decision_data['decisionDate'], response.json["data"]["decisionDate"])
    self.assertEqual('asset', response.json["data"]["decisionOf"])
    decision_id = response.json['data']['id']

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['id'], lot['id'])

    # Change rectification period in db
    fromdb = self.db.get(lot['id'])
    fromdb = Asset(fromdb)

    fromdb.status = 'pending'
    fromdb.rectificationPeriod = rectificationPeriod
    fromdb = fromdb.store(self.db)

    self.assertEqual(fromdb.id, lot['id'])

    response = self.app.get('/{}'.format(lot['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['id'], lot['id'])

    response = self.app.post_json('/{}/decisions'.format(lot['id']),
                                   headers=self.access_header,
                                   params={'data': self.initial_decision_data},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]['description'], 'You can\'t change or add decisions after rectification period')

    response = self.app.patch_json('/{}/decisions/{}'.format(lot['id'], decision_id),
                                   headers=self.access_header,
                                   params={'data': self.initial_decision_data},
                                   status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.json['errors'][0]['description'], 'You can\'t change or add decisions after rectification period')


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
