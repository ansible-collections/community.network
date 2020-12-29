# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.network.tests.unit.compat.mock import patch
from ansible_collections.community.network.plugins.modules.network.icx import icx_aaa_accounting_console
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXaaaAccountingModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_aaa_accounting_console module '''
    module = icx_aaa_accounting_console

    def setUp(self):
        super(TestICXaaaAccountingModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.community.network.plugins.modules.network.icx.icx_aaa_accounting_console.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.community.network.plugins.modules.network.icx.icx_aaa_accounting_console.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXaaaAccountingModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None
        if commands is not None:
            self.exec_command.return_value = ""

    def test_icx_aaa_accounting_expected_success1(self):
        ''' Test for successful aaa accounting for commands and dot1x'''
        set_module_args(dict(commands=dict(privilege_level=0 , primary_method='radius',backup_method1='tacacs+',state='present'),dot1x=dict(primary_method='none',state='absent')))
        expected_commands = [['aaa accounting commands 0 default start-stop radius tacacs+','no aaa accounting dot1x default start-stop none']]
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_accounting_expected_success2(self):
        ''' Test for successful aaa accounting for exec and mac_auth'''
        set_module_args(dict(exec_=dict(primary_method='tacacs+',backup_method1='radius',backup_method2='none'),mac_auth=dict(primary_method='radius',state='absent')))
        expected_commands = [['aaa accounting exec default start-stop tacacs+ radius none','no aaa accounting mac-auth default start-stop radius']]
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_accounting_expected_success3(self):
        ''' Test for successful aaa accounting for system and enable_console'''
        set_module_args(dict(system=dict(primary_method='tacacs+',state='absent'),enable_console=dict(state='absent')))
        expected_commands = [['no aaa accounting system default start-stop tacacs+','no enable aaa console']]
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_accounting_invalid_commands(self):
        ''' Test for invalid privilege_level'''
        set_module_args(dict(commands=dict(privilege_level=2 ,primary_method='tacacs+',backup_method1='radius',state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_accounting_invalid_dot1x(self):
        ''' Test for invalid primary_method'''
        set_module_args(dict(dot1x=dict(primary_method='aaa',state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_accounting_invalid_exec(self):
        ''' Test for invalid backup_method1'''
        set_module_args(dict(dot1x=dict(primary_method='radius',backup_method1='radius',state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_accounting_invalid_mac_auth(self):
        ''' Test for invalid backup_method1'''
        set_module_args(dict(mac_auth=dict(primary_method='none',backup_method1='radius',state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_accounting_invalid_system(self):
        ''' Test for invalid backup_method2'''
        set_module_args(dict(mac_auth=dict(primary_method='radius',backup_method1='none',backup_method2='tacacs+',state='present')))
        result = self.execute_module(failed=True)