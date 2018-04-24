# -*- coding: utf-8 -*-
import logging

from pyramid.interfaces import IRequest
from openregistry.assets.core.interfaces import IContentConfigurator, IAssetManager
from openregistry.assets.bounce.models import Asset, IBounceAsset
from openregistry.assets.bounce.adapters import BounceAssetConfigurator, BounceAssetManagerAdapter

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_config=None):
    config.add_assetType(Asset)
    config.scan("openregistry.assets.bounce.views")
    config.scan("openregistry.assets.bounce.subscribers")
    config.registry.registerAdapter(BounceAssetConfigurator,
                                    (IBounceAsset, IRequest),
                                    IContentConfigurator)
    config.registry.registerAdapter(BounceAssetManagerAdapter,
                                    (IBounceAsset,),
                                    IAssetManager)

    LOGGER.info("Included openregistry.lots.loki plugin", extra={'MESSAGE_ID': 'included_plugin'})
