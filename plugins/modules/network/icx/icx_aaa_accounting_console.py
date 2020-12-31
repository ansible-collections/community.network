#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_aaa_accounting_console
author: "Ruckus Wireless (@Commscope)"
short_description: Configures AAA accounting in Ruckus ICX 7000 series switches
description:
  - Configures AAA accounting in Ruckus ICX 7000 series switches.
notes:
  - Tested against ICX 10.1
options:
  commands:
    description: Configures the AAA accounting configuration parameters for EXEC commands.
    type: dict
    suboptions:
      privilege_level:
        description: Configures the device to perform AAA accounting for the commands available at the specified privilege level. Valid values are 0,4 and 5.
        type: int
        choices: [0,4,5]
      primary_method:
        description: primary accounting method.
        type: str
        choices: ['radius', 'tacacs+', 'none']
      backup_method1:
        description: backup accounting method if primary method fails.
        type: str
        choices: ['radius', 'tacacs+', 'none']
      backup_method2:
        description: bacup accounting method if primary and backup1 metthods fail.
        type: str
        choices: ['none']
      state:
        description: Specifies whether to configure or remove rate limiting.
        type: str
        default: present
        choices: ['present', 'absent']
  dot1x:
    description: Enables 802.1X accounting.
    type: dict
    suboptions:
      primary_method:
        description: primary accounting method.
        type: str
        choices: ['radius','none']
      backup_method1:
        description: backup accounting method if primary method fails.
        type: str
        choices: ['none']
      state:
        description: Specifies whether to configure or remove rate limiting.
        type: str
        default: present
        choices: ['present', 'absent']
  exec_:
    description: Configures the AAA accounting configuration parameters for SSH and Telnet access.
    type: dict
    suboptions:
      primary_method:
        description: primary accounting method.
        type: str
        choices: ['radius', 'tacacs+', 'none']
      backup_method1:
        description: backup accounting method if primary method fails.
        type: str
        choices: ['radius', 'tacacs+', 'none']
      backup_method2:
        description: bacup accounting method if primary and backup1 metthods fail.
        type: str
        choices: ['none']
      state:
        description: Specifies whether to configure or remove rate limiting.
        type: str
        default: present
        choices: ['present', 'absent']
  mac_auth:
    description: Enables or disables RADIUS accounting for MAC authentication sessions..
    type: dict    
    suboptions:
      primary_method:
        description: primary accounting method.
        type: str
        choices: ['radius','none']
      backup_method1:
        description: backup accounting method if primary method fails.
        type: str
        choices: ['none']
      state:
        description: Specifies whether to configure or remove rate limiting.
        type: str
        default: present
        choices: ['present', 'absent']
  system:
    description: Configures AAA accounting to record when system events occur on the device.
    type: dict    
    suboptions:
      primary_method:
        description: primary accounting method.
        type: str
        choices: ['radius', 'tacacs+', 'none']
      backup_method1:
        description: backup accounting method if primary method fails.
        type: str
        choices: ['radius', 'tacacs+', 'none']
      backup_method2:
        description: bacup accounting method if primary and backup1 metthods fail.
        type: str
        choices: ['none']
      state:
        description: Specifies whether to configure or remove rate limiting.
        type: str
        default: present
        choices: ['present', 'absent']
  enable_console:
    description: Enables AAA support for commands entered at the console.
    type: dict    
    suboptions:
      state:
        description: Specifies whether to configure or remove rate limiting.
        type: str
        default: present
        choices: ['present', 'absent'] 
"""
EXAMPLES = """
- name: aaa accounting commands for mac_auth and commands
  community.network.icx_aaa_accounting_console:
    mac_auth:
      primary_method: none
      state: present
    commands:
      privilege_level: 0
      primary_method: radius
      backup_method1: none
      state: present

- name: aaa accounting commands for system
  community.network.icx_aaa_accounting_console:
    system:
      primary_method: tacacs+
      backup_method1: radius
      backup_method2: none
      state: absent
"""

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError,exec_command
from ansible_collections.community.network.plugins.module_utils.network.icx.icx import load_config

def build_command(module, commands=None, dot1x=None, exec_=None, mac_auth=None, system=None, enable_console=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """
    command= [] 
    if commands is not None:
        if commands['state'] == 'absent':
            cmd = "no aaa accounting commands {} default start-stop".format(commands['privilege_level'])      

        else:
            cmd = "aaa accounting commands {} default start-stop".format(commands['privilege_level'])      

        if commands['primary_method'] is not None:
            cmd+= " {}".format(commands['primary_method'])
            if commands['backup_method1'] is not None:
                cmd+= " {}".format(commands['backup_method1'])
                if commands['backup_method2'] is not None:
                    cmd+= " {}".format(commands['backup_method2'])
        command.append(cmd)

    if dot1x is not None:
        if dot1x['state'] == 'absent':
            cmd = "no aaa accounting dot1x default start-stop"      

        else:
            cmd = "aaa accounting dot1x default start-stop"   

        if dot1x['primary_method'] is not None:
            cmd+= " {}".format(dot1x['primary_method'])
            if dot1x['backup_method1'] is not None:
                cmd+= " {}".format(dot1x['backup_method1'])
        command.append(cmd)

    if exec_ is not None:
        if exec_['state'] == 'absent':
            cmd = "no aaa accounting exec default start-stop"

        else:
            cmd = "aaa accounting exec default start-stop"      

        if exec_['primary_method'] is not None:
            cmd+= " {}".format(exec_['primary_method'])
            if exec_['backup_method1'] is not None:
                cmd+= " {}".format(exec_['backup_method1'])
                if exec_['backup_method2'] is not None:
                    cmd+= " {}".format(exec_['backup_method2'])
        command.append(cmd)

    if mac_auth is not None:
        if mac_auth['state'] == 'absent':
            cmd = "no aaa accounting mac-auth default start-stop"      

        else:
            cmd = "aaa accounting mac-auth default start-stop"   

        if mac_auth['primary_method'] is not None:
            cmd+= " {}".format(mac_auth['primary_method'])
            if mac_auth['backup_method1'] is not None:
                cmd+= " {}".format(mac_auth['backup_method1'])  
        command.append(cmd)

    if system is not None:
        if system['state'] == 'absent':
            cmd = "no aaa accounting system default start-stop"

        else:
            cmd = "aaa accounting system default start-stop"      
        
        if system['primary_method'] is not None:
            cmd+= " {}".format(system['primary_method'])
            if system['backup_method1'] is not None:
                cmd+= " {}".format(system['backup_method1'])
                if system['backup_method2'] is not None:
                    cmd+= " {}".format(system['backup_method2'])  
        command.append(cmd)

    if enable_console is not None:
        if system['state'] == 'absent':
            cmd = "no enable aaa console"

        else:
            cmd = "enable aaa console" 
        command.append(cmd)

    return command

def main():
    """entry point for module execution
    """
    commands_spec = dict(
        privilege_level=dict(type='int', choices=[0,4,5]),
        primary_method=dict(type='str', choices=['radius', 'tacacs+', 'none']),
        backup_method1=dict(type='str', choices=['radius', 'tacacs+', 'none']),
        backup_method2=dict(type='str', choices=['none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    dot1x_spec = dict(
        primary_method=dict(type='str', choices=['radius','none']),
        backup_method1=dict(type='str', choices=['none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    exec_spec = dict(
        primary_method=dict(type='str', choices=['radius', 'tacacs+', 'none']),
        backup_method1=dict(type='str', choices=['radius', 'tacacs+', 'none']),
        backup_method2=dict(type='str', choices=['none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    mac_auth_spec = dict(
        primary_method=dict(type='str', choices=['radius','none']),
        backup_method1=dict(type='str', choices=['none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    system_spec = dict(
        primary_method=dict(type='str', choices=['radius', 'tacacs+', 'none']),
        backup_method1=dict(type='str', choices=['radius', 'tacacs+', 'none']),
        backup_method2=dict(type='str', choices=['none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    enable_spec = dict(
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    argument_spec = dict(
        commands = dict(type='dict', options=commands_spec),
        dot1x = dict(type='dict', options=dot1x_spec),
        exec_ = dict(type='dict', options=exec_spec),
        mac_auth = dict(type='dict', options=mac_auth_spec),
        system = dict(type='dict', options=system_spec),
        enable_console = dict(type='dict', options=enable_spec),
    )

    required_one_of = [['commands', 'dot1x', 'exec_', 'mac_auth', 'system']]
    module = AnsibleModule(argument_spec=argument_spec,
                           required_one_of=required_one_of,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    commands = module.params["commands"]
    dot1x = module.params["dot1x"]
    exec_ = module.params["exec_"]
    mac_auth = module.params["mac_auth"]
    system = module.params["system"]
    enable_console = module.params["enable_console"]

    if warnings:
        result['warnings'] = warnings

    commands = [build_command(module, commands, dot1x, exec_, mac_auth, system, enable_console )]
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            for cmd in results['commands']:
                response = load_config(module, cmd)
        results['changed'] = True

    module.exit_json(**results)

if __name__ == '__main__':
    main()
