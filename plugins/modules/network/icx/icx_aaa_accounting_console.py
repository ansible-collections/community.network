from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
---
module: icx_aaa_accounting_console
version_added: "2.10"
author: "Ruckus Wireless (@Commscope)"
short_description: Configures AAA accounting in Ruckus ICX 8000 series switches
description:
  - Configures AAA accounting in Ruckus ICX 7000 series switches.
notes:
  - Tested against ICX 10.1
options:
    commands:
      description: Configures the AAA accounting configuration parameters for EXEC commands.
      suboptions:
        privilege_level:
          description: Configures the device to perform AAA accounting for the commands available at the specified privilege level. Valid values are 0
(Super User level - all commands), 4 (Port Configuration level - port-config and read-only commands), and 5 (Read Only level -
read-only commands)
          type: int
        primary_method:
          description: primary accounting method.
          type: string
        backup_method1:
          description: backup accounting method if primary method fails.
          type: string
        backup_method2:
          description: bacup accounting method if primary and backup1 metthods fail.
          type: string
        state:
          description: Specifies whether to configure or remove rate limiting.
          type: str
          default: present
          choices: ['present', 'absent']
    dot1x:
      description: Enables 802.1X accounting.
      suboptions:
        primary_method:
          description: primary accounting method.
          type: string
        backup_method1:
          description: backup accounting method if primary method fails.
          type: string
        state:
          description: Specifies whether to configure or remove rate limiting.
          type: str
          default: present
          choices: ['present', 'absent']
    exec:
      description: Configures the AAA accounting configuration parameters for SSH and Telnet access.
      suboptions:
        primary_method:
          description: primary accounting method.
          type: string
        backup_method1:
          description: backup accounting method if primary method fails.
          type: string
        backup_method2:
          description: bacup accounting method if primary and backup1 metthods fail.
          type: string
        state:
          description: Specifies whether to configure or remove rate limiting.
          type: str
          default: present
          choices: ['present', 'absent']
    mac_auth:
      description: Enables or disables RADIUS accounting for MAC authentication sessions..
      suboptions:
        primary_method:
          description: primary accounting method.
          type: string
        backup_method1:
          description: backup accounting method if primary method fails.
          type: string
        state:
          description: Specifies whether to configure or remove rate limiting.
          type: str
          default: present
          choices: ['present', 'absent']
    system:
      description: Configures AAA accounting to record when system events occur on the device.
      suboptions:
        primary_method:
          description: primary accounting method.
          type: string
        backup_method1:
          description: backup accounting method if primary method fails.
          type: string
        backup_method2:
          description: bacup accounting method if primary and backup1 metthods fail.
          type: string
        state:
          description: Specifies whether to configure or remove rate limiting.
          type: str
          default: present
          choices: ['present', 'absent']
    enable_console:
        description: Enables AAA support for commands entered at the console.
        sub_options:
          state:
            description: Specifies whether to configure or remove rate limiting.
            type: str
            default: present
            choices: ['present', 'absent']
    check_running_config:
      description: Check running configuration. This can be set as environment variable.
       Module will use environment variable value(default:False), unless it is overridden, by specifying it as module parameter.
     type: bool
     default: no      
"""
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError
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

        if commands['primary_method'] in ['radius', 'tacacs+', 'none']:
            cmd+= " {}".format(commands['primary_method'])
            if commands['backup_method1'] in ['radius', 'tacacs+', 'none'] and commands['primary_method']!= 'none':
                cmd+= " {}".format(commands['backup_method1'])
                if commands['backup_method2'] in ['radius', 'tacacs+', 'none'] and commands['backup_method1']!= 'none':
                    cmd+= " {}".format(commands['backup_method2'])
                elif commands['backup_method2'] is not None:
                    module.fail_json(msg="Invalid input -> {}".format(commands['backup_method2']))
            elif commands['backup_method1'] is not None:
                module.fail_json(msg="Invalid input -> {}".format(commands['backup_method1']))
        elif commands['primary_method'] is not None:
            module.fail_json(msg="Invalid input -> {}".format(commands['primary_method']))

        if commands['primary_method'] == commands['backup_method1'] or commands['primary_method'] == commands['backup_method2'] or commands['backup_method1'] == commands['backup_method2']:
            if commands['backup_method1'] is not None and commands['backup_method2'] is not None:
                module.fail_json(msg="Incomplete command.")
        command.append(cmd)

    if dot1x is not None:
        if dot1x['state'] == 'absent':
            cmd = "no aaa accounting dot1x default start-stop"      

        else:
            cmd = "aaa accounting dot1x default start-stop"   

        if dot1x['primary_method'] in ['radius', 'none']:
            cmd+= " {}".format(dot1x['primary_method'])
            if dot1x['backup_method1'] in ['radius', 'none'] and dot1x['primary_method']!='none':
                cmd+= " {}".format(dot1x['backup_method1'])
            elif dot1x['backup_method1'] is not None:
                module.fail_json(msg="Invalid input -> {}".format(dot1x['backup_method1']))
        elif dot1x['primary_method'] is not None:
            module.fail_json(msg="Invalid input -> {}".format(dot1x['primary_method']))

        if dot1x['primary_method'] == dot1x['backup_method1']:
            module.fail_json(msg="Incomplete command.")
        command.append(cmd)

    if exec_ is not None:
        if exec_['state'] == 'absent':
            cmd = "no aaa accounting exec default start-stop"

        else:
            cmd = "aaa accounting exec default start-stop"      

        if exec_['primary_method'] in ['radius', 'tacacs+', 'none']:
            cmd+= " {}".format(exec_['primary_method'])
            if exec_['backup_method1'] in ['radius', 'tacacs+', 'none'] and exec_['primary_method']!= 'none':
                cmd+= " {}".format(exec_['backup_method1'])
                if exec_['backup_method2'] in ['radius', 'tacacs+', 'none'] and exec_['backup_method1']!= 'none':
                    cmd+= " {}".format(exec_['backup_method2'])
                elif exec_['backup_method2'] is not None:
                    module.fail_json(msg="Invalid input -> {}".format(exec_['backup_method2']))
            elif exec_['backup_method1'] is not None:
                module.fail_json(msg="Invalid input -> {}".format(exec_['backup_method1']))
        elif exec_['primary_method'] is not None:
            module.fail_json(msg="Invalid input -> {}".format(exec_['primary_method']))

        if exec_['primary_method'] == exec_['backup_method1'] or exec_['primary_method'] == exec_['backup_method2'] or exec_['backup_method1'] == exec_['backup_method2']:
            if exec_['backup_method1'] is not None and exec_['backup_method2'] is not None:
                module.fail_json(msg="Incomplete command.")
        command.append(cmd)

    if mac_auth is not None:
        if mac_auth['state'] == 'absent':
            cmd = "no aaa accounting mac-auth default start-stop"      

        else:
            cmd = "aaa accounting mac-auth default start-stop"   

        if mac_auth['primary_method'] in ['radius', 'none']:
            cmd+= " {}".format(mac_auth['primary_method'])
            if mac_auth['backup_method1'] in ['radius', 'none'] and mac_auth['primary_method']!='none':
                cmd+= " {}".format(mac_auth['backup_method1'])  
            elif mac_auth['backup_method1'] is not None:
                module.fail_json(msg="Invalid input -> {}".format(mac_auth['backup_method1']))
        elif mac_auth['primary_method'] is not None:
            module.fail_json(msg="Invalid input -> {}".format(mac_auth['primary_method']))
            
        if mac_auth['primary_method'] == mac_auth['backup_method1']:
            module.fail_json(msg="Incomplete command.")
        command.append(cmd)

    if system is not None:
        if system['state'] == 'absent':
            cmd = "no aaa accounting system default start-stop"

        else:
            cmd = "aaa accounting system default start-stop"      
        
        if system['primary_method'] in ['radius', 'tacacs+', 'none']:
            cmd+= " {}".format(system['primary_method'])
            if system['backup_method1'] in ['radius', 'tacacs+', 'none'] and system['primary_method']!='none':
                cmd+= " {}".format(system['backup_method1'])
                if system['backup_method2'] in ['radius', 'tacacs+', 'none'] and system['backup_method1']!='none':
                    cmd+= " {}".format(system['backup_method2'])  
                elif system['backup_method2'] is not None:
                    module.fail_json(msg="Invalid input -> {}".format(system['backup_method2']))
            elif system['backup_method1'] is not None:
                module.fail_json(msg="Invalid input -> {}".format(system['backup_method1']))
        elif system['primary_method'] is not None:
            module.fail_json(msg="Invalid input -> {}".format(system['primary_method']))

        if system['primary_method'] == system['backup_method1'] or system['primary_method'] == system['backup_method2'] or system['backup_method1'] == system['backup_method2']:
            if system['backup_method1'] is not None and system['backup_method2'] is not None:
                module.fail_json(msg="Incomplete command.")
        command.append(cmd)

    if enable_console is not None:
        if system['state'] == 'absent':
            cmd = "no enable aaa console"

        else:
            cmd = "enable aaa console" 
        command.append(cmd)

    return command

def validate_previlege_level(module, commands):
    """
    This function is used to validate whether the previlege_level values if given is as expected.
    """
    if commands and (commands['privilege_level']) not in [0,4,5]:
        module.fail_json(msg="Invalid command level {}".format(commands['privilege_level']))

def main():
    """entry point for module execution
    """
    commands_spec = dict(
        privilege_level=dict(type='int'),
        primary_method=dict(type='str'),
        backup_method1=dict(type='str'),
        backup_method2=dict(type='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    dot1x_spec = dict(
        primary_method=dict(type='str'),
        backup_method1=dict(type='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    exec_spec = dict(
        primary_method=dict(type='str'),
        backup_method1=dict(type='str'),
        backup_method2=dict(type='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    mac_auth_spec = dict(
        primary_method=dict(type='str'),
        backup_method1=dict(type='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    system_spec = dict(
        primary_method=dict(type='str'),
        backup_method1=dict(type='str'),
        backup_method2=dict(type='str'),
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
        #check_running_config = dict(default=False, type='bool', fallback=(env_fallback, ['ANSIBLE_CHECK_ICX_RUNNING_CONFIG']))
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

    validate_previlege_level(module, commands)
    commands = [build_command(module, commands, dot1x, exec_, mac_auth, system, enable_console )]
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            for i in results['commands']:
                response = load_config(module, i)
        results['changed'] = True

    module.exit_json(**results)

if __name__ == '__main__':
    main()
