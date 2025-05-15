# Arista EOS
Assets for the Itential Platform.

## Projects
### Arista EOS Project
- Perform a Software Upgrade
- Turn Up a Port
- Create a VLAN
- File Transfer

#### Dependencies
- [Automation Gateway 4.x](https://www.itential.com/automation-gateway/)
- Automation Gateway Adapter (_ships with Itential Platform_)

## IAG Inventory
Sample IAG 4.x Inventory using Ansible:
```
{
  "ansible_host": "XXX.XX.XXX.XX",
  "ansible_port": 22,
  "ansible_network_os": "eos",
  "ansible_connection": "network_cli",
  "ansible_user": "USERNAME",
  "ansible_password": "admin",
  "ansible_become": "yes",
  "ansible_become_method": "enable",
  "ansible_become_password": "PASSWORD"
}
```

## Projects
### Arista EOS Project
- Perform a Software Upgrade
- Turn Up a Port
- Create a VLAN
- File Transfer
- Command Template Runner (Shared Asset)
- Command Template Runner v2

#### Dependencies
- [Automation Gateway 4.x](https://www.itential.com/automation-gateway/)
- Automation Gateway Adapter (_ships with Itential Platform_)