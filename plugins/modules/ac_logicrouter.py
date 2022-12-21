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
module: ac_logicrouter
short_description: Manages LogicRouter on HUAWEI iMaster NCE-Fabric Controller.
description:
    - Manages LogicRouter on HUAWEI iMaster NCE-Fabric Controller(AC).
author: ZhiwenZhang (@maomao1995)
notes:
  - This module requires installation iMaster NCE-Fabric Controller.
  - This module depends on module 'GET_TOKEN'.
  - This module also works with C(local) connections for legacy playbooks.
options:
    logicrouter_id:
        description:
            - AC LogicRouter id.
    logicrouter_name:
        description:
            - AC LogicRouter name.
    logicrouter_desc:
        description:
            - AC LogicRouter description.
    fabric_id:
        description:
            - AC Fabric id.
    logicnetwork_id:
        description:
            - AC LogicNetwork id.
'''

EXAMPLES = '''
- name: Create LogicRouter
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicrouter_name"
      prompt: "Please input logic router name "
      private: no
    - name: "logicnetwork_id"
      prompt: "Please input logic network id "
      private: no
    - name: "logicrouter_desc"
      prompt: "Please input logic router description "
      private: no
    - name: "fabric_id"
      prompt: "Please input fabric id "
      private: no
  tasks:
    - name: check logicrouter_name is null
      fail:
        msg: "Create LogicRouter fail! logicrouter_name is null"
      when: logicrouter_name == ''
    - name: check logicnetwork_id is null
      fail:
        msg: "Create LogicRouter fail! logicnetwork_id is null"
      when: logicnetwork_id == ''
    - name: check fabric_id is null
      fail:
        msg: "Create LogicRouter fail! fabric_id is null"
      when: fabric_id == ''
    - name: Create logicrouter "{{logicrouter_name}}"
      tags: create_logicrouter
      vars:
        routerLocation_info:
          fabricId: "{{fabric_id}}"
          fabricRole: "master"
        logicrouter_info:
          router:
            id: "{{ansible_date_time.iso8601_micro | to_uuid}}"
            name: "{{logicrouter_name}}"
            description: "{{logicrouter_desc}}"
            logicNetworkId: "{{logicnetwork_id}}"
            type: "Normal"
            routerLocations: ["{{routerLocation_info}}"]
            additional:
              producer: "default"
              createAt: "{{now_time}}"
              updateAt: "{{now_time}}"
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/routers'
        method: POST
        body: '{{logicrouter_info}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicrouter_result
    - name: response from create logic router
      debug:
        msg: "{{logicrouter_result}}"

- name: Update LogicRouter
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicrouter_id"
      prompt: "Please input the logic router id that you want to update "
      private: no
    - name: "logicrouter_name"
      prompt: "Please input logic router name "
      private: no
    - name: "logicrouter_desc"
      prompt: "Please input logic router description "
      private: no
  tasks:
    - name: check logicrouter_id is null
      fail:
        msg: "Update LogicRouter fail! logicrouter_id is null"
      when: logicrouter_id == ''
    - name: check logicrouter_name is null
      fail:
        msg: "Update LogicRouter fail! logicrouter_name is null"
      when: logicrouter_name == ''
    - name: Update logic router "{{logicrouter_id}}"
      tags: update_logicrouter
      vars:
        logicrouter_info:
          router:
            id: "{{logicrouter_id}}"
            name: "{{logicrouter_name}}"
            description: "{{logicrouter_desc}}"
            additional:
              updateAt: "{{now_time}}"
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/routers/router/{{logicrouter_id}}'
        method: PUT
        body: '{{logicrouter_info}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicrouter_result
      ignore_errors: yes
    - name: response from update a logic router
      debug:
        msg: "{{logicrouter_result}}"

- name: Query LogicRouter
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicrouter_id"
      prompt: "Please input the logic router id that you want to query "
      private: no
  tasks:
    - name: qeury logicrouters
      tags: qeury_logicrouters
      when: logicrouter_id == ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/routers'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicrouters_result
      ignore_errors: yes
    - name: qeury logicrouter "{{logicrouter_id}}"
      tags: qeury_logicrouter
      when: logicrouter_id != ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/routers/router/{{logicrouter_id}}'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicrouter_result
      ignore_errors: yes
    - name: response from get logicrouters
      when: logicrouter_id == ''
      debug:
        msg: "{{logicrouters_result.json.router}}"
    - name: response from query a logicrouter
      when: logicrouter_id != ''
      debug:
        msg: "{{logicrouter_result.json.router}}"

- name: Delete LogicRouter
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicrouter_id"
      prompt: "Please input the logic router id that you want to delete "
      private: no
  tasks:
    - name: check logicrouter_id is null
      fail:
        msg: "Delete LogicRouter fail! logicrouter_id is null"
      when: logicrouter_id == ''
    - name: Delete logicrouter "{{logicrouter_id}}"
      tags: delete_logicrouter
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/routers/router/{{logicrouter_id}}'
        method: DELETE
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicrouter_result
      ignore_errors: yes
    - name: response from delete a logicrouter
      debug:
        msg: "{{logicrouter_result}}"
'''
