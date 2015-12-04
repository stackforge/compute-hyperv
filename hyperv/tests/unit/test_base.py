# Copyright 2014 Cloudbase Solutions Srl
#
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

import mock
from os_win import utilsfactory
from six.moves import builtins

from hyperv.nova import utilsfactory as old_utilsfactory
from hyperv.tests import test


class HyperVBaseTestCase(test.NoDBTestCase):
    def setUp(self):
        super(HyperVBaseTestCase, self).setUp()

        self._mock_wmi = mock.MagicMock()
        wmi_patcher = mock.patch.object(builtins, 'wmi', create=True,
                                        new=self._mock_wmi)
        platform_patcher = mock.patch('sys.platform', 'win32')
        utilsfactory_patcher = mock.patch.object(utilsfactory, '_get_class')
        old_utilsfactory_patcher = mock.patch.object(old_utilsfactory,
                                                     '_get_class')

        platform_patcher.start()
        wmi_patcher.start()
        utilsfactory_patcher.start()
        old_utilsfactory_patcher.start()

        self.addCleanup(wmi_patcher.stop)
        self.addCleanup(platform_patcher.stop)
        self.addCleanup(utilsfactory_patcher.stop)
        self.addCleanup(old_utilsfactory_patcher.stop)
