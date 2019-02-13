# -*- coding: utf-8 -*-
import logging

from openregistry.assets.core.traversal import Root
from openregistry.assets.core.migration import (
    BaseMigrationsRunner,
    BaseMigrationStep,
)

LOGGER = logging.getLogger(__name__)


class BounceMigrationsRunner(BaseMigrationsRunner):

    SCHEMA_VERSION = 1
    SCHEMA_DOC = 'openregistry_assets_bounce_schema'
    ROOT_CLASS = Root


class AddRelatedProcessesStep(BaseMigrationStep):

    TARGET_STATUSES = ('active', 'complete')

    def setUp(self):
        self.view = 'assets/all'

    def migrate_document(self, asset):
        if self._skip_predicate(asset):
            return

        related_lot_id = asset.get('relatedLot')
        if related_lot_id is None:
            LOGGER.warning(
                'Asset has no relatedProcesses and relatedLot. AssetID: {0}'.format(asset.id),
                extra={'MESSAGE_ID': 'migrate_data_failed', 'ASSET_ID': asset.id}
            )
            return
        related_lot = self.db.get(related_lot_id)
        if related_lot is None:
            LOGGER.warning(
                'RelatedLot not found. AssetID: {0}'.format(asset.id),
                extra={'MESSAGE_ID': 'migrate_data_failed', 'ASSET_ID': asset.id}
            )
            return

        relatedProcesses = ({
            'type': 'lot',
            'relatedProcessID': related_lot_id,
            'identifier': related_lot['lotID'],
        },)
        asset['relatedProcesses'] = relatedProcesses

        del asset['relatedLot']
        return asset

    def _skip_predicate(self, asset):
        """Returns True if asset should be skipped by migration"""
        if (
            asset['assetType'] == 'bounce'
            and asset['status'] in self.TARGET_STATUSES
            and not (
                hasattr(asset, 'relatedProcesses')
                and asset['relatedProcesses'] is not None
            )
        ):
            return False
        return True


MIGRATION_STEPS = (
    AddRelatedProcessesStep,
)


def migrate(db):
    runner = BounceMigrationsRunner(db)
    runner.migrate(MIGRATION_STEPS)
