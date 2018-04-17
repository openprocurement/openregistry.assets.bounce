# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist
from openprocurement.api.models.registry_models.roles import schematics_embedded_role

plain_role = (blacklist('_attachments', 'revisions', 'dateModified', 'rectificationPeriod') + schematics_embedded_role)

create_role = (blacklist('owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'assetID', 'documents', 'status', 'rectificationPeriod', 'items') + schematics_embedded_role)
edit_role = (blacklist('assetType', 'owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'assetID', 'documents', 'mode', 'rectificationPeriod', 'items') + schematics_embedded_role)
view_role = (blacklist('owner_token', '_attachments', 'revisions') + schematics_embedded_role)

Administrator_role = whitelist('status', 'mode', 'relatedLot')
concierge_role = (whitelist('status', 'relatedLot'))
