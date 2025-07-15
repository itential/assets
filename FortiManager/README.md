
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
    ├── Delete Objects
    │   ├── Delete Firewall Policy (Workflow)
    │   ├── Delete Policy Package (Workflow)
    │   ├── Delete Adom (Workflow)
    │   ├── Delete Policy Package (Json Form)
    │   ├── Delete FW Policy (Json Form)
    │   └── Delete Adom (Json Form)
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
      <td>Create Adom</td>
      <td> This workflow creates a new Adom using the provided Adom name as input. </td>
    </tr>
    <tr>
      <td>Create Policy Package</td>
      <td> This workflow creates a new Policy Package using the provided Policy Package name and Adom name as inputs. </td>
    </tr>
    <tr>
      <td>Create Firewall Policy</td>
      <td> This workflow creates a new Firewall Policy using the provided Firewall Policy Object,  Policy Package name and Adom name as inputs. </td>
    </tr>
    <tr>
      <td>Read ADOM</td>
      <td> This workflow retrieves the full data object of the specified Adom. Input: Adom name. </td>
    </tr>
    <tr>
      <td>Read Policy Package</td>
      <td> This workflow retrieves the full data object of a specified Policy Package within a given Adom. Inputs: Adom name and Policy Package name. </td>
    </tr>
    <tr>
      <td>Read Firewall Policy</td>
      <td> This workflow retrieves the full data object of a specified Firewall Policy. Inputs: Adom name, Policy Package name, and Firewall Policy name. </td>
    </tr>
    <tr>
      <td>Check ADOM's existence</td>
      <td> This workflow checks whether the specified Adom exists. It returns true if found, otherwise false. Input: Adom name. </td>
    </tr>
    <tr>
      <td>Check Policy Package's existence</td>
      <td> This workflow verifies the existence of a specified Policy Package within a given Adom. It returns true if found, otherwise false. Inputs: Adom name and Policy Package name. </td>
    </tr>
    <tr>
      <td>Check Firewall Policy's existence</td>
      <td> This workflow checks whether a specified Firewall Policy exists within a Policy Package and Adom. It returns true if the policy is found, otherwise false. Inputs: Adom name, Policy Package name, and Firewall Policy name. </td>
    </tr>
    <tr>
      <td>Update Adom</td>
      <td> This workflow updates the specified ADOM by adding a device to it and setting a description. It uses the following inputs: Adom name, Device name, and Description. </td>
    </tr>
    <tr>
      <td>Update Policy Package</td>
      <td> This workflow updates the policy offload level of the specified policy package. It uses the following inputs: Adom name, Policy Package name, and Policy Offload Level. </td>
    </tr>
    <tr>
      <td>Update Firewall Policy</td>
      <td> This workflow updates the specified firewall policy's comment using provided inputs: Adom name, Policy Package name, Firewall Policy, and Comment. </td>
    </tr>
    <tr>
      <td>Delete Adom</td>
      <td> This workflow deletes a specific Adom by taking one required parameter: the Adom name. </td>
    </tr>
    <tr>
      <td>Delete Policy Package</td>
      <td> This workflow deletes a specific policy package by taking two required parameters: the Adom name, policy package name. </td>
    </tr>
    <tr>
      <td>Delete Firewall Policy</td>
      <td> This workflow deletes a specific firewall policy by taking three required parameters: the Adom name, policy package name, and firewall policy name.  </td>
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
<td> This JST prepares the request payload required to create a new firewall policy. </td>
</tr>
<tr>
<td>Standard Output</td>
<td> This JST provides a standardized success or failure message for workflows. In the event of failure, it outputs a failed reason; on success, it confirms completion.</td>
</tr>
</tbody>
</table>

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
<td>Delete Policy Package</td>
<td></td>
</tr>
<tr>
<td>Delete FW Policy</td>
<td></td>
</tr>
<tr>
<td>Delete Adom</td>
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
