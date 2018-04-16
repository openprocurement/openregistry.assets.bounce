# -*- coding: utf-8 -*-
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType
from schematics.exceptions import ValidationError
from zope.interface import implementer
from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset, Item, Document
)

from constants import (
    INFORMATION_DETAILS, BOUNCE_ASSET_DOC_TYPE, ASSET_BOUNCE_DOCUMENT_TYPES
)


class IBounceAsset(IAsset):
    """ Interface for bounce assets """

class Document(Document):
    documentType = StringType(choices=ASSET_BOUNCE_DOCUMENT_TYPES)
    format = StringType(regex='^[-\w]+/[-\.\w\+]+$')


@implementer(IBounceAsset)
class Asset(BaseAsset):
    assetType = StringType(default="bounce")
    items = ListType(ModelType(Item))
    documents = ListType(ModelType(Document), default=list())   # All documents and attachments
                                                                # related to the asset.


    def validate_documents(self, data, docs):
        if not docs:
            return
        if docs[0].documentType != BOUNCE_ASSET_DOC_TYPE:
            raise ValidationError(u"First document should be "
                                  u"document with {}"
                                  "documentType".format(BOUNCE_ASSET_DOC_TYPE))
