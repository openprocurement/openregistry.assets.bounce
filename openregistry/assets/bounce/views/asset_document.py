# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetDocumentResource
from openregistry.assets.core.utils import opassetsresource

from openregistry.assets.core.validation import (
    validate_file_upload,
    validate_document_data,
    validate_patch_document_data,
)
from openregistry.assets.core.utils import (
    json_view,
)

from openregistry.assets.core.validation import (
    validate_document_operation_in_not_allowed_asset_status,
    validate_asset_document_update_not_by_author_or_asset_owner,
)
from openregistry.assets.bounce.validation import rectificationPeriod_document_validation


post_document_validators = (
    validate_file_upload,
    validate_document_operation_in_not_allowed_asset_status,
    rectificationPeriod_document_validation
)
put_document_validators = (
    validate_document_data,
    validate_document_operation_in_not_allowed_asset_status,
    validate_asset_document_update_not_by_author_or_asset_owner,
    rectificationPeriod_document_validation
)

patch_document_validators = (
    validate_patch_document_data,
    validate_document_operation_in_not_allowed_asset_status,
    validate_asset_document_update_not_by_author_or_asset_owner,
    rectificationPeriod_document_validation
)

@opassetsresource(name='bounce:Asset Documents',
                  collection_path='/assets/{asset_id}/documents',
                  path='/assets/{asset_id}/documents/{document_id}',
                  assetType='bounce',
                  description="Asset related binary files (PDFs, etc.)")
class AssetBounceDocumentResource(AssetDocumentResource):

    @json_view(content_type="application/json", permission='upload_asset_documents', validators=post_document_validators)
    def collection_post(self):
        return super(AssetBounceDocumentResource, self).collection_post()

    @json_view(content_type="application/json", permission='upload_asset_documents', validators=put_document_validators)
    def put(self):
        """Asset Document Update"""
        return super(AssetBounceDocumentResource, self).put()

    @json_view(content_type="application/json", permission='upload_asset_documents', validators=patch_document_validators)
    def patch(self):
        """Asset Document Update"""
        return super(AssetBounceDocumentResource, self).patch()
