#!/usr/bin/python
#
# (c) 2018 Extreme Networks Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: exos_facts
deprecated:
  removed_in: 6.0.0
  why: This collection and all content in it is unmaintained and deprecated.
  alternatives: Unknown.
author:
    - "Lance Richardson (@hlrichardson)"
    - "Ujwal Koamrla (@ujwalkomarla)"
short_description: Collect facts from devices running Extreme EXOS
description:
  - Collects a base set of device facts from a remote device that
    is running EXOS.  This module prepends all of the base network
    fact keys with C(ansible_net_<fact>).  The facts module will
    always collect a base set of facts from the device and can
    enable or disable collection of additional facts.
notes:
  - Tested against EXOS 22.5.1.7
  - "The I(gather_network_resources) option currently only works with
    C(ansible_connection: ansible.netcommon.httpapi). For details, see
    U(https://github.com/ansible-collections/community.network/issues/460)."
options:
  gather_subset:
    description:
      - When supplied, this argument will restrict the facts collected
        to a given subset.  Possible values for this argument include
        all, hardware, config, and interfaces.  Can specify a list of
        values to include a larger subset.  Values can also be used
        with an initial C(!) to specify that a specific subset should
        not be collected.
    required: false
    type: list
    default: ['!config']
  gather_network_resources:
    description:
      - When supplied, this argument will restrict the facts collected
        to a given subset. Possible values for this argument include
        all and the resources like interfaces, vlans etc.
        Can specify a list of values to include a larger subset.
        Values can also be used with an initial C(!) to specify that
        a specific subset should not be collected.
        Valid subsets are 'all', 'lldp_global', 'lldp_interfaces',
        'vlans', 'l2_interfaces'.
    type: list
'''

EXAMPLES = """
  - name:  Gather all legacy facts
    community.network.exos_facts:
      gather_subset: all

  - name: Gather only the config and default facts
    community.network.exos_facts:
      gather_subset: config

  - name: Do not gather hardware facts
    community.network.exos_facts:
      gather_subset: "!hardware"

  - name: Gather legacy and resource facts
    community.network.exos_facts:
      gather_subset: all
      gather_network_resources: all

  - name: Gather only the lldp global resource facts and no legacy facts
    community.network.exos_facts:
      gather_subset:
        - '!all'
        - '!min'
      gather_network_resources:
        - lldp_global

  - name: Gather lldp global resource and minimal legacy facts
    community.network.exos_facts:
      gather_subset: min
      gather_network_resources: lldp_global
"""

RETURN = """
ansible_net_gather_subset:
  description: The list of fact subsets collected from the device
  returned: always
  type: list

ansible_net_gather_network_resources:
  description: The list of fact for network resource subsets collected from the device
  returned: when the resource is configured
  type: list

# default
ansible_net_model:
  description: The model name returned from the device
  returned: always
  type: str
ansible_net_serialnum:
  description: The serial number of the remote device
  returned: always
  type: str
ansible_net_version:
  description: The operating system version running on the remote device
  returned: always
  type: str
ansible_net_hostname:
  description: The configured hostname of the device
  returned: always
  type: str

# hardware
ansible_net_memfree_mb:
  description: The available free memory on the remote device in Mb
  returned: when hardware is configured
  type: int
ansible_net_memtotal_mb:
  description: The total memory on the remote device in Mb
  returned: when hardware is configured
  type: int

# config
ansible_net_config:
  description: The current active config from the device
  returned: when config is configured
  type: str

# interfaces
ansible_net_all_ipv4_addresses:
  description: All IPv4 addresses configured on the device
  returned: when interfaces is configured
  type: list
ansible_net_all_ipv6_addresses:
  description: All Primary IPv6 addresses configured on the device
  returned: when interfaces is configured
  type: list
ansible_net_interfaces:
  description: A hash of all interfaces running on the system
  returned: when interfaces is configured
  type: dict
ansible_net_neighbors:
  description: The list of LLDP neighbors from the remote device
  returned: when interfaces is configured
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.network.plugins.module_utils.network.exos.argspec.facts.facts import FactsArgs
from ansible_collections.community.network.plugins.module_utils.network.exos.facts.facts import Facts


def main():
    """Main entry point for AnsibleModule
    """
    argument_spec = FactsArgs.argument_spec

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    warnings = ['default value for `gather_subset` '
                'will be changed to `min` from `!config` in community.network 2.0.0 onwards']

    result = Facts(module).get_facts()

    ansible_facts, additional_warnings = result
    warnings.extend(additional_warnings)

    module.exit_json(ansible_facts=ansible_facts, warnings=warnings)


if __name__ == '__main__':
    main()
