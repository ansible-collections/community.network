# (C) 2017 Red Hat Inc.
# Copyright (C) 2017 Lenovo.
#
# GNU General Public License v3.0+
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Contains Action Plugin methods for ENOS Config Module
# Lenovo Networking
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import copy

from ansible import constants as C
from ansible_collections.ansible.netcommon.plugins.action.network import ActionModule as ActionNetworkModule
from ansible_collections.community.network.plugins.module_utils.network.enos.enos import enos_provider_spec
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import load_provider
from ansible.utils.display import Display

display = Display()


class ActionModule(ActionNetworkModule):

    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        module_name = self._task.action.split('.')[-1]
        self._config_module = True if module_name == 'enos_config' else False
        persistent_connection = self._play_context.connection.split('.')[-1]

        if persistent_connection == 'network_cli':
            provider = self._task.args.get('provider', {})
            if any(provider.values()):
                display.warning('provider is unnecessary when using network_cli and will be ignored')
                del self._task.args['provider']
        elif self._play_context.connection == 'local':
            return {
                'failed': True,
                'msg': "connection local support for this module has been removed use either 'network_cli' or 'ansible.netcommon.network_cli' connection"
            }

        result = super(ActionModule, self).run(task_vars=task_vars)
        return result
