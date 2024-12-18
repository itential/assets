# Cisco NX-OS
Assets for the Itential Platform.

## IAG Inventory
Sample IAG 4.x Inventory using Ansible:
```
{
  "ansible_host": "XXX.XX.XXX.XX",
  "ansible_port": 22,
  "ansible_network_os": "nxos",
  "ansible_connection": "network_cli",
  "ansible_user": "USERNAME",
  "ansible_password": "PASSWORD"
}
```

## Projects
### Cisco NX-OS Project
- Perform a Software Upgrade
- Command Template Runner

#### Dependencies
- [Automation Gateway 4.x](https://www.itential.com/automation-gateway/)
- Automation Gateway Adapter (_ships with Itential Platform_)
