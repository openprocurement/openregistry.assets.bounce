# -*- coding: utf-8 -*-
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType
from schematics.exceptions import ValidationError
from schematics.types.serializable import serializable

from pyramid.security import Allow

from zope.interface import implementer

from openregistry.assets.core.models import (
    IAsset,
    BaseAsset,
    Period,
    LokiDocument as Document,
    LokiItem as Item,
    AssetHolder,
    AssetCustodian,
    Decision,
    RelatedProcess,
)
from openregistry.assets.core.utils import (
    get_now,
    search_list_with_dicts,
)
from openregistry.assets.core.validation import (
    validate_items_uniq,
    validate_decision_uniq
)
from openregistry.assets.bounce.roles import (
    decision_roles,
    bounce_asset_roles,
)


from constants import (
    BOUNCE_ASSET_DOC_TYPE
)


class IBounceAsset(IAsset):
    """ Interface for bounce assets """
    pass


class AssetDocument(Document):
    documentOf = StringType(choices=['asset', 'item'])


class AssetDecision(Decision):
    class Options:
        roles = decision_roles

    decisionOf = StringType(choices=['asset'], default='asset')

    def get_role(self):
        root = self.__parent__.__parent__
        request = root.request
        if request.validated['asset'].status in request.content_configurator.decision_editing_allowed_statuses:
            role = 'edit'
        else:
            role = 'not_edit'
        return role


@implementer(IBounceAsset)
class Asset(BaseAsset):
    description = StringType(required=True)
    _internal_type = 'bounce'
    assetType = StringType(default="bounce")
    assetHolder = ModelType(AssetHolder)
    assetCustodian = ModelType(AssetCustodian, required=True)
    rectificationPeriod = ModelType(Period)
    items = ListType(ModelType(Item), default=list(), validators=[validate_items_uniq])
    decisions = ListType(ModelType(AssetDecision), default=list(), validators=[validate_decision_uniq])
    # All documents and attachments related to the asset
    documents = ListType(ModelType(AssetDocument), default=list())
    relatedProcesses = ListType(ModelType(RelatedProcess), default=list(), max_size=1)

    class Options:
        roles = bounce_asset_roles

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_asset'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_asset_documents'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_asset_items'),
            (Allow, 'g:concierge', 'create_related_process'),
            (Allow, 'g:concierge', 'edit_related_process'),
            (Allow, 'g:concierge', 'delete_related_process'),
        ]
        return acl

    def get_role(self):
        root = self.__parent__
        request = root.request
        if request.authenticated_role == 'Administrator':
            role = 'Administrator'
        elif request.authenticated_role == 'concierge':
            role = 'concierge'
        else:
            role = 'edit_{}'.format(request.context.status)
        return role

    @serializable(serialized_name='rectificationPeriod', serialize_when_none=False)
    def rectificationPeriod_serializable(self):
        if self.status == 'pending' and not self.rectificationPeriod:
            self.rectificationPeriod = type(self).rectificationPeriod.model_class()
            self.rectificationPeriod.startDate = get_now()

    def validate_documents(self, data, docs):
        if not docs:
            return
        if docs[0].documentType != BOUNCE_ASSET_DOC_TYPE:
            raise ValidationError(u"First document should be "
                                  u"document with {}"
                                  "documentType".format(BOUNCE_ASSET_DOC_TYPE))

    def validate_relatedProcesses(self, context, related_processes):
        related_lots = search_list_with_dicts(related_processes, 'type', 'lot')
        if context['status'] == 'active' and not related_lots:
            raise ValidationError(u'Asset must have related lot to become active.')
