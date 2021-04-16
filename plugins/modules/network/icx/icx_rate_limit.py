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
module: icx_rate_limit
version_added: "1.3.0"
author: "Ruckus Wireless (@Commscope)"
short_description: Configures rate limit on icx switch.
description:
  - This module configures rate limit input, output, arp and BUM.
notes:
  - Tested against ICX 10.1.
  - For information on using ICX platform, see L(the ICX OS Platform Options guide,../network/user_guide/platform_icx.html).
options:
  rate_limit_input:
    description: Configures a port-based rate-limiting policy.
    type: dict
    suboptions:
      port:
        description: port(stack/slot/port) on which to set the rate-limiting policy.
        type: str
      lag:
        description: lag id, if port is part of lag.
        type: str
      average_rate:
        description: Specifies the maximum number of kilobits per second (kbps).
        type: int
        required: true
      burst_size:
        description: Specifies the burst size in kilobits.
        type: int
      state:
        description: Specifies whether to configure or remove rate limiting.
        type: str
        default: present
        choices: ['present', 'absent']
  rate_limit_output:
    description: Configures the maximum rate at which outbound traffic is sent on a port priority queue or on a LAG port.
    type: dict
    suboptions:
      port:
        description: port(stack/slot/port) on which to set the rate-limiting policy.
        type: str
      lag:
        description: lag id, if port is part of lag.
        type: str
      priority_queue:
        description: Specifies a rate-shaping priority. The value can range from 0 to 7.
        type: int
      value:
        description: Specifies the rate-shaping limit.
        type: int
        required: true
      state:
        description: Specifies whether to configure or remove output rate shaping.
        type: str
        default: present
        choices: ['present', 'absent']
  rate_limit_arp:
    description: Limits the number of ARP packets the Ruckus device accepts during each second.
    type: dict
    suboptions:
      number:
        description: Specifies the number of ARP packets and can be from 0 through 100. If you specify 0, the device will not accept any ARP packets.
        type: int
        required: true
      state:
        description: Specifies whether to enable or disable arp rate limiting.
        type: str
        default: present
        choices: ['present', 'absent']
  rate_limit_bum:
    description: Configures the global level BUM suppression logging interval. The default logging interval 5 minutes
    type: dict
    suboptions:
      minutes:
        description: Specifies the interval, in whole minutes, between Syslog notifications. The value can be any integer from 1 to 10.
        type: int
        required: true
      state:
        description: Specifies whether to configure or return to the default value.
        type: str
        default: present
        choices: ['present', 'absent']
  broadcast_limit:
    description: Configures the maximum number of broadcast packets allowed per second. Enables Syslog logging of broadcast packets.
    type: dict
    suboptions:
      port:
        description: port( stack/slot/port) on which to set broadcast limit.
        type: str
        required: true
      kbps:
        description: Enables byte-based limiting. The value can be 1 to Max Port Speed. Set to 0 to disable byte-based limiting.
        type: int
        required: true
      log:
        description: True enables Syslog logging when the broadcast limit exceeds kpbs. False will disable logging.
        type: bool
  unknown_unicast_limit:
    description: Configures the maximum number of unknown unicast packets allowed per second. Enables Syslog logging of unknown unicast packets.
    type: dict
    suboptions:
      port:
        description: port(stack/slot/port) on which to set broadcast limit.
        type: str
        required: true
      kbps:
        description: Specifies the maximum number of unknown unicast packets per second. The value can be 1 to Max Port Speed. Set to 0 to disable limiting.
        type: int
        required: true
      log:
        description: Enables Syslog logging when the unknown unicast limit exceeds kpbs. False will disable logging.
        type: bool
  multicast_limit:
    description: Configures the maximum number of multicast packets allowed per second. Enables Syslog logging of multicast packets.
    type: dict
    suboptions:
      port:
        description: port(stack/slot/port) on which to set broadcast limit.
        type: str
        required: true
      kbps:
        description: Specifies the maximum number of multicast packets per second. The value can be 1 to Max Port Speed. Set to 0 to disable limiting..
        type: int
        required: true
      log:
        description: True enables Syslog logging when the multicast limit exceeds kpbs. False will disable logging.
        type: bool
  aggregate:
    description: List of Interfaces definitions.
    type: list
    elements: dict
    suboptions:
      rate_limit_input:
        description: Configures a port-based rate-limiting policy.
        type: dict
        suboptions:
          port:
            description: port(stack/slot/port) on which to set the rate-limiting policy.
            type: str
          lag:
            description: lag id, if port is part of lag.
            type: str
          average_rate:
            description: Specifies the maximum number of kilobits per second (kbps).
            type: int
            required: true
          burst_size:
            description: Specifies the burst size in kilobits.
            type: int
          state:
            description: Specifies whether to configure or remove rate limiting.
            type: str
            default: present
            choices: ['present', 'absent']
      rate_limit_output:
        description: Configures the maximum rate at which outbound traffic is sent on a port priority queue or on a LAG port.
        type: dict
        suboptions:
          port:
            description: port(stack/slot/port) on which to set the rate-limiting policy.
            type: str
          lag:
            description: lag id, if port is part of lag.
            type: str
          priority_queue:
            description: Specifies a rate-shaping priority. The value can range from 0 to 7.
            type: int
          value:
            description: Specifies the rate-shaping limit.
            type: int
            required: true
          state:
            description: Specifies whether to configure or remove output rate shaping.
            type: str
            default: present
            choices: ['present', 'absent']
      rate_limit_arp:
        description: Limits the number of ARP packets the Ruckus device accepts during each second.
        type: dict
        suboptions:
          number:
            description: Specifies the number of ARP packets and can be from 0 through 100. If you specify 0, the device will not accept any ARP packets.
            type: int
            required: true
          state:
            description: Specifies whether to enable or disable arp rate limiting.
            type: str
            default: present
            choices: ['present', 'absent']
      rate_limit_bum:
        description: Configures the global level BUM suppression logging interval. The default logging interval 5 minutes
        type: dict
        suboptions:
          minutes:
            description: Specifies the interval, in whole minutes, between Syslog notifications. The value can be any integer from 1 to 10.
            type: int
            required: true
          state:
            description: Specifies whether to configure or return to the default value.
            type: str
            default: present
            choices: ['present', 'absent']
      broadcast_limit:
        description: Configures the maximum number of broadcast packets allowed per second. Enables Syslog logging of broadcast packets.
        type: dict
        suboptions:
          port:
            description: port(stack/slot/port) on which to set broadcast limit.
            type: str
            required: true
          kbps:
            description: Enables byte-based limiting. The value can be 1 to Max Port Speed. Set to 0 to disable byte-based limiting.
            type: int
            required: true
          log:
            description: True enables Syslog logging when the broadcast limit exceeds kpbs. False will disable logging.
            type: bool
      unknown_unicast_limit:
        description: Configures the maximum number of unknown unicast packets allowed per second. Enables Syslog logging of unknown unicast packets.
        type: dict
        suboptions:
          port:
            description: port(stack/slot/port) on which to set broadcast limit.
            type: str
            required: true
          kbps:
            description: Specifies the maximum number of unknown unicast packets per second. The value can be 1 to Max Port Speed. Set to 0 to disable limiting.
            type: int
            required: true
          log:
            description: Enables Syslog logging when the unknown unicast limit exceeds kpbs. False will disable logging.
            type: bool
      multicast_limit:
        description: Configures the maximum number of multicast packets allowed per second. Enables Syslog logging of multicast packets.
        type: dict
        suboptions:
          port:
            description: port(stack/slot/port) on which to set multicast limit.
            type: str
            required: true
          kbps:
            description: Specifies the maximum number of multicast packets per second. The value can be 1 to Max Port Speed. Set to 0 to disable limiting..
            type: int
            required: true
          log:
            description: True enables Syslog logging when the multicast limit exceeds kpbs. False will disable logging.
            type: bool
  check_running_config:
    description: Check running configuration. This can be set as environment variable.
      Module will use environment variable value, unless it is overridden, by specifying it as module parameter.
    type: bool
    default: no
"""

EXAMPLES = """
- name: set rate-limit input
  icx_rate_limit:
    rate_limit_input:
      interace: 1/1/2
      avergae_rate: 500
- name: set rate-limit output
  icx_rate_limit:
    rate_limit_output:
      interace: 1/1/2
      value: 500
- name: set rate-limit arp
  icx_rate_limit:
    rate_limit_arp:
      number: 100
- name: set rate-limit BUM
  icx_rate_limit:
    rate_limit_bum:
      minutes: 3
"""

RETURN = """
changed:
  description: true when rate-limit command was executed. False otherwise.
  returned: always
  type: bool
"""

from copy import deepcopy
import re

from ansible.module_utils._text import to_text
from ansible_collections.community.network.plugins.module_utils.network.icx.icx import load_config, get_config
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import remove_default_spec


def map_obj_to_commands(updates, module):
    commands = []
    want, have = updates
    for w in want:
        wcmds = []
        wcmd = ''
        interface = ''
        if w.get('rate_limit_input'):
            if w['rate_limit_input']['lag']:
                if not w['rate_limit_input']['port']:
                    module.fail_json(msg="port is required")
                wcmds.append('lag %s' % (w['rate_limit_input']['lag']))
                interface = ('lag %s' % (w['rate_limit_input']['lag']))
            else:
                wcmds.append('interface ethernet %s' % (w['rate_limit_input']['port']))
                interface = ('interface ethernet %s' % (w['rate_limit_input']['port']))
            if w['rate_limit_input']['state'] == 'present':
                if w['rate_limit_input']['lag']:
                    wcmd = 'rate-limit input fixed ethernet %s %s' % (w['rate_limit_input']['port'], w['rate_limit_input']['average_rate'])
                    wcmds.append(wcmd)
                elif w['rate_limit_input']['burst_size']:
                    wcmd = 'rate-limit input fixed %s burst %s' % (w['rate_limit_input']['average_rate'], w['rate_limit_input']['burst_size'])
                    wcmds.append(wcmd)
                else:
                    wcmd = 'rate-limit input fixed %s' % (w['rate_limit_input']['average_rate'])
                    wcmds.append(wcmd)
            else:
                if w['rate_limit_input']['lag']:
                    wcmd = 'no rate-limit input fixed ethernet %s %s' % (w['rate_limit_input']['port'], w['rate_limit_input']['average_rate'])
                    wcmds.append(wcmd)
                elif w['rate_limit_input']['burst_size']:
                    wcmd = 'no rate-limit input fixed %s burst %s' % (w['rate_limit_input']['average_rate'], w['rate_limit_input']['burst_size'])
                    wcmds.append(wcmd)
                else:
                    wcmd = 'no rate-limit input fixed %s' % (w['rate_limit_input']['average_rate'])
                    wcmds.append(wcmd)

        elif w.get('rate_limit_output'):
            if w['rate_limit_output']['lag']:
                if not w['rate_limit_output']['port']:
                    module.fail_json(msg="interface is required")
                wcmds.append('lag %s' % (w['rate_limit_output']['lag']))
                interface = ('lag %s' % (w['rate_limit_output']['lag']))
            else:
                wcmds.append('interface ethernet %s' % (w['rate_limit_output']['port']))
                interface = ('interface ethernet %s' % (w['rate_limit_output']['port']))
            if w['rate_limit_output']['state'] == 'present':
                if w['rate_limit_output']['priority_queue']:
                    if w['rate_limit_output']['lag']:
                        wcmd = ('rate-limit output shaping ethernet %s %s priority %s'
                                % (w['rate_limit_output']['port'], w['rate_limit_output']['value'],
                                   w['rate_limit_output']['priority_queue']))
                        wcmds.append(wcmd)
                    else:
                        wcmd = 'rate-limit output shaping %s priority %s' % (w['rate_limit_output']['value'], w['rate_limit_output']['priority_queue'])
                        wcmds.append(wcmd)
                else:
                    if w['rate_limit_output']['lag']:
                        wcmd = 'rate-limit output shaping ethernet %s %s' % (w['rate_limit_output']['port'], w['rate_limit_output']['value'])
                        wcmds.append(wcmd)
                    else:
                        wcmd = 'rate-limit output shaping %s' % (w['rate_limit_output']['value'])
                        wcmds.append(wcmd)
            else:
                if w['rate_limit_output']['priority_queue']:
                    if w['rate_limit_output']['lag']:
                        wcmd = ('no rate-limit output shaping ethernet %s %s priority %s'
                                % (w['rate_limit_output']['port'], w['rate_limit_output']['value'],
                                   w['rate_limit_output']['priority_queue']))
                        wcmds.append(wcmd)
                    else:
                        wcmd = 'no rate-limit output shaping %s priority %s' % (w['rate_limit_output']['value'], w['rate_limit_output']['priority_queue'])
                        wcmds.append(wcmd)
                else:
                    if w['rate_limit_output']['lag']:
                        wcmd = 'no rate-limit output shaping ethernet %s %s' % (w['rate_limit_output']['port'], w['rate_limit_output']['value'])
                        wcmds.append(wcmd)
                    else:
                        wcmd = 'no rate-limit output shaping %s' % (w['rate_limit_output']['value'])
                        wcmds.append(wcmd)

        elif w.get('broadcast_limit'):
            interface = ('interface ethernet %s' % (w['broadcast_limit']['port']))
            wcmds.append('interface ethernet %s' % (w['broadcast_limit']['port']))
            if w['broadcast_limit']['log']:
                wcmd = 'broadcast limit %s kbps log' % (w['broadcast_limit']['kbps'])
                wcmds.append(wcmd)
            elif not w['broadcast_limit']['log']:
                wcmd = 'no broadcast limit %s kbps log' % (w['broadcast_limit']['kbps'])
                wcmds.append(wcmd)
            elif w['broadcast_limit']['log'] is None:
                wcmd = 'broadcast limit %s kbps' % (w['broadcast_limit']['kbps'])
                wcmds.append(wcmd)

        elif w.get('unknown_unicast_limit'):
            interface = ('interface ethernet %s' % (w['unknown_unicast_limit']['port']))
            wcmds.append('interface ethernet %s' % (w['unknown_unicast_limit']['port']))
            if w['unknown_unicast_limit']['log']:
                wcmd = 'unknown-unicast limit %s kbps log' % (w['unknown_unicast_limit']['kbps'])
                wcmds.append(wcmd)
            elif not w['unknown_unicast_limit']['log']:
                wcmd = 'no unknown-unicast limit %s kbps log' % (w['unknown_unicast_limit']['kbps'])
                wcmds.append(wcmd)
            elif w['unknown_unicast_limit']['log'] is None:
                wcmd = 'unknown-unicast limit %s kbps' % (w['unknown_unicast_limit']['kbps'])
                wcmds.append(wcmd)

        elif w.get('multicast_limit'):
            interface = ('interface ethernet %s' % (w['multicast_limit']['port']))
            wcmds.append('interface ethernet %s' % (w['multicast_limit']['port']))
            if w['multicast_limit']['log']:
                wcmd = 'multicast limit %s kbps log' % (w['multicast_limit']['kbps'])
                wcmds.append(wcmd)
            elif not w['multicast_limit']['log']:
                wcmd = 'no multicast limit %s kbps log' % (w['multicast_limit']['kbps'])
                wcmds.append(wcmd)
            elif w['multicast_limit']['log'] is None:
                wcmd = 'multicast limit %s kbps' % (w['multicast_limit']['kbps'])
                wcmds.append(wcmd)

        elif w.get('rate_limit_arp'):
            if w['rate_limit_arp']['state'] == 'present':
                wcmd = 'rate-limit-arp %s' % (w['rate_limit_arp']['number'])
                wcmds.append(wcmd)
            else:
                wcmd = 'no rate-limit-arp %s' % (w['rate_limit_arp']['number'])
                wcmds.append(wcmd)

        elif w.get('rate_limit_bum'):
            if w['rate_limit_bum']['state'] == 'present':
                wcmd = 'rate-limit-log %s' % (w['rate_limit_bum']['minutes'])
                wcmds.append(wcmd)
            else:
                wcmd = 'no rate-limit-log %s' % (w['rate_limit_bum']['minutes'])
                wcmds.append(wcmd)

        if have:
            if (w.get('rate_limit_bum') or w.get('rate_limit_arp')):
                if "no " in wcmd:
                    if have[""] == []:
                        wcmds = []
                    else:
                        strg = wcmd.split(' ')[1:]
                        if ' '.join(strg) not in have[""]:
                            wcmds = []
                elif wcmd in have['']:
                    wcmds = []

            else:
                hcmds = []
                for key, val in have.items():
                    if interface in key:
                        hcmds = val

                if "no " in wcmd:
                    if hcmds == []:
                        wcmds = []
                    else:
                        strg = wcmd.split(' ')[1:]
                        if ' '.join(strg) not in hcmds:
                            wcmds = []
                else:
                    if hcmds:
                        if(wcmd in hcmds):
                            wcmds = []
        if(wcmds != []):
            [commands.append(i) for i in wcmds]
    return commands


def map_config_to_obj(module):
    config = get_config(module)
    list_interface = dict()

    match = re.findall(r'lag \S+.*?\!', str(config), re.DOTALL)
    if match:
        for i in match:
            split = i.split('\n')
            list_interface[split[0]] = split[1:]

    match = re.findall(r'interface ethernet.*?\!', str(config), re.DOTALL)
    if match:
        for i in match:
            split = i.split('\n')
            list_interface[split[0]] = split[1:]

    list_interface[""] = []
    match = re.search(r'rate-limit-log \d{1,2}', str(config))
    if match:
        list_interface[""].append(match.group(0))

    match = re.search(r'rate-limit-arp \d{1,2}', str(config))
    if match:
        list_interface[""].append(match.group(0))

    for k, v in list_interface.items():
        for i in v:
            list_interface[k] = [i.strip()]
    return list_interface


def map_params_to_obj(module):
    obj = []
    aggregate = module.params.get('aggregate')
    if aggregate:
        for item in aggregate:
            for key in item:
                if key == 'check_running_config' or item.get(key) is None:
                    continue
                temp = dict()
                temp[key] = item[key]
                obj.append(temp)

    else:
        for key in module.params:
            temp = dict()
            if key in ['aggregate', 'check_running_config'] or module.params.get(key) is None:
                continue
            temp[key] = module.params[key]
            obj.append(temp)
    return obj


def main():
    """ main entry point for module execution
    """

    input_spec = dict(
        port=dict(type='str'),
        lag=dict(type='str'),
        average_rate=dict(type='int', required=True),
        burst_size=dict(type='int'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    output_spec = dict(
        port=dict(type='str'),
        priority_queue=dict(type='int'),
        value=dict(type='int', required=True),
        lag=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    broadcast_spec = dict(
        port=dict(type='str', required=True),
        kbps=dict(type='int', required=True),
        log=dict(type='bool')
    )

    unknown_unicast_spec = dict(
        port=dict(type='str', required=True),
        kbps=dict(type='int', required=True),
        log=dict(type='bool')
    )

    multicast_spec = dict(
        port=dict(type='str', required=True),
        kbps=dict(type='int', required=True),
        log=dict(type='bool')
    )

    arp_spec = dict(
        number=dict(type='int', required=True),
        state=dict(default='present', choices=['present', 'absent'])
    )

    bum_spec = dict(
        minutes=dict(type='int', required=True),
        state=dict(default='present', choices=['present', 'absent'])
    )

    element_spec = dict(
        rate_limit_input=dict(type='dict', options=input_spec),
        rate_limit_output=dict(type='dict', options=output_spec),
        rate_limit_arp=dict(type='dict', options=arp_spec),
        rate_limit_bum=dict(type='dict', options=bum_spec),
        broadcast_limit=dict(type='dict', options=broadcast_spec),
        unknown_unicast_limit=dict(type='dict', options=unknown_unicast_spec),
        multicast_limit=dict(type='dict', options=multicast_spec)
    )

    aggregate_spec = deepcopy(element_spec)

    remove_default_spec(aggregate_spec)

    argument_spec = dict(
        aggregate=dict(type='list', elements='dict', options=aggregate_spec)
    )
    element_spec.update(check_running_config=dict(default=False, type='bool',
                        fallback=(env_fallback, ['ANSIBLE_CHECK_ICX_RUNNING_CONFIG'])))
    argument_spec.update(element_spec)
    required_one_of = [['rate_limit_input', 'rate_limit_output',
                        'rate_limit_arp', 'rate_limit_bum', 'broadcast_limit',
                        'unknown_unicast_limit', 'multicast_limit', 'aggregate']]

    module = AnsibleModule(argument_spec=argument_spec, required_one_of=required_one_of,
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
            responses = load_config(module, commands)
            result['changed'] = True
            result['responses'] = responses

    module.exit_json(**result)


if __name__ == '__main__':
    main()