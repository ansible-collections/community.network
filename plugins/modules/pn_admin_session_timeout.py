#!/usr/bin/python
# Copyright: (c) 2018, Pluribus Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: pn_admin_session_timeout
deprecated:
  removed_in: 6.0.0
  why: This collection and all content in it is unmaintained and deprecated.
  alternative: Unknown.
author: "Pluribus Networks (@rajaspachipulusu17)"
short_description: CLI command to modify admin-session-timeout
description:
  - This module can be used to modify admin session timeout.
options:
  pn_cliswitch:
    description:
      - Target switch to run the CLI on.
    required: false
    type: str
  state:
    description:
      - State the action to perform.
        C(update) to modify the admin-session-timeout.
    required: true
    type: str
    choices: ['update']
  pn_timeout:
    description:
      - Maximum time to wait for user activity before
        terminating login session. Minimum should be 60s.
    required: false
    type: str
'''

EXAMPLES = """
- name: Admin session timeout functionality
  community.network.pn_admin_session_timeout:
    pn_cliswitch: "sw01"
    state: "update"
    pn_timeout: "61s"

- name: Admin session timeout functionality
  community.network.pn_admin_session_timeout:
    pn_cliswitch: "sw01"
    state: "update"
    pn_timeout: "1d"

- name: Admin session timeout functionality
  community.network.pn_admin_session_timeout:
    pn_cliswitch: "sw01"
    state: "update"
    pn_timeout: "10d20m3h15s"
"""

RETURN = """
command:
  description: the CLI command run on the target node.
  returned: always
  type: str
stdout:
  description: set of responses from the admin-session-timeout command.
  returned: always
  type: list
stderr:
  description: set of error responses from the admin-session-timeout command.
  returned: on error
  type: list
changed:
  description: indicates whether the CLI caused changes on the target.
  returned: always
  type: bool
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.network.plugins.module_utils.network.netvisor.pn_nvos import pn_cli, run_cli


def main():
    """ This section is for arguments parsing """

    state_map = dict(
        update='admin-session-timeout-modify'
    )

    module = AnsibleModule(
        argument_spec=dict(
            pn_cliswitch=dict(required=False, type='str'),
            state=dict(required=True, type='str',
                       choices=state_map.keys()),
            pn_timeout=dict(required=False, type='str'),
        ),
        required_together=[['state', 'pn_timeout']],
    )

    # Accessing the arguments
    cliswitch = module.params['pn_cliswitch']
    state = module.params['state']
    timeout = module.params['pn_timeout']

    command = state_map[state]

    # Building the CLI command string
    cli = pn_cli(module, cliswitch)
    if command == 'admin-session-timeout-modify':
        cli += ' %s ' % command
        if timeout:
            cli += ' timeout ' + timeout

    run_cli(module, cli, state_map)


if __name__ == '__main__':
    main()
