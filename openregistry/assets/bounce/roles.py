# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist
from openregistry.assets.core.models import assets_embedded_role, listing_role, schematics_default_role

plain_role = (blacklist('_attachments', 'revisions', 'dateModified', 'rectificationPeriod') + assets_embedded_role)

create_role = (
    blacklist(
        'owner_token', 'owner', '_attachments', 'revisions', 'date', 'decisions',
        'dateModified', 'doc_id', 'assetID', 'documents', 'status', 'rectificationPeriod'
    ) +
    assets_embedded_role
)
edit_role = (
    blacklist(
        'assetType', 'owner_token', 'owner', '_attachments', 'revisions', 'date', 'decisions',
        'dateModified', 'doc_id', 'assetID', 'documents', 'mode', 'rectificationPeriod') +
    assets_embedded_role
)
view_role = (blacklist('owner_token', '_attachments', 'revisions') + assets_embedded_role)

Administrator_role = whitelist('status', 'mode', 'relatedLot')
concierge_role = (whitelist('status', 'relatedLot'))

decision_roles = {
    'view': (schematics_default_role + blacklist()),
    'create': blacklist('id', 'decisionOf', 'relatedItem'),
    'edit': blacklist('id', 'decisionOf', 'relatedItem'),
    'not_edit': whitelist()
}

asset_roles = {
    'create': create_role,
    # draft role
    'draft': view_role,
    'edit_draft': edit_role,
    'plain': plain_role,
    'edit': edit_role,
    # pending role
    'edit_pending': edit_role,
    'pending': view_role,
    # verification role
    'verification': view_role,
    'edit_verification': whitelist(),
    # active role
    'active': view_role,
    'edit_active': whitelist(),
    'view': view_role,
    'listing': listing_role,
    'Administrator': Administrator_role,
    # complete role
    'complete': view_role,
    'edit_complete': blacklist('revisions'),
    # deleted role  # TODO: replace with 'delete' view for asset, temporary solution for tests
    'deleted': view_role,
    'edit_deleted': blacklist('revisions'),
    # concierge_role
    'concierge': concierge_role,
    'default': schematics_default_role,
}