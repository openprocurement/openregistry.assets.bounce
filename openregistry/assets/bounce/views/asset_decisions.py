# -*- coding: utf-8 -*-
from openregistry.assets.core.utils import (
    update_file_content_type,
    json_view,
    context_unpack,
    APIResource,
)
from openregistry.assets.core.utils import (
    save_asset, opassetsresource, apply_patch,
)
from openregistry.assets.core.validation import (
    validate_decision_post,
    validate_decision_patch_data,
    validate_decision_update_in_not_allowed_status
)

post_validators = (
    validate_decision_post,
    validate_decision_update_in_not_allowed_status
)
patch_validators = (
    validate_decision_patch_data,
    validate_decision_update_in_not_allowed_status,
)


@opassetsresource(name='bounce:Asset Decisions',
                collection_path='/assets/{asset_id}/decisions',
                path='/assets/{asset_id}/decisions/{decision_id}',
                _internal_type='bounce',
                description="Asset related decisions")
class AssetDecisionResource(APIResource):

    @json_view(permission='view_asset')
    def collection_get(self):
        """Asset Decision List"""
        collection_data = [i.serialize("view") for i in self.context.decisions]
        return {'data': collection_data}

    @json_view(content_type="application/json", permission='upload_asset_decisions', validators=post_validators)
    def collection_post(self):
        """Asset Decision Upload"""
        decision = self.request.validated['decision']
        decision.decisionOf = 'asset'
        self.context.decisions.append(decision)
        if save_asset(self.request):
            self.LOGGER.info(
                'Created asset decision {}'.format(decision.id),
                extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_decision_create'}, {'decision_id': decision.id})
            )
            self.request.response.status = 201
            decision_route = self.request.matched_route.name.replace("collection_", "")
            self.request.response.headers['Location'] = self.request.current_route_url(
                                                            _route_name=decision_route,
                                                            decision_id=decision.id,
                                                            _query={}
                                                            )
            return {'data': decision.serialize("view")}

    @json_view(permission='view_asset')
    def get(self):
        """Asset Decision Read"""
        decision = self.request.validated['decision']
        return {'data': decision.serialize("view")}

    @json_view(content_type="application/json", permission='upload_asset_decisions', validators=patch_validators)
    def patch(self):
        """Asset Decision Update"""
        if apply_patch(self.request, src=self.request.context.serialize()):
            update_file_content_type(self.request)
            self.LOGGER.info(
                'Updated asset decision {}'.format(self.request.context.id),
                extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_decision_patch'})
            )
            return {'data': self.request.context.serialize("view")}
