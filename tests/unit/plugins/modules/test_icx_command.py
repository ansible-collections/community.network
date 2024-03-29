# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from ansible_collections.community.network.tests.unit.compat.mock import patch
from ansible_collections.community.network.plugins.modules import icx_command
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXCommandModule(TestICXModule):

    module = icx_command

    def setUp(self):
        super(TestICXCommandModule, self).setUp()

        self.mock_run_commands = patch('ansible_collections.community.network.plugins.modules.icx_command.run_commands')
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestICXCommandModule, self).tearDown()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None):

        def load_from_file(*args, **kwargs):
            module, commands = args
            output = list()

            for item in commands:
                try:
                    if item == 'skip':
                        continue
                    obj = json.loads(item['command'])
                    command = obj['command']
                except ValueError:
                    command = item['command']
                filename = str(command).replace(' ', '_')
                output.append(load_fixture(filename))

            return output

        self.run_commands.side_effect = load_from_file

    def test_icx_command_simple(self):
        set_module_args(dict(commands=['show version']))
        result = self.execute_module()
        self.assertEqual(len(result['stdout']), 1)
        self.assertTrue(result['stdout'][0].startswith('Copyright (c) 1996-2017 Brocade Communications Systems'))

    def test_icx_command_multiple(self):
        set_module_args(dict(commands=['show version', 'show version']))
        result = self.execute_module()
        self.assertEqual(len(result['stdout']), 2)
        self.assertTrue(result['stdout'][0].startswith('Copyright (c) 1996-2017 Brocade Communications Systems'))

    def test_icx_command_wait_for(self):
        wait_for = 'result[0] contains "ICX"'
        set_module_args(dict(commands=['show version'], wait_for=wait_for))
        self.execute_module()

    def test_icx_command_wait_for_fails(self):
        wait_for = 'result[0] contains "test string"'
        set_module_args(dict(commands=['show version'], wait_for=wait_for))
        self.execute_module(failed=True)
        # run_commands call count is 1(skip) + 10(current)
        self.assertEqual(self.run_commands.call_count, 11)

    def test_icx_command_retries(self):
        wait_for = 'result[0] contains "test string"'
        set_module_args(dict(commands=['show version'], wait_for=wait_for, retries=2))
        self.execute_module(failed=True)
        self.assertEqual(self.run_commands.call_count, 3)

    def test_icx_command_match_any(self):
        wait_for = ['result[0] contains "ICX"',
                    'result[0] contains "test string"']
        set_module_args(dict(commands=['show version'], wait_for=wait_for, match='any'))
        self.execute_module()

    def test_icx_command_match_all(self):
        wait_for = ['result[0] contains "ICX"',
                    'result[0] contains "Version:10.1.09T225"']
        set_module_args(dict(commands=['show version'], wait_for=wait_for, match='all'))
        self.execute_module()

    def test_icx_command_match_all_failure(self):
        wait_for = ['result[0] contains "ICX"',
                    'result[0] contains "test string"']
        commands = ['show version', 'show version']
        set_module_args(dict(commands=commands, wait_for=wait_for, match='all'))
        self.execute_module(failed=True)

    def test_icx_command_configure_check_warning(self):
        commands = ['configure terminal']
        set_module_args({
            'commands': commands,
            '_ansible_check_mode': True,
        })
        result = self.execute_module()
        self.assertEqual(
            result['warnings'],
            ['Only show commands are supported when using check mode, not executing configure terminal'],
        )

    def test_icx_command_configure_not_warning(self):
        commands = ['configure terminal']
        set_module_args(dict(commands=commands))
        result = self.execute_module()
        self.assertEqual(result['warnings'], [])
