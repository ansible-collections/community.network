#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
---
module: icx_qos
version_added: "1.3.0"
author: "Ruckus Wireless (@Commscope)"
short_description: Configures qos features on icx switch.
description:
  - This module configures qos profiles.
notes:
  - Tested against ICX 10.1.
  - For information on using ICX platform, see L(the ICX OS Platform Options guide,../network/user_guide/platform_icx.html).
options:
  egress_buffer_profile_7150:
    description: Configures an egress buffer profile for the share port level. This is supported only on ICX 7150.
      The default egress buffer profile level is level4-1/9 for 1/9 of the buffers in buffer memory.
    type: dict
    suboptions:
      user_profile_name:
        description: Specifies the name of the egress buffer profile to be configured.
        type: str
      port_share_level:
        description: Specifies the number of buffers that can be used in the buffer memory.
        type: str
        choices: ['level3-1/16', 'level4-1/9','level5-1/5','level6-1/3','level7-1/2', 'level8-2/3']
      state:
        description: Specifies whether the egress-buffer-profile should be configured or removed.
          "absent" will detach the profile from any ports that are using it.
        type: str
        default: present
        choices: ['present', 'absent']
  egress_buffer_profile_7X50:
    description: Configures an egress buffer profile for the share queue level.
                 This command is supported only on Ruckus ICX 7250, ICX 7450, and ICX 7750 devices.
                 The default egress buffer profile level is level4-1/9 for 1/9 of the buffers in buffer memory.
                 This is not supported on ICX 7150
    type: dict
    suboptions:
      user_profile_name:
        description: Specifies the name of the egress buffer profile to be configured..
        type: str
      queue_share_level:
        description: Specifies the number of buffers that can be used in a sharing pool. Eight levels are supported.
        type: str
        choices: ['level1-1/64','level2-1/32','level3-1/16','level4-1/9','level5-1/5','level6-1/3','level7-1/2','level8-2/3']
      queue_number:
        description: Specifies the queue to apply the buffer limit to. There are eight hardware queues per port.
        type: int
      state:
        description: Specifies whether the egress-buffer-profile should be configured or removed.
          "absent" will detach the profile from any ports that are using it.
        type: str
        default: present
        choices: ['present', 'absent']
  egress_shape_ifg_bytes:
    description: Configures egress shaper IFG bytes. By default a value of 20 is configured.
    type: dict
    suboptions:
      value_in_bytes:
        description: Specifies the number of preamble and IFG bytes to be added to egress shaping in the range 1 through 127.
        type: int
      state:
        description: Specifies whether egress shape ifg bytes should be configured or reset to default value of 20.
        type: str
        default: present
        choices: ['present', 'absent']
  ingress_buffer_profile:
    description: Configures an ingress buffer profile. By default an ingress buffer profile is not configured.
                 This command is supported only on Ruckus ICX 7250, ICX 7450, and ICX 7750 devices.
                 This command is not supported on the Ruckus ICX 7150 or the Ruckus ICX 7650.
                 For PFC disabled ports, the default PG XOFF limit is level7-1/2.
                 For PFC enabled ports, the default PG XOFF limit is level2-1/32.
    type: dict
    suboptions:
      user_profile_name:
        description: Specifies the name of the ingress buffer profile to be configured.
        type: str
      priority_group_number:
        description: Specifies the priority group (PG) number with the XOFF threshold level that must be configured.
        type: int
      shared_level:
        description: Specifies the per-PG buffer threshold to trigger sending of priority flow control (PFC).
        type: str
        choices: ['level1-1/64','level2-1/32','level3-1/16','level4-1/9','level5-1/5','level6-1/3','level7-1/2']
      state:
        description: Specifies whether ingress buffer profile will be configured or removed. "absent" will detach the profile from any ports that are using it.
        type: str
        default: present
        choices: ['present', 'absent']
  mechanism:
    description: Configures the Quality of Service (QoS) queuing method. Default is WRR
    type: dict
    suboptions:
      queueing_method:
        description: Method of packet prioritization.
        type: str
        choices: ['strict', 'weighted', 'mixed-sp-wrr']
      state:
        description: Specifies whether queueing method should be configured or reset to use the WRR method of packet prioritization.
        type: str
        default: present
        choices: ['present', 'absent']
  monitor_queue_drop_counters:
    description: Configures the port that the Ruckus ICX 7150 device monitors for the incrementing of the egress queue drop counters.
    type: dict
    suboptions:
      port_id:
        description: Specifies the port ID to associate with the egress queue drop counters..
        type: str
      state:
        description: Specifies whether queue drop counters must be associated to a port or reset to the internal local CPU port.
        type: str
        default: present
        choices: ['present', 'absent']
  queue_name:
    description: Renames the queue. The default queue names are qosp7, qosp6, qosp5, qosp4, qosp3, qosp2, qosp1, and qosp0.
    type: dict
    suboptions:
      old_name:
        description: Specifies the name of the queue before the change.
        type: str
      new_name:
        description: Specifies the new name of the queue. The name can be an alphanumeric type, string up to 32 characters long.
        type: str
  priority_to_pg:
    description: Configures priority-to-priority-group (PG) mapping for priority flow control (PFC). This command is supported only
     on Ruckus ICX 7250, ICX 7450, and ICX 7750 devices. This command is not supported on the Ruckus ICX 7150 or the Ruckus ICX 7650.
    type: dict
    suboptions:
      priority0:
        description: PG for QoS internal priority 0.
        type: int
        choices: [0, 1, 2]
      priority1:
        description: PG for QoS internal priority 1.
        type: int
        choices: [0, 1, 2]
      priority2:
        description: PG for QoS internal priority 2.
        type: int
        choices: [0, 1, 2]
      priority3:
        description: PG for QoS internal priority 3.
        type: int
        choices: [0, 1, 2]
      priority4:
        description: PG for QoS internal priority 4.
        type: int
        choices: [0, 1, 2]
      priority5:
        description: PG for QoS internal priority 5.
        type: int
        choices: [0, 1, 2]
      priority6:
        description: PG for QoS internal priority 6.
        type: int
        choices: [0, 1, 2, 3]
      priority7:
        description: PG for QoS internal priority 7.
        type: int
        choices: [0, 1, 2, 3, 4]
      state:
        description: Configures priority to PG mapping or restores the default.
        type: str
        default: present
        choices: ['present', 'absent']
  profile:
    description: Changes the minimum bandwidth percentages of the eight Weighted Round Robin (WRR) queues.
    type: dict
    suboptions:
      percentage0:
        description: Percentage of the device outbound bandwidth allocated to queue 0.
        type: int
      percentage1:
        description: Percentage of the device outbound bandwidth allocated to queue 1.
        type: int
      percentage2:
        description: Percentage of the device outbound bandwidth allocated to queue 2.
        type: int
      percentage3:
        description: Percentage of the device outbound bandwidth allocated to queue 3.
        type: int
      percentage4:
        description: Percentage of the device outbound bandwidth allocated to queue 4.
        type: int
      percentage5:
        description: Percentage of the device outbound bandwidth allocated to queue 5.
        type: int
      percentage6:
        description: Percentage of the device outbound bandwidth allocated to queue 6.
        type: int
      percentage7:
        description: Percentage of the device outbound bandwidth allocated to queue 7.
        type: int
      state:
        description: Changes bandwidth percentages or restores the default bandwidth percentages.
        type: str
        default: present
        choices: ['present', 'absent']
  scheduler_profile:
    description: Configures a user-defined Quality of Service (QoS) scheduler profile.
      Either scheduling-mechanism or profile weight must be specfied.
    type: dict
    suboptions:
      user_profile_name:
        description: Specifies the name of the scheduler profile to be configured.
        type: str
      scheduling_mechanism:
        description: Configures the queue assignment with the specified scheduling mechanism.
        type: str
        choices: ['mixed-sp-wrr', 'strict', 'weighted']
      wt0:
        description: QOS-profile weight for queue 0.
        type: int
      wt1:
        description: QOS-profile weight for queue 1.
        type: int
      wt2:
        description: QOS-profile weight for queue 2.
        type: int
      wt3:
        description: QOS-profile weight for queue 3.
        type: int
      wt4:
        description: QOS-profile weight for queue 4.
        type: int
      wt5:
        description: QOS-profile weight for queue 5.
        type: int
      wt6:
        description: QOS-profile weight for queue 6.
        type: int
      wt7:
        description: QOS-profile weight for queue 7.
        type: int
      state:
        description: Configures or removes the scheduler profile configuration.
        type: str
        default: present
        choices: ['present', 'absent']
  sflow_set_cpu_rate_limit:
    description: Sets the CPU rate limit for sFlow.
                 A CPU rate limit for sFlow is configured with the default values of 100 sFlow
                 sampled packets per second (PPS) and a burst size of 5000 B.
    type: dict
    suboptions:
      packet_rate:
        description: Specifies the number of sFlow sampled PPS into the CPU. The value is measured in PPS and ranges from 1 to 1000.
        type: int
      burst_size:
        description: Specifies the burst size. The value is measured in bytes and ranges from 1 to 99999.
        type: int
      state:
        description: Sets or returns the device to the default CPU rate limit for sFlow.
        type: str
        default: present
        choices: ['present', 'absent']
  tagged_priority:
    description: Changes the VLAN priority of 802.1p to hardware forwarding queue mappings.
    type: dict
    suboptions:
      num:
        description: Specifies the VLAN priority. The value can range from 0 to 7.
        type: int
      queue:
        description: Specifies the hardware forwarding queue on which you are reassigning the priority. The value can range from 0 to 7.
        type: str
      state:
        description: Changed VLAN priority to hardware forwarding queue or sets it to 802.1p.
        type: str
        default: present
        choices: ['present', 'absent']
  internal_trunk_queue:
    description: Modifies the dynamic buffer-share level of inter-packet-processor (inter-pp)
                 HiGig links egress queues on ICX 7450 devices.
                 This command is supported only on ICX 7450 devices or across stack units or for ports
                 across master and slave packet-processor (pp) devices in ICX7450-48 units.
    type: dict
    suboptions:
      level:
        description: Specifies the number of buffers that can be used in a sharing pool.
        type: str
        choices: ['level1-1/64', 'level2-1/32', 'level3-1/16', 'level4-1/9', 'level5-1/5', 'level6-1/3', 'level7-1/2', 'level8-2/3']
      queue:
        description: Specifies the queue to apply the buffer limit to. Each port has eight hardware queues. The value can range from 0 to 7.
        type: int
      state:
        description: Change or restore the default queue share level on the specified queue.
        type: str
        default: present
        choices: ['present', 'absent']
  attach_egress_buffer_profile:
    description: Attaches a user-configured egress buffer profile to one or more ports.
    type: dict
    suboptions:
      port:
        description: Port to which profile should be attached.
        type: str
      profile_name:
        description: Specifies the name of the egress buffer profile to be attached to the port.
        type: str
      state:
        description: Attach or removes a user-configured egress buffer profile from the port and the port uses the default egress buffer profile.
        type: str
        default: present
        choices: ['present', 'absent']
  dscp_priority:
    description: Changes the differentiated Services Code Point (DSCP)-to-internal-forwarding-priority mappings..
    type: dict
    suboptions:
      dscp_value:
        description: Specifies the DSCP value ranges that you are remapping.
                     You can map up to eight DSCP values to the same forwarding priority in the same command.
                     Values can be from 0 to 7
        type: list
        elements: int
      priority:
        description: Specifies the internal forwarding priority.
        type: str
      state:
        description: Changes or restores the default value.
        type: str
        default: present
        choices: ['present', 'absent']
  check_running_config:
    description: Check running configuration. This can be set as environment variable.
       Module will use environment variable value(default:False), unless it is overridden, by specifying it as module parameter.
    type: bool
"""

EXAMPLES = """
  - name: Modifies the dynamic buffer-share
    community.network.icx_qos:
      internal_trunk_queue:
        level: level5-1/5
        queue: 4
        state: present

  - name: update dscp-priority
    community.network.icx_qos:
      dscp_priority:
         dscp_value: 0 1 3 4
         priority: '2'
         state: absent

  - name: update cpu rate limit
    community.network.icx_qos:
      sflow_set_cpu_rate_limit:
        burst_size: 5000
        packet_rate: 1000
        state: present
"""

RETURN = """
changed:
  description: true when qos command was executed. False otherwise.
  returned: always
  type: bool
"""


from copy import deepcopy
import re

from ansible.module_utils._text import to_text
from ansible_collections.community.network.plugins.module_utils.network.icx.icx import run_commands, get_config, load_config
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import remove_default_spec


def map_obj_to_commands(updates, module):
    commands = []
    want, have = updates
    qos_profile = qos_profile_names(module, have)
    cmd = ''
    interface = ''

    for w in want:
        egress_buffer_profile_7150 = w.get('egress_buffer_profile_7150')
        egress_buffer_profile_7X50 = w.get('egress_buffer_profile_7X50')
        egress_shape_ifg_bytes = w.get('egress_shape_ifg_bytes')
        ingress_buffer_profile = w.get('ingress_buffer_profile')
        mechanism = w.get('mechanism')
        monitor_queue_drop_counters = w.get('monitor_queue_drop_counters')
        queue_name = w.get('queue_name')
        priority_to_pg = w.get('priority_to_pg')
        profile = w.get('profile')
        scheduler_profile = w.get('scheduler_profile')
        sflow_set_cpu_rate_limit = w.get('sflow_set_cpu_rate_limit')
        tagged_priority = w.get('tagged_priority')
        internal_trunk_queue = w.get('internal_trunk_queue')
        attach_egress_buffer_profile = w.get('attach_egress_buffer_profile')
        dscp_priority = w.get('dscp_priority')

        if egress_buffer_profile_7150:
            if egress_buffer_profile_7150['state'] == 'present':
                commands.append('qos egress-buffer-profile %s port-share-level %s' %
                                (egress_buffer_profile_7150['user_profile_name'],
                                 egress_buffer_profile_7150['port_share_level']))
            elif egress_buffer_profile_7150['state'] == 'absent':
                commands.append('no qos egress-buffer-profile %s port-share-level %s' %
                                (egress_buffer_profile_7150['user_profile_name'],
                                 egress_buffer_profile_7150['port_share_level']))

        if egress_buffer_profile_7X50:
            if egress_buffer_profile_7X50['state'] == 'present':
                commands.append('qos egress-buffer-profile %s queue-share-level %s %s' %
                                (egress_buffer_profile_7X50['user_profile_name'],
                                 egress_buffer_profile_7X50['queue_share_level'],
                                 egress_buffer_profile_7X50['queue_number']))
            elif egress_buffer_profile_7X50['state'] == 'absent':
                commands.append('no qos egress-buffer-profile %s queue-share-level %s %s' %
                                (egress_buffer_profile_7X50['user_profile_name'],
                                 egress_buffer_profile_7X50['queue_share_level'],
                                 egress_buffer_profile_7X50['queue_number']))

        if egress_shape_ifg_bytes:
            if egress_shape_ifg_bytes['state'] == 'present':
                commands.append('qos egress-shape-ifg-bytes %s' % (egress_shape_ifg_bytes['value_in_bytes']))
            elif egress_shape_ifg_bytes['state'] == 'absent':
                commands.append('no qos egress-shape-ifg-bytes %s' % (egress_shape_ifg_bytes['value_in_bytes']))

        if ingress_buffer_profile:
            if ingress_buffer_profile['state'] == 'present':
                commands.append('qos ingress-buffer-profile %s priority-group %s xoff %s'
                                % (ingress_buffer_profile['user_profile_name'],
                                   ingress_buffer_profile['priority_group_number'],
                                   ingress_buffer_profile['shared_level']))
            elif ingress_buffer_profile['state'] == 'absent':
                commands.append('no qos ingress-buffer-profile %s priority-group %s xoff %s'
                                % (ingress_buffer_profile['user_profile_name'],
                                   ingress_buffer_profile['priority_group_number'],
                                   ingress_buffer_profile['shared_level']))

        if mechanism:
            if mechanism['state'] == 'present':
                commands.append('qos mechanism %s' % (mechanism['queueing_method']))
            else:
                commands.append('no qos mechanism %s' % (mechanism['queueing_method']))

        if monitor_queue_drop_counters:
            if monitor_queue_drop_counters['state'] == 'present':
                commands.append('qos monitor-queue-drop-counters %s' % (monitor_queue_drop_counters['port_id']))
            else:
                commands.append('no qos monitor-queue-drop-counters %s' % (monitor_queue_drop_counters['port_id']))

        if queue_name:
            commands.append('qos name %s %s' % (queue_name['old_name'], queue_name['new_name']))

        if priority_to_pg:
            if priority_to_pg['state'] == 'present':
                commands.append('qos priority-to-pg  qosp0 %s qosp1 %s qosp2 %s qosp3 %s qosp4 %s qosp5 %s qosp6 %s qosp7 %s'
                                % (priority_to_pg['priority0'], priority_to_pg['priority1'], priority_to_pg['priority2'],
                                   priority_to_pg['priority3'], priority_to_pg['priority4'], priority_to_pg['priority5'],
                                   priority_to_pg['priority6'], priority_to_pg['priority7']))
            else:
                commands.append('no qos priority-to-pg  qosp0 %s qosp1 %s qosp2 %s qosp3 %s qosp4 %s qosp5 %s qosp6 %s qosp7 %s'
                                % (priority_to_pg['priority0'], priority_to_pg['priority1'], priority_to_pg['priority2'],
                                   priority_to_pg['priority3'], priority_to_pg['priority4'], priority_to_pg['priority5'],
                                   priority_to_pg['priority6'], priority_to_pg['priority7']))

        if profile:
            if profile['state'] == 'present':
                commands.append('qos profile %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s'
                                % (qos_profile[0], profile['percentage7'], qos_profile[1], profile['percentage6'],
                                   qos_profile[2], profile['percentage5'], qos_profile[3], profile['percentage4'],
                                   qos_profile[4], profile['percentage3'], qos_profile[5], profile['percentage2'],
                                   qos_profile[6], profile['percentage1'], qos_profile[7], profile['percentage0']))
            else:
                commands.append('no qos profile %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s'
                                % (qos_profile[0], profile['percentage7'], qos_profile[1], profile['percentage6'],
                                    qos_profile[2], profile['percentage5'], qos_profile[3], profile['percentage4'],
                                    qos_profile[4], profile['percentage3'], qos_profile[5], profile['percentage2'],
                                    qos_profile[6], profile['percentage1'], qos_profile[7], profile['percentage0']))

        if scheduler_profile:
            if scheduler_profile['state'] == 'present':
                commands.append('qos scheduler-profile %s mechanism %s' % (scheduler_profile['user_profile_name'], scheduler_profile['scheduling_mechanism']))

                commands.append('qos scheduler-profile %s profile qosp0 %s qosp1 %s qosp2 %s qosp3 %s qosp4 %s qosp5'
                                ' %s qosp6 %s qosp7 %s'
                                % (scheduler_profile['user_profile_name'], scheduler_profile['wt0'],
                                   scheduler_profile['wt1'], scheduler_profile['wt2'], scheduler_profile['wt3'],
                                   scheduler_profile['wt4'], scheduler_profile['wt5'], scheduler_profile['wt6'],
                                   scheduler_profile['wt7']))
            else:
                commands.append('no qos scheduler-profile %s' % scheduler_profile['user_profile_name'])

        if sflow_set_cpu_rate_limit:
            if sflow_set_cpu_rate_limit['state'] == 'present':
                commands.append('qos sflow-set-cpu-rate-limit %s %s' % (sflow_set_cpu_rate_limit['packet_rate'], sflow_set_cpu_rate_limit['burst_size']))
            else:
                command = 'no qos sflow-set-cpu-rate-limit %s %s' % (sflow_set_cpu_rate_limit['packet_rate'], sflow_set_cpu_rate_limit['burst_size'])
                commands.append(command)

        if tagged_priority:
            if tagged_priority['state'] == 'present':
                commands.append('qos tagged-priority %s %s' % (tagged_priority['num'], tagged_priority['queue']))
            else:
                commands.append('no qos tagged-priority %s %s' % (tagged_priority['num'], tagged_priority['queue']))

        if internal_trunk_queue:
            if internal_trunk_queue['state'] == 'present':
                commands.append('qos-internal-trunk-queue %s %s' % (internal_trunk_queue['level'], internal_trunk_queue['queue']))
            else:
                commands.append('no qos-internal-trunk-queue %s %s' % (internal_trunk_queue['level'], internal_trunk_queue['queue']))

        if attach_egress_buffer_profile:
            interface = 'interface ethernet %s' % (attach_egress_buffer_profile['port'])
            commands.append(interface)
            if attach_egress_buffer_profile['state'] == 'present':
                cmd = 'egress-buffer-profile %s' % (attach_egress_buffer_profile['profile_name'])
                commands.append(cmd)
            else:
                cmd = 'no egress-buffer-profile %s' % (attach_egress_buffer_profile['profile_name'])
                commands.append(cmd)

        if dscp_priority:
            temp = dscp_priority['dscp_value']
            dscp_value = ' '.join(str(i) for i in temp)
            if dscp_priority['state'] == 'present':
                commands.append('qos-tos map dscp-priority %s to %s' % (dscp_value, dscp_priority['priority']))
            else:
                commands.append('no qos-tos map dscp-priority %s to %s' % (dscp_value, dscp_priority['priority']))
    if have:
        if attach_egress_buffer_profile:
            prof = map_config_to_obj_egress_prof(module)
            if 'no' in cmd:
                strg = cmd.split(' ')[1:]
                for k, v in prof.items():
                    if attach_egress_buffer_profile['port'] not in k:
                        if interface and cmd in commands:
                            commands.remove(interface)
                            commands.remove(cmd)
                    elif attach_egress_buffer_profile['port'] in k and ' '.join(strg) not in v:
                        if interface and cmd in commands:
                            commands.remove(interface)
                            commands.remove(cmd)
            else:
                for k, v in prof.items():
                    if attach_egress_buffer_profile['port'] in k and cmd in v:
                        commands.remove(interface)
                        commands.remove(cmd)
        else:
            for i in commands:
                if 'no ' in i:
                    strg = i.split(' ')[1:]
                    Flag = 0
                    if 'qos scheduler-profile' in ' '.join(strg):
                        for k in have:
                            if 'qos scheduler-profile' in k:
                                Flag = 1
                        if not Flag:
                            commands.remove(i)
                    elif ' '.join(strg) not in have:
                        commands.remove(i)
                else:
                    if i in have:
                        commands.remove(i)
    return commands


def map_config_to_obj(module):
    config = get_config(module)
    match = re.findall(r'qos.*?[\n]', str(config), re.DOTALL)
    list_interface = [i.rstrip("\n").strip() for i in match]
    return list_interface


def map_config_to_obj_egress_prof(module):
    config = get_config(module)
    list_interface = dict()
    match = re.findall(r'interface ethernet.*?\!', str(config), re.DOTALL)
    if match:
        for i in match:
            split = i.split('\n')
            list_interface[split[0]] = split[1:]
    for k, v in list_interface.items():
        list_interface[k] = [i.strip() for i in v]
    return list_interface


def qos_profile_names(module, have):
    if 'qos mechanism strict' in have:
        qos_profile = ['qosp7', 'qosp6', 'qosp5', 'qosp4', 'qosp3', 'qosp2', 'qosp1', 'qosp0']
        return qos_profile
    command = 'show qos-profile all'
    rc, out, err = exec_command(module, command)
    qos_profile = []
    if 'Unicast Traffic\n' and 'Multicast Traffic\n' in out:
        profile = out.split('Unicast Traffic\n')[1].split('Multicast Traffic\n')[0]
        for i in profile.strip().split('\n'):
            qos_profile.append(i.split(' ')[1])
    else:
        profile = []
        for i in out.strip().split('\n'):
            profile.append(i.split(' ')[1])
        qos_profile = profile[1:]
    return qos_profile


def map_params_to_obj(module):
    obj = []
    params = {
        'egress_buffer_profile_7150': module.params['egress_buffer_profile_7150'],
        'egress_buffer_profile_7X50': module.params['egress_buffer_profile_7X50'],
        'egress_shape_ifg_bytes': module.params['egress_shape_ifg_bytes'],
        'ingress_buffer_profile': module.params['ingress_buffer_profile'],
        'mechanism': module.params['mechanism'],
        'monitor_queue_drop_counters': module.params['monitor_queue_drop_counters'],
        'queue_name': module.params['queue_name'],
        'priority_to_pg': module.params['priority_to_pg'],
        'profile': module.params['profile'],
        'scheduler_profile': module.params['scheduler_profile'],
        'sflow_set_cpu_rate_limit': module.params['sflow_set_cpu_rate_limit'],
        'tagged_priority': module.params['tagged_priority'],
        'internal_trunk_queue': module.params['internal_trunk_queue'],
        'attach_egress_buffer_profile': module.params['attach_egress_buffer_profile'],
        'dscp_priority': module.params['dscp_priority'],
    }
    obj.append(params)
    return obj


def check_fail(module, output):
    error = [
        re.compile(br"^error", re.I)
    ]
    for x in output:
        for regex in error:
            if regex.search(x):
                module.fail_json(msg=x)


def main():
    """ main entry point for module execution
    """

    egress_buffer_profile_7150_spec = dict(
        port_share_level=dict(type='str', choices=['level3-1/16', 'level4-1/9', 'level5-1/5', 'level6-1/3', 'level7-1/2', 'level8-2/3']),
        user_profile_name=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    egress_buffer_profile_7x50_spec = dict(
        queue_share_level=dict(type='str',
                               choices=['level1-1/64', 'level2-1/32',
                                        'level3-1/16', 'level4-1/9',
                                        'level5-1/5', 'level6-1/3',
                                        'level7-1/2', 'level8-2/3']),
        user_profile_name=dict(type='str'),
        queue_number=dict(type='int'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    egress_shape_ifg_bytes_spec = dict(
        value_in_bytes=dict(type='int'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    ingress_buffer_profile_spec = dict(
        user_profile_name=dict(type='str'),
        priority_group_number=dict(type='int'),
        shared_level=dict(type='str', choices=['level1-1/64', 'level2-1/32', 'level3-1/16', 'level4-1/9', 'level5-1/5', 'level6-1/3', 'level7-1/2']),
        state=dict(default='present', choices=['present', 'absent'])
    )

    mechanism_spec = dict(
        queueing_method=dict(type='str', choices=['strict', 'weighted', 'mixed-sp-wrr']),
        state=dict(default='present', choices=['present', 'absent'])
    )

    monitor_queue_drop_counters_spec = dict(
        port_id=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    queue_name_spec = dict(
        old_name=dict(type='str'),
        new_name=dict(type='str')
    )

    priority_to_pg_spec = dict(
        priority0=dict(type='int', choices=[0, 1, 2]),
        priority1=dict(type='int', choices=[0, 1, 2]),
        priority2=dict(type='int', choices=[0, 1, 2]),
        priority3=dict(type='int', choices=[0, 1, 2]),
        priority4=dict(type='int', choices=[0, 1, 2]),
        priority5=dict(type='int', choices=[0, 1, 2]),
        priority6=dict(type='int', choices=[0, 1, 2, 3]),
        priority7=dict(type='int', choices=[0, 1, 2, 3, 4]),
        state=dict(default='present', choices=['present', 'absent'])
    )

    profile_spec = dict(
        percentage0=dict(type='int'),
        percentage1=dict(type='int'),
        percentage2=dict(type='int'),
        percentage3=dict(type='int'),
        percentage4=dict(type='int'),
        percentage5=dict(type='int'),
        percentage6=dict(type='int'),
        percentage7=dict(type='int'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    scheduler_profile_spec = dict(
        user_profile_name=dict(type='str'),
        scheduling_mechanism=dict(type='str', choices=['mixed-sp-wrr', 'strict', 'weighted']),
        wt0=dict(type='int'),
        wt1=dict(type='int'),
        wt2=dict(type='int'),
        wt3=dict(type='int'),
        wt4=dict(type='int'),
        wt5=dict(type='int'),
        wt6=dict(type='int'),
        wt7=dict(type='int'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    sflow_set_cpu_rate_limit_spec = dict(
        packet_rate=dict(type='int'),
        burst_size=dict(type='int'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    tagged_priority_spec = dict(
        num=dict(type='int'),
        queue=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    internal_trunk_queue_spec = dict(
        level=dict(type='str', choices=['level1-1/64', 'level2-1/32', 'level3-1/16', 'level4-1/9', 'level5-1/5', 'level6-1/3', 'level7-1/2', 'level8-2/3']),
        queue=dict(type='int'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    attach_egress_buffer_profile_spec = dict(
        port=dict(type='str'),
        profile_name=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    dscp_priority_spec = dict(
        dscp_value=dict(type='list', elements='int'),
        priority=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    argument_spec = dict(
        egress_buffer_profile_7150=dict(type='dict', options=egress_buffer_profile_7150_spec),
        egress_buffer_profile_7X50=dict(type='dict', options=egress_buffer_profile_7x50_spec),
        egress_shape_ifg_bytes=dict(type='dict', options=egress_shape_ifg_bytes_spec),
        ingress_buffer_profile=dict(type='dict', options=ingress_buffer_profile_spec),
        mechanism=dict(type='dict', options=mechanism_spec),
        monitor_queue_drop_counters=dict(type='dict', options=monitor_queue_drop_counters_spec),
        queue_name=dict(type='dict', options=queue_name_spec),
        priority_to_pg=dict(type='dict', options=priority_to_pg_spec),
        profile=dict(type='dict', options=profile_spec),
        scheduler_profile=dict(type='dict', options=scheduler_profile_spec),
        sflow_set_cpu_rate_limit=dict(type='dict', options=sflow_set_cpu_rate_limit_spec),
        tagged_priority=dict(type='dict', options=tagged_priority_spec),
        internal_trunk_queue=dict(type='dict', options=internal_trunk_queue_spec),
        attach_egress_buffer_profile=dict(type='dict', options=attach_egress_buffer_profile_spec),
        dscp_priority=dict(type='dict', options=dscp_priority_spec),
        check_running_config=dict(default=False, type='bool',
                                  fallback=(env_fallback, ['ANSIBLE_CHECK_ICX_RUNNING_CONFIG']))
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = {}
    result['changed'] = False
    want = map_params_to_obj(module)
    result['want'] = want
    if module.params['check_running_config'] is False:
        have = []
    else:
        have = map_config_to_obj(module)
        result['have'] = have
    commands = map_obj_to_commands((want, have), module)
    result['commands'] = commands

    if commands:
        if not module.check_mode:
            output = load_config(module, commands)
            if output:
                check_fail(module, output)
            result['output'] = output
        result['changed'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()
