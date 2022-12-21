#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

DOCUMENTATION = '''
module: ac_endport
short_description: Manages EndPort on HUAWEI iMaster NCE-Fabric Controller.
description:
    - Manages EndPort on HUAWEI iMaster NCE-Fabric Controller(AC).
author: ZhiwenZhang (@maomao1995)
notes:
  - This module requires installation iMaster NCE-Fabric Controller.
  - This module depends on module 'GET_TOKEN'.
  - This module also works with C(local) connections for legacy playbooks.
options:
    endport_id:
        description:
            - AC EndPort id.
    endport_name:
        description:
            - AC EndPort name.
    endport_desc:
        description:
            - AC EndPort description.
    logicport_id:
        description:
            - AC LogicPort id.
'''

EXAMPLES = '''
- name: Create EndPort
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "endport_name"
      prompt: "Please input end port name "
      private: no
    - name: "logicnetwork_id"
      prompt: "Please input logic network id "
      private: no
    - name: "endport_desc"
      prompt: "Please input end port description "
      private: no
    - name: "logicport_id"
      prompt: "Please input logic port id "
      private: no
  tasks:
    - name: check endport_name is null
      fail:
        msg: "Create EndPort fail! endport_name is null"
      when: endport_name == ''
    - name: check logicnetwork_id is null
      fail:
        msg: "Create EndPort fail! logicnetwork_id is null"
      when: logicnetwork_id == ''
    - name: check logicport_id is null
      fail:
        msg: "Create EndPort fail! logicport_id is null"
      when: logicport_id == ''
    - name: Create endport "{{endport_name}}"
      tags: create_endport
      vars:
        endport_info:
          endPort:
            id: "{{ansible_date_time.iso8601_micro | to_uuid}}"
            name: "{{endport_name}}"
            description: "{{endport_desc}}"
            logicNetworkId: "{{logicnetwork_id}}"
            logicPortId: "{{logicport_id}}"
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/endports'
        method: POST
        body: '{{endport_info}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: endport_result
    - name: response from create end port
      debug:
        msg: "{{endport_result}}"

- name: Update EndPort
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "endport_id"
      prompt: "Please input the end port id that you want to update "
      private: no
    - name: "endport_name"
      prompt: "Please input end port name "
      private: no
    - name: "endport_desc"
      prompt: "Please input end port description "
      private: no
  tasks:
    - name: check endport_id is null
      fail:
        msg: "Update EndPort fail! endport_id is null"
      when: endport_id == ''
    - name: check endport_name is null
      fail:
        msg: "Update EndPort fail! endport_name is null"
      when: endport_name == ''
    - name: Update end port "{{endport_id}}"
      tags: update_endport
      vars:
        endport_info:
          endPort:
            id: "{{endport_id}}"
            name: "{{endport_name}}"
            description: "{{endport_desc}}"
            additional:
              updateAt: "{{now_time}}"
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/endports/endport/{{endport_id}}'
        method: PUT
        body: '{{endport_info}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: endport_result
      ignore_errors: yes
    - name: response from update a end port
      debug:
        msg: "{{endport_result}}"

- name: Query EndPort
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "endport_id"
      prompt: "Please input the end port id that you want to query "
      private: no
  tasks:
    - name: qeury endports
      tags: qeury_endports
      when: endport_id == ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/endports'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: endports_result
      ignore_errors: yes
    - name: qeury endport "{{endport_id}}"
      tags: qeury_endport
      when: endport_id != ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/endports/endport/{{endport_id}}'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: endport_result
      ignore_errors: yes
    - name: response from get endports
      when: endport_id == ''
      debug:
        msg: "{{endports_result.json.endPorts}}"
    - name: response from query a endport
      when: endport_id != ''
      debug:
        msg: "{{endport_result.json.endPort}}"

- name: Delete EndPort
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "endport_id"
      prompt: "Please input the end port id that you want to delete "
      private: no
  tasks:
    - name: check endport_id is null
      fail:
        msg: "Delete EndPort fail! endport_id is null"
      when: endport_id == ''
    - name: Delete endport "{{endport_id}}"
      tags: delete_endport
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/endports/endport/{{endport_id}}'
        method: DELETE
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: endport_result
      ignore_errors: yes
    - name: response from delete a endport
      debug:
        msg: "{{endport_result}}"
'''
