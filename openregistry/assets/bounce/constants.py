# -*- coding: utf-8 -*-
from datetime import timedelta


BOUNCE_ASSET_DOC_TYPE = "informationDetails"

INFORMATION_DETAILS = {
    'title': 'Інформація про оприлюднення інформаційного повідомлення',
    'url': 'https://prozorro.sale/info/ssp_details',
    'documentOf': "asset",
    'documentType': BOUNCE_ASSET_DOC_TYPE
}
RECTIFICATION_PERIOD_DURATION = timedelta(days=1)
DEFAULT_ASSET_BOUNCE_TYPE = 'bounce'

DECISION_EDITING_STATUSES = ['draft', 'pending']
