# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Copyright (c) 2020 Ernst Oudhof, ernst@mailfrom.nl
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from os import path
import json

from mock import MagicMock, call

from ansible_collections.community.network.tests.unit.compat import unittest
from ansible_collections.community.network.plugins.cliconf import weos4

FIXTURE_DIR = b'%s/fixtures/weos4' % (
    path.dirname(path.abspath(__file__)).encode('utf-8')
)


def _connection_side_effect(*args, **kwargs):
    try:
        if args:
            value = args[0]
        else:
            value = kwargs.get('command')

        fixture_path = path.abspath(
            b'%s/%s' % (FIXTURE_DIR, b'_'.join(value.split(b' ')))
        )
        with open(fixture_path, 'rb') as file_desc:
            return file_desc.read()
    except (OSError, IOError):
        if args:
            value = args[0]
            return value
        elif kwargs.get('command'):
            value = kwargs.get('command')
            return value

        return 'Nope'


class TestPluginCLIConfWEOS4(unittest.TestCase):
    """ Test class for WeOS4 CLI Conf Methods
    """
    def setUp(self):
        self._mock_connection = MagicMock()
        self._mock_connection.send.side_effect = _connection_side_effect
        self._cliconf = weos4.Cliconf(self._mock_connection)
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_get_device_info(self):
        """ Test get_device_info
        """
        device_info = self._cliconf.get_device_info()

        mock_device_info = {
            'network_os': 'weos4',
            'network_os_hostname': 'weos4-router',
            'network_os_model': 'DDW-226',
            'network_os_version': '4.21.2',
        }

        self.assertEqual(device_info, mock_device_info)

    def test_get_config(self):
        """ Test get_config
        """
        running_config = self._cliconf.get_config()

        fixture_path = path.abspath(b'%s/show_running-config' % FIXTURE_DIR)
        with open(fixture_path, 'rb') as file_desc:
            mock_running_config = file_desc.read()
            self.assertEqual(running_config, mock_running_config)

    def test_get_diff(self):
        """ Test diff_config
        """
        test_diff_candidate = b'ip\n\tfirewall\n\t\tenable'
        mock_diff = {
            'config_diff': 'ip\nfirewall\nenable\nend\nend',
        }

        diff = self._cliconf.get_diff(test_diff_candidate)

        self.assertEqual(diff, mock_diff)

    def test_edit_config(self):
        """ Test edit_config
        """
        test_config_command = b'ip\nfirewall\nenable\nend\nend'

        self._cliconf.edit_config(test_config_command)

        send_calls = []

        for command in [b'configure terminal', test_config_command, b'leave']:
            send_calls.append(call(
                command=command,
                prompt_retry_check=False,
                sendonly=False,
                newline=True,
                check_all=False
            ))

        self._mock_connection.send.assert_has_calls(send_calls)

    def test_get_capabilities(self):
        """ Test get_capabilities
        """
        capabilities = json.loads(self._cliconf.get_capabilities())
        mock_capabilities = {
            'network_api': 'cliconf',
            'rpc': [
                'get_config',
                'edit_config',
                'get_capabilities',
                'get',
                'enable_response_logging',
                'disable_response_logging',
                'get_diff',
                'run_commands',
            ],
            'device_info': {
                'network_os': 'weos4',
                'network_os_hostname': 'weos4-router',
                'network_os_model': 'DDW-226',
                'network_os_version': '4.21.2',
            },
            'device_operations': {
                'supports_commit': False,
                'supports_commit_comment': False,
                'supports_defaults': False,
                'supports_diff_ignore_lines': True,
                'supports_diff_match': True,
                'supports_diff_replace': True,
                'supports_generate_diff': True,
                'supports_multiline_delimiter': False,
                'supports_onbox_diff': False,
                'supports_replace': True,
                'supports_rollback': False,
            },
            'diff_match': [
                'line',
                'strict',
                'exact',
                'none',
            ],
            'diff_replace': [
                'line',
                'block',
                'config',
            ],
            'format': [
                'text',
            ],
            'output': [
            ],

        }

        self.assertEqual(
            mock_capabilities,
            capabilities
        )
