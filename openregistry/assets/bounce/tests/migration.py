# -*- coding: utf-8 -*-
import unittest

from openregistry.assets.core.tests.base import MigrationResourcesDTO_mock
from openregistry.assets.bounce.tests.base import (
    BaseAssetWebTest,
    get_snapshot,
)
from openregistry.assets.bounce.migration import (
    AddRelatedProcessesStep,
    BounceMigrationsRunner,
)
from openregistry.assets.bounce.tests.json_data import test_asset_bounce_data_schema_0


class AddRelatedProcessesMigrationStepTest(BaseAssetWebTest):

    def setUp(self):
        super(AddRelatedProcessesMigrationStepTest, self).setUp()
        self.initial_data = test_asset_bounce_data_schema_0

        asset_data = get_snapshot('bounce_migration_1.json')
        # create relatedLot
        lot_data = {'lotID': 'id' * 16}
        self.lot_id = self.db.save(lot_data)[0]
        # connect asset to the lot
        asset_data['relatedLot'] = self.lot_id
        self.asset_id = self.db.save(asset_data)[0]
        migration_resources = MigrationResourcesDTO_mock(self.db)
        self.runner = BounceMigrationsRunner(migration_resources)

    def test_ok(self):
        """General migration test"""
        steps = (AddRelatedProcessesStep,)
        self.runner.migrate(steps, schema_version_max=1)

        asset_doc = self.db[self.asset_id]
        self.assertIn('relatedProcesses', asset_doc.keys())
        self.assertNotIn('relatedLot', asset_doc.keys())
        self.assertEqual(self.lot_id, asset_doc['relatedProcesses'][0]['relatedProcessID'])

    def test_status_without_related_lot(self):
        """
        Only certain statuses could have the `relatedLot` attribute

        So there is a need to test that skip predicate works correctly with them.
        """
        # set lot status to that one, that have not relatedLot
        TARGET_STATUS = 'draft'

        asset_doc = self.db[self.asset_id]
        asset_doc['status'] = TARGET_STATUS
        self.db.save(asset_doc)

        steps = (AddRelatedProcessesStep, )
        self.runner.migrate(steps, schema_version_max=1)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(Migration0to1Test))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
