# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Copyright (c) 2020 Ernst Oudhof, ernst@mailfrom.nl
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
author: Ernst Oudhof (@ernst-s)
cliconf: weos4
short_description: Use weos4 cliconf to run commands on Westermo platform
description:
  - This weos4 plugin provides low level abstraction APIs for
    sending and receiving CLI commands from Westermo WeOS 4 network devices.
version_added: '2.2.0'
"""

import re
import json

from itertools import chain

from ansible.module_utils._text import to_text
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible.module_utils.common._collections_compat import Mapping
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import NetworkConfig
from ansible.plugins.cliconf import CliconfBase


class Cliconf(CliconfBase):

    def get_device_info(self):
        device_info = {}

        device_info['network_os'] = 'weos4'
        reply = self.get('show system-information')
        data = to_text(reply, errors='surrogate_or_strict').strip()

        match = re.search(r'Main firmware ver.\s+: (\S+)', data, re.M)
        if match:
            device_info['network_os_version'] = match.group(1)

        match = re.search(r'Model\s+: (\S+)', data, re.M)
        if match:
            device_info['network_os_model'] = match.group(1)

        match = re.search(r'System Name\s+: (\S+)', data, re.M)
        if match:
            device_info['network_os_hostname'] = match.group(1)

        return device_info

    def get_diff(self, candidate=None, running=None, diff_match='line', diff_ignore_lines=None, path=None, diff_replace='line'):
        diff = {}
        device_operations = self.get_device_operations()
        option_values = self.get_option_values()

        if candidate is None and device_operations['supports_generate_diff'] and diff_match != 'none':
            raise ValueError("candidate configuration is required to generate diff")

        if diff_match not in option_values['diff_match']:
            raise ValueError("'match' value %s in invalid, valid values are %s" % (diff_match, ', '.join(option_values['diff_match'])))

        if diff_replace not in option_values['diff_replace']:
            raise ValueError("'replace' value %s in invalid, valid values are %s" % (diff_replace, ', '.join(option_values['diff_replace'])))

        # prepare candidate configuration
        candidate_obj = NetworkConfig(indent=1)
        candidate_obj.load(candidate)

        if running and diff_match != 'none':
            # running configuration
            running_obj = NetworkConfig(indent=1, contents=running, ignore_lines=diff_ignore_lines)
            configdiffobjs = candidate_obj.difference(running_obj, path=path, match=diff_match, replace=diff_replace)
        else:
            configdiffobjs = candidate_obj.items

        if configdiffobjs and diff_replace == 'config':
            diff['config_diff'] = candidate
        elif configdiffobjs:
            configlines = list()
            for i, o in enumerate(configdiffobjs):
                configlines.append(o.text)
                if i + 1 < len(configdiffobjs):
                    levels = len(o.parents) - len(configdiffobjs[i + 1].parents)
                else:
                    levels = len(o.parents)
                if o.text == 'end':
                    levels -= 1
                if levels > 0:
                    for i in range(levels):
                        configlines.append("end")
            diff['config_diff'] = "\n".join(configlines)
        else:
            diff['config_diff'] = ''

        return diff

    def get_config(self, source='running', format='text', flags=None):
        if source not in ('running', 'startup'):
            return self.invalid_params("fetching configuration from %s is not supported" % source)
        if source == 'running':
            cmd = 'show running-config'
        else:
            cmd = 'show startup-config'
        return self.send_command(cmd)

    def edit_config(self, candidate=None, commit=True, replace=None, comment=None):
        resp = {}
        operations = self.get_device_operations()
        self.check_edit_config_capability(operations, candidate, commit, replace, comment)
        results = []
        requests = []

        if commit and replace is True:
            config = "\n".join(candidate)
            self.send_command('copy console running-config', sendonly=True)
            self.send_command(config, sendonly=True)
            results.append(self.send_command("\x04"))
            requests.append(config)
        elif commit and replace:
            candidate = 'copy {0} running-config'.format(replace)
            results.append(self.send_command(candidate))
            requests.append(candidate)
        elif commit:
            self.send_command('configure terminal')
            for line in to_list(candidate):
                if not isinstance(line, Mapping):
                    line = {'command': line}
                cmd = line['command']
                if cmd != 'leave':
                    results.append(self.send_command(**line))
                    requests.append(cmd)
            self.send_command('leave')
        else:
            raise ValueError('check mode is not supported')
        resp['request'] = requests
        resp['response'] = results
        return resp

    def get(self, command, prompt=None, answer=None, sendonly=False, newline=True, check_all=False):
        return self.send_command(command=command, prompt=prompt, answer=answer, sendonly=sendonly, newline=newline, check_all=check_all)

    def get_device_operations(self):
        return {
            'supports_diff_replace': True,
            'supports_commit': False,
            'supports_rollback': False,
            'supports_defaults': False,
            'supports_onbox_diff': False,
            'supports_commit_comment': False,
            'supports_multiline_delimiter': False,
            'supports_diff_match': True,
            'supports_diff_ignore_lines': True,
            'supports_generate_diff': True,
            'supports_replace': True
        }

    def get_option_values(self):
        return {
            'format': ['text'],
            'diff_match': ['line', 'strict', 'exact', 'none'],
            'diff_replace': ['line', 'block', 'config'],
            'output': []
        }

    def get_capabilities(self):
        result = super(Cliconf, self).get_capabilities()
        result['rpc'] += ['get_diff', 'run_commands']
        result['device_operations'] = self.get_device_operations()
        result.update(self.get_option_values())
        return json.dumps(result)
