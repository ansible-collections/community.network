===============================
Community Network Release Notes
===============================

.. contents:: Topics


v1.3.7
======

Release Summary
---------------

This is the patch release of the ``community.network`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.network`` 1.3.6.

Major Changes
-------------

- The community.network 1.x.y release stream will be **End of Life** on 2022-05-23, which coincides with the latest day that community.network 4.0.0 must be released (see `the Roadmap for Ansible 6 <https://github.com/ansible/ansible/blob/devel/docs/docsite/rst/roadmap/COLLECTIONS_6.rst#release-schedule>`_). Thank you very much to everyone who contributed to the 1.x.y releases!

v1.3.6
======

Release Summary
---------------

This is the patch release of the ``community.network`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.network`` 1.3.5.

Bugfixes
--------

- Collection core functions - use vendored version of ``distutils.version`` instead of the deprecated Python standard library ``distutils``.

v1.3.5
======

Release Summary
---------------

This is the patch release of the ``community.network`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.network`` 1.3.4.

Bugfixes
--------

- ce - Modify the bug in the query configuration method (https://github.com/ansible-collections/community.network/pull/56).
- community.network.ce_switchport - fix error causing by ``KeyError:`` ``host`` due to properties aren't used anywhere (https://github.com/ansible-collections/community.network/issues/313)
- exos_config - fix a hang due to an unexpected prompt during save_when (https://github.com/ansible-collections/community.network/pull/110).

v1.3.4
======

Release Summary
---------------

Bugfix release for ansible-core 2.11 compatibility.

Bugfixes
--------

- {cnos,icx}_static_route modules - fix modules to work with ansible-core 2.11 (https://github.com/ansible-collections/community.network/pull/228).

v1.3.3
======

Release Summary
---------------

Security bugfix (potential information leaks in multiple modules) release.

Security Fixes
--------------

- avi_cloudconnectoruser - mark the ``azure_userpass``, ``gcp_credentials``, ``oci_credentials``, and ``tencent_credentials`` parameters as ``no_log`` to prevent leaking of secret values (https://github.com/ansible-collections/community.network/pull/223).
- avi_sslkeyandcertificate - mark the ``enckey_base64`` parameter as ``no_log`` to prevent potential leaking of secret values (https://github.com/ansible-collections/community.network/pull/223).
- avi_webhook - mark the ``verification_token`` parameter as ``no_log`` to prevent potential leaking of secret values (https://github.com/ansible-collections/community.network/pull/223).
- panos_sag - mark the ``password`` parameter as ``no_log`` to prevent potential leaking of secret values (https://github.com/ansible-collections/community.network/pull/226).

v1.3.2
======

Release Summary
---------------

Security bugfix (potential information leaks in multiple modules, CVE-2021-20191) release.

Security Fixes
--------------

- ce_vrrp - mark the ``auth_key`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- cloudengine/ce_vrrp - enabled ``no_log`` for the options ``auth_key`` to prevent accidental disclosure (CVE-2021-20191, https://github.com/ansible-collections/community.network/pull/203).
- cnos_* modules - mark the ``passwords`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- enos_* modules - mark the ``passwords`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- iap_start_workflow - mark the ``token_key`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- icx_system - mark the ``auth_key`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- itential/iap_start_workflow - enabled ``no_log`` for the options ``token_key`` to prevent accidental disclosure (CVE-2021-20191, https://github.com/ansible-collections/community.network/pull/203).
- netscaler/netscaler_lb_monitor - enabled ``no_log`` for the options ``radkey`` to prevent accidental disclosure (CVE-2021-20191, https://github.com/ansible-collections/community.network/pull/203).
- netscaler_lb_monitor - mark the ``password`` and ``secondarypassword`` parameters as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).

v1.3.1
======

Release Summary
---------------

This release contains no code changes, only announcements in the changelogs and changes to CI.

Major Changes
-------------

- For community.network 2.0.0, the Cisco NSO modules will be moved to the `cisco.nso <https://galaxy.ansible.com/cisco/nso>`_ collection.
  A redirection will be inserted so that users using ansible-base 2.10 or newer do not have to change anything.

  If you use Ansible 2.9 and explicitly use Cisco NSO modules from this collection, you will need to adjust your playbooks and roles to use FQCNs starting with ``cisco.nso.`` instead of ``community.network.``,
  for example replace ``community.network.nso_config`` in a task by ``cisco.nso.nso_config``.

  If you use ansible-base and installed ``community.network`` manually and rely on the Cisco NSO modules, you have to make sure to install the ``cisco.nso`` collection as well.
  If you are using FQCNs, for example ``community.network.nso_config`` instead of ``nso_config``, it will continue working, but we still recommend to adjust the FQCNs as well.
- For community.network 2.0.0, the FortiOS modules will be moved to the `community.fortios <https://galaxy.ansible.com/ansible-collections/community.fortios>`_ collection.
  A redirection will be inserted so that users using ansible-base 2.10 or newer do not have to change anything.

  If you use Ansible 2.9 and explicitly use FortiOS modules from this collection, you will need to adjust your playbooks and roles to use FQCNs starting with ``community.fortios.`` instead of ``community.network.``,
  for example replace ``community.network.fmgr_device`` in a task by ``community.fortios.fmgr_device``.

  If you use ansible-base and installed ``community.network`` manually and rely on the FortiOS modules, you have to make sure to install the ``community.fortios`` collection as well.
  If you are using FQCNs, for example ``community.network.fmgr_device`` instead of ``fmgr_device``, it will continue working, but we still recommend to adjust the FQCNs as well.

v1.3.0
======

Release Summary
---------------

This is the last minor 1.x.0 release. The next releases from the stable-1 branch will be 1.3.y patch releases.

Major Changes
-------------

- For community.network 2.0.0, the ``routeros`` modules and plugins will be moved to the `community.routeros <https://galaxy.ansible.com/community/routeros>`_ collection.
  A redirection will be inserted so that users using ansible-base 2.10 or newer do not have to change anything.

  If you use Ansible 2.9 and explicitly use ``routeros`` content from this collection, you will need to adjust your playbooks and roles to use FQCNs starting with ``community.routeros.`` instead of ``community.network.routeros_``,
  for example replace ``community.network.routeros_api`` in a task by ``community.routeros.api``.

  If you use ansible-base and installed ``community.network`` manually and rely on the ``routeros`` content, you have to make sure to install the ``community.routeros`` collection as well.
  If you are using FQCNs, i.e. ``community.network.routeros_command`` instead of ``routeros_command``, it will continue working, but we still recommend to adjust the FQCNs as well.
- In community.network 2.0.0, the ``fortimanager`` httpapi plugin will be removed and replaced by a redirect to the corresponding plugin in the fortios.fortimanager collection. For Ansible 2.10 and ansible-base 2.10 users, this means that it will continue to work assuming that collection is installed. For Ansible 2.9 users, this means that they have to adjust the FQCN from ``community.network.fortimanager`` to ``fortios.fortimanager.fortimanager`` (https://github.com/ansible-collections/community.network/pull/151).

Deprecated Features
-------------------

- Deprecate connection=local support for network platforms using persistent framework (https://github.com/ansible-collections/community.network/pull/120).

Bugfixes
--------

- action pugins - add check for network_cli connection type (https://github.com/ansible-collections/community.network/issues/119, https://github.com/ansible-collections/community.network/pull/120).
- api - fix crash when the ``ssl`` parameter is used (https://github.com/ansible-collections/community.routeros/pull/3).
- dladm_vnic - fixed issue where setting vlan in Python 3 caused a type error (https://github.com/ansible-collections/community.network/issues/131).
- dladm_vnic - vlan IDs 0 and 4095 are now correctly identified as invalid (https://github.com/ansible-collections/community.network/pull/132).
- fortimanager httpapi plugin - fix imports to load module_utils from fortios.fortimanager, where it actually exists. Please note that you must have the fortios.fortimanager collection installed for the plugin to work (https://github.com/ansible-collections/community.network/pull/151).
- ftd httpapi plugin - make sure that plugin errors out on initialization if the required library is not found, and not on load-time (https://github.com/ansible-collections/community.network/pull/150).
- routeros terminal plugin - allow slashes in hostnames for terminal detection. Without this, slashes in hostnames will result in connection timeouts (https://github.com/ansible-collections/community.network/pull/138).

v1.2.0
======

Release Summary
---------------

Regular bimonthly minor release.

Minor Changes
-------------

- edgeswitch_facts - added ``startupconfig`` to facts module - to allow the comparision between startup and running config (https://github.com/ansible-collections/community.network/pull/105).
- routeros_facts - now also collecting data about BGP and OSPF (https://github.com/ansible-collections/community.network/pull/101).
- routeros_facts - set configuration export on to verbose, for full configuration export (https://github.com/ansible-collections/community.network/pull/104).

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
