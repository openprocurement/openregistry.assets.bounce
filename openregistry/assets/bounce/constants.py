# -*- coding: utf-8 -*-

from openregistry.assets.core.constants import DOCUMENT_TYPES


BOUNCE_ASSET_DOC_TYPE = "informationDetails"

INFORMATION_DETAILS = {
    'title': 'TODO',
    'url': 'TODO',
    'documentOf': "asset",
    'documentType': BOUNCE_ASSET_DOC_TYPE
}


ASSET_BOUNCE_DOCUMENT_TYPES = DOCUMENT_TYPES + [BOUNCE_ASSET_DOC_TYPE, 'cancellationDetails']
