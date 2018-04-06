# -*- coding: utf-8 -*-

def create_resource_document_json(self):
    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_document_data})
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

    response = self.app.get('/{}/documents'.format(self.resource_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"][1]["id"])
    self.assertEqual(u'укр.doc', response.json["data"][1]["title"])

    response = self.app.get('/{}/documents/{}'.format(self.resource_id, doc_id),
                            params={'download': 'some_id'}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location': u'url', u'name': u'download'}
    ])

    response = self.app.get('/{}/documents/{}'.format(self.resource_id, doc_id),
                            params={'download': key})
    self.assertEqual(response.status, '302 Moved Temporarily')
    self.assertIn('http://localhost/get/', response.location)
    self.assertIn('Signature=', response.location)
    self.assertIn('KeyID=', response.location)
    self.assertNotIn('Expires=', response.location)

    response = self.app.get('/{}/documents/{}'.format(
        self.resource_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual(u'укр.doc', response.json["data"]["title"])

    self.set_status(self.forbidden_document_modification_actions_status)

    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_document_data},
                                  status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't update document in current ({}) {} status".format(self.forbidden_document_modification_actions_status, self.resource_name[:-1]))


def put_resource_document_json(self):
    response = self.app.post_json('/{}/documents'.format(self.resource_id),
                                  headers=self.access_header,
                                  params={'data': self.initial_document_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(u'укр.doc', response.json["data"]["title"])
    doc_id = response.json["data"]['id']
    dateModified = response.json["data"]['dateModified']
    datePublished = response.json["data"]['datePublished']
    self.assertIn(doc_id, response.headers['Location'])

    response = self.app.put_json('/{}/documents/{}'.format(self.resource_id, doc_id),
        headers=self.access_header, params={
            'data': {
                'title': u'name.doc',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
            }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertIn('Signature=', response.json["data"]["url"])
    self.assertIn('KeyID=', response.json["data"]["url"])
    self.assertNotIn('Expires=', response.json["data"]["url"])
    key = response.json["data"]["url"].split('/')[-1].split('?')[0]
    tender = self.db.get(self.resource_id)
    self.assertIn(key, tender['documents'][-1]["url"])
    self.assertIn('Signature=', tender['documents'][-1]["url"])
    self.assertIn('KeyID=', tender['documents'][-1]["url"])
    self.assertNotIn('Expires=', tender['documents'][-1]["url"])

    response = self.app.get('/{}/documents/{}'.format(self.resource_id, doc_id),
                            params={'download': key})
    self.assertEqual(response.status, '302 Moved Temporarily')
    self.assertIn('http://localhost/get/', response.location)
    self.assertIn('Signature=', response.location)
    self.assertIn('KeyID=', response.location)
    self.assertNotIn('Expires=', response.location)

    response = self.app.get('/{}/documents/{}'.format(
        self.resource_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual(u'name.doc', response.json["data"]["title"])
    dateModified2 = response.json["data"]['dateModified']
    self.assertTrue(dateModified < dateModified2)
    self.assertEqual(dateModified, response.json["data"]["previousVersions"][0]['dateModified'])
    self.assertEqual(response.json["data"]['datePublished'], datePublished)

    response = self.app.get('/{}/documents'.format(self.resource_id), params={'all': 'true'})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(dateModified, response.json["data"][1]['dateModified'])
    self.assertEqual(dateModified2, response.json["data"][2]['dateModified'])

    response = self.app.post_json('/{}/documents'.format(self.resource_id),
        headers=self.access_header, params={
            'data': {
                'title': 'name.doc',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
            }})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    dateModified = response.json["data"]['dateModified']
    self.assertIn(doc_id, response.headers['Location'])

    response = self.app.get('/{}/documents'.format(self.resource_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(dateModified2, response.json["data"][1]['dateModified'])
    self.assertEqual(dateModified, response.json["data"][2]['dateModified'])

    response = self.app.put_json('/{}/documents/{}'.format(self.resource_id, doc_id),
                                 headers=self.access_header,
                                 params={'data': self.initial_document_data})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertIn('Signature=', response.json["data"]["url"])
    self.assertIn('KeyID=', response.json["data"]["url"])
    self.assertNotIn('Expires=', response.json["data"]["url"])
    key = response.json["data"]["url"].split('/')[-1].split('?')[0]
    tender = self.db.get(self.resource_id)
    self.assertIn(key, tender['documents'][-1]["url"])
    self.assertIn('Signature=', tender['documents'][-1]["url"])
    self.assertIn('KeyID=', tender['documents'][-1]["url"])
    self.assertNotIn('Expires=', tender['documents'][-1]["url"])

    response = self.app.get('/{}/documents/{}'.format(self.resource_id, doc_id),
                            params={'download': key})
    self.assertEqual(response.status, '302 Moved Temporarily')
    self.assertIn('http://localhost/get/', response.location)
    self.assertIn('Signature=', response.location)
    self.assertIn('KeyID=', response.location)
    self.assertNotIn('Expires=', response.location)

    self.set_status(self.forbidden_document_modification_actions_status)

    response = self.app.put_json('/{}/documents/{}'.format(self.resource_id, doc_id),
                                 headers=self.access_header,
                                 params={'data': self.initial_document_data},
                                 status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't update document in current ({}) {} status".format(self.forbidden_document_modification_actions_status, self.resource_name[:-1]))
