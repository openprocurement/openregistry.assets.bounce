# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest
from openregistry.assets.core.interfaces import IContentConfigurator
from openregistry.assets.loki.models import Asset, ILokiAsset
from openregistry.assets.loki.adapters import CompoundAssetConfigurator


def includeme(config):
    config.add_assetType(Asset)
    config.scan("openregistry.assets.loki.views")
    config.scan("openregistry.assets.loki.subscribers")
    config.registry.registerAdapter(CompoundAssetConfigurator,
                                    (ILokiAsset, IRequest),
                                    IContentConfigurator)
