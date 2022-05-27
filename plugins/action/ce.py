#
# Copyright: (c) 2016, Red Hat Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import copy

from ansible import constants as C
from ansible_collections.ansible.netcommon.plugins.action.network import ActionModule as ActionNetworkModule
from ansible_collections.community.network.plugins.module_utils.network.cloudengine.ce import ce_provider_spec
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import load_provider
from ansible.utils.display import Display

display = Display()

CLI_SUPPORTED_MODULES = ['ce_rollback', 'ce_mlag_interface', 'ce_startup', 'ce_config',
                         'ce_command', 'ce_facts', 'ce_evpn_global', 'ce_evpn_bgp_rr',
                         'ce_mtu', 'ce_evpn_bgp', 'ce_snmp_location', 'ce_snmp_contact',
                         'ce_snmp_traps', 'ce_netstream_global', 'ce_netstream_aging',
                         'ce_netstream_export', 'ce_netstream_template', 'ce_ntp_auth',
                         'ce_stp', 'ce_vxlan_global', 'ce_vxlan_arp', 'ce_vxlan_gateway',
                         'ce_acl_interface']


class ActionModule(ActionNetworkModule):

    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        module_name = self._task.action.split('.')[-1]
        self._config_module = True if module_name == 'ce_config' else False
        socket_path = None
        persistent_connection = self._play_context.connection.split('.')[-1]

        if self._play_context.connection == 'local':
            return {
                'failed': True,
                'msg': "connection local support for this module has been removed use either 'network_cli' or 'ansible.netcommon.network_cli' connection"
            }

        elif persistent_connection in ('netconf', 'network_cli'):
            provider = self._task.args.get('provider', {})
            if any(provider.values()):
                display.warning('provider is unnecessary when using %s and will be ignored' % self._play_context.connection)
                del self._task.args['provider']

            if (persistent_connection == 'network_cli' and module_name not in CLI_SUPPORTED_MODULES) or \
                    (persistent_connection == 'netconf' and module_name in CLI_SUPPORTED_MODULES):
                return {'failed': True, 'msg': "Connection type '%s' is not valid for '%s' module."
                        % (self._play_context.connection, self._task.action)}

        result = super(ActionModule, self).run(task_vars=task_vars)
        return result
