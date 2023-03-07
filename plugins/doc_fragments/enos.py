# -*- coding: utf-8 -*-

# Copyright: (c) 2017, Red Hat Inc.
# Copyright: (c) 2017, Lenovo.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):

    # Standard files documentation fragment
    DOCUMENTATION = r'''
options:
  authorize:
    description:
      - Instructs the module to enter privileged mode on the remote device
        before sending any commands.  If not specified, the device will
        attempt to execute all commands in non-privileged mode. If the value
        is not specified in the task, the value of environment variable
        C(ANSIBLE_NET_AUTHORIZE) will be used instead.
    type: bool
    default: false
  auth_pass:
    description:
      - Specifies the password to use if required to enter privileged mode
        on the remote device.  If I(authorize) is false, then this argument
        does nothing. If the value is not specified in the task, the value of
        environment variable C(ANSIBLE_NET_AUTH_PASS) will be used instead.
'''
