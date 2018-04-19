# -*- coding: utf-8 -*-
from openregistry.assets.core.utils import (
    get_file,
    update_file_content_type,
    json_view,
    context_unpack,
    APIResource,
)
from openregistry.assets.core.utils import (
    save_asset, opassetsresource, apply_patch,
)
from openregistry.assets.bounce.validation import (
    rectificationPeriod_item_validation,
    validate_item_data
)


@opassetsresource(name='assets:Asset Items',
                collection_path='/assets/{asset_id}/items',
                path='/assets/{asset_id}/items/{item_id}',
                assetType='bounce',
                description="Asset related items")
class AssetBounceItemResource(APIResource):

    @json_view(permission='view_asset')
    def collection_get(self):
        """Asset Item List"""
        if self.request.params.get('all', ''):
            collection_data = [i.serialize("view") for i in self.context.items]
        else:
            collection_data = sorted(dict([
                (i.id, i.serialize("view"))
                for i in self.context.items
            ]).values(), key=lambda i: i['dateModified'])
        return {'data': collection_data}

    @json_view(content_type="application/json", permission='upload_asset_items', validators=(validate_item_data, rectificationPeriod_item_validation))
    def collection_post(self):
        """Asset Item Upload"""
        item = self.request.validated['item']
        self.context.items.append(item)
        if save_asset(self.request):
            self.LOGGER.info('Created asset item {}'.format(item.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_item_create'}, {'item_id': item.id}))
            self.request.response.status = 201
            item_route = self.request.matched_route.name.replace("collection_", "")
            self.request.response.headers['Location'] = self.request.current_route_url(_route_name=item_route, item_id=item.id, _query={})
            return {'data': item.serialize("view")}

    @json_view(permission='view_asset')
    def get(self):
        """Asset Item Read"""
        item = self.request.validated['item']
        item_data = item.serialize("view")
        return {'data': item_data}

    @json_view(content_type="application/json", permission='upload_asset_items', validators=(validate_item_data, rectificationPeriod_item_validation))
    def patch(self):
        """Asset Item Update"""
        if apply_patch(self.request, src=self.request.context.serialize()):
            update_file_content_type(self.request)
            self.LOGGER.info('Updated asset item {}'.format(self.request.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_item_patch'}))
            return {'data': self.request.context.serialize("view")}
