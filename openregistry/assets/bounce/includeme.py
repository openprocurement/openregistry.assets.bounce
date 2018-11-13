# -*- coding: utf-8 -*-
import logging

from pyramid.interfaces import IRequest
from openregistry.assets.core.interfaces import IContentConfigurator, IAssetManager
from openregistry.assets.core.utils import add_related_processes_views
from openregistry.assets.core.constants import ENDPOINTS
from openregistry.assets.bounce.models import Asset, IBounceAsset
from openregistry.assets.bounce.adapters import BounceAssetConfigurator, BounceAssetManagerAdapter
from openregistry.assets.core.traversal import factory
from openregistry.assets.bounce.constants import (
    DEFAULT_ASSET_BOUNCE_TYPE,
    DEFAULT_LEVEL_OF_ACCREDITATION
)
from openregistry.assets.bounce.migration import (
    BounceMigrationsRunner,
    MIGRATION_STEPS,
)

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

    # migrate data
    if plugin_config.get('migration') is True:
        runner = BounceMigrationsRunner(config.registry)
        runner.migrate(MIGRATION_STEPS)

    LOGGER.info("Included openregistry.assets.bounce plugin", extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    if not plugin_config.get('accreditation'):
        config.registry.accreditation['asset'][Asset._internal_type] = DEFAULT_LEVEL_OF_ACCREDITATION
    else:
        config.registry.accreditation['asset'][Asset._internal_type] = plugin_config['accreditation']

    # add related processes views
    add_related_processes_views(config, ENDPOINTS['assets'], factory)
