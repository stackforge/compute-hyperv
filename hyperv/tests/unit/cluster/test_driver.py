# Copyright 2016 Cloudbase Solutions SRL
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Unit tests for the Hyper-V Cluster Driver."""

import mock

from hyperv.nova.cluster import clusterops
from hyperv.nova.cluster import driver
from hyperv.nova import driver as base_driver
from hyperv.tests.unit import test_base


class HyperVClusterTestCase(test_base.HyperVBaseTestCase):

    @mock.patch.object(clusterops, 'ClusterOps')
    @mock.patch.object(base_driver.hostops, 'api', mock.MagicMock())
    @mock.patch.object(base_driver.HyperVDriver,
                       '_check_minimum_windows_version')
    def setUp(self, mock_check_minimum_windows_version, mock_clusterops_init):
        super(HyperVClusterTestCase, self).setUp()

        self.context = 'context'
        self.driver = driver.HyperVClusterDriver(mock.sentinel.virtapi)

    @mock.patch.object(base_driver.HyperVDriver, 'spawn')
    def test_spawn(self, mock_superclass_spawn):
        self.driver.spawn(self.context, mock.sentinel.fake_instance,
                          mock.sentinel.image_meta,
                          mock.sentinel.injected_files,
                          mock.sentinel.admin_pass,
                          mock.sentinel.network_info,
                          mock.sentinel.block_dev_info)

        mock_superclass_spawn.assert_called_once_with(
            self.context, mock.sentinel.fake_instance,
            mock.sentinel.image_meta, mock.sentinel.injected_files,
            mock.sentinel.admin_pass, mock.sentinel.network_info,
            mock.sentinel.block_dev_info)
        self.driver._clops.add_to_cluster.assert_called_once_with(
            mock.sentinel.fake_instance)

    @mock.patch.object(base_driver.HyperVDriver, 'destroy')
    def test_destroy(self, mock_superclass_destroy):
        self.driver.destroy(self.context, mock.sentinel.fake_instance,
                            mock.sentinel.network_info,
                            mock.sentinel.block_dev_info,
                            mock.sentinel.destroy_disks)

        mock_superclass_destroy.assert_called_once_with(
            self.context, mock.sentinel.fake_instance,
            mock.sentinel.network_info, mock.sentinel.block_dev_info,
            mock.sentinel.destroy_disks)

    @mock.patch.object(base_driver.HyperVDriver, 'migrate_disk_and_power_off')
    def test_migrate_disk_and_power_off(self, mock_superclass_migrate):
        disk_info = self.driver.migrate_disk_and_power_off(
            self.context,
            mock.sentinel.fake_instance,
            mock.sentinel.destination,
            mock.sentinel.flavor,
            mock.sentinel.network_info,
            mock.sentinel.block_dev_info,
            mock.sentinel.timeout,
            mock.sentinel.retry_interval)

        self.assertEqual(mock_superclass_migrate.return_value, disk_info)
        self.driver._clops.remove_from_cluster.assert_called_once_with(
            mock.sentinel.fake_instance)
        mock_superclass_migrate.assert_called_once_with(
            self.context, mock.sentinel.fake_instance,
            mock.sentinel.destination, mock.sentinel.flavor,
            mock.sentinel.network_info, mock.sentinel.block_dev_info,
            mock.sentinel.timeout, mock.sentinel.retry_interval)

    @mock.patch.object(base_driver.HyperVDriver, 'finish_migration')
    def test_finish_migration(self, mock_superclass_finish_migration):
        self.driver.finish_migration(self.context,
                                     mock.sentinel.migration,
                                     mock.sentinel.fake_instance,
                                     mock.sentinel.disk_info,
                                     mock.sentinel.network_info,
                                     mock.sentinel.image_meta,
                                     mock.sentinel.resize_instance,
                                     mock.sentinel.block_dev_info,
                                     mock.sentinel.power_on)
        mock_superclass_finish_migration.assert_called_once_with(
            self.context, mock.sentinel.migration, mock.sentinel.fake_instance,
            mock.sentinel.disk_info, mock.sentinel.network_info,
            mock.sentinel.image_meta, mock.sentinel.resize_instance,
            mock.sentinel.block_dev_info, mock.sentinel.power_on)
        self.driver._clops.add_to_cluster.assert_called_once_with(
            mock.sentinel.fake_instance)

    @mock.patch.object(base_driver.HyperVDriver, 'finish_revert_migration')
    def test_finish_revert_migration(self, mock_superclass_finish_rev_migr):
        self.driver.finish_revert_migration(self.context,
                                            mock.sentinel.fake_instance,
                                            mock.sentinel.network_info,
                                            mock.sentinel.block_dev_info,
                                            mock.sentinel.power_on)
        mock_superclass_finish_rev_migr.assert_called_once_with(
            self.context, mock.sentinel.fake_instance,
            mock.sentinel.network_info, mock.sentinel.block_dev_info,
            mock.sentinel.power_on)
        self.driver._clops.add_to_cluster.assert_called_once_with(
            mock.sentinel.fake_instance)

    @mock.patch.object(base_driver.HyperVDriver,
                       'post_live_migration_at_destination')
    def test_post_live_migration_at_destination(self, mock_superclass_post):
        self.driver.post_live_migration_at_destination(
            self.context, mock.sentinel.fake_instance,
            mock.sentinel.network_info, mock.sentinel.block_migration,
            mock.sentinel.block_dev_info)

        self.driver._clops.post_migration.assert_called_once_with(
            mock.sentinel.fake_instance)
        mock_superclass_post.assert_called_once_with(
            self.context, mock.sentinel.fake_instance,
            mock.sentinel.network_info, mock.sentinel.block_migration,
            mock.sentinel.block_dev_info)
