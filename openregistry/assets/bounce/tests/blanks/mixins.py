# -*- coding: utf-8 -*-

# from openregistry.assets.bounce.tests.base import snitch

from openregistry.assets.core.tests.base import snitch

from openregistry.assets.core.tests.blanks.document import (
    not_found,
    create_document_in_forbidden_resource_status,
    put_resource_document_invalid,
    create_resource_document_error,
    create_resource_document_json_invalid
)


from .document import (
    create_resource_document_json,
    put_resource_document_json,
    patch_resource_document,
    rectificationPeriod_document_workflow
)

class AssetBounceResourceDocumentTestMixin(object):
    """ Mixin with asset bounce tests for Asset and Lot documents
    """

    test_01_not_found = snitch(not_found)
    test_02_create_document_in_forbidden_resource_status = snitch(create_document_in_forbidden_resource_status)
    test_03_put_resource_document_invalid = snitch(put_resource_document_invalid)
    test_04_patch_resource_document = snitch(patch_resource_document)
    test_05_create_resource_document_error = snitch(create_resource_document_error)
    test_06_create_resource_document_json_invalid = snitch(create_resource_document_json_invalid)
    test_07_create_resource_document_json = snitch(create_resource_document_json)
    test_08_put_resource_document_json = snitch(put_resource_document_json)
    test_rectificationPeriod_document_workflow = snitch(rectificationPeriod_document_workflow)
