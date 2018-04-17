# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from openregistry.assets.core.events import AssetInitializeEvent
from openregistry.assets.core.utils import get_now
from openregistry.assets.bounce.constants import (
    INFORMATION_DETAILS
)


@subscriber(AssetInitializeEvent, assetType="bounce")
def tender_init_handler(event):
    """ initialization handler for bounce assets """
    asset = event.asset
    asset.date = get_now()
    asset.documents.append(type(asset).documents.model_class(INFORMATION_DETAILS))
