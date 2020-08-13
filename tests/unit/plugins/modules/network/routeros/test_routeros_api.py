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

'''
Unit test require RouterOS API. 

Can be used agains hardware with routeros or Mikrotik CHR.
For more information.
    https://wiki.mikrotik.com/wiki/Manual:CHR
    https://wiki.mikrotik.com/wiki/Manual:CHR#How_to_Install_CHR

EVE-NG setup.
    https://www.eve-ng.net
    https://www.eve-ng.net/index.php/documentation/installation/
    https://www.eve-ng.net/index.php/documentation/howtos/howto-add-mikrotik-cloud-router/
    https://github.com/NikolayDachev/chr-eve-ng

Any other virtual setup probably will work without issue. 

Unit test use "fixtures/routeros_api_config.json" config file which contain needed module args and unit test settings.
-  test_routeros_api_path
       Will check routeros "interface" path.
       manual run: pytest test_routeros_api.py::TestRouterosApiModule:: test_routeros_api_path

- test_routeros_api_add_bridge
       Will add new bridge interface with name ["settings"]["bridge_name"].
       manual run: pytest test_routeros_api.py::TestRouterosApiModule::test_routeros_api_add_bridge

- test_routeros_api_query
       Will query '.id' for ["settings"]["bridge_name"] bridge.
       dependency: test_routeros_api_add_bridge
       manual run: pytest test_routeros_api.py::TestRouterosApiModule::test_routeros_api_query

- test_routeros_api_query_and_update.
       Will rename ["settings"]["bridge_name"] bridge to ["settings"]["bridge_new_name"].
       dependency: test_routeros_api_add_bridge
       manual run: pytest test_routeros_api.py::TestRouterosApiModule::test_routeros_api_query_and_update

- test_routeros_api_remove.
       Will delete ["settings"]["bridge_new_name"] bridge.
       dependency: test_routeros_api_add_bridge
       manual run: pytest test_routeros_api.py::TestRouterosApiModule::test_routeros_api_remove

- test_clear_test_artefacts.
       This is help test to cleare any unit test artefacts from routeros
       Delete ["settings"]["bridge_name"], ["settings"]["bridge_new_name"] bridges from routeros (if exist).
       manual run: pytest test_routeros_api.py::TestRouterosApiModule::test_clear_test_artefacts
'''

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

from ansible_collections.community.network.tests.unit.compat.mock import patch
from ansible_collections.community.network.plugins.modules.network.routeros import routeros_api
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from .routeros_module import TestRouterosModule
from librouteros import connect
from librouteros.query import Key


class TestRouterosApiModule(TestRouterosModule):
    module = routeros_api


    def load_config_file(self):
        config_file = "fixtures/routeros_api_config.json"
        with open(config_file) as json_file:
            self.config_data = json.load(json_file)
        self.config = self.config_data["module_args"]
        self.bridge_name =  self.config_data["settings"]["bridge_name"]
        self.bridge_new_name = self.config_data["settings"]["bridge_new_name"]


    def setUp(self):
        super(TestRouterosApiModule, self).setUp()

        self.load_config_file()

        self.mock_run_api = patch('ansible_collections.community.network.plugins.modules.network.routeros.routeros_api')
        self.run_api = self.mock_run_api.start()


    def tearDown(self):
        super(TestRouterosApiModule, self).tearDown()
        self.mock_run_api.stop()


    def test_routeros_api_path(self):
        config = self.config.copy()
        config['path'] = "interface"
        set_module_args(config)

        result = self.execute_module()
        for r in result['msg']:
            self.assertIn('mac-address', r)
            self.assertIn('name', r)


    def test_routeros_api_add_bridge(self):
        config = self.config.copy()
        config['add'] = "name=%s" % self.bridge_name
        set_module_args(config)

        result = self.execute_module()
        for r in result['msg']:
            self.assertNotIn('already have', r)
            self.assertIn('*', r)


    def test_routeros_api_query(self):
        config = self.config.copy()
        config['query'] = ".id name WHERE name == %s" % self.bridge_name
        set_module_args(config)

        result = self.execute_module()
        r = result['msg'][0]
        id = r['.id']
        self.assertIn('*', id)


    def test_routeros_api_query_and_update(self):
        # do query for '.id' self.bridge_name
        config = self.config.copy()
        config['query'] = ".id name WHERE name == %s" % self.bridge_name
        set_module_args(config)

        result = self.execute_module()
        r = result['msg'][0]
        id = r['.id']

        # do update for 'id' with name self.bridge_new_name
        config = self.config.copy()
        config['update'] = ".id=%s name=%s" % (id, self.bridge_new_name)
        set_module_args(config)

        result = self.execute_module()
        r = result['msg'][0]
        self.assertIn('updated', r)


    def test_routeros_api_remove(self):
        # do query for '.id' self.bridge_new_name
        config = self.config.copy()
        config['query'] = ".id name WHERE name == %s" % self.bridge_new_name
        set_module_args(config)

        result = self.execute_module()
        r = result['msg'][0]
        id = r['.id']

        # do remove 'id' for name  self.bridge_new_name
        config = self.config.copy()
        config['remove']="%s" % id
        set_module_args(config)

        result = self.execute_module()
        r = result['msg'][0]
        self.assertIn('removed', r)


    def test_clear_test_artefacts(self):
        api = connect(username=self.config['username'],
                      password=self.config['password'],
                      host=self.config['hostname'])
        path = api.path('interface', 'bridge')
        name = Key('name')
        id = Key('.id')
        for art in [self.bridge_name, self.bridge_new_name]:
            for s in path.select(name, id).where(name == art):
                if s['.id']:
                    path.remove(s['.id'])
