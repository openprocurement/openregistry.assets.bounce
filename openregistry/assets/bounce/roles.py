# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist
from openregistry.assets.core.models import (
    sensitive_embedded_role,
    listing_role,
    schematics_default_role,
)


decision_roles = {
    'view': (schematics_default_role + blacklist()),
    'create': blacklist('decisionOf', 'relatedItem'),
    'edit': blacklist('id', 'decisionOf', 'relatedItem'),
    'not_edit': whitelist()
}


bounce_asset_roles = {
    'create': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'assetID',
            'date',
            'dateModified',
            'doc_id',
            'documents',
            'owner',
            'owner_token',
            'rectificationPeriod',
            'relatedLot',
            'revisions',
            'status',
        )
    ),
    # draft role
    'draft': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'owner_token',
            'relatedLot',
            'revisions',
        )
    ),
    'edit_draft': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'assetID',
            'assetType',
            'date',
            'dateModified',
            'decisions',
            'doc_id',
            'documents',
            'mode',
            'owner',
            'owner_token',
            'rectificationPeriod',
            'relatedLot',
            'revisions',
        )
    ),
    'plain': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'dateModified',
            'relatedLot',
            'revisions',
        )
    ),
    'edit': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'assetID',
            'assetType',
            'date',
            'dateModified',
            'decisions',
            'doc_id',
            'documents',
            'mode',
            'owner',
            'owner_token',
            'rectificationPeriod',
            'relatedLot',
            'revisions',
        )
    ),
    # pending role
    'edit_pending': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'assetID',
            'assetType',
            'date',
            'dateModified',
            'decisions',
            'doc_id',
            'documents',
            'mode',
            'owner',
            'owner_token',
            'rectificationPeriod',
            'relatedLot',
            'revisions',
        )
    ),
    'pending': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'owner_token',
            'relatedLot',
            'revisions',
        )
    ),
    # verification role
    'verification': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'owner_token',
            'relatedLot',
            'revisions',
        )
    ),
    'edit_verification': whitelist(),
    # active role
    'active': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'owner_token',
            'relatedLot',
            'revisions',
        )
    ),
    'edit_active': whitelist(),
    'view': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'owner_token',
            'relatedLot',
            'revisions',
        )
    ),
    'listing': listing_role,
    'Administrator': (
        whitelist('status',
            'mode',
            'rectificationPeriod',
        )
    ),
    # complete role
    'complete': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'owner_token',
            'relatedLot',
            'revisions',
        )
    ),
    'edit_complete': blacklist('revisions'),
    # deleted role  # TODO: replace with 'delete' view for asset, temporary solution for tests
    'deleted': (
        sensitive_embedded_role +
        blacklist(
            '_attachments',
            'owner_token',
            'relatedLot',
            'revisions',
        )
    ),
    'edit_deleted': blacklist('revisions', 'relatedLot'),
    # concierge_role
    'concierge': (
        whitelist(
            'status',
        )
    ),
    'default': schematics_default_role,
}
