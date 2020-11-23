# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from units.compat.mock import patch
from ansible.modules.network.icx import icx_firmware_upgrade
from units.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXfirmwareUpgradeModule(TestICXModule):

    module = icx_firmware_upgrade

    def setUp(self):
        super(TestICXfirmwareUpgradeModule, self).setUp()
        self.mock_exec_scp = patch('ansible.modules.network.icx.icx_firmware_upgrade.exec_scp')
        self.mock_run_commands = patch('ansible.modules.network.icx.icx_firmware_upgrade.run_commands')
        self.exec_command = self.mock_exec_scp.start()
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestICXfirmwareUpgradeModule, self).tearDown()
        self.mock_exec_scp.stop()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None):
        if(commands is not None):
            self.mock_exec_scp.return_value = load_fixture("icx_firmware_upgrade_config").strip()
            self.mock_run_commands.return_value = load_fixture("icx_firmware_upgrade_config").strip()

    def test_icx_firmware_upgrade_tftp(self):
        set_module_args(
            dict(
                server_type='tftp',
                server_address='10.198.137.217',
                partition='secondary',
                filename='SPR08095_b412ufi.bin',
                boot_only=False,
                save_running_config=False
            )
        )

        commands = ['copy tftp flash 10.198.137.217 SPR08095_b412ufi.bin secondary', 'boot system flash secondary yes']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_firmware_upgrade_tftp_save_running_config_True(self):
        set_module_args(
            dict(
                server_type='tftp',
                server_address='10.198.137.217',
                partition='secondary',
                filename='SPR08095_b412ufi.bin',
                boot_only=False,
                save_running_config=True
            )
        )

        commands = ['copy tftp flash 10.198.137.217 SPR08095_b412ufi.bin secondary', 'write memory', 'boot system flash secondary yes']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_firmware_upgrade_tftp_missingPartition(self):
        set_module_args(
            dict(
                server_type='tftp',
                server_address='10.198.137.217',
                filename='SPR08095_b412ufi.bin',
                boot_only=False,
                save_running_config=False
            )
        )

        commands = ['copy tftp flash 10.198.137.217 SPR08095_b412ufi.bin secondary', 'boot system flash secondary yes']
        self.execute_module(changed=False, failed=True)

    def test_icx_firmware_upgrade_scp(self):
        set_module_args(
            dict(
                server_type='scp',
                server_address='10.198.137.217',
                partition='secondary',
                filename='/tftpboot/SPR08095_b412ufi.bin',
                scp_user='alethea',
                scp_pass='alethea123',
                boot_only=False,
                save_running_config=True
            )
        )

        commands = ['copy scp flash 10.198.137.217 /tftpboot/SPR08095_b412ufi.bin secondary', 'write memory', 'boot system flash secondary yes']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_firmware_upgrade_scp_diffPartition(self):
        set_module_args(
            dict(
                server_type='scp',
                server_address='10.198.137.217',
                partition='fips-ufi-primary-sig',
                filename='/tftpboot/SPR08095_b412ufi.bin',
                scp_user='alethea',
                scp_pass='alethea123',
                boot_only=False,
                save_running_config=False
            )
        )

        commands = ['copy scp flash 10.198.137.217 /tftpboot/SPR08095_b412ufi.bin fips-ufi-primary-sig', 'boot system flash primary yes']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_firmware_upgrade_https(self):
        set_module_args(
            dict(
                server_type='https',
                server_address='172.26.66.68',
                server_port='443',
                partition='secondary',
                filename='SPR08095_B10ufi.bin',
                boot_only=False,
                save_running_config=False
            )
        )

        commands = ['copy https flash 172.26.66.68 SPR08095_B10ufi.bin secondary port 443', 'boot system flash secondary yes']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_firmware_upgrade_https_missingServer_type(self):
        set_module_args(
            dict(
                server_address='172.26.66.68',
                server_port='443',
                partition='secondary',
                filename='SPR08095_B10ufi.bin',
                boot_only=False,
                save_running_config=False
            )
        )

        commands = ['copy https flash 172.26.66.68 SPR08095_B10ufi.bin secondary port 443', 'boot system flash secondary yes']
        self.execute_module(changed=False, failed=True)

    def test_icx_firmware_upgrade_https_missingServer_address(self):
        set_module_args(
            dict(
                server_type='https',
                server_port='443',
                partition='secondary',
                filename='SPR08095_B10ufi.bin',
                boot_only=False,
                save_running_config=False
            )
        )

        commands = ['copy https flash 172.26.66.68 SPR08095_B10ufi.bin secondary port 443', 'boot system flash secondary yes']
        self.execute_module(changed=False, failed=True)

    def test_icx_firmware_upgrade_https_missingFilename(self):
        set_module_args(
            dict(
                server_type='https',
                server_address='172.26.66.68',
                server_port='443',
                partition='secondary',
                boot_only=False,
                save_running_config=False
            )
        )

        commands = ['copy https flash 172.26.66.68 SPR08095_B10ufi.bin secondary port 443', 'boot system flash secondary yes']
        self.execute_module(changed=False, failed=True)

    def test_icx_firmware_upgrade_boot_onlyTrue_save_running_configFalse(self):
        set_module_args(
            dict(
                boot_only=True,
                save_running_config=False,
                partition='secondary',
                server_type='https',
            )
        )

        commands = ['boot system flash secondary yes']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_firmware_upgrade_boot_onlyTrue_save_running_configTrue(self):
        set_module_args(
            dict(
                boot_only=True,
                save_running_config=True,
                partition='secondary'
            )
        )

        commands = ['write memory', 'boot system flash secondary yes']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)
