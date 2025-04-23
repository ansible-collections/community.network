#!/usr/bin/env python
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
"""Check BOTMETA file."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ast
import os
import re
import sys

import yaml

from voluptuous import All, Any, MultipleInvalid, PREVENT_EXTRA
from voluptuous import Required, Schema, Invalid
from voluptuous.humanize import humanize_error


IGNORE_NO_MAINTAINERS = [
    'plugins/action/aireos.py',
    'plugins/action/nos_config.py',
    'plugins/terminal/aireos.py',
    'plugins/terminal/apconos.py',
    'plugins/terminal/cnos.py',
    'plugins/terminal/enos.py',
    'plugins/terminal/icx.py',
    'plugins/terminal/netvisor.py',
    'plugins/terminal/weos4.py',
    'plugins/cliconf/aireos.py',
    'plugins/cliconf/cnos.py',
    'plugins/cliconf/edgeos.py',
    'plugins/cliconf/enos.py',
    'plugins/cliconf/netvisor.py',
]


class BotmetaCheck(object):
    def __init__(self):
        self.errors: list[str] = []
        self.botmeta_filename = '.github/BOTMETA.yml'
        self.list_entries = frozenset(('supershipit', 'maintainers', 'labels', 'keywords', 'notify', 'ignore'))
        self.author_regex = re.compile(r'^\w.*\(@([\w-]+)\)(?![\w.])')

    def report_error(self, error: str) -> None:
        self.errors.append(error)

    def read_authors(self, filename: str) -> list[str]:
        data = {}
        try:
            with open(filename, 'rb') as b_module_data:
                M = ast.parse(b_module_data.read())

            for child in M.body:
                if isinstance(child, ast.Assign):
                    for t in child.targets:
                        try:
                            theid = t.id
                        except AttributeError:
                            # skip errors can happen when trying to use the normal code
                            continue

                        if theid == 'DOCUMENTATION':
                            if isinstance(child.value, ast.Dict):
                                data = ast.literal_eval(child.value)
                            else:
                                data = yaml.safe_load(child.value.value)

        except Exception as e:
            self.report_error(f'{filename}:0:0: Cannot load DOCUMENTATION: {e}')
            return []

        author = data.get('author') or []
        if isinstance(author, str):
            author = [author]
        return author

    def extract_author_name(self, author: str) -> str | None:
        m = self.author_regex.match(author)
        if m:
            return m.group(1)
        if author == 'Ansible Core Team':
            return '$team_ansible_core'
        return None

    def validate(self, filename: str, filedata: dict) -> None:
        if not filename.startswith('plugins/'):
            return
        if filename.startswith(('plugins/doc_fragments/', 'plugins/module_utils/')):
            return
        # Compile list of all active and inactive maintainers
        all_maintainers = filedata['maintainers'] + filedata['ignore']
        if not filename.startswith('plugins/filter/'):
            maintainers = self.read_authors(filename)
            for maintainer in maintainers:
                maintainer = self.extract_author_name(maintainer)
                if maintainer is not None and maintainer not in all_maintainers:
                    others = ', '.join(all_maintainers)
                    msg = f'Author {maintainer} not mentioned as active or inactive maintainer for {filename} (mentioned are: {others})'
                    self.report_error(f'{self.botmeta_filename}:0:0: {msg}')
        should_have_no_maintainer = filename in IGNORE_NO_MAINTAINERS
        if not all_maintainers and not should_have_no_maintainer:
            self.report_error(f'{self.botmeta_filename}:0:0: No (active or inactive) maintainer mentioned for {filename}')
        if all_maintainers and should_have_no_maintainer:
            self.report_error(f'{self.botmeta_filename}:0:0: Please remove {filename} from the ignore list of {sys.argv[0]}')

    def run(self) -> None:
        try:
            with open(self.botmeta_filename, 'rb') as f:
                botmeta = yaml.safe_load(f)
        except yaml.error.MarkedYAMLError as ex:
            msg = re.sub(r'\s+', ' ', str(ex))
            self.report_error('f{self.botmeta_filename}:{ex.context_mark.line + 1}:{ex.context_mark.column + 1}: YAML load failed: {msg}')
            return
        except Exception as ex:  # pylint: disable=broad-except
            msg = re.sub(r'\s+', ' ', str(ex))
            self.report_error(f'{self.botmeta_filename}:0:0: YAML load failed: {msg}')
            return

        # Validate schema

        MacroSchema = Schema({
            (str): Any(str, None),
        }, extra=PREVENT_EXTRA)

        FilesSchema = Schema({
            (str): {
                ('supershipit'): str,
                ('support'): Any('community'),
                ('maintainers'): str,
                ('labels'): str,
                ('keywords'): str,
                ('notify'): str,
                ('ignore'): str,
            },
        }, extra=PREVENT_EXTRA)

        schema = Schema({
            ('notifications'): bool,
            ('automerge'): bool,
            ('macros'): MacroSchema,
            ('files'): FilesSchema,
        }, extra=PREVENT_EXTRA)

        try:
            schema(botmeta)
        except MultipleInvalid as ex:
            for error in ex.errors:
                # No way to get line/column numbers
                self.report_error(f'{self.botmeta_filename}:0:0: {humanize_error(botmeta, error)}')
            return

        # Preprocess (substitute macros, convert to lists)
        macros = botmeta.get('macros') or {}
        macro_re = re.compile(r'\$([a-zA-Z_]+)')

        def convert_macros(text, macros):
            def f(m):
                macro = m.group(1)
                replacement = (macros[macro] or '')
                if macro == 'team_ansible_core':
                    return f'$team_ansible_core {replacement}'
                return replacement

            return macro_re.sub(f, text)

        files = {}
        try:
            for file, filedata in (botmeta.get('files') or {}).items():
                file = convert_macros(file, macros)
                filedata = {k: convert_macros(v, macros) for k, v in filedata.items()}
                files[file] = filedata
                for k, v in filedata.items():
                    if k in self.list_entries:
                        filedata[k] = v.split()
        except KeyError as e:
            self.report_error(f'{self.botmeta_filename}:0:0: Found unknown macro {e}')
            return

        # Scan all files
        unmatched = set(files)
        for dirs in ('plugins', ):
            for dirpath, _dirnames, filenames in os.walk(dirs):
                for file in sorted(filenames):
                    if file.endswith('.pyc'):
                        continue
                    if file == '__init__.py':
                        continue
                    filename = os.path.join(dirpath, file)
                    if os.path.islink(filename):
                        continue
                    if os.path.isfile(filename):
                        matching_files = []
                        for file, filedata in files.items():
                            if filename.startswith(file):
                                matching_files.append((file, filedata))
                                if file in unmatched:
                                    unmatched.remove(file)
                        if not matching_files:
                            self.report_error(f'{self.botmeta_filename}:0:0: Did not find any entry for {filename}')

                        matching_files.sort(key=lambda kv: kv[0])
                        filedata = {}
                        for k in self.list_entries:
                            filedata[k] = []
                        for dummy, data in matching_files:
                            for k, v in data.items():
                                if k in self.list_entries:
                                    v = filedata[k] + v
                                filedata[k] = v
                        self.validate(filename, filedata)

        for file in unmatched:
            self.report_error(f'{self.botmeta_filename}:0:0: Entry {file} was not used')


def main() -> int:
    """Main entry point."""
    check = BotmetaCheck()
    check.run()
    for error in sorted(check.errors):
        print(error)
    return 1 if check.errors else 0


if __name__ == '__main__':
    sys.exit(main())
