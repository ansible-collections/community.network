# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.network.tests.unit.compat.mock import patch
from ansible_collections.community.network.plugins.modules.network.icx import icx_aaa_accounting_console
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAaaAccountingModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_aaa_accounting_console module '''
    module = icx_aaa_accounting_console

    def setUp(self):
        super(TestICXAaaAccountingModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.community.network.plugins.modules.network.icx.icx_aaa_accounting_console.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.community.network.plugins.modules.network.icx.icx_aaa_accounting_console.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAaaAccountingModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None): 
	    self.load_config.return_value = None

    def test_icx_aaa_accounting_all_options(self):
        ''' Test for successful aaa accounting with all options'''
        set_module_args(dict(commands=dict(privilege_level=0,primary_method='radius',backup_method1='tacacs+',backup_method2='none'),
                             dot1x=dict(primary_method='radius',backup_method1='none'),
                             exec_=dict(primary_method='radius',backup_method1='tacacs+',backup_method2='none'),
                             mac_auth=dict(primary_method='radius',backup_method1='none'),
                             system=dict(primary_method='radius',backup_method1='tacacs+',backup_method2='none'),
                             enable_console=dict(state='present')))
        expected_commands = [
            'aaa accounting commands 0 default start-stop radius tacacs+ none',
            'aaa accounting dot1x default start-stop radius none',
            'aaa accounting exec default start-stop radius tacacs+ none',
            'aaa accounting mac-auth default start-stop radius none',
            'aaa accounting system default start-stop radius tacacs+ none',
            'enable aaa console'
            ]
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)
        
    def test_icx_aaa_accounting_all_options_no_backup(self):
        ''' Test for successful aaa accounting with no backup option'''
        set_module_args(dict(commands=dict(privilege_level=0,primary_method='radius',backup_method1='tacacs+'),
                             dot1x=dict(primary_method='radius'),
                             exec_=dict(primary_method='radius',backup_method1='tacacs+'),
                             mac_auth=dict(primary_method='radius'),
                             system=dict(primary_method='radius',backup_method1='tacacs+')))
        expected_commands = [
            'aaa accounting commands 0 default start-stop radius tacacs+',
            'aaa accounting dot1x default start-stop radius',
            'aaa accounting exec default start-stop radius tacacs+',
            'aaa accounting mac-auth default start-stop radius',
            'aaa accounting system default start-stop radius tacacs+'
            ]
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_accounting_all_options_remove(self):
        ''' Test for removing aaa accounting with all options'''
        set_module_args(dict(commands=dict(privilege_level=0,primary_method='radius',backup_method1='tacacs+',backup_method2='none',state='absent'),
                             dot1x=dict(primary_method='radius',backup_method1='none',state='absent'),
                             exec_=dict(primary_method='radius',backup_method1='tacacs+',backup_method2='none',state='absent'),
                             mac_auth=dict(primary_method='radius',backup_method1='none',state='absent'),
                             system=dict(primary_method='radius',backup_method1='tacacs+',backup_method2='none',state='absent'),
                             enable_console=dict(state='absent')))
        expected_commands = [
            'no aaa accounting commands 0 default start-stop radius tacacs+ none',
            'no aaa accounting dot1x default start-stop radius none',
            'no aaa accounting exec default start-stop radius tacacs+ none',
            'no aaa accounting mac-auth default start-stop radius none',
            'no aaa accounting system default start-stop radius tacacs+ none',
            'no enable aaa console'
            ]
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_accounting_all_options_backup_remove(self):
        ''' Test for removing aaa accounting with no backup options'''
        set_module_args(dict(commands=dict(privilege_level=0,primary_method='radius',backup_method1='tacacs+',state='absent'),
                             dot1x=dict(primary_method='radius',state='absent'),
                             exec_=dict(primary_method='radius',backup_method1='tacacs+',state='absent'),
                             mac_auth=dict(primary_method='radius',state='absent'),
                             system=dict(primary_method='radius',backup_method1='tacacs+',state='absent')))
        expected_commands = [
            'no aaa accounting commands 0 default start-stop radius tacacs+',
            'no aaa accounting dot1x default start-stop radius',
            'no aaa accounting exec default start-stop radius tacacs+',
            'no aaa accounting mac-auth default start-stop radius',
            'no aaa accounting system default start-stop radius tacacs+'
            ]
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_accounting_commands_dot1x(self):
        ''' Test for successful aaa accounting for commands and dot1x'''
        set_module_args(dict(commands=dict(privilege_level=4,primary_method='radius',state='present'),dot1x=dict(primary_method='none',state='present')))
        expected_commands = ['aaa accounting commands 4 default start-stop radius','aaa accounting dot1x default start-stop none']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_accounting_exec_mac_auth_system(self):
        ''' Test for successful aaa accounting for exec,mac_auth and system'''
        set_module_args(dict(exec_=dict(primary_method='tacacs+'),mac_auth=dict(primary_method='radius'),system=dict(primary_method='tacacs+')))
        expected_commands = ['aaa accounting exec default start-stop tacacs+','aaa accounting mac-auth default start-stop radius','aaa accounting system default start-stop tacacs+']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_accounting_console_enable(self):
        ''' Test for successful aaa accounting for enable_console'''
        set_module_args(dict(enable_console=dict(state='present')))
        expected_commands = ['enable aaa console']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def  test_icx_aaa_accounting_console_disbale(self):
        ''' Test for successful disable console'''
        set_module_args(dict(enable_console=dict(state='absent')))
        expected_commands = ['no enable aaa console']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_accounting_invalid_args_commands(self):
        ''' Test for invalid privilege_level'''
        set_module_args(dict(commands=dict(privilege_level=2,primary_method='tacacs+',backup_method1='radius',state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_accounting_invalid_args_exec(self):
        ''' Test for invalid primary_method'''
        set_module_args(dict(exec_=dict(primary_method='aaa',state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_accounting_invalid_args_dot1x(self):
        ''' Test for invalid backup_method1'''
        set_module_args(dict(dot1x=dict(primary_method='radius',backup_method1='radius',state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_accounting_invalid_args_mac_auth(self):
        ''' Test for invalid backup_method1'''
        set_module_args(dict(mac_auth=dict(primary_method='none',backup_method1='radius',state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_accounting_invalid_args_system(self):
        ''' Test for invalid backup_method2'''
        set_module_args(dict(mac_auth=dict(primary_method='radius',backup_method1='none',backup_method2='tacacs+',state='present')))
        result = self.execute_module(failed=True)