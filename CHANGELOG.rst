===============================
Community Network Release Notes
===============================

.. contents:: Topics

This changelog describes changes after version 1.0.0.

v2.0.1
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

v2.0.0
======

Release Summary
---------------

This is release 2.0.0 of `community.network`, released on 2021-01-27.

Minor Changes
-------------

- cnos terminal plugin - prevent timeout connection failure by adding "no logging terminal" after log in (https://github.com/ansible-collections/community.network/pull/16).
- edgeos_config - added diff result when applying configuration changes (https://github.com/ansible-collections/community.network/pull/184).
- edgeswitch_facts - added ``startupconfig`` to facts module - to allow the comparision between startup and running config (https://github.com/ansible-collections/community.network/pull/105).

Breaking Changes / Porting Guide
--------------------------------

- If you use Ansible 2.9 and the FortiOS modules from this collection, community.network 2.0.0 results in errors when trying to use the FortiOS content by FQCN, like ``community.network.fmgr_device``.
  Since Ansible 2.9 is not able to use redirections, you will have to adjust your playbooks and roles manually to use the new FQCNs (``community.fortios.fmgr_device`` for the previous example) and to make sure that you have ``community.fortios`` installed.

  If you use ansible-base 2.10 or newer and did not install Ansible 3.0.0, but installed (and/or upgraded) community.network manually, you need to make sure to also install ``community.fortios`` if you are using any of the FortiOS modules.
  While ansible-base 2.10 or newer can use the redirects that community.network 2.0.0 adds, the collection they point to (community.fortios) must be installed for them to work.
- If you use Ansible 2.9 and the ``cp_publish`` module from this collection, community.network 2.0.0 results in errors when trying to use the module by FQCN, i.e. ``community.network.cp_publish``. Since Ansible 2.9 is not able to use redirections, you will have to adjust your playbooks and roles manually to use the new FQCNs (``check_point.mgmt.cp_mgmt_publish``) and to make sure that you have ``check_point.mgmt`` installed.
  If you use ansible-base 2.10 or newer and did not install Ansible 3.0.0, but installed (and/or upgraded) community.network manually, you need to make sure to also install ``check_point.mgmt`` if you are using the ``cp_publish`` module. While ansible-base 2.10 or newer can use the redirects that community.network 2.0.0 adds, the collection they point to (check_point.mgmt) must be installed for them to work.
- If you use Ansible 2.9 and the ``fortimanager`` httpapi plugin from this collection, community.network 2.0.0 results in errors when trying to use it by FQCN (``community.network.fortimanager``).
  Since Ansible 2.9 is not able to use redirections, you will have to adjust your playbooks and roles manually to use the new FQCN ``fortinet.fortimanager.fortimanager`` and to make sure that you have ``fortinet.fortimanager`` installed.

  If you use ansible-base 2.10 or newer and did not install Ansible 3.0.0, but installed (and/or upgraded) community.network manually, you need to make sure to also install ``fortinet.fortimanager`` if you are using the ``fortimanager`` httpapi plugin.
  While ansible-base 2.10 or newer can use the redirect that community.network 2.0.0 adds, the collection they point to (fortinet.fortimanager) must be installed for it to work.
- If you use Ansible 2.9 and the ``nso`` modules from this collection, community.network 2.0.0 results in errors when trying to use the nso content by FQCN, like ``community.network.nso_config``.
  Since Ansible 2.9 is not able to use redirections, you will have to adjust your playbooks and roles manually to use the new FQCNs (``cisco.nso.nso_config`` for the previous example) and to make sure that you have ``cisco.nso`` installed.

  If you use ansible-base 2.10 or newer and did not install Ansible 3.0.0, but installed (and/or upgraded) community.network manually, you need to make sure to also install ``cisco.nso`` if you are using any of the ``nso`` modules.
  While ansible-base 2.10 or newer can use the redirects that community.network 2.0.0 adds, the collection they point to (cisco.nso) must be installed for them to work.
- If you use Ansible 2.9 and the ``routeros`` plugins or modules from this collections, community.network 2.0.0 results in errors when trying to use the routeros content by FQCN, like ``community.network.routeros_command``.
  Since Ansible 2.9 is not able to use redirections, you will have to adjust your playbooks and roles manually to use the new FQCNs (``community.routeros.command`` for the previous example) and to make sure that you have ``community.routeros`` installed.

  If you use ansible-base 2.10 or newer and did not install Ansible 3.0.0, but installed (and/or upgraded) community.network manually, you need to make sure to also install ``community.routeros`` if you are using any of the ``routeros`` plugins or modules.
  While ansible-base 2.10 or newer can use the redirects that community.network 2.0.0 adds, the collection they point to (community.routeros) must be installed for them to work.
- cnos_static_route - move ipaddress import from ansible.netcommon to builtin or package before ipaddress is removed from ansible.netcommon. You need to make sure to have the ipaddress package installed if you are using this module on Python 2.7 (https://github.com/ansible-collections/community.network/pull/129).

Deprecated Features
-------------------

- Deprecate connection=local support for network platforms using persistent framework (https://github.com/ansible-collections/community.network/pull/120).

Removed Features (previously deprecated)
----------------------------------------

- All FortiOS modules and plugins have been removed from this collection.
  They have been migrated to the `community.fortios <https://galaxy.ansible.com/community/fortios>`_ collection.
  If you use ansible-base 2.10 or newer, redirections have been provided.

  If you use Ansible 2.9 and installed this collection, you need to adjust the FQCNs (``community.network.fmgr_device`` → ``community.fortios.fmgr_device``) and make sure to install the `community.fortios` collection.
- All ``nso`` modules have been removed from this collection.
  They have been migrated to the `cisco.nso <https://galaxy.ansible.com/cisco/nso>`_ collection.
  If you use ansible-base 2.10 or newer, redirections have been provided.

  If you use Ansible 2.9 and installed this collection, you need to adjust the FQCNs (``community.network.nso_config`` → ``cisco.nso.nso_config``) and make sure to install the `cisco.nso` collection.
- All ``routeros`` modules and plugins have been removed from this collection.
  They have been migrated to the `community.routeros <https://galaxy.ansible.com/community/routeros>`_ collection.
  If you use ansible-base 2.10 or newer, redirections have been provided.

  If you use Ansible 2.9 and installed this collection, you need to adjust the FQCNs (``community.network.routeros_command`` → ``community.routeros.command``) and make sure to install the community.routeros collection.
- The ``cp_publish`` module has been removed from this collection. It was a duplicate of ``check_point.mgmt.cp_mgmt_publish`` in the `check_point.mgmt <https://galaxy.ansible.com/check_point/mgmt>`_ collection. If you use ansible-base 2.10 or newer, redirections have been provided.
  If you use Ansible 2.9 and installed this collection, you need to adjust the FQCNs (``community.network.cp_publish`` → ``check_point.mgmt.cp_mgmt_publish``) and make sure to install the check_point.mgmt collection.
- The ``fortimanager`` httpapi plugin has been removed from this collection.
  It was a duplicate of the one in the `fortinet.fortimanager <https://galaxy.ansible.com/fortinet/fortimanager>`_ collection.
  If you use ansible-base 2.10 or newer, a redirection has been provided.

  If you use Ansible 2.9 and installed this collection, you need to adjust the FQCNs (``community.network.fortimanager`` → ``fortinet.fortimanager.fortimanager``) and make sure to install the `fortinet.fortimanager` collection.
- The dependency on the ``check_point.mgmt`` collection has been removed. If you depend on that installing ``community.network`` also installs ``check_point.mgmt``, you have to make sure to install ``check_point.mgmt`` explicitly.
- The deprecated Pluribus Networks modules ``pn_cluster``, ``pn_ospf``, ``pn_ospfarea``, ``pn_show``, ``pn_trunk``, ``pn_vlag``, ``pn_vlan``, ``pn_vrouter``, ``pn_vrouterbgp``, ``pn_vrouterif``, ``pn_vrouterlbif`` have been removed (https://github.com/ansible-collections/community.network/pull/176).
- The deprecated modules ``panos_admin``, ``panos_admpwd``, ``panos_cert_gen_ssh``, ``panos_check``, ``panos_commit``, ``panos_dag``, ``panos_dag_tags``, ``panos_import``, ``panos_interface``, ``panos_lic``, ``panos_loadcfg``, ``panos_match_rule``, ``panos_mgtconfig``, ``panos_nat_rule``, ``panos_object``, ``panos_op``, ``panos_pg``, ``panos_query_rules``, ``panos_restart``, ``panos_sag``, ``panos_security_rule``, ``panos_set`` have been removed. Use modules from the `paloaltonetworks.panos collection <https://galaxy.ansible.com/paloaltonetworks/panos>`_ instead (https://github.com/ansible-collections/community.network/pull/176).
- The redirect to the ``mellanox.onyx`` collection was removed for: the ``onyx`` cliconf plugin, terminal plugin, module_utils, action plugin, doc fragment, and the following modules: ``onyx_aaa``, ``onyx_bfd``, ``onyx_bgp``, ``onyx_buffer_pool``, ``onyx_command``, ``onyx_config``, ``onyx_facts``, ``onyx_igmp``, ``onyx_igmp_interface``, ``onyx_igmp_vlan``, ``onyx_interface``, ``onyx_l2_interface``, ``onyx_l3_interface``, ``onyx_linkagg``, ``onyx_lldp``, ``onyx_lldp_interface``, ``onyx_magp``, ``onyx_mlag_ipl``, ``onyx_mlag_vip``, ``onyx_ntp``, ``onyx_ntp_servers_peers``, ``onyx_ospf``, ``onyx_pfc_interface``, ``onyx_protocol``, ``onyx_ptp_global``, ``onyx_ptp_interface``, ``onyx_qos``, ``onyx_snmp``, ``onyx_snmp_hosts``, ``onyx_snmp_users``, ``onyx_syslog_files``, ``onyx_syslog_remote``, ``onyx_traffic_class``, ``onyx_username``, ``onyx_vlan``, ``onyx_vxlan``, ``onyx_wjh`` (https://github.com/ansible-collections/community.network/pull/175).
- onyx - all onyx modules and plugins have been moved to the mellanox.onyx collection. Redirects have been added that will be removed in community.network 2.0.0 (https://github.com/ansible-collections/community.network/pull/83).

Bugfixes
--------

- action pugins - add check for network_cli connection type (https://github.com/ansible-collections/community.network/issues/119, https://github.com/ansible-collections/community.network/pull/120).
- dladm_vnic - fixed issue where setting vlan in Python 3 caused a type error (https://github.com/ansible-collections/community.network/issues/131).
- dladm_vnic - vlan IDs 0 and 4095 are now correctly identified as invalid (https://github.com/ansible-collections/community.network/pull/132).
- edgeos_config - Added `cat` command to allow display of large files without `less`. Led to a timeout error. (https://github.com/ansible-collections/community.network/issues/79)
- edgeos_config - fixed issue where config could be saved while in check mode (https://github.com/ansible-collections/community.network/pull/78)
- edgeos_facts - Added `cat` command to allow display of large files without `less`. Led to a timeout error. (https://github.com/ansible-collections/community.network/issues/79)
- ftd httpapi plugin - make sure that plugin errors out on initialization if the required library is not found, and not on load-time (https://github.com/ansible-collections/community.network/pull/150).
