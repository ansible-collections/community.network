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
module: ac_logicinterface
short_description: Manages LogicInterface on HUAWEI iMaster NCE-Fabric Controller.
description:
    - Manages LogicInterface on HUAWEI iMaster NCE-Fabric Controller(AC).
author: ZhiwenZhang (@maomao1995)
notes:
  - This module requires installation iMaster NCE-Fabric Controller.
  - This module depends on module 'GET_TOKEN'.
  - This module also works with C(local) connections for legacy playbooks.
options:
    logicinterface_id:
        description:
            - AC LogicInterface id.
    logicinterface_name:
        description:
            - AC LogicInterface name.
    logicrouter_id:
        description:
            - AC LogicRouter id.
    logicswitch_id:
        description:
            - AC LogicSwitch id.
    logicsubnet_id:
        description:
            - AC LogicSubnet id.
'''

EXAMPLES = '''
- name: Create LogicInterface
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicinterface_name"
      prompt: "Please input logic interface name "
      private: no
    - name: "logicrouter_id"
      prompt: "Please input logic router id "
      private: no
    - name: "logicswitch_id"
      prompt: "Please input logic switch id "
      private: no
    - name: "logicsubnet_id"
      prompt: "Please input logic subnet id "
      private: no
  tasks:
    - name: check logicinterface_name is null
      fail:
        msg: "Create LogicInterface fail! logicinterface_name is null"
      when: logicinterface_name == ''
    - name: check logicrouter_id is null
      fail:
        msg: "Create LogicInterface fail! logicrouter_id is null"
      when: logicrouter_id == ''
    - name: check logicswitch_id is null
      fail:
        msg: "Create LogicInterface fail! logicswitch_id is null"
      when: logicswitch_id == ''
    - name: check logicsubnet_id is null
      fail:
        msg: "Create LogicInterface fail! logicsubnet_id is null"
      when: logicsubnet_id == ''
    - name: Create logicinterface "{{logicinterface_name}}"
      tags: create_logicinterface
      vars:
        logicinterface_info:
          id: "{{ansible_date_time.iso8601_micro | to_uuid}}"
          name: "{{logicinterface_name}}"
          interfaceType: "RouterInterface"
          logicRouterId: "{{logicrouter_id}}"
          logicSwitchId: "{{logicswitch_id}}"
          ip:
            subnetId: "{{logicsubnet_id}}"
          additional:
            producer: "default"
            createAt: "{{now_time}}"
            updateAt: "{{now_time}}"
        logicinterface_infos:
          interface: [ "{{logicinterface_info}}" ]
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/interfaces'
        method: POST
        body: '{{logicinterface_infos}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicinterface_result
    - name: response from create logic interface
      debug:
        msg: "{{logicinterface_result}}"

- name: Query LogicInterface
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicinterface_id"
      prompt: "Please input the logic interface id that you want to query "
      private: no
  tasks:
    - name: qeury logicinterfaces
      tags: qeury_logicinterfaces
      when: logicinterface_id == ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/interfaces'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicinterfaces_result
      ignore_errors: yes
    - name: qeury logicinterface "{{logicinterface_id}}"
      tags: qeury_logicinterface
      when: logicinterface_id != ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/interfaces/interface/{{logicinterface_id}}'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: logicinterface_result
      ignore_errors: yes
    - name: response from get logicinterfaces
      when: logicinterface_id == ''
      debug:
        msg: "{{logicinterfaces_result.json.interface}}"
    - name: response from query a logicinterface
      when: logicinterface_id != ''
      debug:
        msg: "{{logicinterface_result.json.interface}}"

- name: Delete LogicInterface
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "logicinterface_id"
      prompt: "Please input the logic interface id that you want to delete "
      private: no
  tasks:
    - name: check logicinterface_id is null
      fail:
        msg: "Delete LogicInterface fail! logicinterface_id is null"
      when: logicinterface_id == ''
    - name: Delete logicinterface "{{logicinterface_id}}"
      tags: delete_logicinterface
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/logicnetwork/interfaces/interface/{{logicinterface_id}}'
        method: DELETE
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: logicinterface_result
      ignore_errors: yes
    - name: response from delete a logicinterface
      debug:
        msg: "{{logicinterface_result}}"
'''
