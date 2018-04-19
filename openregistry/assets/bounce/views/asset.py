# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetResource
from openregistry.assets.core.utils import opassetsresource, json_view

from openregistry.assets.core.validation import (
    validate_patch_asset_data,
    validate_data_by_model,
    validate_change_status,
)
from  openregistry.assets.bounce.validation import validate_deleted_status

patch_asset_validators = (
    validate_patch_asset_data,
    validate_change_status,
    validate_data_by_model,
    validate_deleted_status
)

@opassetsresource(name='bounce:Asset',
                  path='/assets/{asset_id}',
                  assetType='bounce',
                  description="Open Contracting compatible data exchange format.")
class AssetBounceResource(AssetResource):


    @json_view(content_type="application/json",
               validators=patch_asset_validators,
               permission='edit_asset')
    def patch(self):
        return super(AssetBounceResource, self).patch()