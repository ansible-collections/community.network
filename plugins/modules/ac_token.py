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
module: ac_token
short_description: Get Token from HUAWEI iMaster NCE-Fabric Controller.
description:
    - Get Tenant from HUAWEI iMaster NCE-Fabric Controller(AC).
author: ZhiwenZhang (@maomao1995)
notes:
  - This module requires installation iMaster NCE-Fabric Controller.
  - This module is dependent by other modules.
  - This module also works with C(local) connections for legacy playbooks.
options:
    userName:
        description:
            - AC User name.
    password:
        description:
            - AC User password.
'''

EXAMPLES = '''
- name: Get Token
  hosts: localhost
  serial: True
  vars_prompt:
    - name: "userName"
      prompt: "Please input userName "
      private: no
    - name: "password"
      prompt: "Please input password "
      echo: no
  tasks:
    - name: delete old access token
      tags: always
      vars:
        token_info:
          token: "{{lookup('file','/tmp/ansible-temp')}}"
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/v2/tokens'
        method: DELETE
        body: '{{token_info}}'
        body_format: json
        validate_certs: False
        headers:
          Accept: application/json
      ignore_errors: yes
    - name: get access token
      tags: always
      vars:
        auth_user:
          userName: '{{userName}}'
          password: '{{password}}'
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/v2/tokens'
        method: POST
        body: '{{auth_user}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          Accept: application/json
        status_code: 200
      register: token_result
    - local_action: copy content='{{token_result.json.data.token_id}}' dest="/tmp/ansible-temp"

- name: Delete Token
  hosts: localhost
  serial: True
  tasks:
    - name: delete access token
      tags: always
      vars:
        token_info:
          token: "{{lookup('file','/tmp/ansible-temp')}}"
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/v2/tokens'
        method: DELETE
        body: '{{token_info}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          Accept: application/json
        status_code: 200
      register: token_result
    - name: response from delete access token
      tags: always
      debug:
        msg: "{{token_result.json}}"
'''
