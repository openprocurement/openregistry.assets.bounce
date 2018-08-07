# -*- coding: utf-8 -*-
import logging

from pyramid.interfaces import IRequest
from openregistry.assets.core.interfaces import IContentConfigurator, IAssetManager
from openregistry.assets.bounce.models import Asset, IBounceAsset
from openregistry.assets.bounce.adapters import BounceAssetConfigurator, BounceAssetManagerAdapter
from openregistry.assets.bounce.constants import DEFAULT_ASSET_BOUNCE_TYPE

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_config=None):
    config.scan("openregistry.assets.bounce.views")
    config.scan("openregistry.assets.bounce.subscribers")
    config.registry.registerAdapter(BounceAssetConfigurator,
                                    (IBounceAsset, IRequest),
                                    IContentConfigurator)
    config.registry.registerAdapter(BounceAssetManagerAdapter,
                                    (IBounceAsset,),
                                    IAssetManager)
    asset_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        asset_types.append(DEFAULT_ASSET_BOUNCE_TYPE)
    for at in asset_types:
        config.add_assetType(Asset, at)

    LOGGER.info("Included openregistry.assets.bounce plugin", extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    config.registry.accreditation['asset'][Asset._internal_type] = plugin_config['accreditation']
