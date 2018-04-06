# -*- coding: utf-8 -*-
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType
from schematics.exceptions import ValidationError
from zope.interface import implementer
from openprocurement.api.constants import DOCUMENT_TYPES
from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset, Item
)
from openprocurement.api.models.registry_models.ocds import Document

from constants import (
    INFORMATION_DETAILS, LOKI_ASSET_DOC_TYPE, ASSET_LOKI_DOCUMENT_TYPES
)


class ILokiAsset(IAsset):
    """ Interface for loki assets """

class Document(Document):
    documentType = StringType(choices=ASSET_LOKI_DOCUMENT_TYPES)
    format = StringType(regex='^[-\w]+/[-\.\w\+]+$')


@implementer(ILokiAsset)
class Asset(BaseAsset):
    assetType = StringType(default="loki")
    items = ListType(ModelType(Item))
    documents = ListType(ModelType(Document), default=list())   # All documents and attachments
                                                                # related to the asset.


    def validate_documents(self, data, docs):
        if not docs:
            return
        if docs[0].documentType != LOKI_ASSET_DOC_TYPE:
            raise ValidationError(u"First document should be "
                                  u"document with {}"
                                  "documentType".format(LOKI_ASSET_DOC_TYPE))
