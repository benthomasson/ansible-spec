# ansible-spec

Ansible Spec is a utility that will allow developers to describe an Ansible
module argments, examples and return values.  The spec file is a YAML file 
that can be compiled into a skeleton Ansible module.


# Example

Spec file
```
ansible-spec compile examples/eos_vlan_spec.yaml
```

Generated Ansible module code
```
$ ansible-spec compile examples/eos_vlan_spec.yaml 

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

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'core',
    'version': '1.0'
}

DOCUMENTATION = """
---
module: eos_vlan
short_description: Manage the collection of local uesrs on Arista EOS devices
description:
  - This module provides declarative management of the local usernames
    configured on Arista EOS devices.  It allows playbooks to manage
    either individual usernames or the collection of usernames in the
    current running config.  It also supports purging usernames from the
    configuration that are not explicitly defined.
options:
  username:
    description:
      - The username to be configured on the remote Arista EOS device.  This
        argument accepts a stringv value and is mutually exclusive with the
        C(users) argument.
    default: null
  update_password:
    description:
      - Since passwords are encrypted in the device running config, this
        argument will instruct the module when to change the password.  When
        set to C(always), the password will always be updated in the device
        and when set to C(on_create) the password will be updated only if the
        username is created.
    default: always
    choices:
      - on_create
      - always
  users:
    description:
      - The set of username objects to be configured on the remote Arista EOS
        device.  The list entries can either be the username or a hash of
        username and properties.  This argument is mutually exclusive with the
        C(username) argument.
    default: null
  purge:
    description:
      - The C(purge) argument instructs the module to consider the resource
        definition absolute.  It will remove any previously configured
        usernames on the device with the exception of the `admin` user which
        cannot be deleted per EOS constraints.
    default: false
  privilege:
    description:
      - The C(privilege) argument configures the privilege level of the user
        when logged into the system.  This argument accepts integer values in
        the range of 1 to 15.
    default: null
  state:
    description:
      - The C(state) argument configures the state of the uername definition
        as it relates to the device operational configuration.  When set to
        I(present), the username(s) should be configured in the device active
        configuration and when set to I(absent) the username(s) should not be
        in the device active configuration
    default: present
    choices:
      - present
      - absent
  role:
    description:
      - The C(role) argument configures the role for the username in the
        device running configuration.  The argument accepts a string value
        defining the role name.  This argument does not check if the role has
        been configured on the device.
  nopassword:
    description:
      - The C(nopassword) argument defines the username without assigning a
        password.  This will allow the user to login to the system without
        being authenticated by a password.  This argument accepts boolean
        values.
    default: null
    choices:
      - true
      - false
  sshkey:
    description:
      - The C(sshkey) argument defines the SSH public key to configure for the
        username.  This argument accepts a valid SSH key value.
    default: null
"""

EXAMPLES = """
- name: create a new user
  eos_user:
    username: ansible
    sshkey: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
    state: present
- name: remove all users except admin
  eos_user:
    purge: yes
- name: set multiple users to privilege level
  users:
    - username: netop
    - username: netend
  privilege: 15
  state: present
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - username ansible secret password
    - username admin secret admin
session_name:
  description: The EOS config session name used to load the configuration
  returned: when changed is True
  type: str
  sample: ansible_1479315771
"""
from ansible.module_utils.basic import AnsibleModule

def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        username=dict(),
        update_password=dict(default='always', choices=['on_create', 'always']),
        users=dict(type='list'),
        purge=dict(type='bool', default=False),
        privilege=dict(type='int'),
        state=dict(default='present', choices=['present', 'absent']),
        role=dict(),
        nopassword=dict(type='bool'),
        sshkey=dict()
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    module.fail_json(msg='not implemented')

if __name__ == "__main__":
    main()



```
