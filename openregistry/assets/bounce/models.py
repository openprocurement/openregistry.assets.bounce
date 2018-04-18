# -*- coding: utf-8 -*-
from datetime import timedelta

from schematics.types import StringType, URLType, IntType
from schematics.transforms import whitelist, blacklist
from schematics.types.compound import ListType, ModelType
from schematics.exceptions import ValidationError
from schematics.types.serializable import serializable

from pyramid.security import Allow

from zope.interface import implementer

from openregistry.assets.core.models import (
    IAsset,
    Asset as BaseAsset,
    Period,
    LokiDocument as Document,
    LokiItem as Item,
    AssetHolder,
    AssetCustodian,
    Decision,
)
from openregistry.assets.core.utils import (
    get_now,
    calculate_business_date
)

from openregistry.assets.bounce.roles import (
    asset_roles,
    edit_role
)


from constants import (
    BOUNCE_ASSET_DOC_TYPE, RECTIFICATION_PERIOD_DURATION
)


class IBounceAsset(IAsset):
    """ Interface for bounce assets """


class Document(Document):
    documentOf = StringType(choices=['asset', 'item'])


@implementer(IBounceAsset)
class Asset(BaseAsset):
    description = StringType(required=True)
    assetType = StringType(default="bounce")
    assetHolder= ModelType(AssetHolder)
    assetCustodian = ModelType(AssetCustodian, required=True)
    rectificationPeriod = ModelType(Period)
    items = ListType(ModelType(Item), default=list())
    decisions = ListType(ModelType(Decision), min_size=1, max_size=1, required=True)
    documents = ListType(ModelType(Document), default=list())   # All documents and attachments
                                                                # related to the asset.
    class Options:
        roles = asset_roles

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_asset'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_asset_documents'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_asset_items'),
        ]
        return acl

    def __init__(self, *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)
        if self.rectificationPeriod and self.rectificationPeriod.endDate < get_now():
            self._options.roles['edit_pending'] = whitelist('status')
        else:
            self._options.roles['edit_pending'] = edit_role

    @serializable(serialized_name='rectificationPeriod', serialize_when_none=False)
    def rectificationPeriod_serializable(self):
        if self.status == 'pending' and not self.rectificationPeriod:
            self.rectificationPeriod = type(self).rectificationPeriod.model_class()
            self.rectificationPeriod.startDate = get_now()
            self.rectificationPeriod.endDate = calculate_business_date(self.rectificationPeriod.startDate,
                                                                       RECTIFICATION_PERIOD_DURATION)

    def validate_status(self, data, value):
        can_be_deleted = any([doc.documentType == 'cancellationDetails' for doc in data['documents']])
        if value == 'deleted' and not can_be_deleted:
            raise ValidationError(u"You can set deleted status"
                                  u"only when asset have at least one document with \'cancellationDetails\' documentType")

    def validate_documents(self, data, docs):
        if not docs:
            return
        if docs[0].documentType != BOUNCE_ASSET_DOC_TYPE:
            raise ValidationError(u"First document should be "
                                  u"document with {}"
                                  "documentType".format(BOUNCE_ASSET_DOC_TYPE))
