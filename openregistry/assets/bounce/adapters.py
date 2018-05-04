# -*- coding: utf-8 -*-
from openregistry.assets.core.adapters import AssetConfigurator, AssetManagerAdapter
from openregistry.assets.core.constants import STATUS_CHANGES

from openregistry.assets.bounce.validation import validate_deleted_status


class BounceAssetConfigurator(AssetConfigurator):
    """ BelowThreshold Tender configuration adapter """

    name = "Bounce Asset configurator"
    available_statuses = STATUS_CHANGES


class BounceAssetManagerAdapter(AssetManagerAdapter):
    name = "Asset Manager for bounce asset"
    context = None
    create_validation = []
    change_validation = [validate_deleted_status]

    def __init__(self, context):
        self.context = context

    def create_asset(self, request):
        self._validate(request, self.create_validation)

    def change_asset(self, request):
        self._validate(request, self.change_validation)
