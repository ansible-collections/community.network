#!/usr/bin/python
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

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community"
}

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community"
}

DOCUMENTATION = '''
---
module: fmgr_adom
notes:
    - Full Documentation at U(https://ftnt-ansible-docs.readthedocs.io/en/latest/).
author:
    - Peter McDonald (@petermcd)
short_description: Add or remove adom from FortiManager.
description:
  - Add or remove an adom from FortiManager using JSON RPC API.

options:
  adom:
    description:
      - The ADOM to be added or removed.
    required: true
    type: str

  mode:
    description:
      - The desired mode of the specified object.
    required: false
    default: add
    choices: ["add", "delete"]
    type: str

  desc:
    description:
      - Description of the adom
    required: false
    default: ""
    type: str

  log_db_retention_hours:
    description:
      - Log retention hours
    required: false
    default: 1440
    type: int

  log_disk_quota:
    description:
      - Log disk quota
    required: false
    default: 0
    type: int

  log_disk_quota_alert_thres:
    description:
      - Disk quota alert threshold
    required: false
    default: 90
    type: int

  log_disk_quota_split_ratio:
    description:
      - Ratio for split between logs and archived logs
    required: false
    default: 70
    type: int

  log_file_retention_hours:
    description:
      - Log file retention period in hours
    required: false
    default: 8760
    type: int

  mig_mr:
    description:
      - Mig minor release
    required: false
    default: 2
    type: int

  mig_os_ver:
    description:
      - Mig major operating system version
    required: false
    default: "6.0"
    choices: ["unknown", "0.0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0"]
    type: str

  management_mode:
    description:
      - Mode
    required: false
    default: "gms"
    choices: ["ems", "gms", "provider"]
    type: str

  minor_release:
    description:
      - Minor release
    required: false
    default: 2
    type: int

  os_ver:
    description:
      - Major operating system version
    required: false
    default: "6.0"
    choices: ["unknown", "0.0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0"]
    type: str

  state:
    description:
      - Adom state, Disabled = 0, Enabled = 1
    required: false
    default: 1
    type: int
'''

EXAMPLES = '''
- name: Create a new ADOM
  fmgr_adom:
    adom: "Adom1"
    desc: "Adom used for testing"
    mode: "add"
    log_db_retention_hours: 100

- name: Create a new ADOM specifying some parameters
  fmgr_adom:
    adom: "Adom1"
    mode: "add"

- name: Delete an existing ADOM
  fmgr_adom:
    adom: "Adom1"
    mode: "delete"
'''

RETURN = """
api_result:
  description: full API response, includes status code and message
  returned: always
  type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortios.plugins.module_utils.fortimanager.fortimanager import FortiManagerHandler
from ansible_collections.fortinet.fortios.plugins.module_utils.fortimanager.common import FMGBaseException
from ansible_collections.fortinet.fortios.plugins.module_utils.fortimanager.common import FMGRCommon
from ansible_collections.fortinet.fortios.plugins.module_utils.fortimanager.common import FMGRMethods
from ansible_collections.fortinet.fortios.plugins.module_utils.fortimanager.common import DEFAULT_RESULT_OBJ
from ansible_collections.fortinet.fortios.plugins.module_utils.fortimanager.common import FAIL_SOCKET_MSG


def add_adom(fmgr, paramgram):
    """
    This method is used to add adoms to the FMGR

    :param fmgr: The fmgr object instance from fmgr_utils.py
    :type fmgr: class object
    :param paramgram: The formatted dictionary of options to process
    :type paramgram: dict

    :return: The response from the FortiManager
    :rtype: dict
    """

    datagram = {
        "desc": paramgram["desc"],
        "log_db_retention_hours": paramgram["log_db_retention_hours"],
        "log_disk_quota": paramgram["log_disk_quota"],
        "log_disk_quota_alert_thres": paramgram["log_disk_quota_alert_thres"],
        "log_disk_quota_split_ratio": paramgram["log_disk_quota_split_ratio"],
        "log_file_retention_hours": paramgram["log_file_retention_hours"],
        "mig_mr": paramgram["mig_mr"],
        "mig_os_ver": paramgram["mig_os_ver"],
        "mode": paramgram["management_mode"],
        "mr": paramgram["minor_release"],
        "os_ver": paramgram["os_ver"],
        "state": paramgram["state"],
        "name": paramgram["adom"]
    }

    url = '/dvmdb/adom/'
    response = fmgr.process_request(url, datagram, FMGRMethods.ADD)
    return response


def delete_adom(fmgr, paramgram):
    """
    This method deletes an adom from the FMGR

    :param fmgr: The fmgr object instance from fmgr_utils.py
    :type fmgr: class object
    :param paramgram: The formatted dictionary of options to process
    :type paramgram: dict

    :return: The response from the FortiManager
    :rtype: dict
    """
    url = '/dvmdb/adom/{adom}'.format(adom=paramgram["adom"])
    datagram = {
        "name": paramgram["adom"]
    }
    response = fmgr.process_request(url, datagram, FMGRMethods.DELETE)
    return response


def main():
    argument_spec = dict(
        adom=dict(required=True, type="str"),
        mode=dict(choices=["add", "delete"], type="str", default="add"),
        desc=dict(type="str", default=""),
        log_db_retention_hours=dict(type="int", default=1440),
        log_disk_quota=dict(type="int", default=0),
        log_disk_quota_alert_thres=dict(type="int", default=90),
        log_disk_quota_split_ratio=dict(type="int", default=70),
        log_file_retention_hours=dict(type="int", default=8760),
        mig_mr=dict(type="int", default=2),
        mig_os_ver=dict(choices=["unknown", "0.0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0"], type="str", default="6.0"),
        management_mode=dict(choices=["ems", "gms", "provider"], type="str", default="gms"),
        minor_release=dict(type="int", default=2),
        os_ver=dict(choices=["unknown", "0.0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0"], type="str", default="6.0"),
        state=dict(type="int", default=1)
    )

    # BUILD MODULE OBJECT SO WE CAN BUILD THE PARAMGRAM
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False, )

    # BUILD THE PARAMGRAM
    paramgram = {
        "adom": module.params["adom"],
        "mode": module.params["mode"],
        "desc": module.params["desc"],
        "log_db_retention_hours": module.params["log_db_retention_hours"],
        "log_disk_quota": module.params["log_disk_quota"],
        "log_disk_quota_alert_thres": module.params["log_disk_quota_alert_thres"],
        "log_disk_quota_split_ratio": module.params["log_disk_quota_split_ratio"],
        "log_file_retention_hours": module.params["log_file_retention_hours"],
        "mig_mr": module.params["mig_mr"],
        "mig_os_ver": module.params["mig_os_ver"],
        "management_mode": module.params["management_mode"],
        "minor_release": module.params["minor_release"],
        "os_ver": module.params["os_ver"],
        "state": module.params["state"]
    }

    # INSERT THE PARAMGRAM INTO THE MODULE SO WHEN WE PASS IT TO MOD_UTILS.FortiManagerHandler IT HAS THAT INFO
    module.paramgram = paramgram

    # TRY TO INIT THE CONNECTION SOCKET PATH AND FortiManagerHandler OBJECT AND TOOLS
    fmgr = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        fmgr = FortiManagerHandler(connection, module)
        fmgr.tools = FMGRCommon()
    else:
        module.fail_json(**FAIL_SOCKET_MSG)

    # BEGIN MODULE-SPECIFIC LOGIC -- THINGS NEED TO HAPPEN DEPENDING ON THE ENDPOINT AND OPERATION
    results = DEFAULT_RESULT_OBJ
    try:
        if paramgram["mode"] == "add":
            results = add_adom(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results,
                                 ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))

        if paramgram["mode"] == "delete":
            results = delete_adom(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results,
                                 ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))

    except Exception as err:
        raise FMGBaseException(err)

    return module.exit_json(**results[1])


if __name__ == "__main__":
    main()
