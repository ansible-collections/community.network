# Copyright: (c) 2018, Pluribus Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.network.tests.unit.compat.mock import patch
from ansible_collections.community.network.plugins.modules import pn_snmp_community
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from .nvos_module import TestNvosModule


class TestSnmpCommunityModule(TestNvosModule):

    module = pn_snmp_community

    def setUp(self):
        self.mock_run_nvos_commands = patch('ansible_collections.community.network.plugins.modules.pn_snmp_community.run_cli')
        self.run_nvos_commands = self.mock_run_nvos_commands.start()

        self.mock_run_check_cli = patch('ansible_collections.community.network.plugins.modules.pn_snmp_community.check_cli')
        self.run_check_cli = self.mock_run_check_cli.start()

    def tearDown(self):
        self.mock_run_nvos_commands.stop()
        self.run_check_cli.stop()

    def run_cli_patch(self, module, cli, state_map):
        if state_map['present'] == 'snmp-community-create':
            results = dict(
                changed=True,
                cli_cmd=cli
            )
        elif state_map['absent'] == 'snmp-community-delete':
            results = dict(
                changed=True,
                cli_cmd=cli
            )
        elif state_map['update'] == 'snmp-community-modify':
            results = dict(
                changed=True,
                cli_cmd=cli
            )
        module.exit_json(**results)

    def load_fixtures(self, commands=None, state=None, transport='cli'):
        self.run_nvos_commands.side_effect = self.run_cli_patch
        if state == 'present':
            self.run_check_cli.return_value = False
        if state == 'absent':
            self.run_check_cli.return_value = True
        if state == 'update':
            self.run_check_cli.return_value = True

    def test_snmp_community_create(self):
        set_module_args({'pn_cliswitch': 'sw01', 'pn_community_string': 'foo',
                         'pn_community_type': 'read-write', 'state': 'present'})
        result = self.execute_module(changed=True, state='present')
        expected_cmd = ' switch sw01 snmp-community-create community-string foo  community-type read-write'
        self.assertEqual(result['cli_cmd'], expected_cmd)

    def test_snmp_community_delete(self):
        set_module_args({'pn_cliswitch': 'sw01', 'pn_community_string': 'foo',
                         'state': 'absent'})
        result = self.execute_module(changed=True, state='absent')
        expected_cmd = ' switch sw01 snmp-community-delete community-string foo '
        self.assertEqual(result['cli_cmd'], expected_cmd)

    def test_snmp_community_update(self):
        set_module_args({'pn_cliswitch': 'sw01', 'pn_community_string': 'foo',
                         'pn_community_type': 'read-only', 'state': 'update'})
        result = self.execute_module(changed=True, state='update')
        expected_cmd = ' switch sw01 snmp-community-modify community-string foo  community-type read-only'
        self.assertEqual(result['cli_cmd'], expected_cmd)
