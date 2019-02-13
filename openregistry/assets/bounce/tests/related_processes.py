# -*- coding: utf-8 -*-
import unittest

from openregistry.assets.core.tests.base import (
    RelatedProcessesTestMixinBase,
)
from openregistry.assets.bounce.tests.base import (
    BaseAssetWebTest,
)

from openregistry.assets.core.tests.blanks.json_data import (
    test_related_process_data,
)
from openregistry.assets.bounce.tests.json_data import (
    test_asset_bounce_data,
)
from openregistry.assets.bounce.models import Asset as AssetBounce


class RelatedProcessesTestMixin(RelatedProcessesTestMixinBase):
    """These methods adapt test blank to the test case

    This adaptation is required because the mixin would test different types
    of resources, e.g. auctions, lots, assets.
    """

    def mixinSetUp(self):
        asset = self.create_resource()
        self.base_resource_collection_url = '/'
        self.base_resource_url = '/{0}'.format(asset['id'])

        token = self.db[asset['id']]['owner_token']
        self.access_header = {'X-Access-Token': str(token)}

        self.base_resource_initial_data = test_asset_bounce_data
        self.initial_related_process_data = test_related_process_data

        self.app.authorization = ('Basic', ('concierge', ''))
        self.parent_resource_create_authorization = ('Basic', ('broker', ''))


class BounceAssetRelatedProcessResourceTest(BaseAssetWebTest, RelatedProcessesTestMixin):
    initial_status = 'draft'
    asset_model = AssetBounce
    docservice = True
    initial_data = test_asset_bounce_data
    initial_status = 'pending'
    precision = 4


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BounceAssetRelatedProcessResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
