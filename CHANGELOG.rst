===============================
Community Network Release Notes
===============================

.. contents:: Topics

This changelog describes changes after version 2.0.0.

v3.3.0
======

Release Summary
---------------

This is the minor release of the community.network collection. This changelog contains all changes to the modules in this collection that have been added after the release of 
community.network 3.2.0.

Deprecated Features
-------------------

- Support for Ansible 2.9 and ansible-base 2.10 is deprecated, and will be removed in the next major release (community.network 4.0.0) this spring. While most content will probably still work with ansible-base 2.10, we will remove symbolic links for modules and action plugins, which will make it impossible to use them with Ansible 2.9 anymore. Please use community.network 3.x.y with Ansible 2.9 and ansible-base 2.10, as these releases will continue to support Ansible 2.9 and ansible-base 2.10 even after they are End of Life (https://github.com/ansible-community/community-topics/issues/50, https://github.com/ansible-collections/community.network/pull/382).

Bugfixes
--------

- Collection core functions - use vendored version of ``distutils.version`` instead of the deprecated Python standard library ``distutils``.
- Include ``PSF-license.txt`` file for ``plugins/module_utils/_version.py``.

v3.2.0
======

Release Summary
---------------

This is the minor release of the ``community.network`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.network`` 3.1.0.

Deprecated Features
-------------------

- Support for Ansible 2.9 and ansible-base 2.10 is deprecated, and will be removed in the next major release (community.network 4.0.0) this spring. While most content will probably still work with ansible-base 2.10, we will remove symbolic links for modules and action plugins, which will make it impossible to use them with Ansible 2.9 anymore. Please use community.network 3.x.y with Ansible 2.9 and ansible-base 2.10, as these releases will continue to support Ansible 2.9 and ansible-base 2.10 even after they are End of Life (https://github.com/ansible-community/community-topics/issues/50, https://github.com/ansible-collections/community.network/pull/382).

Bugfixes
--------

- Collection core functions - use vendored version of ``distutils.version`` instead of the deprecated Python standard library ``distutils``.

v3.1.0
======

Release Summary
---------------

This is the minor release of the ``community.network`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.network`` 3.0.0.

Minor Changes
-------------

- community.network.ce_switchport - add support of decode a few stdout values from bitmap to human readable format(https://github.com/ansible-collections/community.network/issues/315)
- community.network.edgeos_config - append save command into result (https://github.com/ansible-collections/community.network/pull/189)

Bugfixes
--------

- ce - Modify the bug in the query configuration method (https://github.com/ansible-collections/community.network/pull/56).
- community.network.ce_switchport - fix error causing by ``KeyError:`` ``host`` due to properties aren't used anywhere (https://github.com/ansible-collections/community.network/issues/313)
- exos_config - fix a hang due to an unexpected prompt during save_when (https://github.com/ansible-collections/community.network/pull/110).
- weos4 cliconf plugin - fix linting errors in documentation data (https://github.com/ansible-collections/community.network/pull/368).

v3.0.0
======

Release Summary
---------------

This is release 3.0.0 of ``community.network``, released on 2021-04-22.

Minor Changes
-------------

- edgeos_config - match the space after ``set`` and ``delete`` commands (https://github.com/ansible-collections/community.network/pull/199).
- nclu - execute ``net commit description <description>`` only if changed ``net pending``'s diff field (https://github.com/ansible-collections/community.network/pull/219).

Removed Features (previously deprecated)
----------------------------------------

- The deprecated ``community.network.ce_sflow`` parameters: ``rate_limit``, ``rate_limit_slot``, and ``forward_enp_slot`` have been removed (https://github.com/ansible-collections/community.network/pull/255).
- The deprecated ``community.network.sros`` netconf plugin has been removed. Use ``nokia.sros.md`` instead (https://github.com/ansible-collections/community.network/pull/255).

Security Fixes
--------------

- avi_cloudconnectoruser - mark the ``azure_userpass``, ``gcp_credentials``, ``oci_credentials``, and ``tencent_credentials`` parameters as ``no_log`` to prevent leaking of secret values (https://github.com/ansible-collections/community.network/pull/223).
- avi_sslkeyandcertificate - mark the ``enckey_base64`` parameter as ``no_log`` to prevent potential leaking of secret values (https://github.com/ansible-collections/community.network/pull/223).
- avi_webhook - mark the ``verification_token`` parameter as ``no_log`` to prevent potential leaking of secret values (https://github.com/ansible-collections/community.network/pull/223).
- ce_vrrp - mark the ``auth_key`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- cloudengine/ce_vrrp - enabled ``no_log`` for the options ``auth_key`` to prevent accidental disclosure (CVE-2021-20191, https://github.com/ansible-collections/community.network/pull/203).
- cnos_* modules - mark the ``passwords`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- enos_* modules - mark the ``passwords`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- iap_start_workflow - mark the ``token_key`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- icx_system - mark the ``auth_key`` parameter as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).
- itential/iap_start_workflow - enabled ``no_log`` for the options ``token_key`` to prevent accidental disclosure (CVE-2021-20191, https://github.com/ansible-collections/community.network/pull/203).
- netscaler/netscaler_lb_monitor - enabled ``no_log`` for the options ``radkey`` to prevent accidental disclosure (CVE-2021-20191, https://github.com/ansible-collections/community.network/pull/203).
- netscaler_lb_monitor - mark the ``password`` and ``secondarypassword`` parameters as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.network/pull/206).

Bugfixes
--------

- nclu - fix ``net pending`` delimiter string (https://github.com/ansible-collections/community.network/pull/219).
- {cnos,icx}_static_route modules - fix modules to work with ansible-core 2.11 (https://github.com/ansible-collections/community.network/pull/228).

New Plugins
-----------

Cliconf
~~~~~~~

- weos4 - Use weos4 cliconf to run commands on Westermo platform
