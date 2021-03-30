# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Copyright (c) 2020 Ernst Oudhof, ernst@mailfrom.nl
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from mock import MagicMock

from ansible_collections.community.network.tests.unit.compat import unittest
from ansible_collections.community.network.plugins.terminal import weos4
from ansible.errors import AnsibleConnectionFailure


class TestPluginTerminalWEOS4(unittest.TestCase):
    """ Test class for WeOS4 Terminal Module
    """
    def setUp(self):
        self._mock_connection = MagicMock()
        self._terminal = weos4.TerminalModule(self._mock_connection)

    def test_on_open_shell(self):
        """ Test on_open_shell
        """
        self._mock_connection.exec_command.side_effect = [
            b'Looking out my window I see a brick building, and people. Cool.',
        ]
        self._terminal.on_open_shell()
        self._mock_connection.exec_command.assert_called_with(u'batch')

    def test_on_open_shell_error(self):
        """ Test on_open_shell with error
        """
        self._mock_connection.exec_command.side_effect = [
            AnsibleConnectionFailure
        ]

        with self.assertRaises(AnsibleConnectionFailure):
            self._terminal.on_open_shell()
