# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetResource
from openregistry.assets.core.utils import opassetsresource


@opassetsresource(name='loki:Asset',
                  path='/assets/{asset_id}',
                  assetType='loki',
                  description="Open Contracting compatible data exchange format.")
class AssetCompoundResource(AssetResource):
    pass
