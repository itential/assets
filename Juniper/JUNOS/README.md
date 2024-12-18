# Juniper JUNOS
Assets for the Itential Platform.

## IAG Inventory
Sample IAG 4.x Inventory using Ansible:
```
{
  "ansible_connection": "netconf",
  "ansible_host": "XXX.XX.XXX.XX",
  "ansible_network_os": "junos",
  "ansible_port": 22,
  "ansible_password": "PASSWORD",
  "ansible_user": "USERNAME"
}
```

## Projects
### Juniper JUNOS Project
- Perform a Software Upgrade
- Turn Up a Port
- Command Template Runner
- Push Configuration

#### Dependencies
- [Automation Gateway 4.x](https://www.itential.com/automation-gateway/)
- Automation Gateway Adapter (_ships with Itential Platform_)

## Golden Configurations
- [Juniper JUNOS - Simple](./Golden%20Configurations/Juniper%20JUNOS%20-%20Simple.json)
- [Juniper JUNOS - Jinja2](./Golden%20Configurations/Juniper%20JUNOS%20-%20Jinja2.json)

#### Dependencies
- [Automation Gateway 4.x](https://www.itential.com/automation-gateway/)
- Automation Gateway Adapter (_ships with Itential Platform_)
