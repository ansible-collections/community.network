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
module: ac_logicsubnet
short_description: Manages LogicSubnet on HUAWEI iMaster NCE-Fabric Controller.
description:
    - Manages LogicSubnet on HUAWEI iMaster NCE-Fabric Controller(AC).
author: ZhiwenZhang (@maomao1995)
notes:
  - This module requires installation iMaster NCE-Fabric Controller.
  - This module depends on module 'GET_TOKEN'.
  - This module also works with C(local) connections for legacy playbooks.
options:
    logicsubnet_id:
        description:
            - AC LogicSubnet id.
    logicrouter_id:
        description:
            - AC LogicRouter id.
    cidr:
        description:
            - AC LogicSubnet cidr.
    gateway_ip:
        description:
            - AC LogicSubnet gateway ip.
'''

EXAMPLES = '''
- name: Create LogicSubnet
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicrouter_id"
      prompt: "Please input logic router id "
      private: no
    - name: "cidr"
      prompt: "Please input cidr "
      private: no
    - name: "gateway_ip"
      prompt: "Please input gateway ip "
      private: no
  tasks:
    - name: check logicrouter_id is null
      fail:
        msg: "Create LogicSubnet fail! logicrouter_id is null"
      when: logicrouter_id == ''
    - name: check cidr is null
      fail:
        msg: "Create LogicSubnet fail! cidr is null"
      when: cidr == ''
    - name: check gateway_ip is null
      fail:
        msg: "Create LogicSubnet fail! gateway_ip is null"
      when: gateway_ip == ''
    - name: Create logicsubnet "{{logicsubnet_name}}"
      tags: create_logicsubnet
      vars:
        logicsubnet_info:
          id: "{{ansible_date_time.iso8601_micro | to_uuid}}"
          cidr: "{{cidr}}"
          gatewayIp: "{{gateway_ip}}"
          logicRouterId: "{{logicrouter_id}}"
          additional:
            producer: "default"
            createAt: "{{now_time}}"
            updateAt: "{{now_time}}"
        logicsubnet_infos:
          subnet: [ "{{logicsubnet_info}}" ]
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/subnets'
        method: POST
        body: '{{logicsubnet_infos}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicsubnet_result
    - name: response from create logic subnet
      debug:
        msg: "{{logicsubnet_result}}"

- name: Update LogicSubnet
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicsubnet_id"
      prompt: "Please input the logic subnet id that you want to update "
      private: no
    - name: "cidr"
      prompt: "Please input cidr "
      private: no
    - name: "gateway_ip"
      prompt: "Please input gateway ip "
      private: no
  tasks:
    - name: check logicsubnet_id is null
      fail:
        msg: "Update LogicSubnet fail! logicsubnet_id is null"
      when: logicsubnet_id == ''
    - name: check cidr is null
      fail:
        msg: "Update LogicSubnet fail! cidr is null"
      when: cidr == ''
    - name: check gateway_ip is null
      fail:
        msg: "Update LogicSubnet fail! gateway_ip is null"
      when: gateway_ip == ''
    - name: Update logic subnet "{{logicsubnet_id}}"
      tags: update_logicsubnet
      vars:
        logicsubnet_info:
          id: "{{logicsubnet_id}}"
          cidr: "{{cidr}}"
          gatewayIp: "{{gateway_ip}}"
          additional:
            updateAt: "{{now_time}}"
        logicsubnet_infos:
          subnet: [ "{{logicsubnet_info}}" ]
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/subnets/subnet/{{logicsubnet_id}}'
        method: PUT
        body: '{{logicsubnet_infos}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicsubnet_result
      ignore_errors: yes
    - name: response from update a logic subnet
      debug:
        msg: "{{logicsubnet_result}}"

- name: Query LogicSubnet
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicsubnet_id"
      prompt: "Please input the logic subnet id that you want to query "
      private: no
  tasks:
    - name: qeury logicsubnets
      tags: qeury_logicsubnets
      when: logicsubnet_id == ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/subnets'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicsubnets_result
      ignore_errors: yes
    - name: qeury logicsubnet "{{logicsubnet_id}}"
      tags: qeury_logicsubnet
      when: logicsubnet_id != ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/subnets/subnet/{{logicsubnet_id}}'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicsubnet_result
      ignore_errors: yes
    - name: response from get logicsubnets
      when: logicsubnet_id == ''
      debug:
        msg: "{{logicsubnets_result.json.subnet}}"
    - name: response from query a logicsubnet
      when: logicsubnet_id != ''
      debug:
        msg: "{{logicsubnet_result.json.subnet}}"

- name: Delete LogicSubnet
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicsubnet_id"
      prompt: "Please input the logic subnet id that you want to delete "
      private: no
  tasks:
    - name: check logicsubnet_id is null
      fail:
        msg: "Delete LogicSubnet fail! logicsubnet_id is null"
      when: logicsubnet_id == ''
    - name: Delete logicsubnet "{{logicsubnet_id}}"
      tags: delete_logicsubnet
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/subnets/subnet/{{logicsubnet_id}}'
        method: DELETE
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicsubnet_result
      ignore_errors: yes
    - name: response from delete a logicsubnet
      debug:
        msg: "{{logicsubnet_result}}"
'''
