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
module: ac_logicport
short_description: Manages LogicPort on HUAWEI iMaster NCE-Fabric Controller.
description:
    - Manages LogicPort on HUAWEI iMaster NCE-Fabric Controller(AC).
author: ZhiwenZhang (@maomao1995)
notes:
  - This module requires installation iMaster NCE-Fabric Controller.
  - This module depends on module 'GET_TOKEN'.
  - This module also works with C(local) connections for legacy playbooks.
options:
    logicport_id:
        description:
            - AC LogicPort id.
    logicport_name:
        description:
            - AC LogicPort name.
    logicport_desc:
        description:
            - AC LogicPort description.
    fabric_id:
        description:
            - AC Fabric id.
    logicswitch_id:
        description:
            - AC LogicSwitch id.
    device_ip:
        description:
            - AC Device manage ip.
    port_name:
        description:
            - AC Device port name.
'''

EXAMPLES = '''
- name: Create LogicPort
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicport_name"
      prompt: "Please input logic port name "
      private: no
    - name: "logicswitch_id"
      prompt: "Please input logic switch id "
      private: no
    - name: "logicport_desc"
      prompt: "Please input logic port description "
      private: no
    - name: "device_ip"
      prompt: "Please input device ip "
      private: no
    - name: "port_name"
      prompt: "Please input port name "
      private: no
  tasks:
    - name: check logicport_name is null
      fail:
        msg: "Create LogicPort fail! logicport_name is null"
      when: logicport_name == ''
    - name: check logicswitch_id is null
      fail:
        msg: "Create LogicPort fail! logicswitch_id is null"
      when: logicswitch_id == ''
    - name: check device_ip is null
      fail:
        msg: "Create LogicPort fail! device_ip is null"
      when: device_ip == ''
    - name: check port_name is null
      fail:
        msg: "Create LogicPort fail! port_name is null"
      when: port_name == ''
    - name: Create logicport "{{logicport_name}}"
      tags: create_logicport
      vars:
        location_info:
          deviceIp: "{{device_ip}}"
          portName: "{{port_name}}"
        logicport_info:
          id: "{{ansible_date_time.iso8601_micro | to_uuid}}"
          name: "{{logicport_name}}"
          description: "{{logicport_desc}}"
          logicSwitchId: "{{logicswitch_id}}"
          accessInfo:
            mode: "UNI"
            type: "UNTAG"
            location: [ "{{location_info}}" ]
          additional:
            producer: "default"
            createAt: "{{now_time}}"
            updateAt: "{{now_time}}"
        logicport_infos:
          port: [ '{{logicport_info}}' ]
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/ports'
        method: POST
        body: '{{logicport_infos}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicport_result
    - name: response from create logic port
      debug:
        msg: "{{logicport_result}}"

- name: Update LogicPort
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicport_id"
      prompt: "Please input the logic port id that you want to update "
      private: no
    - name: "logicswitch_id"
      prompt: "Please input logicswitch id "
      private: no
    - name: "fabric_id"
      prompt: "Please input fabric id "
      private: no
    - name: "logicport_name"
      prompt: "Please input logic port name "
      private: no
    - name: "logicport_desc"
      prompt: "Please input logic port description "
      private: no
    - name: "device_ip"
      prompt: "Please input device ip "
      private: no
    - name: "port_name"
      prompt: "Please input port name "
      private: no
  tasks:
    - name: check logicport_id is null
      fail:
        msg: "Update LogicPort fail! logicport_id is null"
      when: logicport_id == ''
    - name: check logicswitch_id is null
      fail:
        msg: "Update LogicPort fail! logicswitch_id is null"
      when: logicswitch_id == ''
    - name: check fabric_id is null
      fail:
        msg: "Update LogicPort fail! fabric_id is null"
      when: fabric_id == ''
    - name: check logicport_name is null
      fail:
        msg: "Update LogicPort fail! logicport_name is null"
      when: logicport_name == ''
    - name: check device_ip is null
      fail:
        msg: "Update LogicPort fail! device_ip is null"
      when: device_ip == ''
    - name: check port_name is null
      fail:
        msg: "Update LogicPort fail! port_name is null"
      when: port_name == ''
    - name: Update logic port "{{logicport_id}}"
      tags: update_logicport
      vars:
        location_info:
          deviceIp: "{{device_ip}}"
          portName: "{{port_name}}"
        logicport_info:
          id: "{{logicport_id}}"
          name: "{{logicport_name}}"
          description: "{{logicport_desc}}"
          fabricId: "{{fabric_id}}"
          logicSwitchId: "{{logicswitch_id}}"
          accessInfo:
            mode: "UNI"
            type: "UNTAG"
            location: [ "{{location_info}}" ]
          additional:
            updateAt: "{{now_time}}"
        logicport_infos:
          port: [ '{{logicport_info}}' ]
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/ports/port/{{logicport_id}}'
        method: PUT
        body: '{{logicport_infos}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicport_result
      ignore_errors: yes
    - name: response from update a logic port
      debug:
        msg: "{{logicport_result}}"

- name: Query LogicPort
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicport_id"
      prompt: "Please input the logic port id that you want to query "
      private: no
  tasks:
    - name: qeury logicports
      tags: qeury_logicports
      when: logicport_id == ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/ports'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicports_result
      ignore_errors: yes
    - name: qeury logicport "{{logicport_id}}"
      tags: qeury_logicport
      when: logicport_id != ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/ports/port/{{logicport_id}}'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicport_result
      ignore_errors: yes
    - name: response from get logicports
      when: logicport_id == ''
      debug:
        msg: "{{logicports_result.json.port}}"
    - name: response from query a logicport
      when: logicport_id != ''
      debug:
        msg: "{{logicport_result.json.port}}"

- name: Delete LogicPort
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicport_id"
      prompt: "Please input the logic port id that you want to delete "
      private: no
  tasks:
    - name: check logicport_id is null
      fail:
        msg: "Delete LogicPort fail! logicport_id is null"
      when: logicport_id == ''
    - name: Delete logicport "{{logicport_id}}"
      tags: delete_logicport
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/ports/port/{{logicport_id}}'
        method: DELETE
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicport_result
      ignore_errors: yes
    - name: response from delete a logicport
      debug:
        msg: "{{logicport_result}}"
'''
