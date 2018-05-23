# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.assets.bounce.tests.base import (
    AssetContentWebTest
)
from openregistry.assets.core.tests.blanks.json_data import test_document_data

from openregistry.assets.core.constants import LOKI_DOCUMENT_TYPES
from blanks.mixins import AssetBounceResourceDocumentTestMixin


class AssetDocumentWithDSResourceTest(AssetContentWebTest, AssetBounceResourceDocumentTestMixin):
    docservice = True
    document_types = LOKI_DOCUMENT_TYPES

    # status, in which operations with asset documents (adding, updating) are forbidden
    forbidden_document_modification_actions_status = 'active'

    def setUp(self):
        super(AssetDocumentWithDSResourceTest, self).setUp()
        self.initial_document_data = deepcopy(test_document_data)
        self.initial_document_data['documentType'] = 'notice'
        self.initial_document_data['url'] = self.generate_docservice_url()


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
