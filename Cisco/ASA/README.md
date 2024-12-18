# Cisco ASA
Assets for the Itential Platform.

## IAG Inventory
Sample IAG 4.x Inventory using Ansible:
```
{
  "ansible_host": "XXX.XX.XXX.XX",
  "ansible_port": 22,
  "ansible_network_os": "asa",
  "ansible_connection": "network_cli",
  "ansible_user": "USERNAME",
  "ansible_password": "PASSWORD",
  "ansible_become": "yes",
  "ansible_become_method": "enable",
  "ansible_become_pass": "PASSWORD"
}
```

## Projects
### Cisco ASA Project
- Perform a Software Upgrade
- Add ACL Rule
- Delete ACL Rule
- Command Template Runner

#### Dependencies
- [Automation Gateway 4.x](https://www.itential.com/automation-gateway/)
- Automation Gateway Adapter (_ships with Itential Platform_)

