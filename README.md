# Community Network Collection

[![Build Status](https://dev.azure.com/ansible/community.network/_apis/build/status/CI?branchName=stable-5)](https://dev.azure.com/ansible/community.network/_build?definitionId=32)
[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.network)](https://codecov.io/gh/ansible-collections/community.network)

This repository contains the `community.network` Ansible Collection. The collection is a part of the `ansible` package and includes many network modules and plugins supported by Ansible community which are not part of more specialized community collections.

You can find [documentation for this collection on the Ansible docs site](https://docs.ansible.com/ansible/latest/collections/community/network/).

## Code of Conduct

We follow [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior violating the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html), please refer to the [policy violations](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html#policy-violations) section of the Code of Conduct for information on how to raise a complaint.

## Contributing to this collection

The content of this collection is made by good people just like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

All types of contributions are very welcome.

You don't know how to start? Refer to our [contribution guide](https://github.com/ansible-collections/community.network/blob/main/CONTRIBUTING.md)!

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

If you're interested in becoming a maintainer of this collection, refer to the [Maintainer guidelines](https://github.com/ansible/community-docs/blob/main/maintaining.rst) for details.

## Communication

We announce important development changes and releases through Ansible's [The Bullhorn newsletter](https://github.com/ansible/community/wiki/News#the-bullhorn). If you are a contributor, be sure you are [subscribed](https://eepurl.com/gZmiEP).

Join us on:

- IRC - the ``#ansible-network`` [irc.libera.chat](https://libera.chat/) channel
- Slack - https://ansiblenetwork.slack.com

Contributors to this collection take part in the global [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://eepurl.com/gZmiEP) and join us.

For more information about communication, refer to the [Ansible communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Tested with Ansible

Tested with the Ansible 2.11, 2.12, and 2.13 releases, and the current development version of Ansible. Ansible-core versions before 2.11.0 are not supported. In particular, ansible-base 2.10 and Ansible 2.9 are not supported. Use community.network 3.x.y if you are using Ansible 2.9 or ansible-base 2.10.

### Supported connections
The community network collection supports `network_cli`  and `httpapi` connections.

## Included content

Click the `Content` button to see the list of content included in this collection, or check the [documentation on the Ansible docs site](https://docs.ansible.com/ansible/latest/collections/community/network/).

## Installing this collection

This collection is shipped with the `ansible` package. So if you have it installed, no more action is required.

If you have a minimal installation (only Ansible Core installed) or you want to use the latest version of the collection along with the whole `ansible` package, you need to install the collection from [Ansible Galaxy](https://galaxy.ansible.com/community/network) manually with the `ansible-galaxy` command-line tool:

    ansible-galaxy collection install community.network

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.network
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

Note that if you install the collection manually, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install community.network --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax where `X.Y.Z` can be any [available version](https://galaxy.ansible.com/community/network):

```bash
ansible-galaxy collection install community.network:==X.Y.Z
```
See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Using this collection

You can call modules by their Fully Qualified Collection Name (FQCN), such as `community.network.a10_server`.
The following example task creates a new server load balancer object on an A10 Networks device, using the FQCN:

```yaml
---
    - name: Create a new server
      community.network.a10_server:
        host: a10.mydomain.com
        username: myadmin
        password: mypassword
        partition: mypartition
        server: test
        server_ip: 192.0.2.100
        server_ports:
          - port_num: 8080
            protocol: tcp
          - port_num: 8443
            protocol: TCP
```

Alternately, you can call modules by their short name if you list the `community.network` collection in the playbook's `collections`, as follows:

```yaml
---
- hosts: "{{desired_inventory_group}}"
  connection: local

  collections:
    - community.network

  tasks:
    - name: Create a new server
      a10_server:
            host: a10.mydomain.com
            username: myadmin
            password: mypassword
            partition: mypartition
            server: test
            server_ip: 192.0.2.100
            server_ports:
              - port_num: 8080
                protocol: tcp
              - port_num: 8443
                protocol: TCP
```

### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Changelogs

See [here](https://github.com/ansible-collections/community.network/tree/stable-5/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
