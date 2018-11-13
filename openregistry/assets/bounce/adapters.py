# -*- coding: utf-8 -*-
from openregistry.assets.core.adapters import (
    AssetConfigurator,
    AssetManagerAdapter,
    Manager,
)
from openregistry.assets.core.constants import STATUS_CHANGES
from openregistry.assets.core.utils import save_asset, apply_patch

from openregistry.assets.bounce.utils import status_change_depending_actions
from openregistry.assets.bounce.validation import (
    validate_deleted_status,
    validate_pending_status
)
from openregistry.assets.bounce.constants import DECISION_EDITING_STATUSES


class BounceAssetConfigurator(AssetConfigurator):
    """ BelowThreshold Tender configuration adapter """

    name = "Bounce Asset configurator"
    available_statuses = STATUS_CHANGES
    decision_editing_allowed_statuses = DECISION_EDITING_STATUSES


class BounceRelatedProcessesManager(Manager):
    def create(self, request):
        self.context.relatedProcesses.append(request.validated['relatedProcess'])
        return save_asset(request)

    def update(self, request):
        return apply_patch(request, src=request.context.serialize())

    def delete(self, request):
        self.context.relatedProcesses.remove(request.validated['relatedProcess'])
        self.context.modified = False
        return save_asset(request)


class BounceAssetManagerAdapter(AssetManagerAdapter):
    name = "Asset Manager for bounce asset"
    context = None
    create_validation = []
    change_validation = (
        validate_deleted_status,
        validate_pending_status
    )

    def __init__(self, context):
        self.context = context
        self.related_processes_manager = BounceRelatedProcessesManager(parent=context, parent_name='context')

    def create_asset(self, request):
        self._validate(request, self.create_validation)

    def change_asset(self, request):
        self._validate(request, self.change_validation)
        status_change_depending_actions(request)
