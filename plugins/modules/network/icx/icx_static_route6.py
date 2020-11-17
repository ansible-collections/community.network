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
module: icx_static_route6
version_added: "2.10"
author: "Ruckus Wireless (@Commscope)"
short_description: Manage static IPV6 routes on Ruckus ICX 7000 series switches
description:
  - This module provides declarative management of static
    IP routes on Ruckus ICX network devices.
notes:
  - Tested against ICX 10.1.
  - For information on using ICX platform, see L(the ICX OS Platform Options guide,../network/user_guide/platform_icx.html).
options:
  prefix:
    description:
      - Destination IPv6 address, including prefix length.
    type: str
  next_hop:
    description:
      - IPv6 address of a next-hop gateway. The next-hop address may be a global IPv6 address or a link-local IPv6 address.
    type: str
  admin_distance:
    description:
      - Specifies the route's administrative distance. The default value is 1.
    type: int
  aggregate:
    description: List of static route definitions.
    type: list
    suboptions:
      prefix:
        description:
          - Destination IPv6 address, including prefix length.
        type: str
      next_hop:
        description:
          - IPv6 address of a next-hop gateway. The next-hop address may be a global IPv6 address or a link-local IPv6 address.
        type: str
      admin_distance:
        description:
          - Specifies the route's administrative distance. The default value is 1.
        type: int
      state:
        description:
          - State of the static route configuration.
        type: str
        choices: ['present', 'absent']
      check_running_config:
        description:
          - Check running configuration. This can be set as environment variable.
           Module will use environment variable value(default:False), unless it is overridden, by specifying it as module parameter.
        type: bool
  purge:
    description:
      - Purge routes not defined in the I(aggregate) parameter.
    default: no
    type: bool
  state:
    description:
      - State of the static route configuration.
    type: str
    default: present
    choices: ['present', 'absent']
  check_running_config:
    description:
      - Check running configuration. This can be set as environment variable.
       Module will use environment variable value(default:False), unless it is overridden, by specifying it as module parameter.
    type: bool
    default: False
"""


EXAMPLES = """
- name: configure static route
  icx_static_route6:
    prefix: 6666:1:1::/64
    next_hop: 6666:1:2::0

- name: remove configuration
  icx_static_route6:
    prefix: 6666:1:1::/64
    next_hop: 6666:1:2::0
    state: absent

- name: Add static route aggregates
  icx_static_route6:
    aggregate:
      - { prefix: 6666:1:8::/64, next_hop: 6666:1:9::0 }
      - { prefix: 6666:1:5::/64, next_hop: 6666:1:6::0 }

- name: remove static route aggregates
  icx_static_route6:
    aggregate:
      - { prefix: 6666:1:8::/64, next_hop: 6666:1:9::0 }
      - { prefix: 6666:1:5::/64, next_hop: 6666:1:6::0 }
    state: absent
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - ip route 6666:1:1::/64 6666:1:2::0
"""


from copy import deepcopy
import re

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils.network.common.utils import remove_default_spec
from ansible.module_utils.network.icx.icx import get_config, load_config
try:
    from ipaddress import ip_network, ip_interface, IPv6Address
    HAS_IPADDRESS = True
except ImportError:
    HAS_IPADDRESS = False


def shorten_ip(want):
    try:
        unicode('')
    except NameError:
        unicode = str
    for item in want:
        item['prefix'] = str(ip_interface(item['prefix'].decode('UTF-8')).network.compressed)
        item['next_hop'] = str(IPv6Address(item['next_hop'].decode('UTF-8')).compressed)
    return want


def map_obj_to_commands(want, have, module):
    commands = list()
    purge = module.params['purge']
    want = shorten_ip(want)
    for w in want:
        for h in have:
            for key in ['prefix', 'next_hop']:
                if w[key] != h[key]:
                    break
            else:
                break
        else:
            h = None

        prefix = w['prefix']
        next_hop = w['next_hop']
        admin_distance = w.get('admin_distance')
        if not admin_distance and h:
            w['admin_distance'] = admin_distance = h['admin_distance']
        state = w['state']
        del w['state']
        if 'check_running_config' in w.keys():
            del w['check_running_config']

        if state == 'absent' and have == []:
            commands.append('no ipv6 route %s %s' % (prefix, next_hop))

        if state == 'absent' and w in have:
            commands.append('no ipv6 route %s  %s' % (prefix, next_hop))
        elif state == 'present' and w not in have:
            if admin_distance:
                commands.append('ipv6 route %s  %s distance %s' % (prefix, next_hop, admin_distance))
            else:
                commands.append('ipv6 route %s  %s' % (prefix, next_hop))
    if purge:
        for h in have:
            if h not in want:
                commands[:0] = ['no ipv6 route %s  %s' % (h['prefix'], h['next_hop'])]
    return commands


def map_config_to_obj(module):
    obj = []
    compare = module.params['check_running_config']
    out = get_config(module, flags='| include ipv6 route', compare=compare)
    for line in out.splitlines():
        splitted_line = line.split()
        if len(splitted_line) not in (4, 5, 6):
            continue
        prefix = splitted_line[2]
        next_hop = splitted_line[3]
        if len(splitted_line) == 6:
            admin_distance = splitted_line[5]
        else:
            admin_distance = '1'

        obj.append({
            'prefix': prefix, 'next_hop': next_hop,
            'admin_distance': admin_distance
        })
    return obj


def prefix_length_parser(prefix, module):
    '''if '/' in prefix and mask is not None:
        module.fail_json(msg='Ambigous, specifed both length and mask')'''
    if '/' in prefix:
        cidr = ip_network(to_text(prefix))
        prefix = str(cidr.network_address)
    return prefix


def map_params_to_obj(module, required_together=None):
    keys = ['prefix', 'next_hop', 'admin_distance', 'state']
    obj = []
    aggregate = module.params.get('aggregate')
    if aggregate:
        for item in aggregate:
            route = item.copy()
            for key in keys:
                if route.get(key) is None:
                    route[key] = module.params.get(key)
            module._check_required_together(required_together, route)
            obj.append(route)
    else:
        module._check_required_together(required_together, module.params)

        obj.append({
            'prefix': module.params['prefix'],
            'next_hop': module.params['next_hop'],
            'admin_distance': module.params.get('admin_distance'),
            'state': module.params['state'],
        })

    for route in obj:
        if route['admin_distance']:
            route['admin_distance'] = str(route['admin_distance'])
    return obj


def main():
    """ main entry point for module execution
    """
    element_spec = dict(
        prefix=dict(type='str'),
        next_hop=dict(type='str'),
        admin_distance=dict(type='int'),
        state=dict(default='present', choices=['present', 'absent']),
        check_running_config=dict(default=False, type='bool', fallback=(env_fallback, ['ANSIBLE_CHECK_ICX_RUNNING_CONFIG']))
    )
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['prefix'] = dict(required=True)
    remove_default_spec(aggregate_spec)

    argument_spec = dict(
        aggregate=dict(type='list', elements='dict', options=aggregate_spec),
        purge=dict(default=False, type='bool')
    )

    argument_spec.update(element_spec)

    required_one_of = [['aggregate', 'prefix']]
    required_together = [['prefix', 'next_hop']]
    mutually_exclusive = [['aggregate', 'prefix']]

    module = AnsibleModule(argument_spec=argument_spec,
                           required_one_of=required_one_of,
                           mutually_exclusive=mutually_exclusive,
                           supports_check_mode=True)

    if not HAS_IPADDRESS:
        module.fail_json(msg="ipaddress python package is required")
    result = {'changed': False}
    warnings = list()
    if warnings:
        result['warnings'] = warnings

    want = map_params_to_obj(module, required_together=required_together)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands(want, have, module)
    result['commands'] = commands
    if commands:
        if not module.check_mode:
            response = load_config(module, commands)
        result['changed'] = True
        result['response'] = response

    module.exit_json(**result)


if __name__ == '__main__':
    main()
