# F5 BIG-IP
Assets for the Itential Platform.

## IAG Inventory
Sample IAG 4.x Inventory using Ansible:
```
{
  "ansible_host": "XXX.XX.XXX.XX",
  "ansible_network_os": "bigip",
  "ansible_connection": "local",
  "ansible_provider": "{\"password\":\"PASSWORD\",\"server\":\"XXX.XX.XXX.XX\",\"server_port\":\"8443\",\"transport\":\"rest\",\"user\":\"USERNAME\",\"validate_certs\":false}",
  "ansible_port": 8443
}
```

## Projects
### F5 BIG-IP Project
- Create Pool and Members
- Create a Virtual Server
- _Sample Use Cases_
    - Create Pool, Members, and Virtual Server


#### Dependencies
- [Automation Gateway 4.x](https://www.itential.com/automation-gateway/)
- Automation Gateway Adapter (_ships with Itential Platform_)

