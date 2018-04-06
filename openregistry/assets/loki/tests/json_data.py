# -*- coding: utf-8 -*-
from copy import deepcopy
from openprocurement.api.tests.blanks.json_data import (
    test_organization,
    schema_properties,
    test_loki_item_data
)
from openprocurement.api.constants import IS_SCHEMAS_PROPERTIES_ENABLED_LOKI

test_item_data = deepcopy(test_loki_item_data)

if IS_SCHEMAS_PROPERTIES_ENABLED_LOKI:
    test_loki_item_data['schema_properties'] = schema_properties

test_asset_loki_data = {
    "title": u"Земля для космодрому",
    "description": u"Опис землі для космодрому",
    "assetType": "loki",
    "items": [test_item_data, test_item_data],
    "assetCustodian": deepcopy(test_organization),
    "classification": {
        "scheme": u"CAV",
        "id": u"39513200-3",
        "description": u"Земельні ділянки"
    },
    "unit": {
        "name": u"item",
        "code": u"39513200-3"
    },
    "quantity": 5,
    "address": {
        "countryName": u"Україна",
        "postalCode": "79000",
        "region": u"м. Київ",
        "locality": u"м. Київ",
        "streetAddress": u"вул. Банкова 1"
    },
    "value": {
        "amount": 100,
        "currency": u"UAH"
    }
}


