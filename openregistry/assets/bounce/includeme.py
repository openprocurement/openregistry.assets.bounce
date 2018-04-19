# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest
from openregistry.assets.core.interfaces import IContentConfigurator
from openregistry.assets.bounce.models import Asset, IBounceAsset
from openregistry.assets.bounce.adapters import BounceAssetConfigurator


def includeme(config):
    config.add_assetType(Asset)
    config.scan("openregistry.assets.bounce.views")
    config.scan("openregistry.assets.bounce.subscribers")
    config.registry.registerAdapter(BounceAssetConfigurator,
                                    (IBounceAsset, IRequest),
                                    IContentConfigurator)
