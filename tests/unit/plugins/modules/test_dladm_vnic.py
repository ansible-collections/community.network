# Copyright (c) 2020 Justin Bronn <jbronn@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json

import pytest
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.network.plugins.modules.network.illumos import (
    dladm_vnic,
)
from ansible_collections.community.network.tests.unit.plugins.modules.utils import (
    set_module_args,
)


DLADM = "/usr/sbin/dladm"


def mocker_vnic_set(mocker, vnic_exists=False, rc=0, out="", err=""):
    """
    Common mocker object
    """
    get_bin_path = mocker.patch.object(AnsibleModule, "get_bin_path")
    get_bin_path.return_value = DLADM
    run_command = mocker.patch.object(AnsibleModule, "run_command")
    run_command.return_value = (rc, out, err)
    vnic_exists_func = mocker.patch.object(dladm_vnic.VNIC, "vnic_exists")
    vnic_exists_func.return_value = vnic_exists


@pytest.fixture
def mocked_vnic_create(mocker):
    mocker_vnic_set(mocker)


@pytest.fixture
def mocked_vnic_delete(mocker):
    mocker_vnic_set(mocker, vnic_exists=True)


def test_vnic_create(mocked_vnic_create, capfd):
    """
    vnic creation
    """
    vnic_name = "vnic0"
    vnic_link = "e1000g0"
    set_module_args(
        {
            "name": vnic_name,
            "link": vnic_link,
            "state": "present",
            "_ansible_check_mode": False,
        }
    )
    with pytest.raises(SystemExit):
        dladm_vnic.main()

    assert AnsibleModule.run_command.call_count == 1
    args = AnsibleModule.run_command.call_args_list[0][0]
    assert args[0][0] == DLADM
    assert args[0][1] == "create-vnic"
    assert args[0][2] == "-l"
    assert args[0][3] == vnic_link
    assert args[0][4] == vnic_name

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert not results.get("failed")
    assert results["changed"]


def test_vnic_delete(mocked_vnic_delete, capfd):
    """
    vnic deletion
    """
    vnic_name = "net0"
    vnic_link = "xge1"
    vnic_temp = (False, True)

    for temp in vnic_temp:
        set_module_args(
            {
                "name": vnic_name,
                "state": "absent",
                "link": vnic_link,
                "temporary": temp,
                "_ansible_check_mode": False,
            }
        )
        with pytest.raises(SystemExit):
            dladm_vnic.main()

        out, err = capfd.readouterr()
        results = json.loads(out)
        assert not results.get("failed")
        assert results["changed"]

    assert AnsibleModule.run_command.call_count == len(vnic_temp)
    for i, call_args in enumerate(AnsibleModule.run_command.call_args_list):
        args = call_args[0][0]
        print(args)
        assert args[0] == DLADM
        assert args[1] == "delete-vnic"
        if vnic_temp[i]:
            assert args[2] == '-t'
            assert args[3] == vnic_name
        else:
            assert args[2] == vnic_name


def test_vnic_create_vlan(mocked_vnic_create, capfd):
    """
    vnic creation with valid vlan
    """
    vnic_name = "vnic0"
    vnic_link = "e1000g0"
    vnic_vlans = (1, "23", 23, 4094)
    vnic_temp = (True, False, False, True)

    for vlan, temp in zip(vnic_vlans, vnic_temp):
        set_module_args(
            {
                "name": vnic_name,
                "link": vnic_link,
                "state": "present",
                "temporary": temp,
                "vlan": vlan,
                "_ansible_check_mode": False,
            }
        )
        with pytest.raises(SystemExit):
            dladm_vnic.main()

        out, err = capfd.readouterr()
        results = json.loads(out)
        assert not results.get("failed")
        assert results["changed"]

    assert AnsibleModule.run_command.call_count == len(vnic_vlans)
    for i, call_args in enumerate(AnsibleModule.run_command.call_args_list):
        args = call_args[0][0]
        assert args[0] == DLADM
        assert args[1] == "create-vnic"
        if vnic_temp[i]:
            assert args[2] == "-t"
            arg_idx = 3
        else:
            arg_idx = 2
        assert args[arg_idx] == "-v"
        assert args[arg_idx + 1] == int(vnic_vlans[i])
        assert args[arg_idx + 2] == "-l"
        assert args[arg_idx + 3] == vnic_link
        assert args[arg_idx + 4] == vnic_name


def test_vnic_create_vlan_invalid(mocked_vnic_create, capfd):
    """
    vnic creation failures with invalid vlan
    """
    vnic_name = "vnic1"
    vnic_link = "e1000g1"
    vnic_vlans = ("foo", ["bar"], 0, 4095)

    for vlan in vnic_vlans:
        set_module_args(
            {
                "name": vnic_name,
                "link": vnic_link,
                "state": "present",
                "vlan": vlan,
                "_ansible_check_mode": False,
            }
        )
        with pytest.raises(SystemExit):
            dladm_vnic.main()

        out, err = capfd.readouterr()
        results = json.loads(out)
        assert results.get("failed")


def test_vnic_create_mac(mocked_vnic_create, capfd):
    """
    vnic creation with valid mac address
    """
    vnic_name = "vnic0"
    vnic_link = "ibg0"
    vnic_macs = ("00:20:91:de:ad:be", "00:0c:29:be:ef:be")
    vnic_temp = (False, True)

    for mac, temp in zip(vnic_macs, vnic_temp):
        set_module_args(
            {
                "name": vnic_name,
                "link": vnic_link,
                "mac": mac,
                "state": "present",
                "temporary": temp,
                "_ansible_check_mode": False,
            }
        )
        with pytest.raises(SystemExit):
            dladm_vnic.main()

        out, err = capfd.readouterr()
        results = json.loads(out)
        assert not results.get("failed")
        assert results["changed"]

    assert AnsibleModule.run_command.call_count == len(vnic_macs)
    for i, call_args in enumerate(AnsibleModule.run_command.call_args_list):
        args = call_args[0][0]
        assert args[0] == DLADM
        assert args[1] == "create-vnic"
        if vnic_temp[i]:
            assert args[2] == "-t"
            arg_idx = 3
        else:
            arg_idx = 2
        assert args[arg_idx] == "-m"
        assert args[arg_idx + 1] == vnic_macs[i]
        assert args[arg_idx + 2] == "-l"
        assert args[arg_idx + 3] == vnic_link
        assert args[arg_idx + 4] == vnic_name


def test_vnic_create_mac_invalid(mocked_vnic_create, capfd):
    """
    vnic creation with an invalid mac address
    """
    vnic_name = "vnic0"
    vnic_link = "ibg0"
    mac_invalid_args = ("01:20:91:de:ad:be", "00:0c:29:be:ef:")

    for mac in mac_invalid_args:
        set_module_args(
            {
                "name": vnic_name,
                "link": vnic_link,
                "state": "present",
                "mac": mac,
                "_ansible_check_mode": False,
            }
        )
        with pytest.raises(SystemExit):
            dladm_vnic.main()

        out, err = capfd.readouterr()
        results = json.loads(out)
        assert results.get("failed")
