# -*- coding: utf-8 -*-
from copy import deepcopy
from openregistry.assets.core.tests.blanks.json_data import (
    test_organization,
    test_item_data_with_schema
)


test_asset_loki_data = {
    "title": u"Земля для космодрому",
    "assetType": "loki",
    "items": [test_item_data_with_schema, test_item_data_with_schema],
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


