#!/usr/bin/python
#
# @author: Gaurav Rastogi (grastogi@avinetworks.com)
#          Eric Anderson (eanderson@avinetworks.com)
# module_check: supported
#
# Copyright: (c) 2017 Gaurav Rastogi, <grastogi@avinetworks.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: avi_poolgroupdeploymentpolicy
deprecated:
  removed_in: 6.0.0
  why: This collection and all content in it is unmaintained and deprecated.
  alternative: Unknown.
author: Gaurav Rastogi (@grastogi23) <grastogi@avinetworks.com>

short_description: Module for setup of PoolGroupDeploymentPolicy Avi RESTful Object
description:
    - This module is used to configure PoolGroupDeploymentPolicy object
    - more examples at U(https://github.com/avinetworks/devops)
requirements: [ avisdk ]
options:
    state:
        description:
            - The state that should be applied on the entity.
        default: present
        choices: ["absent", "present"]
    avi_api_update_method:
        description:
            - Default method for object update is HTTP PUT.
            - Setting to patch will override that behavior to use HTTP PATCH.
        default: put
        choices: ["put", "patch"]
    avi_api_patch_op:
        description:
            - Patch operation to use when using avi_api_update_method as patch.
        choices: ["add", "replace", "delete"]
    auto_disable_old_prod_pools:
        description:
            - It will automatically disable old production pools once there is a new production candidate.
            - Default value when not specified in API or module is interpreted by Avi Controller as True.
        type: bool
    description:
        description:
            - User defined description for the object.
    evaluation_duration:
        description:
            - Duration of evaluation period for automatic deployment.
            - Allowed values are 60-86400.
            - Default value when not specified in API or module is interpreted by Avi Controller as 300.
    name:
        description:
            - The name of the pool group deployment policy.
        required: true
    rules:
        description:
            - List of pgdeploymentrule.
    scheme:
        description:
            - Deployment scheme.
            - Enum options - BLUE_GREEN, CANARY.
            - Default value when not specified in API or module is interpreted by Avi Controller as BLUE_GREEN.
    target_test_traffic_ratio:
        description:
            - Target traffic ratio before pool is made production.
            - Allowed values are 1-100.
            - Default value when not specified in API or module is interpreted by Avi Controller as 100.
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    test_traffic_ratio_rampup:
        description:
            - Ratio of the traffic that is sent to the pool under test.
            - Test ratio of 100 means blue green.
            - Allowed values are 1-100.
            - Default value when not specified in API or module is interpreted by Avi Controller as 100.
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Uuid of the pool group deployment policy.
    webhook_ref:
        description:
            - Webhook configured with url that avi controller will pass back information about pool group, old and new pool information and current deployment
            - rule results.
            - It is a reference to an object of type webhook.
            - Field introduced in 17.1.1.
extends_documentation_fragment:
- community.network.avi

'''

EXAMPLES = """
- name: Example to create PoolGroupDeploymentPolicy object
  community.network.avi_poolgroupdeploymentpolicy:
    controller: 10.10.25.42
    username: admin
    password: something
    state: present
    name: sample_poolgroupdeploymentpolicy
"""

RETURN = '''
obj:
    description: PoolGroupDeploymentPolicy (api/poolgroupdeploymentpolicy) object
    returned: success, changed
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.community.network.plugins.module_utils.network.avi.avi import (
        avi_common_argument_spec, avi_ansible_api, HAS_AVI)
except ImportError:
    HAS_AVI = False


def main():
    argument_specs = dict(
        state=dict(default='present',
                   choices=['absent', 'present']),
        avi_api_update_method=dict(default='put',
                                   choices=['put', 'patch']),
        avi_api_patch_op=dict(choices=['add', 'replace', 'delete']),
        auto_disable_old_prod_pools=dict(type='bool',),
        description=dict(type='str',),
        evaluation_duration=dict(type='int',),
        name=dict(type='str', required=True),
        rules=dict(type='list',),
        scheme=dict(type='str',),
        target_test_traffic_ratio=dict(type='int',),
        tenant_ref=dict(type='str',),
        test_traffic_ratio_rampup=dict(type='int',),
        url=dict(type='str',),
        uuid=dict(type='str',),
        webhook_ref=dict(type='str',),
    )
    argument_specs.update(avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (avisdk>=17.1) or requests is not installed. '
            'For more details visit https://github.com/avinetworks/sdk.'))
    return avi_ansible_api(module, 'poolgroupdeploymentpolicy',
                           set([]))


if __name__ == '__main__':
    main()
