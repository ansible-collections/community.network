# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

from ansible_collections.community.network.tests.unit.compat.mock import patch, MagicMock
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args, basic, AnsibleExitJson, AnsibleFailJson, ModuleTestCase
from ansible_collections.community.network.plugins.modules.network.routeros import routeros_api


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


class fake_ros_api:
    def __init__(self):
        pass

    def path(self, api, path):
        return [{".id": "*DC", "name": "b2", "mtu": "auto", "actual-mtu": 1500,
                 "l2mtu": 65535, "arp": "enabled", "arp-timeout": "auto",
                 "mac-address": "3A:C1:90:D6:E8:44", "protocol-mode": "rstp",
                 "fast-forward": "true", "igmp-snooping": "false",
                 "auto-mac": "true", "ageing-time": "5m", "priority":
                 "0x8000", "max-message-age": "20s", "forward-delay": "15s",
                 "transmit-hold-count": 6, "vlan-filtering": "false",
                 "dhcp-snooping": "false", "running": "true", "disabled": "false"}]


class TestRouterosApiModule(ModuleTestCase):

    def setUp(self):
        self.module = routeros_api
        self.module.connect = MagicMock(return_value=True)

        self.config_module_args = {"username": "admin",
                                   "password": "pаss",
                                   "hostname": "127.0.0.1",
                                   "path": "interface bridge"}

        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    @patch('ansible_collections.community.network.plugins.modules.network.routeros.routeros_api.ROS_api_module.api_add_path', new=fake_ros_api.path)
    def test_routeros_api_path(self):
        with self.assertRaises(AnsibleExitJson):
            set_module_args(self.config_module_args)
            self.module.main()

    '''
    def test_routeros_api_add(self):
        pass

    def test_routeros_api_query(self):
        pass

    def test_routeros_api_query_and_update(self):
        pass

    def test_routeros_api_remove(self):
        pass

    def test_clear_test_artefacts(self):
        pass
    '''
