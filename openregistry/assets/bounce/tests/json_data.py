# -*- coding: utf-8 -*-
import os
from copy import deepcopy

from openregistry.assets.core.constants import SANDBOX_MODE
from openregistry.assets.core.tests.base import DEFAULT_ACCELERATION
from openregistry.assets.core.tests.blanks.json_data import (
    test_organization_loki,
    schema_properties,
    test_loki_item_data
)
from openregistry.assets.core.utils import get_now

test_item_data = deepcopy(test_loki_item_data)
del test_item_data['id']

# test_loki_item_data['schema_properties'] = schema_properties
asset_type = os.environ.get('ASSET_TYPE', 'bounce')
test_asset_bounce_data = {
    "title": u"Земля для космодрому",
    "description": u"Опис землі для космодрому",
    "assetType": asset_type,
    "items": [test_item_data, test_item_data],
    "assetCustodian": deepcopy(test_organization_loki),
    "decisions": [{
        'decisionDate': get_now().isoformat(),
        'decisionID': '1111-4'
    }]
}

if SANDBOX_MODE:
    test_asset_bounce_data['sandboxParameters'] = 'quick, accelerator={}'.format(DEFAULT_ACCELERATION)


