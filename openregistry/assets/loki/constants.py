# -*- coding: utf-8 -*-

from openregistry.assets.core.constants import DOCUMENT_TYPES


LOKI_ASSET_DOC_TYPE = "informationDetails"

INFORMATION_DETAILS = {
    'title': 'TODO',
    'url': 'TODO',
    'documentOf': "asset",
    'documentType': LOKI_ASSET_DOC_TYPE
}


ASSET_LOKI_DOCUMENT_TYPES = DOCUMENT_TYPES + [LOKI_ASSET_DOC_TYPE, 'cancellationDetails']
