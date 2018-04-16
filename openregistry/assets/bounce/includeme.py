# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest
from openregistry.assets.core.interfaces import IContentConfigurator
from openregistry.assets.bounce.models import Asset, ILokiAsset
from openregistry.assets.bounce.adapters import CompoundAssetConfigurator


def includeme(config):
    config.add_assetType(Asset)
    config.scan("openregistry.assets.bounce.views")
    config.scan("openregistry.assets.bounce.subscribers")
    config.registry.registerAdapter(CompoundAssetConfigurator,
                                    (ILokiAsset, IRequest),
                                    IContentConfigurator)
