# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.community.network.tests.unit.compat.mock import patch
from ansible_collections.community.network.plugins.modules.network.icx import icx_qos
from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXQosModule(TestICXModule):

    module = icx_qos

    def setUp(self):
        super(TestICXQosModule, self).setUp()
        self.mock_exec_command = patch('ansible_collections.community.network.plugins.modules.network.icx.icx_qos.exec_command')
        self.mock_run_commands = patch('ansible_collections.community.network.plugins.modules.network.icx.icx_qos.run_commands')
        self.mock_get_config = patch('ansible_collections.community.network.plugins.modules.network.icx.icx_qos.get_config')
        self.mock_load_config = patch('ansible_collections.community.network.plugins.modules.network.icx..icx_qos.load_config')
        self.load_config = self.mock_load_config.start()
        self.get_config = self.mock_get_config.start()
        self.run_commands = self.mock_run_commands.start()
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXQosModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_exec_command.stop()
        self.mock_get_config.stop()

    def load_fixtures(self, commands=None):

        def load_file(*args, **kwargs):
            module = args
            for arg in args:
                if arg.params['check_running_config'] is True:
                    return load_fixture('icx_qos_config').strip()
                else:
                    return ''

        self.exec_command.return_value = (0, load_fixture('icx_qos_show_profile').strip(), None)
        self.get_config.side_effect = load_file

    def test_egress_buffer_profile_absent(self):
        set_module_args(
            dict(
                egress_buffer_profile_7150=dict(
                    port_share_level='level5-1/5',
                    user_profile_name='euser1',
                    state='absent')
            ))
        result = self.execute_module(changed=True)
        expected_commands = ['no qos egress-buffer-profile euser1 port-share-level level5-1/5']
        self.assertEqual(result['commands'], expected_commands)

    def test_egress_buffer_profile_present(self):
        set_module_args(
            dict(
                egress_buffer_profile_7150=dict(
                    port_share_level='level5-1/5',
                    user_profile_name='euser1',
                    state='present')
            ))
        result = self.execute_module(changed=True)
        expected_commands = ['qos egress-buffer-profile euser1 port-share-level level5-1/5']
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_egress_buffer_profile_7X50_present(self):
        set_module_args(
            dict(
                egress_buffer_profile_7X50=dict(
                    queue_share_level='level6-1/3',
                    user_profile_name='euser1',
                    queue_number=4,
                    state='present')
            ))
        commands = ['qos egress-buffer-profile euser1 queue-share-level level6-1/3 4']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_egress_buffer_profile_7X50_absent(self):
        set_module_args(
            dict(
                egress_buffer_profile_7X50=dict(
                    queue_share_level='level6-1/3',
                    user_profile_name='euser1',
                    queue_number=4,
                    state='absent')
            ))
        commands = ['no qos egress-buffer-profile euser1 queue-share-level level6-1/3 4']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_egress_shape_ifg_bytes_absent(self):
        set_module_args(
            dict(
                egress_shape_ifg_bytes=dict(
                    value_in_bytes=25,
                    state='absent')
            ))
        commands = ['no qos egress-shape-ifg-bytes 25']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_egress_shape_ifg_bytes_present(self):
        set_module_args(
            dict(
                egress_shape_ifg_bytes=dict(
                    value_in_bytes=25,
                    state='present')
            ))
        commands = ['qos egress-shape-ifg-bytes 25']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_ingress_buffer_profile_present(self):
        set_module_args(
            dict(
                ingress_buffer_profile=dict(
                    user_profile_name='iuser1',
                    priority_group_number=1,
                    shared_level='level4-1/9',
                    state='present')
            ))
        commands = ['qos ingress-buffer-profile iuser1 priority-group 1 xoff level4-1/9']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_ingress_buffer_profile_absent(self):
        set_module_args(
            dict(
                ingress_buffer_profile=dict(
                    user_profile_name='iuser1',
                    priority_group_number=1,
                    shared_level='level4-1/9',
                    state='absent')
            ))
        commands = ['no qos ingress-buffer-profile iuser1 priority-group 1 xoff level4-1/9']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_mechanism_absent(self):
        set_module_args(
            dict(
                mechanism=dict(
                    queueing_method='weighted',
                    state='absent')
            ))
        commands = ['no qos mechanism weighted']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_monitor_queue_drop_counters_preset(self):
        set_module_args(
            dict(
                monitor_queue_drop_counters=dict(
                    port_id='1/1/4',
                    state='present')
            ))
        commands = ['qos monitor-queue-drop-counters 1/1/4']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_monitor_queue_drop_counters_absent(self):
        set_module_args(
            dict(
                monitor_queue_drop_counters=dict(
                    port_id='1/1/4',
                    state='absent')
            ))
        commands = ['no qos monitor-queue-drop-counters 1/1/4']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_queue_name(self):
        set_module_args(
            dict(
                queue_name=dict(
                    old_name='qosp1',
                    new_name='euser1')
            ))
        commands = ['qos name qosp1 euser1']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_priority_to_pg_preset(self):
        set_module_args(
            dict(
                priority_to_pg=dict(
                    priority0='0',
                    priority1='1',
                    priority2='1',
                    priority3='1',
                    priority4='2',
                    priority5='2',
                    priority6='2',
                    priority7='4',
                    state='present')
            ))
        commands = ['qos priority-to-pg  qosp0 0 qosp1 1 qosp2 1 qosp3 1 qosp4 2 qosp5 2 qosp6 2 qosp7 4']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_priority_to_pg_absent(self):
        set_module_args(
            dict(
                priority_to_pg=dict(
                    priority0='0',
                    priority1='1',
                    priority2='1',
                    priority3='1',
                    priority4='2',
                    priority5='2',
                    priority6='2',
                    priority7='4',
                    state='absent')
            ))
        commands = ['no qos priority-to-pg  qosp0 0 qosp1 1 qosp2 1 qosp3 1 qosp4 2 qosp5 2 qosp6 2 qosp7 4']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_profile_absent(self):
        set_module_args(
            dict(
                profile=dict(
                    percentage0='6',
                    percentage1='10',
                    percentage2='10',
                    percentage3='10',
                    percentage4='12',
                    percentage5='12',
                    percentage6='15',
                    percentage7='25',
                    state='absent')
            ))
        commands = ['no qos profile qosp7 25 qosp6 15 qosp5 12 qosp4 12 qosp3 10 qosp2 10 qosp1 10 qosp0 6']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_profile_absent(self):
        set_module_args(
            dict(
                profile=dict(
                    percentage0='6',
                    percentage1='10',
                    percentage2='10',
                    percentage3='10',
                    percentage4='12',
                    percentage5='12',
                    percentage6='15',
                    percentage7='25',
                    state='present')
            ))
        commands = ['qos profile qosp7 25 qosp6 15 qosp5 12 qosp4 12 qosp3 10 qosp2 10 qosp1 10 qosp0 6']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_scheduler_profile_preset(self):
        set_module_args(
            dict(
                scheduler_profile=dict(
                    scheduling_mechanism='weighted',
                    user_profile_name='euser1',
                    wt0='1',
                    wt1='1',
                    wt2='10',
                    wt3='10',
                    wt4='10',
                    wt5='10',
                    wt6='20',
                    wt7='38',
                    state='present')
            ))
        commands = ['qos scheduler-profile euser1 mechanism weighted',
                    'qos scheduler-profile euser1 profile qosp0 1 qosp1 1 qosp2 10 qosp3 10 qosp4 10 qosp5 10 qosp6 20 qosp7 38']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_scheduler_profile_absent(self):
        set_module_args(dict(
            scheduler_profile=dict(
                scheduling_mechanism='weighted',
                user_profile_name='euser1',
                wt0='1',
                wt1='1',
                wt2='10',
                wt3='10',
                wt4='10',
                wt5='10',
                wt6='20',
                wt7='38',
                state='absent')))
        commands = ['no qos scheduler-profile euser1']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_sflow_set_cpu_rate_limit_absent(self):
        set_module_args(dict(sflow_set_cpu_rate_limit=dict(packet_rate='1000', burst_size='5000', state='absent')))

        commands = ['no qos sflow-set-cpu-rate-limit 1000 5000']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_sflow_set_cpu_rate_limit_present(self):
        set_module_args(dict(sflow_set_cpu_rate_limit=dict(packet_rate='1000', burst_size='5000', state='present')))

        commands = ['qos sflow-set-cpu-rate-limit 1000 5000']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_tagged_priority_preset(self):
        set_module_args(dict(tagged_priority=dict(num=2, queue='qosp0', state='present')))
        commands = ['qos tagged-priority 2 qosp0']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_internal_trunk_queue_absent(self):
        set_module_args(dict(internal_trunk_queue=dict(level='level6-1/3', queue=6, state='absent')))
        commands = ['no qos-internal-trunk-queue level6-1/3 6']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_attach_egress_buffer_profile_preset(self):
        set_module_args(dict(attach_egress_buffer_profile=dict(port='1/1/3', profile_name='euser1', state='present')))
        commands = ['interface ethernet 1/1/3', 'egress-buffer-profile euser1']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)

    def test_icx_dscp_priority(self):
        set_module_args(dict(dscp_priority=dict(dscp_value='0 2 3 4', priority=1, state='present')))
        commands = ['qos-tos map dscp-priority 0 2 3 4 to 1']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], commands)
