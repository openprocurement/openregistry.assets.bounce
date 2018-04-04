# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest
from openprocurement.api.interfaces import IContentConfigurator
from openregistry.assets.loki.models import Asset, ICompoundAsset
from openregistry.assets.loki.adapters import CompoundAssetConfigurator


def includeme(config):
    config.add_assetType(Asset)
    config.scan("openregistry.assets.loki.views")
    config.scan("openregistry.assets.loki.subscribers")
    config.registry.registerAdapter(CompoundAssetConfigurator,
                                    (ICompoundAsset, IRequest),
                                    IContentConfigurator)
