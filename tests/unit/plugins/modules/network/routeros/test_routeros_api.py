# (c) 2016 Red Hat Inc.
#
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
from ansible_collections.community.network.plugins.modules.network.routeros.routeros_api import ROS_api_module
from librouteros.api import Api, Path
from librouteros.query import Query


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


class TestRouterosApiModule(ModuleTestCase):

    def setUp(self):
        self.config_module_args = { "username": "admin",
                                    "password": "pаss",
                                    "hostname": "127.0.0.1",
                                    "path":     "interface bridge"}

        self.api = Api(protocol=MagicMock())

        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)


    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            ROS_api_module()


    def test_routeros_api_path(self):
        libros_path = self.api.path("interface", "bridge")
        r = ROS_api_module.api_add_path(self, self.api, ["interface", "bridge"])
        self.assertEqual(r.path, libros_path.path)

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
