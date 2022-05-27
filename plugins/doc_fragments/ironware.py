# -*- coding: utf-8 -*-

# Copyright: (c) 2017, Paul Baker <@paulquack>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):

    # Standard files documentation fragment
    DOCUMENTATION = r'''
options:
  authorize:
    description:
      - B(Deprecated)
      - "Starting with Ansible 2.7 we recommend using C(connection: network_cli) and C(become: yes)."
      - For more information please see the L(IronWare Platform Options guide, ../network/user_guide/platform_ironware.html).
      - HORIZONTALLINE
      - Instructs the module to enter privileged mode on the remote device
        before sending any commands.  If not specified, the device will
        attempt to execute all commands in non-privileged mode. If the value
        is not specified in the task, the value of environment variable
        C(ANSIBLE_NET_AUTHORIZE) will be used instead.
    type: bool
    default: no
notes:
  - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
'''
