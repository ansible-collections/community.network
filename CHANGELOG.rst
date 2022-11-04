===============================
Community Network Release Notes
===============================

.. contents:: Topics

This changelog describes changes after version 4.0.0.

v5.0.0
======

Release Summary
---------------

This is release 5.0.0 of the community.network collection.

Major Changes
-------------

- The community.network collection no longer supports Ansible 2.9 and ansible-base 2.10. While we take no active measures to prevent usage, we will remove compatibility code and other compatility measures that will effectively prevent using most content from this collection with Ansible 2.9, and some content of this collection with ansible-base 2.10. Both Ansible 2.9 and ansible-base 2.10 will very soon be End of Life and if you are still using them, you should consider upgrading to ansible-core 2.11 or later as soon as possible (https://github.com/ansible-collections/community.network/pull/426).
- The internal structure of the collection was changed for modules and action plugins. These no longer live in a directory hierarchy ordered by topic, but instead are now all in a single (flat) directory. This has no impact on users *assuming they did not use internal FQCNs*. These will still work, but result in deprecation warnings. They were never officially supported and thus the redirects are kept as a courtsey, and this is not labelled as a breaking change. Note that for example the Ansible VScode plugin started recommending these internal names. If you followed its recommendation, you will now have to change back to the short names to avoid deprecation warnings, and potential errors in the future as these redirects will be removed in community.network 8.0.0 (https://github.com/ansible-collections/community.network/pull/482).

Minor Changes
-------------

- community.network.ce_switchport - add support of decode a few stdout values from bitmap to human readable format(https://github.com/ansible-collections/community.network/issues/315)
- community.network.edgeos_config - append save command into result (https://github.com/ansible-collections/community.network/pull/189)

Removed Features (previously deprecated)
----------------------------------------

- aireos modules - removed deprecated ``connection: local`` support. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- aireos modules - removed deprecated ``provider`` option. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- aruba modules - removed deprecated ``connection: local`` support. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- aruba modules - removed deprecated ``provider`` option. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- ce modules - removed deprecated ``connection: local`` support. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- ce modules - removed deprecated ``provider`` option. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- enos modules - removed deprecated ``connection: local`` support. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- enos modules - removed deprecated ``provider`` option. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- ironware modules - removed deprecated ``connection: local`` support. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- ironware modules - removed deprecated ``provider`` option. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- sros modules - removed deprecated ``connection: local`` support. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).
- sros modules - removed deprecated ``provider`` option. Use ``connection: network_cli`` instead (https://github.com/ansible-collections/community.network/pull/440).

Bugfixes
--------

- Collection core functions - use vendored version of ``distutils.version`` instead of the deprecated Python standard library ``distutils``.
- Include ``PSF-license.txt`` file for ``plugins/module_utils/_version.py``.
- Include ``simplified_bsd.txt`` license file for the ``icx`` and ``netvisor`` module utils.
- ce - Modify the bug in the query configuration method (https://github.com/ansible-collections/community.network/pull/56).
- community.network.ce_switchport - fix error causing by ``KeyError:`` ``host`` due to properties aren't used anywhere (https://github.com/ansible-collections/community.network/issues/313)
- exos_config - fix a hang due to an unexpected prompt during save_when (https://github.com/ansible-collections/community.network/pull/110).
- weos4 cliconf plugin - fix linting errors in documentation data (https://github.com/ansible-collections/community.network/pull/368).
