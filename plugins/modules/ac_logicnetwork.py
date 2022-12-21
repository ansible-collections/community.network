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
module: ac_logicnetwork
short_description: Manages LogicNetwork on HUAWEI iMaster NCE-Fabric Controller.
description:
    - Manages LogicNetwork on HUAWEI iMaster NCE-Fabric Controller(AC).
author: ZhiwenZhang (@maomao1995)
notes:
  - This module requires installation iMaster NCE-Fabric Controller.
  - This module depends on module 'GET_TOKEN'.
  - This module also works with C(local) connections for legacy playbooks.
options:
    logicnetwork_id:
        description:
            - AC LogicNetwork id.
    logicnetwork_name:
        description:
            - AC LogicNetwork name.
    logicnetwork_desc:
        description:
            - AC LogicNetwork description.
    fabric_id:
        description:
            - AC Fabric id.
    tenant_id:
        description:
            - AC Tenant id.
'''

EXAMPLES = '''
- name: Create LogicNetwork
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicnetwork_name"
      prompt: "Please input logic network name "
      private: no
    - name: "tenant_id"
      prompt: "Please input tenant id "
      private: no
    - name: "fabric_id"
      prompt: "Please input fabric id "
      private: no
    - name: "logicnetwork_desc"
      prompt: "Please input logic network description "
      private: no
  tasks:
    - name: check logicnetwork_name is null
      fail:
        msg: "Create LogicNetwork fail! logicnetwork_name is null"
      when: logicnetwork_name == ''
    - name: check tenant_id is null
      fail:
        msg: "Create LogicNetwork fail! tenant_id is null"
      when: tenant_id == ''
    - name: check fabric_id is null
      fail:
        msg: "Create LogicNetwork fail! fabric_id is null"
      when: fabric_id == ''
    - name: Create logic network "{{logicnetwork_name}}"
      tags: create_logicnetwork
      vars:
        logicnetwork_info:
          network:
            id: "{{ansible_date_time.iso8601_micro | to_uuid}}"
            name: "{{logicnetwork_name}}"
            description: "{{logicnetwork_desc}}"
            tenantId: "{{tenant_id}}"
            fabricId: ["{{fabric_id}}"]
            additional:
              producer: "default"
              createAt: "{{now_time}}"
              updateAt: "{{now_time}}"
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/networks'
        method: POST
        body: '{{logicnetwork_info}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicnetwork_result
    - name: response from create logic network
      debug:
        msg: "{{logicnetwork_result}}"

- name: Update LogicNetwork
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicnetwork_id"
      prompt: "Please input the logic network id that you want to update "
      private: no
    - name: "logicnetwork_name"
      prompt: "Please input logic network name "
      private: no
    - name: "logicnetwork_desc"
      prompt: "Please input logic network description "
      private: no
  tasks:
    - name: check logicnetwork_id is null
      fail:
        msg: "Update LogicNetwork fail! logicnetwork_id is null"
      when: logicnetwork_id == ''
    - name: check logicnetwork_name is null
      fail:
        msg: "Update LogicNetwork fail! logicnetwork_name is null"
      when: logicnetwork_name == ''
    - name: Update logic network "{{logicnetwork_id}}"
      tags: update_logicnetwork
      vars:
        logicnetwork_info:
          network:
            id: "{{logicnetwork_id}}"
            name: "{{logicnetwork_name}}"
            description: "{{logicnetwork_desc}}"
            additional:
              updateAt: "{{now_time}}"
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/networks/network/{{logicnetwork_id}}'
        method: PUT
        body: '{{logicnetwork_info}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicnetwork_result
      ignore_errors: yes
    - name: response from update a logic network
      debug:
        msg: "{{logicnetwork_result}}"

- name: Query LogicNetwork
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicnetwork_id"
      prompt: "Please input the logicnetwork id that you want to query "
      private: no
  tasks:
    - name: qeury logicnetworks
      tags: qeury_logicnetworks
      when: logicnetwork_id == ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/networks'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicnetworks_result
      ignore_errors: yes
    - name: qeury logicnetwork "{{logicnetwork_id}}"
      tags: qeury_logicnetwork
      when: logicnetwork_id != ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/networks/network/{{logicnetwork_id}}'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicnetwork_result
      ignore_errors: yes
    - name: response from get logicnetworks
      when: logicnetwork_id == ''
      debug:
        msg: "{{logicnetworks_result.json.network}}"
    - name: response from query a logicnetwork
      when: logicnetwork_id != ''
      debug:
        msg: "{{logicnetwork_result.json.network}}"

- name: Delete LogicNetwork
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicnetwork_id"
      prompt: "Please input the logicnetwork id that you want to delete "
      private: no
  tasks:
    - name: check logicnetwork_id is null
      fail:
        msg: "Delete LogicNetwork fail! logicnetwork_id is null"
      when: logicnetwork_id == ''
    - name: Delete logicnetwork "{{logicnetwork_id}}"
      tags: delete_logicnetwork
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/networks/network/{{logicnetwork_id}}'
        method: DELETE
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicnetwork_result
      ignore_errors: yes
    - name: response from delete a logicnetwork
      debug:
        msg: "{{logicnetwork_result}}"
'''
