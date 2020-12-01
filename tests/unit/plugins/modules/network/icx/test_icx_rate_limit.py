# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from units.compat.mock import patch
from ansible.modules.network.icx import icx_rate_limit
from units.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXRateLimitModule(TestICXModule):

    module = icx_rate_limit

    def setUp(self):
        super(TestICXRateLimitModule, self).setUp()
        self.mock_exec_command = patch('ansible.modules.network.icx.icx_rate_limit.exec_command')
        self.mock_run_commands = patch('ansible.modules.network.icx.icx_rate_limit.run_commands')
        self.mock_get_config = patch('ansible.modules.network.icx.icx_rate_limit.get_config')
        self.get_config = self.mock_get_config.start()
        self.run_commands = self.mock_run_commands.start()
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXRateLimitModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_exec_command.stop()
        self.mock_get_config.stop()

    def load_fixtures(self, commands=None):

        def load_file(*args, **kwargs):
            module = args
            for arg in args:
                if arg.params['check_running_config'] is True:
                    return load_fixture('icx_rate_limit_config').strip()
                else:
                    return ''
        self.get_config.side_effect = load_file

    def test_icx_rate_limit_bum_absent(self):
        set_module_args(
            dict(
                rate_limit_bum=dict(minutes=7, state='absent')
            ))
        result = self.execute_module(changed=True)
        expected_commands = ['conf t', 'no rate-limit-log 7']
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_rate_limit_bum_present(self):
        set_module_args(
            dict(
                rate_limit_bum=dict(minutes=7, state='present')
            ))
        commands = ['conf t', 'rate-limit-log 7']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_arp_absent(self):
        set_module_args(
            dict(
                rate_limit_arp=dict(number=77, state='absent')
            ))
        commands = ['conf t', 'no rate-limit-arp 77']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_arp_present(self):
        set_module_args(
            dict(
                rate_limit_arp=dict(number=77, state='present')
            ))
        commands = ['conf t', 'rate-limit-arp 77']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_input_lag_absent(self):
        set_module_args(
            dict(
                rate_limit_input=dict(
                    port='1/1/2',
                    lag='LAG1',
                    average_rate=500,
                    state='absent')
            ))
        commands = ['conf t', 'lag LAG1', 'no rate-limit input fixed ethernet 1/1/2 500', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_input_lag_preset(self):
        set_module_args(
            dict(
                rate_limit_input=dict(
                    port='1/1/2',
                    lag='LAG1',
                    average_rate=800),
            ))
        commands = ['conf t', 'lag LAG1', 'rate-limit input fixed ethernet 1/1/2 800', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_input_absent(self):
        set_module_args(
            dict(
                rate_limit_input=dict(
                    port='1/1/2',
                    average_rate=500,
                    state='absent')
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'no rate-limit input fixed 500', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_input_preset(self):
        set_module_args(
            dict(
                rate_limit_input=dict(
                    port='1/1/2',
                    average_rate=500)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'rate-limit input fixed 500', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_input_aggregate(self):
        aggregate = [
            dict(
                rate_limit_output=dict(
                    lag='LAG1',
                    port='1/1/2',
                    value=800)
            ),
            dict(
                rate_limit_output=dict(
                    port="1/1/3",
                    value=800)
            )
        ]
        set_module_args(dict(aggregate=aggregate))
        expected_commands = ['conf t', 'lag LAG1', 'rate-limit output shaping ethernet 1/1/2 800',
                             'exit', 'interface ethernet 1/1/3', 'rate-limit output shaping 800', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_rate_limit_input_absent_burst_size(self):
        set_module_args(
            dict(
                rate_limit_input=dict(
                    port='1/1/2',
                    average_rate=500,
                    burst_size=500,
                    state='absent')
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'no rate-limit input fixed 500 burst 500', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_input_preset_burst_size(self):
        set_module_args(
            dict(
                rate_limit_input=dict(
                    port='1/1/2',
                    average_rate=500,
                    burst_size=500)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'rate-limit input fixed 500 burst 500', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_lag_absent(self):
        set_module_args(
            dict(
                rate_limit_output=dict(
                    port='1/1/2',
                    lag='LAG1',
                    value=800,
                    state='present'),
                check_running_config='True'
            ))

        if self.get_running_config(compare=False):
            if not self.ENV_ICX_USE_DIFF:
                result = self.execute_module(changed=False)
                expected_commands = []
                self.assertEqual(result['commands'], expected_commands)
            else:
                result = self.execute_module(changed=True)
                expected_commands = ['conf t', 'lag LAG1', 'rate-limit output shaping ethernet 1/1/2 800', 'exit']
                self.assertEqual(result['commands'], expected_commands)

    def test_icx_rate_limit_output_lag_preset(self):
        set_module_args(
            dict(
                rate_limit_output=dict(
                    port='1/1/2',
                    lag='LAG1',
                    value=500,
                    state='present')
            ))
        commands = ['conf t', 'lag LAG1', 'rate-limit output shaping ethernet 1/1/2 500', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_absent(self):
        set_module_args(
            dict(
                rate_limit_output=dict(
                    port='1/1/2',
                    value=500,
                    state='absent')
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'no rate-limit output shaping 500', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_preset(self):
        set_module_args(
            dict(
                rate_limit_output=dict(
                    port='1/1/2',
                    value=500)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'rate-limit output shaping 500', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_absent_priority_queue(self):
        set_module_args(
            dict(
                rate_limit_output=dict(
                    port='1/1/2',
                    value=500,
                    priority_queue=5,
                    state='absent')
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'no rate-limit output shaping 500 priority 5', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_preset_priority_queue(self):
        set_module_args(
            dict(
                rate_limit_output=dict(
                    port='1/1/2',
                    value=500,
                    priority_queue=5)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'rate-limit output shaping 500 priority 5', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_preset_broadcast_limit(self):
        set_module_args(
            dict(
                broadcast_limit=dict(
                    port='1/1/2',
                    kbps=50,
                    log=True)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'broadcast limit 50 kbps log', 'exit']
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_absent_broadcast_limit(self):
        set_module_args(
            dict(
                broadcast_limit=dict(
                    port='1/1/2',
                    kbps=50,
                    log=False)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'no broadcast limit 50 kbps log', 'exit']
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_preset_unknown_unicast_limit(self):
        set_module_args(
            dict(
                unknown_unicast_limit=dict(
                    port='1/1/2',
                    kbps=50,
                    log=True)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'unknown-unicast limit 50 kbps log', 'exit']
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_absent_unknown_unicast_limit(self):
        set_module_args(
            dict(
                unknown_unicast_limit=dict(
                    port='1/1/2',
                    kbps=50,
                    log=False)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'no unknown-unicast limit 50 kbps log', 'exit']
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_preset_multicast_limit(self):
        set_module_args(
            dict(
                multicast_limit=dict(
                    port='1/1/2',
                    kbps=50,
                    log=True)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'multicast limit 50 kbps log', 'exit']
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(result['commands'], commands)

    def test_icx_rate_limit_output_absent_multicast_limit(self):
        set_module_args(
            dict(
                multicast_limit=dict(
                    port='1/1/2',
                    kbps=50,
                    log=False)
            ))
        commands = ['conf t', 'interface ethernet 1/1/2', 'no multicast limit 50 kbps log', 'exit']
        result = self.execute_module(changed=True, failed=False)
        self.assertEqual(result['commands'], commands)
