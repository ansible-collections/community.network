# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Copyright (c) 2020 Ernst Oudhof, ernst@mailfrom.nl
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
import json

from ansible.module_utils._text import to_text, to_bytes
from ansible.plugins.terminal import TerminalBase
from ansible.errors import AnsibleConnectionFailure


class TerminalModule(TerminalBase):

    terminal_stdout_re = [
        re.compile(br"[\r\n]?[\w\+\-\.:\/\[\]]+(?:\([^\)]+\)){0,3}(?:#>) ?$")
    ]

    terminal_stderr_re = [
        re.compile(br"% ?Error"),
        re.compile(br"invalid input", re.I),
        re.compile(br"connection timed out", re.I),
        re.compile(br"[^\r\n]+ not found"),
        re.compile(br"[^\r\n]+ not allowed"),
        re.compile(br"[^\r\n]+ not supported"),
        re.compile(br"[^\r\n]+ not exist"),
        re.compile(br"[^\r\n]+ Invalid")
    ]

    def on_open_shell(self):
        try:
            self._exec_cli_command(u'batch')
        except AnsibleConnectionFailure:
            raise AnsibleConnectionFailure('unable to set terminal parameters')
