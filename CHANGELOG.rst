===============================
Community Network Release Notes
===============================

.. contents:: Topics


v1.1.0
======

Release Summary
---------------

Release for Ansible 2.10.0.


Minor Changes
-------------

- cnos terminal plugin - prevent timeout connection failure by adding "no logging terminal" after log in (https://github.com/ansible-collections/community.network/pull/16).

New Modules
-----------

Network
~~~~~~~

routeros
^^^^^^^^

- routeros_api - Ansible module for RouterOS API

v1.0.0
======

Release Summary
---------------

This is release 1.0.0 of ``community.network``, released on 2020-07-31.


Removed Features (previously deprecated)
----------------------------------------

- onyx - all onyx modules and plugins have been moved to the mellanox.onyx collection. Redirects have been added that will be removed in community.network 2.0.0 (https://github.com/ansible-collections/community.network/pull/83).

Bugfixes
--------

- edgeos_config - Added `cat` command to allow display of large files without `less`. Led to a timeout error. (https://github.com/ansible-collections/community.network/issues/79)
- edgeos_config - fixed issue where config could be saved while in check mode (https://github.com/ansible-collections/community.network/pull/78)
- edgeos_facts - Added `cat` command to allow display of large files without `less`. Led to a timeout error. (https://github.com/ansible-collections/community.network/issues/79)

v0.2.0
======

Release Summary
---------------

This is the first proper release of the ``community.network`` collection on 2020-06-20.
The changelog describes all changes made to the modules and plugins included in this
collection since Ansible 2.9.0.


Minor Changes
-------------

- ce_bgp_neighbor_af - Rename the parameter ``redirect_ip_vaildation`` to ``redirect_ip_validation`` (https://github.com/ansible/ansible/pull/62403).

Breaking Changes / Porting Guide
--------------------------------

- routeros_facts - allow multiple addresses and neighbors per interface. This makes ``ansible_net_neighbors`` a list instead of a dict (https://github.com/ansible-collections/community.network/pull/6).

Bugfixes
--------

- Cloudengine module_utils - the ``set-id`` (RPC-REPLY XML attribute) may change over the time althougth ``set-id`` is the identity of the next RPC packet.
- Cloudengine netconf plugin - add a dispatch RPC function,just return original RPC-REPLY, the function is used by ``Cloudengine module_utils``.
- Fixes in network action plugins to work in network connection plugin and modules in collection
- Make netconf plugin configurable to set ncclient device handler name in netconf plugin (https://github.com/ansible/ansible/pull/65718)
- Some cloudengine modules have options which should have been removed for Ansible 2.9. see https://github.com/ansible/ansible/issues/67020 and https://github.com/ansible-collections/community.network/pull/68
- Some cloudengine modules were missing ``import __future__`` and ``metaclass``. (https://github.com/ansible/ansible/pull/67634).
- Some cloudengine modules were missing ``import __future__`` and ``metaclass``. (https://github.com/ansible/ansible/pull/67635).
- action/ce - fix a bug, some new version os will not discard uncommitted configure with a return directly.(https://github.com/ansible/ansible/pull/63513).
- ce - Modify exception handling method to make display information more obvious (https://github.com/ansible-collections/community.network/pull/51).
- ce - Modify the way of parsing NETCONF XML message in ce.py (https://github.com/ansible-collections/community.network/pull/39).
- ce_config - fixed issue - Re-building commands(config src) by replacing '#' with 'quit','quit' commands may close connection (https://github.com/ansible/ansible/issues/62872)
- ce_is_is_interface - fix compile error for Python 3.9 (https://github.com/ansible-collections/community.network/pull/36).
- edgeos_config - fix issue where module would silently filter out encrypted passwords
- edgeos_config - fixed issue of handling single quotation marks. Now fails when unmatched (odd numbers)
- edgeos_config - fixed issue where any change in check mode would cause all subsequent tasks to be treated as changes
- netscaler_nitro_request - use all filters for get_filtered instead of only the first one (https://github.com/ansible-collections/community.network/issues/48).
- plugins-netconf-ce - Fix failed to get version information.
- plugins-netconf-ce - to get attribute 'set-id' from rpc-reply.
- routeros module_utils - created a ``try``/``except`` block on the function ``get_capabilities`` (https://github.com/ansible-collections/community.network/pull/27).
- routeros_facts - Prevent crash of module when ``ipv6`` package is not installed

New Modules
-----------

Network
~~~~~~~

apconos
^^^^^^^

- apconos_command - Run arbitrary commands on APCON devices

cloudengine
^^^^^^^^^^^

- ce_is_is_instance - Manages isis process id configuration on HUAWEI CloudEngine devices.
- ce_is_is_interface - Manages isis interface configuration on HUAWEI CloudEngine devices.
- ce_is_is_view - Manages isis view configuration on HUAWEI CloudEngine devices.
- ce_lacp - Manages Eth-Trunk interfaces on HUAWEI CloudEngine switches
- ce_lldp - Manages LLDP configuration on HUAWEI CloudEngine switches.
- ce_lldp_interface - Manages INTERFACE LLDP configuration on HUAWEI CloudEngine switches.
- ce_mdn_interface - Manages MDN configuration on HUAWEI CloudEngine switches.
- ce_multicast_global - Manages multicast global configuration on HUAWEI CloudEngine switches.
- ce_multicast_igmp_enable - Manages multicast igmp enable configuration on HUAWEI CloudEngine switches.
- ce_static_route_bfd - Manages static route configuration on HUAWEI CloudEngine switches.

exos
^^^^

- exos_l2_interfaces - Manage L2 interfaces on Extreme Networks EXOS devices.
- exos_lldp_interfaces - Manage link layer discovery protocol (LLDP) attributes of interfaces on EXOS platforms.
- exos_vlans - Manage VLANs on Extreme Networks EXOS devices.

onyx
^^^^

- onyx_aaa - Configures AAA parameters
- onyx_bfd - Configures BFD parameters
- onyx_ntp - Manage NTP general configurations and ntp keys configurations on Mellanox ONYX network devices
- onyx_ntp_servers_peers - Configures NTP peers and servers parameters
- onyx_snmp - Manages SNMP general configurations on Mellanox ONYX network devices
- onyx_snmp_hosts - Configures SNMP host parameters
- onyx_snmp_users - Configures SNMP User parameters
- onyx_syslog_files - Configure file management syslog module
- onyx_syslog_remote - Configure remote syslog module
- onyx_username - Configure username module
