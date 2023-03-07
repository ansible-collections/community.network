# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''

options:
    nsip:
        description:
            - The ip address of the netscaler appliance where the nitro API calls will be made.
            - "The port can be specified with the colon (:). E.g. 192.168.1.1:555."
        type: str
        required: true

    nitro_user:
        description:
            - The username with which to authenticate to the netscaler node.
        type: str
        required: true

    nitro_pass:
        description:
            - The password with which to authenticate to the netscaler node.
        type: str
        required: true

    nitro_protocol:
        description:
            - Which protocol to use when accessing the nitro API objects.
        type: str
        choices: [ http, https ]
        default: http

    validate_certs:
        description:
            - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
        type: bool
        default: true

    nitro_timeout:
        description:
            - Time in seconds until a timeout error is thrown when establishing a new session with Netscaler
        type: float
        default: 310

    state:
        description:
            - The state of the resource being configured by the module on the netscaler node.
            - When present the resource will be created if needed and configured according to the module's parameters.
            - When absent the resource will be deleted from the netscaler node.
        type: str
        choices: [ absent, present ]
        default: present

    save_config:
        description:
            - If C(yes) the module will save the configuration on the netscaler node if it makes any changes.
            - The module will not save the configuration on the netscaler node if it made no changes.
        type: bool
        default: true
notes:
  - For more information on using Ansible to manage Citrix NetScaler Network devices see U(https://www.ansible.com/ansible-netscaler).
'''
