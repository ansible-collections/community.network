#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2016-2018, Cumulus Networks <ce-ceng@cumulusnetworks.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: nclu
author: "Cumulus Networks (@isharacomix)"
short_description: Configure network interfaces using NCLU
description:
    - Interface to the Network Command Line Utility, developed to make it easier
      to configure operating systems running ifupdown2 and Quagga, such as
      Cumulus Linux. Command documentation is available at
      U(https://docs.cumulusnetworks.com/cumulus-linux/System-Configuration/Network-Command-Line-Utility-NCLU/)
options:
    commands:
        description:
            - A list of strings containing the net commands to run. Mutually
              exclusive with I(template).
    template:
        description:
            - A single, multi-line string with jinja2 formatting. This string
              will be broken by lines, and each line will be run through net.
              Mutually exclusive with I(commands).
    commit:
        description:
            - When true, performs a 'net commit' at the end of the block.
              Mutually exclusive with I(atomic).
        default: false
        type: bool
    abort:
        description:
            - Boolean. When true, perform a 'net abort' before the block.
              This cleans out any uncommitted changes in the buffer.
              Mutually exclusive with I(atomic).
        default: false
        type: bool
    atomic:
        description:
            - When true, equivalent to both I(commit) and I(abort) being true.
              Mutually exclusive with I(commit) and I(atomic).
        default: false
        type: bool
    description:
        description:
            - Commit description that will be recorded to the commit log if
              I(commit) or I(atomic) are true.
        default: "Ansible-originated commit"
notes:
    - Supports check_mode. Note that when using check_mode, I(abort) is always true.
'''

EXAMPLES = '''

- name: Add two interfaces without committing any changes
  community.network.nclu:
    commands:
        - add int swp1
        - add int swp2

- name: Modify hostname to Cumulus-1 and commit the change
  community.network.nclu:
    commands:
        - add hostname Cumulus-1
    commit: true

- name: Add 48 interfaces and commit the change.
  community.network.nclu:
    template: |
        {% for iface in range(1,49) %}
        add int swp{{iface}}
        {% endfor %}
    commit: true
    description: "Ansible - add swps1-48"

- name: Fetch Status Of Interface
  community.network.nclu:
    commands:
        - show interface swp1
  register: output

- name: Print Status Of Interface
  ansible.builtin.debug:
    var: output

- name: Fetch Details From All Interfaces In JSON Format
  community.network.nclu:
    commands:
        - show interface json
  register: output

- name: Print Interface Details
  ansible.builtin.debug:
    var: output["msg"]

- name: Atomically add an interface
  community.network.nclu:
    commands:
        - add int swp1
    atomic: true
    description: "Ansible - add swp1"

- name: Remove IP address from interface swp1
  community.network.nclu:
    commands:
        - del int swp1 ip address 1.1.1.1/24

- name: Configure BGP AS and add 2 EBGP neighbors using BGP Unnumbered
  community.network.nclu:
    commands:
        - add bgp autonomous-system 65000
        - add bgp neighbor swp51 interface remote-as external
        - add bgp neighbor swp52 interface remote-as external
    commit: true

- name: Configure BGP AS and Add 2 EBGP neighbors Using BGP Unnumbered via Template
  community.network.nclu:
    template: |
      {% for neighbor in range(51,53) %}
      add bgp neighbor swp{{neighbor}} interface remote-as external
      add bgp autonomous-system 65000
      {% endfor %}
    atomic: true

- name: Check BGP Status
  community.network.nclu:
    commands:
        - show bgp summary json
  register: output

- name: Print BGP Status In JSON
  ansible.builtin.debug:
    var: output["msg"]
'''

RETURN = '''
changed:
    description: whether the interface was changed
    returned: changed
    type: bool
    sample: true
msg:
    description: human-readable report of success or failure
    returned: always
    type: str
    sample: "interface bond0 config updated"
'''

import re
from ansible.module_utils.basic import AnsibleModule


def command_helper(module, command, errmsg=None):
    """Run a command, catch any nclu errors"""
    (_rc, output, _err) = module.run_command("/usr/bin/net %s" % command)
    if _rc or 'ERROR' in output or 'ERROR' in _err:
        module.fail_json(msg=errmsg or output)
    return str(output)


def check_pending(module):
    """Check the pending diff of the nclu buffer."""
    pending = command_helper(module, "pending", "Error in pending config. You may want to view `net pending` on this target.")

    delimeter1 = re.compile('''net add/del commands since the last ['"]net commit['"]''')
    color1 = '\x1b[94m'
    if re.search(delimeter1, pending):
        pending = re.split(delimeter1, pending)[0]
        pending = pending.replace(color1, '')
    return pending.strip()


def run_nclu(module, command_list, command_string, commit, atomic, abort, description):
    _changed = False

    commands = []
    if command_list:
        commands = command_list
    elif command_string:
        commands = command_string.splitlines()

    do_commit = False
    do_abort = abort
    if commit or atomic:
        do_commit = True
        if atomic:
            do_abort = True

    if do_abort:
        command_helper(module, "abort")

    # First, look at the staged commands.
    before = check_pending(module)
    # Run all of the net commands
    output_lines = []
    for line in commands:
        if line.strip():
            output_lines += [command_helper(module, line.strip(), "Failed on line %s" % line)]
    output = "\n".join(output_lines)

    # If pending changes changed, report a change.
    diff = {}
    after = check_pending(module)
    if before == after:
        _changed = False
    else:
        _changed = True
        diff = {"prepared": after}

    if module.check_mode:
        command_helper(module, "abort")

    # Do the commit.
    if (do_commit and _changed and not module.check_mode):
        result = command_helper(module, "commit description '%s'" % description)
        if "commit ignored" in result:
            _changed = False
            command_helper(module, "abort")
        elif command_helper(module, "show commit last") == "":
            _changed = False
    elif do_abort:
        command_helper(module, "abort")

    return _changed, output, diff


def main(testing=False):
    module = AnsibleModule(argument_spec=dict(
        commands=dict(required=False, type='list'),
        template=dict(required=False, type='str'),
        description=dict(required=False, type='str', default="Ansible-originated commit"),
        abort=dict(required=False, type='bool', default=False),
        commit=dict(required=False, type='bool', default=False),
        atomic=dict(required=False, type='bool', default=False)),
        supports_check_mode=True,
        mutually_exclusive=[('commands', 'template'),
                            ('commit', 'atomic'),
                            ('abort', 'atomic')]
    )
    command_list = module.params.get('commands', None)
    command_string = module.params.get('template', None)
    commit = module.params.get('commit')
    atomic = module.params.get('atomic')
    abort = module.params.get('abort')
    description = module.params.get('description')

    if module.check_mode:
        commit = False

    _changed, output, diff = run_nclu(module, command_list, command_string, commit, atomic, abort, description)
    result = {
        "changed": _changed,
        "msg": output,
        "diff": diff
    }

    if not testing:
        module.exit_json(**result)
    elif testing:
        return {"changed": _changed, "msg": output}


if __name__ == '__main__':
    main()
