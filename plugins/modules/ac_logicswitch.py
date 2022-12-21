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
module: ac_logicswitch
short_description: Manages LogicSwitch on HUAWEI iMaster NCE-Fabric Controller.
description:
    - Manages LogicSwitch on HUAWEI iMaster NCE-Fabric Controller(AC).
author: ZhiwenZhang (@maomao1995)
notes:
  - This module requires installation iMaster NCE-Fabric Controller.
  - This module depends on module 'GET_TOKEN'.
  - This module also works with C(local) connections for legacy playbooks.
options:
    logicswitch_id:
        description:
            - AC LogicSwitch id.
    logicswitch_name:
        description:
            - AC LogicSwitch name.
    logicswitch_desc:
        description:
            - AC LogicSwitch description.
    logicnetwork_id:
        description:
            - AC LogicNetwork id.
'''

EXAMPLES = '''
- name: Create LogicSwitch
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicswitch_name"
      prompt: "Please input logic switch name "
      private: no
    - name: "logicnetwork_id"
      prompt: "Please input logic network id "
      private: no
    - name: "logicswitch_desc"
      prompt: "Please input logic switch description "
      private: no
  tasks:
    - name: check logicswitch_name is null
      fail:
        msg: "Create LogicSwitch fail! logicswitch_name is null"
      when: logicswitch_name == ''
    - name: check logicnetwork_id is null
      fail:
        msg: "Create LogicSwitch fail! logicnetwork_id is null"
      when: logicnetwork_id == ''
    - name: Create logicswitch "{{logicswitch_name}}"
      tags: create_logicswitch
      vars:
        logicswitch_info:
          id: "{{ansible_date_time.iso8601_micro | to_uuid}}"
          name: "{{logicswitch_name}}"
          description: "{{logicswitch_desc}}"
          logicNetworkId: "{{logicnetwork_id}}"
          additional:
            producer: "default"
            createAt: "{{now_time}}"
            updateAt: "{{now_time}}"
        logicswitch_infos:
          switch: [ "{{logicswitch_info}}" ]
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/switchs'
        method: POST
        body: '{{logicswitch_infos}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicswitch_result
    - name: response from create logic switch
      debug:
        msg: "{{logicswitch_result}}"

- name: Update LogicSwitch
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicswitch_id"
      prompt: "Please input the logic switch id that you want to update "
      private: no
    - name: "logicswitch_name"
      prompt: "Please input logic switch name "
      private: no
    - name: "logicswitch_desc"
      prompt: "Please input logic switch description "
      private: no
  tasks:
    - name: check logicswitch_id is null
      fail:
        msg: "Update LogicSwitch fail! logicswitch_id is null"
      when: logicswitch_id == ''
    - name: check logicswitch_name is null
      fail:
        msg: "Update LogicSwitch fail! logicswitch_name is null"
      when: logicswitch_name == ''
    - name: Update logic switch "{{logicswitch_id}}"
      tags: update_logicswitch
      vars:
        logicswitch_info:
          id: "{{logicswitch_id}}"
          name: "{{logicswitch_name}}"
          description: "{{logicswitch_desc}}"
          logicNetworkId: ""
          additional:
            updateAt: "{{now_time}}"
        logicswitch_infos:
          switch: [ "{{logicswitch_info}}" ]
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/switchs/switch/{{logicswitch_id}}'
        method: PUT
        body: '{{logicswitch_infos}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicswitch_result
      ignore_errors: yes
    - name: response from update a logic switch
      debug:
        msg: "{{logicswitch_result}}"

- name: Query LogicSwitch
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicswitch_id"
      prompt: "Please input the logic switch id that you want to query "
      private: no
  tasks:
    - name: qeury logicswitchs
      tags: qeury_logicswitchs
      when: logicswitch_id == ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/switchs'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicswitchs_result
      ignore_errors: yes
    - name: qeury logicswitch "{{logicswitch_id}}"
      tags: qeury_logicswitch
      when: logicswitch_id != ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/switchs/switch/{{logicswitch_id}}'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicswitch_result
      ignore_errors: yes
    - name: response from get logicswitchs
      when: logicswitch_id == ''
      debug:
        msg: "{{logicswitchs_result.json.switch}}"
    - name: response from query a logicswitch
      when: logicswitch_id != ''
      debug:
        msg: "{{logicswitch_result.json.switch}}"

- name: Delete LogicSwitch
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicswitch_id"
      prompt: "Please input the logic switch id that you want to delete "
      private: no
  tasks:
    - name: check logicswitch_id is null
      fail:
        msg: "Delete LogicSwitch fail! logicswitch_id is null"
      when: logicswitch_id == ''
    - name: Delete logicswitch "{{logicswitch_id}}"
      tags: delete_logicswitch
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/switchs/switch/{{logicswitch_id}}'
        method: DELETE
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicswitch_result
      ignore_errors: yes
    - name: response from delete a logicswitch
      debug:
        msg: "{{logicswitch_result}}"
'''
