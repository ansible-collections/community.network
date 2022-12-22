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
module: ac_tenant
short_description: Manages Tenant on HUAWEI iMaster NCE-Fabric Controller.
description:
    - Manages Tenant on HUAWEI iMaster NCE-Fabric Controller(AC).
author: ZhiwenZhang (@maomao1995)
notes:
  - This module requires installation iMaster NCE-Fabric Controller.
  - This module depends on module 'GET_TOKEN'.
  - This module also works with C(local) connections for legacy playbooks.
options:
    tenant_id:
        description:
            - AC Tenant id.
    tenant_name:
        description:
            - AC Tenant name.
    tenant_desc:
        description:
            - AC Tenant description.
    fabric_id:
        description:
            - AC Fabric id.
'''

EXAMPLES = '''
- name: Create Tenant
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "tenant_name"
      prompt: "Please input tenant name "
      private: no
    - name: "tenant_desc"
      prompt: "Please input tenant description "
      private: no
    - name: "fabric_id"
      prompt: "Please input fabric id "
      private: no
  tasks:
    - name: check tenant_name is null
      fail:
        msg: "Create Tenant fail! tenant_name is null"
      when: tenant_name == ''
    - name: fabric_id is not null
      when: fabric_id != ''
      vars:
        fabricIds: ["{{fabric_id}}"]
      debug: var=fabricIds
    - name: fabric_id is null
      when: fabric_id == ''
      vars:
        fabricIds: []
      debug: var=fabricIds
    - name: Create tenant "{{tenant_name}}"
      tags: create_tenant
      vars:
        tenant_info:
          id: "{{ansible_date_time.iso8601_micro | to_uuid}}"
          name: "{{tenant_name}}"
          description: "{{tenant_desc}}"
          producer: "default"
          createAt: "{{now_time}}"
          updateAt: "{{now_time}}"
          resPool:
            fabricIds: "{{fabric_id}}"
        tenant_infos:
          tenant: ["{{tenant_info}}"]
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/tenants'
        method: POST
        body: '{{tenant_infos}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: tenant_result
    - name: response from create tenant
      debug:
        msg: "{{tenant_result}}"

- name: Update Tenant
  hosts: localhost
  serial: True
  vars:
    now_time: "{{ansible_date_time.date}} {{ansible_date_time.time}}"
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "tenant_id"
      prompt: "Please input the tenant id that you want to update "
      private: no
    - name: "tenant_name"
      prompt: "Please input tenant name "
      private: no
    - name: "tenant_desc"
      prompt: "Please input tenant description "
      private: no
  tasks:
    - name: check tenant_id is null
      fail:
        msg: "Update Tenant fail! tenant_id is null"
      when: tenant_id == ''
    - name: check tenant_name is null
      fail:
        msg: "Update Tenant fail! tenant_name is null"
      when: tenant_name == ''
    - name: Update tenant "{{tenant_id}}"
      tags: update_tenant
      vars:
        tenant_info:
          id: "{{tenant_id}}"
          name: "{{tenant_name}}"
          description: "{{tenant_desc}}"
          updateAt: "{{now_time}}"
        tenant_infos:
          tenant: ["{{tenant_info}}"]
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/tenants/tenant/{{tenant_id}}'
        method: PUT
        body: '{{tenant_infos}}'
        body_format: json
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: tenant_result
      ignore_errors: yes
    - name: response from update a tenant
      debug:
        msg: "{{tenant_result}}"

- name: Query Tenant
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "tenant_id"
      prompt: "Please input the tenant id that you want to query "
      private: no
  tasks:
    - name: qeury tenants
      tags: qeury_tenants
      when: tenant_id == ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/tenants'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: tenants_result
      ignore_errors: yes
    - name: qeury tenant "{{tenant_id}}"
      tags: qeury_tenant
      when: tenant_id != ''
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/tenants/tenant/{{tenant_id}}'
        method: GET
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 200
      register: tenant_result
      ignore_errors: yes
    - name: response from get tenants
      when: tenant_id == ''
      debug:
        msg: "{{tenants_result.json.tenant}}"
    - name: response from query a tenant
      when: tenant_id != ''
      debug:
        msg: "{{tenant_result.json.tenant}}"

- name: Delete Tenant
  hosts: localhost
  serial: True
  vars:
    token_id: "{{lookup('file','/tmp/ansible-temp')}}"
  vars_prompt:
    - name: "tenant_id"
      prompt: "Please input the tenant id that you want to delete "
      private: no
  tasks:
    - name: check tenant_id is null
      fail:
        msg: "Delete Tenant fail! tenant_id is null"
      when: tenant_id == ''
    - name: Delete tenant "{{tenant_id}}"
      tags: delete_tenant
      uri:
        url: 'https://{{north_ip}}:{{north_port}}/controller/dc/v3/tenants/tenant/{{tenant_id}}'
        method: DELETE
        validate_certs: False
        return_content: yes
        headers:
          X-ACCESS-TOKEN: "{{token_id}}"
          Accept: application/json
          Content_Type: application/json
        status_code: 204
      register: tenant_result
      ignore_errors: yes
    - name: response from delete a tenant
      debug:
        msg: "{{tenant_result}}"
'''
