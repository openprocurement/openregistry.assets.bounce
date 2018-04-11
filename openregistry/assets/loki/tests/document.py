# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.assets.loki.tests.base import (
    AssetContentWebTest
)
from openprocurement.api.tests.blanks.json_data import test_document_data

from openprocurement.api.models.registry_models.ocds import LOKI_DOCUMENT_TYPES
from blanks.mixins import AssetLokiResourceDocumentTestMixin


class AssetDocumentWithDSResourceTest(AssetContentWebTest, AssetLokiResourceDocumentTestMixin):
    docservice = True
    document_types = LOKI_DOCUMENT_TYPES

    # status, in which operations with asset documents (adding, updating) are forbidden
    forbidden_document_modification_actions_status = 'active'

    def setUp(self):
        super(AssetDocumentWithDSResourceTest, self).setUp()
        self.initial_document_data = deepcopy(test_document_data)
        self.initial_document_data['url'] = self.generate_docservice_url()


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
