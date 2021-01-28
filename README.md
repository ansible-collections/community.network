# Community Network Collection

[![Build Status](https://dev.azure.com/ansible/community.network/_apis/build/status/CI?branchName=stable-2)](https://dev.azure.com/ansible/community.network/_build?definitionId=32)
[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.network)](https://codecov.io/gh/ansible-collections/community.network)

The Community Network collection includes community maintained content to help automate network appliances.

You can find [documentation for this collection on the Ansible docs site](https://docs.ansible.com/ansible/latest/collections/community/network/).

## Tested with Ansible

Tested with the current Ansible 2.9 and 2.10 releases and the current development version of Ansible. Ansible versions before 2.9.10 are not supported.

### Supported connections
The community network collection supports `network_cli`  and `httpapi` connections.

## Included content

Click the `Content` button to see the list of content included in this collection, or check the [documentation on the Ansible docs site](https://docs.ansible.com/ansible/latest/collections/community/network/).

## Installing this collection

You can install the community network collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install community.network

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.network
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```
## Using this collection

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `community.network.routeros_command`.
The following example task replaces configuration changes in the existing configuration on a network device, using the FQCN:

```yaml
---
  - name: run command on remote devices
    community.network.routeros_command:
      commands: /system routerboard print

```

Alternately, you can call modules by their short name if you list the `community.network` collection in the playbook's `collections`, as follows:

```yaml
---
- hosts: routeros01
  gather_facts: false
  connection: network_cli

  collections:
    - community.network

  tasks:
    - name: Gather facts from the device.
      routeros_facts:
         gather_subset: all
```


### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Community Network collection repository](https://github.com/ansible-collections/community.network).

You can also join us on:

- Freenode IRC - ``#ansible-network`` Freenode channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.


## Changelogs

See [here](https://github.com/ansible-collections/community.network/tree/stable-2/CHANGELOG.rst).

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
