
# FortiManager

<img src="powered-by-itential.png" width="200"/>


## Table of Contents
<!--TOC-->
<!--TOC--> 




## Overview



## Project Contents
The tree below outlines the structure of the project:
```
┐
└── FortiManager
    ├── ForTesting
    │   ├── fm_testFortiManager (Workflow)
    │   ├── fm_testFortiManager2 (Workflow)
    │   └── lhTest_FortiManager (Workflow)
    ├── Delete Objects
    │   ├── Delete Firewall Policy (Workflow)
    │   ├── Delete Policy Package (Workflow)
    │   ├── Delete Adom (Workflow)
    │   ├── FortiManager Delete Policy Package (Json Form)
    │   ├── FortiManager Delete FW Policy (Json Form)
    │   └── FortiManager Delete Adom (Json Form)
    ├── Update Objects
    │   ├── Update Firewall Policy (Workflow)
    │   ├── Update Adom (Workflow)
    │   ├── Update Policy Package (Workflow)
    │   ├── Update Adom with new device and description (Json Form)
    │   ├── Update Firewall Policy's comment (Json Form)
    │   └── Update Policy Package with policy offload level (Json Form)
    ├── Create Objects (Adom, Policy Pkg, Policy)
    │   ├── Create Adom (Workflow)
    │   ├── Create Policy Package (Workflow)
    │   ├── Create Firewall Policy (Workflow)
    │   ├── Create Firewall Policy Payload (Transformation)
    │   ├── Create Policy Package (Json Form)
    │   └── Create Adom (Json Form)
    ├── Read Objects
    │   ├── Read Policy Package (Workflow)
    │   ├── Read Firewall Policy (Workflow)
    │   ├── Read ADOM (Workflow)
    │   ├── Read Firewall Policy (Json Form)
    │   ├── Read Policy Package (Json Form)
    │   └── Read Adom (Json Form)
    ├── Check Objects Existence
    │   ├── Check Policy Package's existence (Workflow)
    │   ├── Check ADOM's existence (Workflow)
    │   ├── Check Firewall Policy's existence (Workflow)
    │   ├── Check Firewall Policy (Json Form)
    │   ├── Check Policy Package (Json Form)
    │   └── Check Adom (Json Form)
    └── Shared Components
        └── Standard Output (Transformation)
```

<!---
No external project dependencies were found in this project. Uncomment and fill in this section if this is inaccurate.
## Project Dependencies
The table below outlines all the external project dependencies of this project:

<table>
<thead>
<tr>
<th>Source Project</th>
<th>Referenced Assets</th>
</tr>
</thead>
<tbody>
<tr>
<td><em>None</em></td>
<td><em>None</em></td>
</tr>
</tbody>
</table>
-->

<!---
No associated automations were found in this project. If you did not use the --ops_manager flag, this section will not populate. Uncomment and fill in this section or rerun with --ops-manager if this is inaccurate.
## Operations Manager Automations
<table>
<thead>
<tr>
<th>Automation Name</th>
<th>Workflow</th>
<th>Description</th>
<th>Triggers</th>
</tr>
</thead>
<tbody>
<tr>
<td><em>None</em></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>
-->

## Adapters and Integrations
The table below outlines all the adapter and integration dependencies of this project:
<table>
<thead>
<tr>
<th>Name</th>
<th>Version</th>
</tr>
</thead>
<tbody>
<tr>
<td>FortiManager</td>
<td></td>
</tr>
</tbody>
</table>

## Platform Assets
### Workflows
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>fm_testFortiManager</td>
      <td></td>
    </tr>
    <tr>
      <td>fm_testFortiManager2</td>
      <td></td>
    </tr>
    <tr>
      <td>lhTest_FortiManager</td>
      <td></td>
    </tr>
    <tr>
      <td>Delete Firewall Policy</td>
      <td></td>
    </tr>
    <tr>
      <td>Delete Policy Package</td>
      <td></td>
    </tr>
    <tr>
      <td>Delete Adom</td>
      <td></td>
    </tr>
    <tr>
      <td>Update Firewall Policy</td>
      <td></td>
    </tr>
    <tr>
      <td>Update Adom</td>
      <td></td>
    </tr>
    <tr>
      <td>Update Policy Package</td>
      <td></td>
    </tr>
    <tr>
      <td>Create Adom</td>
      <td></td>
    </tr>
    <tr>
      <td>Create Policy Package</td>
      <td></td>
    </tr>
    <tr>
      <td>Create Firewall Policy</td>
      <td></td>
    </tr>
    <tr>
      <td>Read Policy Package</td>
      <td></td>
    </tr>
    <tr>
      <td>Read Firewall Policy</td>
      <td></td>
    </tr>
    <tr>
      <td>Read ADOM</td>
      <td></td>
    </tr>
    <tr>
      <td>Check Policy Package's existence</td>
      <td></td>
    </tr>
    <tr>
      <td>Check ADOM's existence</td>
      <td></td>
    </tr>
    <tr>
      <td>Check Firewall Policy's existence</td>
      <td></td>
    </tr>
  </tbody>
</table>

### Transformations
<table>
<thead>
<tr>
<th>Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>Create Firewall Policy Payload</td>
<td></td>
</tr>
<tr>
<td>Standard Output</td>
<td></td>
</tr>
</tbody>
</table>

### Templates
<table>
<thead>
<tr>
<th>Name</th>
<th>Type</th>
<th>Description</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<!---
No command templates were found in this project. Uncomment and fill in this section if this is inaccurate.
### Command Templates
<table>
<thead>
<tr>
<th>Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
</tbody>
</table>
-->

<!---
No analytic templates were found in this project. Uncomment and fill in this section if this is inaccurate.
### Analytic Templates
<table>
<thead>
<tr>
<th>Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
</tbody>
</table>
-->

### JSON Forms
<table>
<thead>
<tr>
<th>Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>FortiManager Delete Policy Package</td>
<td></td>
</tr>
<tr>
<td>FortiManager Delete FW Policy</td>
<td></td>
</tr>
<tr>
<td>FortiManager Delete Adom</td>
<td></td>
</tr>
<tr>
<td>Update Adom with new device and description</td>
<td></td>
</tr>
<tr>
<td>Update Firewall Policy's comment</td>
<td></td>
</tr>
<tr>
<td>Update Policy Package with policy offload level</td>
<td></td>
</tr>
<tr>
<td>Create Policy Package</td>
<td></td>
</tr>
<tr>
<td>Create Adom</td>
<td></td>
</tr>
<tr>
<td>Read Firewall Policy</td>
<td></td>
</tr>
<tr>
<td>Read Policy Package</td>
<td></td>
</tr>
<tr>
<td>Read Adom</td>
<td></td>
</tr>
<tr>
<td>Check Firewall Policy</td>
<td></td>
</tr>
<tr>
<td>Check Policy Package</td>
<td></td>
</tr>
<tr>
<td>Check Adom</td>
<td></td>
</tr>
</tbody>
</table>

## Gateway Assets
<table>
<thead>
<tr>
<th>Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><em>None</em></td>
<td></td>
</tr>
</tbody>
</table>
