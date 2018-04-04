# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetDocumentResource
from openregistry.assets.core.utils import opassetsresource


@opassetsresource(name='loki:Asset Documents',
                  collection_path='/assets/{asset_id}/documents',
                  path='/assets/{asset_id}/documents/{document_id}',
                  assetType='loki',
                  description="Asset related binary files (PDFs, etc.)")
class AssetCompoundDocumentResource(AssetDocumentResource):
    pass
