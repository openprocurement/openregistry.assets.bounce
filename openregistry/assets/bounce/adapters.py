# -*- coding: utf-8 -*-
from openregistry.assets.core.adapters import AssetConfigurator
from openregistry.assets.core.constants import STATUS_CHANGES


class BounceAssetConfigurator(AssetConfigurator):
    """ BelowThreshold Tender configuration adapter """

    name = "Bounce Asset configurator"
    available_statuses = STATUS_CHANGES
