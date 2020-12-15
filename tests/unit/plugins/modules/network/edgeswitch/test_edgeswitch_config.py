#
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

from ansible_collections.community.network.tests.unit.compat.mock import patch
from ansible_collections.community.network.plugins.modules.network.edgeswitch import edgeswitch_config
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from .edgeswitch_module import TestEdgeswitchModule, load_fixture


class TestEdgeswitchConfigModule(TestEdgeswitchModule):

    module = edgeswitch_config

    def setUp(self):
        super(TestEdgeswitchConfigModule, self).setUp()

        self.mock_get_config = patch('ansible_collections.community.network.plugins.modules.network.edgeswitch.edgeswitch_config.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.community.network.plugins.modules.network.edgeswitch.edgeswitch_config.load_config')
        self.load_config = self.mock_load_config.start()

        self.mock_run_commands = patch('ansible_collections.community.network.plugins.modules.network.edgeswitch.edgeswitch_config.run_commands')
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestEdgeswitchConfigModule, self).tearDown()

        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None):
        config_file = 'edgeswitch_config_config.cfg'
        self.get_config.return_value = load_fixture(config_file)
        self.load_config.return_value = None

    def test_edgeswitch_config_unchanged(self):
        src = load_fixture('edgeswitch_config_config.cfg')
        set_module_args(dict(src=src))
        self.execute_module()

    def test_edgeswitch_config_src(self):
        src = load_fixture('edgeswitch_config_src.cfg')
        set_module_args(dict(src=src))
        commands = ['domain-name foo',
                    'interface 0/1',
                    'no ip address']
        self.execute_module(changed=True, commands=commands)

    def test_edgeswitch_config_backup(self):
        set_module_args(dict(backup=True))
        result = self.execute_module()
        self.assertIn('__backup__', result)

    def test_edgeswitch_config_save_always(self):
        self.run_commands.return_value = "domain-name foo"
        set_module_args(dict(save_when='always'))
        self.execute_module(changed=True)
        self.assertEqual(self.run_commands.call_count, 1)
        self.assertEqual(self.get_config.call_count, 0)
        self.assertEqual(self.load_config.call_count, 0)
        args = self.run_commands.call_args[0][1]
        self.assertIn('write memory', args['command'])

    def test_edgeswitch_config_save_changed_true(self):
        src = load_fixture('edgeswitch_config_src.cfg')
        set_module_args(dict(src=src, save_when='changed'))
        commands = ['domain-name foo',
                    'interface 0/1',
                    'no ip address']
        self.execute_module(changed=True, commands=commands)
        self.assertEqual(self.run_commands.call_count, 1)
        self.assertEqual(self.get_config.call_count, 1)
        self.assertEqual(self.load_config.call_count, 1)
        args = self.run_commands.call_args[0][1]
        self.assertIn('write memory', args['command'])

    def test_edgeswitch_config_save_changed_false(self):
        set_module_args(dict(save_when='changed'))
        self.execute_module(changed=False)
        self.assertEqual(self.run_commands.call_count, 0)
        self.assertEqual(self.get_config.call_count, 0)
        self.assertEqual(self.load_config.call_count, 0)

    def test_edgeswitch_config_lines_wo_parents(self):
        set_module_args(dict(lines=['domain-name foo']))
        commands = ['domain-name foo']
        self.execute_module(changed=True, commands=commands)

    def test_edgeswitch_config_lines_w_parents(self):
        set_module_args(dict(lines=['shutdown'], parents=['interface 0/1']))
        commands = ['interface 0/1', 'shutdown']
        self.execute_module(changed=True, commands=commands)

    def test_edgeswitch_config_before(self):
        set_module_args(dict(lines=['domain-name foo'], before=['test1', 'test2']))
        commands = ['test1', 'test2', 'domain-name foo']
        self.execute_module(changed=True, commands=commands, sort=False)

    def test_edgeswitch_config_after(self):
        set_module_args(dict(lines=['domain-name foo'], after=['test1', 'test2']))
        commands = ['domain-name foo', 'test1', 'test2']
        self.execute_module(changed=True, commands=commands, sort=False)

    def test_edgeswitch_config_before_after_no_change(self):
        set_module_args(dict(lines=['domain-name bar'],
                             before=['test1', 'test2'],
                             after=['test3', 'test4']))
        self.execute_module()

    def test_edgeswitch_config_config(self):
        config = 'domain-name example.ede'
        set_module_args(dict(lines=['domain-name bar'], config=config))
        commands = ['domain-name bar']
        self.execute_module(changed=True, commands=commands)

    def test_edgeswitch_config_replace_block(self):
        lines = ['description test-string', 'test-string']
        parents = ['interface 0/1']
        set_module_args(dict(lines=lines, replace='block', parents=parents))
        commands = parents + lines
        self.execute_module(changed=True, commands=commands)

    def test_edgeswitch_config_force(self):
        lines = ['domain-name bar']
        set_module_args(dict(lines=lines, match='none'))
        self.execute_module(changed=True, commands=lines)

    def test_edgeswitch_config_match_none(self):
        lines = ['ip address 1.2.3.4 255.255.255.0', 'description test-string']
        parents = ['interface 0/1']
        set_module_args(dict(lines=lines, parents=parents, match='none'))
        commands = parents + lines
        self.execute_module(changed=True, commands=commands, sort=False)

    def test_edgeswitch_config_match_strict(self):
        lines = ['ip address 1.2.3.4 255.255.255.0', 'description test-string',
                 'shutdown']
        parents = ['interface 0/1']
        set_module_args(dict(lines=lines, parents=parents, match='strict'))
        commands = parents + ['shutdown']
        self.execute_module(changed=True, commands=commands, sort=False)

    def test_edgeswitch_config_match_exact(self):
        lines = ['ip address 1.2.3.4 255.255.255.0', 'description test-string',
                 'shutdown']
        parents = ['interface 0/1']
        set_module_args(dict(lines=lines, parents=parents, match='exact'))
        commands = parents + lines
        self.execute_module(changed=True, commands=commands, sort=False)
