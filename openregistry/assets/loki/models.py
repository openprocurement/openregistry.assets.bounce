# -*- coding: utf-8 -*-
from datetime import timedelta

from schematics.types import StringType, URLType, IntType
from schematics.transforms import whitelist, blacklist
from schematics.types.compound import ListType, ModelType
from schematics.exceptions import ValidationError
from schematics.types.serializable import serializable

from zope.interface import implementer

from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset
)

from openprocurement.api.models.models import (
    Period
)
from openprocurement.api.utils import (
    get_now,
    calculate_business_date
)

from openprocurement.api.models.registry_models.roles import schematics_default_role, plain_role, listing_role
from openregistry.assets.loki.roles import (
    create_role,
    edit_role,
    view_role,
    plain_role,
    Administrator_role,
    concierge_role
)
from openprocurement.api.models.registry_models.ocds import (
    lokiDocument as Document,
    lokiItem as Item
)
from openprocurement.api.constants import DOCUMENT_TYPES

from constants import INFORMATION_DETAILS, LOKI_ASSET_DOC_TYPE


class ILokiAsset(IAsset):
    """ Interface for loki assets """

    def initialize():
        """Add additional data to object then it creates"""
        raise NotImplementedError


DOCUMENT_TYPES += [LOKI_ASSET_DOC_TYPE, 'cancellationDetails']


class Document(Document):
    documentType = StringType(choices=DOCUMENT_TYPES)
    format = StringType(regex='^[-\w]+/[-\.\w\+]+$')


@implementer(ILokiAsset)
class Asset(BaseAsset):
    assetType = StringType(default="loki")
    rectificationPeriod = ModelType(Period)
    items = ListType(ModelType(Item))
    documents = ListType(ModelType(Document), default=list())   # All documents and attachments
                                                                # related to the asset.
    class Options:
        roles = {
            'create': create_role,
            # draft role
            'draft': view_role,
            'edit_draft': edit_role,
            'plain': plain_role,
            'edit': edit_role,
            # pending role
            'edit_pending': edit_role,
            'pending': view_role,
            # verification role
            'verification': view_role,
            'edit_verification': whitelist(),
            # active role
            'active': view_role,
            'edit_active': whitelist(),
            'view': view_role,
            'listing': listing_role,
            'Administrator': Administrator_role,
            # complete role
            'complete': view_role,
            'edit_complete': blacklist('revisions'),
            # deleted role  # TODO: replace with 'delete' view for asset, temporary solution for tests
            'deleted': view_role,
            'edit_deleted': blacklist('revisions'),
            # concierge_role
            'concierge': concierge_role,
            'default': schematics_default_role,
        }

    @serializable(serialized_name='rectificationPeriod')
    def rectificationPeriod_serializable(self):
        if self.status == 'pending' and not self.rectificationPeriod:
            self.rectificationPeriod = type(self).rectificationPeriod.model_class()
            self.rectificationPeriod.startDate = get_now()
            self.rectificationPeriod.endDate = calculate_business_date(self.rectificationPeriod.startDate, timedelta(1))

    def initialize(self):
        self.documents.append(type(self).documents.model_class(INFORMATION_DETAILS))

    def validate_status(self, data, value):
        can_be_deleted = any([doc.documentType == 'cancellationDetails' for doc in data['documents']])
        if value == 'deleted' and not can_be_deleted:
            raise ValidationError('You can set deleted status only when asset have at least one document with \'cancellationDetails\' documentType')

    def validate_documents(self, data, docs):
        if not docs:
            return
        if docs[0].documentType != LOKI_ASSET_DOC_TYPE:
            raise ValidationError(u"First document should be "
                                  u"document with {}"
                                  "documentType".format(LOKI_ASSET_DOC_TYPE))
