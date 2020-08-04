#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Nikolay Dachev <nikolay@dachev.info>
# GNU General Public License v3.0+ https://www.gnu.org/licenses/gpl-3.0.txt

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: routeros_api
version_added: 1.1.0
author: Nikolay Dachev (@nikolaydachev)
short_description: Ansible module for RouterOS API
description:
  - Ansible module for RouterOS API with python librouteros.
    This module can add, remove, update, query and execute arbitrary command
    in routeros via api.
options:
  hostname:
    description:
      - RouterOS hostname api.
    required: true
    type: str
  username:
    description:
      - RouterOS login user.
    required: true
    type: str
  password:
    description:
      - RouterOS user password.
    required: true
    type: str
  ssl:
    description:
      - If is set ssl will be used for RouterOS api connection.
    required: false
    type: bool
  port:
    description:
      - RouterOS api port. If ssl is set, port will apply to ssl connection.
        Defaults are http api - C(8728), https api - C(8729).
    type: int
  path:
    description:
      - Main path for all other arguments.
        If other arguments are not set, api will return all items in selected path.
        Example "ip address". Eqvivalent of RouterOS cli "/ip address print".
    required: true
    type: str
  add:
    description:
      - Will add selected arguments in selected path to RouterOS config.
        Example "address=1.1.1.1/32 interface=ether1".
        Equivalent in RouterOS cli "/ip address add address=1.1.1.1/32 interface=ether1".
    type: str
  remove:
    description:
      - Remove config/value from RouterOS by '.id'.
         Example "*03" will remove config/value with "id=*03" in selected path.
          Equivalent in RouterOS cli "/ip address remove numbers=1".
          Note "number" in RouterOS cli is different from ".id".
    type: str
  update:
    description:
      - Update config/value in RouterOS by ".id" in selected path.
         Example ".id=*03 address=1.1.1.3/32" and path "ip address"
         will replace existing ip address with ".id=*03".
         Equivalent in RouterOS cli
         "/ip address set address=1.1.1.3/32 numbers=1".
         Note number in RouterOS cli is different from ".id".
    type: str
  query:
    description:
      - Query given path for selected query attributes from
         RouterOS aip and return '.id'.
          WHERE is key word which extend query. WHERE format is
         key operator value - with spaces.
          WHERE valid operators are "==", "!=", ">", "<".
          Example path "ip address" and query ".id address" will return
         only ".id" and "address" for all items in "ip address" path.
          Example path "ip address" and
          query ".id address WHERE address == 1.1.1.3/32"
         will return only ".id" and "address" for items in "ip address"
          path, where address is eq to 1.1.1.3/32.
          Example path "interface" and query "mtu name WHERE mut > 1400" will
         return only interfaces "mtu,name" where mtu is bigger than 1400.
          Equivalent in RouterOS cli "/interface print where mtu > 1400".
    type: str
  cmd:
    description:
      - Execute any/arbitrary command in selected path,
         after the command we can add ".id".
         Example path "system script" and cmd "run .id=*03"
         is equivalent in RouterOS cli "/system script run number=0",
          example path "ip address" and cmd "print"
         equivalent in RouterOS cli "/ip address print".
    type: str
'''

EXAMPLES = '''
---
- name: routeros_api test
  hosts: localhost
  gather_facts: no
  vars:
    hostname: "ros_api_hostname/ip"
    username: "admin"
    password: "secret_password"

    path: "ip address"

    nic: "ether2"
    ip1: "1.1.1.1/32"
    ip2: "2.2.2.2/32"
    ip3: "3.3.3.3/32"

    addips:
      - "address={{ ip1 }} interface={{ nic }}"
      - "address={{ ip2 }} interface={{ nic }}"

    rmips:
      - "{{ ip2 }}"
      - "{{ ip3 }}"
  tasks:
    - name: get "{{ path }} print"
      routeros_api:
        hostname: "{{ hostname }}"
        password: "{{ password }}"
        username: "{{ username }}"
        path: "{{ path }}"
      register: print_path

    - name: result "{{ path }} print"
      ansible.builtin.debug:
        msg: '{{ print_path }}'

    - name: add "ip address add {{ addips[0] }}" "ip address add {{ addips[1] }}"
      routeros_api:
        hostname: "{{ hostname }}"
        password: "{{ password }}"
        username: "{{ username }}"
        path: "{{ path }}"
        add: "{{ item }}"
      loop: "{{ addips }}"
      register: addout

    - name: result routeros '.id' for new added items
      ansible.builtin.debug:
        msg: '{{ addout }}'

    - name: query for ".id" in "{{ path }} WHERE address == {{ ip2 }}"
      routeros_api:
        hostname: "{{ hostname }}"
        password: "{{ password }}"
        username: "{{ username }}"
        path: "{{ path }}"
        query: ".id address WHERE address == {{ ip2 }}"
      register: queryout

    - name: result query result and set fact with '.id' for {{ ip2 }}
      ansible.builtin.debug:
        msg: '{{ queryout }}'

    - ansible.builtin.set_fact:
        query_id : "{{ queryout['msg'][0]['.id'] }}"

    - name: update ".id = {{ query_id }}" taken with custom fact "fquery_id"
      routeros_api:
        hostname: "{{ hostname }}"
        password: "{{ password }}"
        username: "{{ username }}"
        path: "{{ path }}"
        update: ".id={{ query_id }} address={{ ip3 }}"
      register: updateout

    - name: result prunt update status
      ansible.builtin.debug:
        msg: '{{ updateout }}'

    - name: remove ips -  stage 1 - query for '.id' {{ rmips }}
      routeros_api:
        hostname: "{{ hostname }}"
        password: "{{ password }}"
        username: "{{ username }}"
        path: "{{ path }}"
        query: ".id address WHERE address == {{ item }}"
      register: id_to_remove
      loop: "{{ rmips }}"

    # set fact for '.id' from 'query for {{ path }}'
    - ansible.builtin.set_fact:
        to_be_remove: "{{ to_be_remove |default([]) + [item['msg'][0]['.id']] }}"
      loop: "{{ id_to_remove.results }}"

    - name: remove ips stage 1 - dump '.id'
      ansible.builtin.debug:
        msg: '{{ to_be_remove }}'

    # Remove {{ 'rmips' }} with '.id' by 'to_be_remove' from query
    - name: remove ips -  stage 2 - remove {{ rmips }} by '.id'
      routeros_api:
        hostname: "{{ hostname }}"
        password: "{{ password }}"
        username: "{{ username }}"
        path: "{{ path }}"
        remove: "{{ item }}"
      register: remove
      loop: "{{ to_be_remove }}"

    - name: remove ips stage 2 dump result
      ansible.builtin.debug:
        msg: '{{ remove }}'

    - name: arbitrary command example "/system identity print"
      routeros_api:
        hostname: "{{ hostname }}"
        password: "{{ password }}"
        username: "{{ username }}"
        path: "system identity"
        cmd: "print"
      register: cmdout

    - name: dump "/system identity print" output
      ansible.builtin.debug:
        msg: "{{ cmdout }}"
'''

RETURN = '''
---
message:
    description: All outputs are in list with dictionary elements returned from RouterOS api.
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

import ssl
try:
    from librouteros import connect
    from librouteros.query import Key
    HAS_LIB = True
except Exception as e:
    HAS_LIB = False


class ROS_api_module:
    def __init__(self, module_args):
        self.module = AnsibleModule(argument_spec=module_args,
                                    supports_check_mode=False)

        if not HAS_LIB:
            self.module.fail_json(msg=to_native('librouteros for Python is required for this module'))

        # ros api config
        self.user = self.module.params['username']
        self.password = self.module.params['password']
        self.host = self.module.params['hostname']
        self.port = self.module.params['port']
        self.ssl = self.module.params['ssl']

        self.path = self.list_remove_empty(self.module.params['path'].split(' '))

        self.add = self.module.params['add']
        self.remove = self.module.params['remove']
        self.update = self.module.params['update']
        self.arbitrary = self.module.params['cmd']

        self.where = None
        self.query = self.module.params['query']
        if self.query:
            if 'WHERE' in self.query:
                split = self.query.split('WHERE')
                self.query = self.list_remove_empty(split[0].split(' '))
                self.where = self.list_remove_empty(split[1].split(' '))
            else:
                self.query = self.list_remove_empty(self.module.params['query'].split(' '))

        self.result = dict(
            message=[])

        # connect to routeros api
        try:
            conn_status = {"connection": {"username": self.user,
                                          "hostname": self.host,
                                          "port": self.port,
                                          "ssl": self.ssl,
                                          "status": "Connected"}}
            if self.ssl is True:
                if not self.port:
                    self.port = 8729
                    conn_status["connection"]["port"] = self.port
                self.conn_ssl()
            else:
                if not self.port:
                    self.port = 8728
                    conn_status["connection"]["port"] = self.port
                self.conn()
        except Exception as e:
            conn_status["connection"]["status"] = "error: %s" % e
            self.result['message'].append(conn_status)
            self.return_result(False, False)

        # create api base path
        self.api_add_path()

        # api call's
        if self.add:
            self.api_add()
        elif self.remove:
            self.api_remove()
        elif self.update:
            self.api_update()
        elif self.query:
            self.api_query()
        elif self.arbitrary:
            self.api_arbitrary()
        else:
            self.api_get_all()

    def conn(self):
        self.api = connect(username=self.user,
                           password=self.password,
                           host=self.host,
                           port=self.port)

    def conn_ssl(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.set_ciphers('ADH:@SECLEVEL=0')
        self.api = connect(username=self.user,
                           password=self.password,
                           host=self.host,
                           ssl_wrapper=ctx.wrap_socket,
                           port=self.port)

    def list_remove_empty(self, check_list):
        while("" in check_list):
            check_list.remove("")
        return check_list

    def list_to_dic(self, ldict):
        dict = {}
        for p in ldict:
            if '=' not in p:
                self.errors("missing '=' after '%s'" % p)
            p = p.split('=')
            if p[0] == 'id':
                self.errors("'%s' must be '.id'" % p[0])
            if p[1]:
                dict[p[0]] = p[1]
        return dict

    def api_add_path(self):
        self.api_path = self.api.path()
        for p in self.path:
            self.api_path = self.api_path.join(p)

    def api_get_all(self):
        try:
            for i in self.api_path:
                self.result['message'].append(i)
            self.return_result(False, True)
        except Exception as e:
            self.errors(e)

    def api_add(self):
        param = self.list_to_dic(self.add.split(' '))
        try:
            self.result['message'].append("added: .id= %s"
                                          % self.api_path.add(**param))
            self.return_result(True)
        except Exception as e:
            self.errors(e)

    def api_remove(self):
        try:
            self.api_path.remove(self.remove)
            self.result['message'].append("removed: .id= %s" % self.remove)
            self.return_result(True)
        except Exception as e:
            self.errors(e)

    def api_update(self):
        param = self.list_to_dic(self.update.split(' '))
        if '.id' not in param.keys():
            self.errors("missing '.id' for %s" % param)
        try:
            self.api_path.update(**param)
            self.result['message'].append("updated: %s" % param)
            self.return_result(True)
        except Exception as e:
            self.errors(e)

    def api_query(self):
        keys = {}
        for k in self.query:
            if 'id' in k and k != ".id":
                self.errors("'%s' must be '.id'" % k)
            keys[k] = Key(k)
        try:
            if self.where:
                if len(self.where) < 3:
                    self.errors("invalid syntax for 'WHERE %s'"
                                % ' '.join(self.where))

                where = []
                if self.where[1] == '==':
                    select = self.api_path.select(*keys).where(keys[self.where[0]] == self.where[2])
                elif self.where[1] == '!=':
                    select = self.api_path.select(*keys).where(keys[self.where[0]] != self.where[2])
                elif self.where[1] == '>':
                    select = self.api_path.select(*keys).where(keys[self.where[0]] > self.where[2])
                elif self.where[1] == '<':
                    select = self.api_path.select(*keys).where(keys[self.where[0]] < self.where[2])
                else:
                    self.errors("'%s' is not operator for 'where'"
                                % self.where[1])
                for row in select:
                    self.result['message'].append(row)
            else:
                for row in self.api_path.select(*keys):
                    self.result['message'].append(row)
            if len(self.result['message']) < 1:
                msg = "no results for '%s 'query' %s" % (' '.join(self.path),
                                                         ' '.join(self.query))
                if self.where:
                    msg = msg + ' WHERE %s' % ' '.join(self.where)
                self.result['message'].append(msg)
            self.return_result(False)
        except Exception as e:
            self.errors(e)

    def api_arbitrary(self):
        param = {}
        self.arbitrary = self.arbitrary.split(' ')
        arb_cmd = self.arbitrary[0]
        if len(self.arbitrary) > 1:
            param = self.list_to_dic(self.arbitrary[1:])
        try:
            arbitrary_result = self.api_path(arb_cmd, **param)
            for i in arbitrary_result:
                self.result['message'].append(i)
            self.return_result(False)
        except Exception as e:
            self.errors(e)

    def return_result(self, ch_status=False, status=True):
        if not status:
            self.module.fail_json(msg=to_native(self.result['message']))
        else:
            self.module.exit_json(changed=ch_status,
                                  msg=self.result['message'])

    def errors(self, e):
        if e.__class__.__name__ == 'TrapError':
            self.result['message'].append("%s" % e)
            self.return_result(False, True)
        self.result['message'].append("%s" % e)
        self.return_result(False, False)


def main():
    # define available arguments/parameters a user can pass to the module
    ros = ROS_api_module(dict(
        username=dict(type='str', required=True, no_log=False),
        password=dict(type='str', required=True, no_log=True),
        hostname=dict(type='str', required=True, no_log=False),
        port=dict(type='int', required=False, no_log=False),
        ssl=dict(type='bool', required=False, default=False, no_log=False),
        path=dict(type='str', required=True, no_log=False),
        add=dict(type='str', required=False, no_log=False),
        remove=dict(type='str', required=False, no_log=False),
        update=dict(type='str', required=False, no_log=False),
        cmd=dict(type='str', required=False, no_log=False),
        query=dict(type='str', required=False, no_log=False)))


if __name__ == '__main__':
    main()
