===============================
Community Network Release Notes
===============================

.. contents:: Topics

This changelog describes changes after version 2.0.0.

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
