===============================
Community Network Release Notes
===============================

.. contents:: Topics

This changelog describes changes after version 3.0.0.

v4.0.0
======

Release Summary
---------------

This is release 4.0.0 of ``community.network``, released on 2022-05-26.

Major Changes
-------------

- The community.network collection no longer supports Ansible 2.9 and ansible-base 2.10. While we take no active measures to prevent usage, we will remove compatibility code and other compatility measures that will effectively prevent using most content from this collection with Ansible 2.9, and some content of this collection with ansible-base 2.10. Both Ansible 2.9 and ansible-base 2.10 will very soon be End of Life and if you are still using them, you should consider upgrading to ansible-core 2.11 or later as soon as possible (https://github.com/ansible-collections/community.network/pull/426).

Minor Changes
-------------

- community.network.ce_switchport - add support of decode a few stdout values from bitmap to human readable format(https://github.com/ansible-collections/community.network/issues/315)
- community.network.edgeos_config - append save command into result (https://github.com/ansible-collections/community.network/pull/189)

Bugfixes
--------

- Collection core functions - use vendored version of ``distutils.version`` instead of the deprecated Python standard library ``distutils``.
- Include ``PSF-license.txt`` file for ``plugins/module_utils/_version.py``.
- ce - Modify the bug in the query configuration method (https://github.com/ansible-collections/community.network/pull/56).
- community.network.ce_switchport - fix error causing by ``KeyError:`` ``host`` due to properties aren't used anywhere (https://github.com/ansible-collections/community.network/issues/313)
- exos_config - fix a hang due to an unexpected prompt during save_when (https://github.com/ansible-collections/community.network/pull/110).
- weos4 cliconf plugin - fix linting errors in documentation data (https://github.com/ansible-collections/community.network/pull/368).
