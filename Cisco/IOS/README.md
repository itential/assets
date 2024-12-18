# Cisco IOS
Assets for the Itential Platform.

## IAG Inventory
Sample IAG 4.x Inventory using Ansible:
```
{
  "ansible_host": "XXX.XX.XXX.XX",
  "ansible_port": 22,
  "ansible_network_os": "ios",
  "ansible_connection": "network_cli",
  "ansible_user": "USERNAME",
  "ansible_password": "admin",
  "ansible_become": "yes",
  "ansible_become_method": "enable",
  "ansible_become_password": "PASSWORD"
}
```

Sample IAG 4.x Inventory using Netmiko (via Ansible):
```
{
  "ansible_connection": "local",
  "get_state_command": "show version",
  "ansible_port": 22,
  "ansible_password": "PASSWORD",
  "ansible_host": "XXX.XX.XXX.XX",
  "netmiko_device_type": "cisco_ios",
  "get_config_command": "show run",
  "ansible_user": "USERNAME"
}
```

## Projects
### Cisco IOS Project
- Perform a Software Upgrade
- Turn Up a Port
- Command Template Runner
- Push Configuration

#### Dependencies
- [Automation Gateway 4.x](https://www.itential.com/automation-gateway/)
- Automation Gateway Adapter (_ships with Itential Platform_)

## Golden Configurations
- [Cisco IOS - Simple](./Golden%20Configurations/Cisco%20IOS%20-%20Simple.json)
- [Cisco IOS - Jinja2](./Golden%20Configurations/Cisco%20IOS%20-%20Jinja2.json)

#### Dependencies
- [Automation Gateway 4.x](https://www.itential.com/automation-gateway/)
- Automation Gateway Adapter (_ships with Itential Platform_)
