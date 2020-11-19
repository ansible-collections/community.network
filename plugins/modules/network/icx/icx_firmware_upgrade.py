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
module: icx_firmware_upgrade
version_added: "2.10"
author: "Ruckus Wireless (@Commscope)"
short_description: Upgrades firmware of ICX switches
description:
  - This module copies new firmware to switch, flashes it to primary/secondary and reboots the switch.
notes:
  - Tested against ICX 10.1.
  - For information on using ICX platform, see L(the ICX OS Platform Options guide,../network/user_guide/platform_icx.html).
options:
  server_type:
    description:
      - Data transfer protocol to be used
    type: str
    choices: ['scp', 'https', 'tftp']
    required: true
  server_address:
    description:
      - IPV4/IPV6 address of the scp/https/tftp server
    type: str
    required: true
  server_port:
    description:
      - The port number of the server. Default values will be selected based on protocol type.
        Default scp:22, https:443
    type: int
  partition:
    description:
     - Partition to be used for upgrade.
    type: str
    choices: ['primary','secondary','fips-ufi-primary-sig','fips-ufi-secondary-sig']
  scp_user:
    description:
      - remote username to be used for scp login.
    type: str
  scp_pass:
    description:
      - remote password to be used for scp login.
    type: str
  boot_only:
    description:
      - Boot the switch if True.
    default: no
    type: bool
  save_running_config:
    description:
      - execute Write memory Command.
    default: no
    type: bool
  filename:
    description:
      - The path of the .bin/.sig file.
    type: str
    required: true
"""

EXAMPLES = """
- name: upgrade firmware using scp
  icx_firmware_upgrade:
    server_type: scp
    server_address: 10.20.1.1
    partition: secondary
    filename: SPR08030.bin
    boot_only: False
    save_running_config: False
    scp_user: alethea
    scp_pass: alethea123

- name: upgrade firmware using tftp
  icx_firmware_upgrade:
    server_type: tftp
    server_address: 2001:db8::1
    partition: fips-ufi-primary-sig
    filename: signature_ufi.sig
    boot_only: False
    save_running_config: False

- name: upgrade firmware using https
  icx_firmware_upgrade:
    server_type: https
    server_address: 10.20.1.8
    partition: primary
    filename: SPR08030.bin
    boot_only: False
    save_running_config: False

- name: run only boot command
  icx_firmware_upgrade:
    boot_only: True
    save_running_config: True
"""

RETURN = """
changed:
  description: true when file is copied and switch flashed with it. false otherwise.
  returned: always
  type: bool
"""

from copy import deepcopy
import re

from ansible.module_utils._text import to_text
from ansible_collections.community.network.plugins.module_utils.network.icx.icx import run_commands, exec_scp
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils.network.common.utils import remove_default_spec


def map_params_to_obj(module):
    commands = dict()
    command = ''
    res_commands = []
    server_type = module.params['server_type']
    server_address = module.params['server_address']
    server_port = module.params['server_port']
    filename = module.params['filename']
    partition = module.params['partition']
    if partition in ['fips-ufi-primary-sig', 'fips-ufi-secondary-sig']:
        boot_partition = partition.split('-')[2]
    else:
        boot_partition = partition
    boot_only = module.params['boot_only']
    save_running_config = module.params['save_running_config']
    if not boot_only:
        if server_type == 'tftp':
            command = 'copy tftp flash %s %s %s' % (server_address, filename, partition)
            commands['command'] = command

        elif server_type == 'scp':
            if server_port:
                command = 'copy scp flash %s %d %s %s' % (server_address, server_port, filename, partition)
            else:
                command = 'copy scp flash %s %s %s' % (server_address, filename, partition)
            commands['command'] = command
            commands['scp_user'] = module.params['scp_user']
            commands['scp_pass'] = module.params['scp_pass']

        elif server_type == 'https':
            if server_port:
                command = 'copy https flash %s %s %s port %d' % (server_address, filename, partition, server_port)
            else:
                command = 'copy https flash %s %s %s' % (server_address, filename, partition)

            commands['command'] = command
        res_commands.append(commands)
        if save_running_config:
            res_commands.append('write memory')
            res_commands.append('boot system flash %s yes' % (boot_partition))
        else:
            res_commands.append('boot system flash %s yes' % (boot_partition))
    else:
        if save_running_config:
            res_commands.append('write memory')
            res_commands.append('boot system flash %s yes' % (boot_partition))
        else:
            res_commands.append('boot system flash %s yes' % (boot_partition))

    return res_commands


def checkValidations(module):
    server_type = module.params['server_type']
    server_address = module.params['server_address']
    # server_port = module.params['server_port']
    filename = module.params['filename']
    boot_only = module.params['boot_only']
    scp_user = module.params['scp_user']
    scp_pass = module.params['scp_pass']

    if not boot_only:
        if server_type is None:
            module.fail_json(msg="server_type is required")
        if server_address is None:
            module.fail_json(msg="server_address is required")
        if filename is None:
            module.fail_json(msg="filename is required")
        if server_type == 'scp':
            if scp_user is None:
                module.fail_json(msg="scp_user is required")
            if scp_pass is None:
                module.fail_json(msg="scp_pass is required")


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        server_type=dict(type='str', choices=['scp', 'https', 'tftp'], required=False),
        server_address=dict(type='str', required=False),
        server_port=dict(type='int'),
        partition=dict(type='str', choices=['primary', 'secondary', 'fips-ufi-primary-sig',
                                            'fips-ufi-secondary-sig'], required=True),
        filename=dict(type='str', required=False),
        boot_only=dict(type='bool', required=True),
        save_running_config=dict(type='bool', required=True),
        scp_user=dict(type='str', required=False),
        scp_pass=dict(type='str', required=False, no_log=True),
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    checkValidations(module)
    result = {'changed': False}

    commands = map_params_to_obj(module)

    if module.params['save_running_config']:
        if module.params['boot_only']:
            result['commands'] = [commands[0], commands[1]]
        else:
            result['commands'] = [commands[0]['command'], commands[1], commands[2]]
    else:
        if module.params['boot_only']:
            result['commands'] = [commands[0]]
        else:
            result['commands'] = [commands[0]['command'], commands[1]]

    if commands:
        if not module.check_mode:
            if module.params['server_type'] == 'scp':
                responses = exec_scp(module, commands[0])
                responses = run_commands(module, commands[1:])
            else:
                responses = run_commands(module, commands)
        result['changed'] = True
        result['responses'] = responses

    module.exit_json(**result)


if __name__ == '__main__':
    main()
