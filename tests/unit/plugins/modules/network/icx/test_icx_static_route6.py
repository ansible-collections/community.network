# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.network.tests.unit.plugins.modules.utils import set_module_args
from ansible_collections.community.network.tests.unit.compat.mock import patch
from ansible_collections.community.network.plugins.modules.network.icx import icx_static_route6
from .icx_module import TestICXModule, load_fixture


class TestICXStaticRouteModule6(TestICXModule):

    module = icx_static_route6

    def setUp(self):
        super(TestICXStaticRouteModule6, self).setUp()
        self.mock_get_config = patch('ansible_collections.community.network.plugins.modules.network.icx.icx_static_route6.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.community.network.plugins.modules.network.icx.icx_static_route6.load_config')
        self.load_config = self.mock_load_config.start()
        self.set_running_config()

    def tearDown(self):
        super(TestICXStaticRouteModule6, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        compares = None

        def load_file(*args, **kwargs):
            module = args
            for arg in args:
                if arg.params['check_running_config'] is True:
                    return load_fixture('icx_static_route_config6.txt').strip()
                else:
                    return ''

        self.get_config.side_effect = load_file
        self.load_config.return_value = None

    def test_icx_static_route_config(self):
        set_module_args(dict(prefix='6666:1:2::0/64', next_hop='6666:1:2::0'))
        if not self.ENV_ICX_USE_DIFF:
            result = self.execute_module(changed=True)
            expected_commands = [
                'ipv6 route 6666:1:2::/64  6666:1:2::'
            ]
            self.assertEqual(result['commands'], expected_commands)
        else:
            result = self.execute_module(changed=True)
            expected_commands = [
                'ipv6 route 6666:1:2::/64  6666:1:2::'
            ]
            self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_config_compare(self):
        set_module_args(dict(prefix='6666:1:1::0/64', next_hop='6666:1:1::0', check_running_config=True))
        if self.get_running_config(compare=True):
            if not self.ENV_ICX_USE_DIFF:
                result = self.execute_module(changed=False)
                expected_commands = [
                ]
                self.assertEqual(result['commands'], expected_commands)
            else:
                result = self.execute_module(changed=False)
                expected_commands = [
                ]
                self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_distance_config(self):
        set_module_args(dict(prefix='6666:1:1::/64', next_hop='6666:1:1::', admin_distance='40'))
        if not self.ENV_ICX_USE_DIFF:
            result = self.execute_module(changed=True)
            expected_commands = [
                'ipv6 route 6666:1:1::/64  6666:1:1:: distance 40'
            ]
            self.assertEqual(result['commands'], expected_commands)
        else:
            result = self.execute_module(changed=True)
            expected_commands = [
                'ipv6 route 6666:1:1::/64  6666:1:1:: distance 40'
            ]
            self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_aggregate(self):
        aggregate = [
            dict(prefix='6666:1:3::/64', next_hop='6666:1:3::', admin_distance=1),
            dict(prefix='6666:1:2::/64', next_hop='6666:1:2::', admin_distance=40)
        ]
        set_module_args(dict(aggregate=aggregate))
        if not self.ENV_ICX_USE_DIFF:
            result = self.execute_module(changed=True)
            expected_commands = [
                'ipv6 route 6666:1:3::/64  6666:1:3:: distance 1',
                'ipv6 route 6666:1:2::/64  6666:1:2:: distance 40',
            ]
            self.assertEqual(result['commands'], expected_commands)
        else:
            result = self.execute_module(changed=True)
            expected_commands = [
                'ipv6 route 6666:1:3::/64  6666:1:3:: distance 1',
                'ipv6 route 6666:1:2::/64  6666:1:2:: distance 40',
            ]
            self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_remove(self):
        set_module_args(dict(prefix="6666:1:1::0/64", next_hop="6666:1:1::0", state="absent"))
        if not self.ENV_ICX_USE_DIFF:
            result = self.execute_module(changed=True)
            expected_commands = [
                'no ipv6 route 6666:1:1::/64 6666:1:1::',
            ]
            self.assertEqual(result['commands'], expected_commands)

        else:
            result = self.execute_module(changed=True)
            expected_commands = [
                'no ipv6 route 6666:1:1::/64 6666:1:1::',
            ]
            self.assertEqual(result['commands'], expected_commands)
