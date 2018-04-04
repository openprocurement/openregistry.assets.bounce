# -*- coding: utf-8 -*-
from schematics.types import StringType
from schematics.types.loki import ListType, ModelType
from zope.interface import implementer

from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset, Item
)


class ICompoundAsset(IAsset):
    """ Marker interface for loki assets """


@implementer(ICompoundAsset)
class Asset(BaseAsset):
    assetType = StringType(default="loki")
    items = ListType(ModelType(Item))
