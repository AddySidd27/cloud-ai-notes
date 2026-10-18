---
title: "Prepare Your Azure Environment for Azure Virtual Desktop"
layout: post.njk
permalink: "/azure-virtual-desktop/prepare-your-azure-environment/"
order: 103
part: 3
tags: [avd-series]
deck: "Prepare the tenant, subscription, access, licensing, quota and cost controls before deployment."
description: "Prepare an Azure tenant and subscription for Azure Virtual Desktop: access roles, user licensing, resource provider, quota, policy checks and a cost budget."
---

In the previous post, we followed how an Azure Virtual Desktop connection works. Now, we will prepare the Azure environment before building the first host pool (a group of virtual machines, built from the same image, that deliver desktops to users).

## Key terms

Each term is explained again where it is first used. This table is for quick lookup.

| Term | What it means |
|---|---|
| Tenant | Your organization's cloud directory in Microsoft Entra ID. It holds users and groups. |
| Subscription | The Azure container where resources are created and their usage is billed. |
| Resource group | A folder-like container for related Azure resources inside a subscription. |
| Scope | The set of resources a permission applies to: a management group, subscription, resource group or single resource. |
| RBAC | Role-based access control: permissions are given as roles at a scope. |
| Resource provider | The service behind a type of Azure resource. Registering it sets your subscription up to use that service. |
| Quota | A limit on how much of a resource, such as VM vCPUs, a subscription can use in a region. |
| VM family | A group of VM sizes that share one quota. |
| Budget | A cost limit you set on a scope. It sends alerts when spending reaches the thresholds you choose. It does not stop spending. |
| Action group | A saved list of people or tools to notify when an alert fires. |
| Initiative | A group of Azure Policy rules that are assigned together. |
| Terraform | An open-source tool that builds cloud resources from configuration files. |
| Landing zone | The shared Azure foundation, such as networks, identity and policy, that workloads like AVD sit on. |
| Hub | The shared network that holds common services. Other networks, called spokes, connect to it. |
| Host pool | A group of virtual machines, built from the same image, that deliver desktops to users. |
| Peering | A link that lets two virtual networks communicate directly. |
| Default outbound access | A public outbound IP address that Azure gives a VM automatically when no explicit outbound method is set up. |
| Per-user access pricing | A pay-as-you-go charge for external users who connect to AVD. It is billed through an Azure subscription. |
| Usage location | The country or region set on a user account. A license assignment can fail when it is invalid. |

## Start with the environment you already have

Before opening the deployment wizard, answer three questions: Which directory holds the users? Which subscription will hold the resources? Who has permission to build and operate them?

A **Microsoft Entra tenant** is the organization's cloud directory. It holds identities such as users and groups. An **Azure subscription** is where Azure resources are created and their usage is billed. A **resource group** organizes related resources inside that subscription.

These serve different purposes. An Azure subscription does not, by itself, give a user access to an AVD desktop.

Our Azure Landing Zone series introduced the landing zone, the shared foundation of networks, identity and policy that workloads sit on. AVD is a workload that uses it. The platform provides shared services and controls; the AVD environment adds the desktops, applications and their workload configuration.

| Your starting point | What to do here |
|---|---|
| An organization already has a landing zone | Confirm the approved tenant, workload subscription, resource placement and platform owners. Reuse their services. |
| You already built the platform lab | Check its actual outputs and controls before adding AVD. Do not deploy another hub (the shared network that holds common services) simply because this is a new series. |
| You are starting a personal lab | Use an active subscription in the intended tenant. Prepare the access and resource organization described below. Plan the network in the [networking article](/azure-virtual-desktop/plan-avd-networking/). |

The [Minimum Viable Platform Landing Zone](https://adnanasiddiqui.com/azure-landing-zone/minimum-viable-platform-landing-zone/) post explains the wider foundation. Here, we cover the checks needed to continue with AVD.

If you have no active subscription, request one through your organization or complete Azure account and subscription setup first. Confirm its tenant association before following the steps below.

The screenshots below come from an existing development environment. We check the existing foundation, add the selected test user to its access group and create a workload budget. Identifiers and account details are hidden.

The administrator prepares the environment. A separate non-administrator account will test the desktop after the identity model is selected.

## 1. Confirm the tenant and subscription together

The same account can appear in several directories. Start by checking the directory you are working in, rather than relying on the account name in the top-right corner.

1. Sign in to the Azure portal. Open **Settings > Directories + subscriptions**.
2. Check **Current directory**. If necessary, find the intended directory and select **Switch**.

![Azure portal Directories + subscriptions page with the current directory marked; directory name, directory ID and domain hidden](/img/avd/AVD-Post-03-directory-redacted.png)

*The Current indicator identifies the active directory. Record its ID privately.*


3. Open **Subscriptions**, then the subscription you intend to use. Record its name and subscription ID; confirm it is enabled for use.

![Subscription overview showing status Active; subscription name, subscription ID, directory and offer details hidden](/img/avd/AVD-Post-03-subscription-redacted.png)

*This subscription shows Active. Check its Directory field against the directory selected above; the value is hidden here.*


4. Open **Microsoft Entra ID > Overview > Properties** and record the tenant ID. Confirm this is the directory associated with your selected subscription.

![Microsoft Entra directory Properties tab with the Name, Tenant ID and Technical contact fields; the values are hidden](/img/avd/AVD-Post-03-tenant-redacted.png)

*The tenant ID is on the Properties tab. Compare the original value with your private subscription record.*



An ID identifies the exact object. Two subscriptions can have similar display names, so keep the IDs in your private build notes.

If you use an installed Azure CLI, first sign in with **az login**. These commands then check and select the subscription context. Replace the example text with your actual subscription ID.

```bash
az account list --output table
az account set --subscription "YOUR-SUBSCRIPTION-ID"
az account show --query "{Name:name,Id:id,Tenant:tenantId,State:state}" -o table
```

**Check the result:** the CLI subscription and tenant must match your intended deployment context. Selecting a directory in the portal does not automatically change the context of a separate local CLI session.

The AVD test user needs a supported identity in the Microsoft Entra tenant used for AVD. A personal Microsoft account used to manage an Azure subscription is different from the work or school identity used to sign in to the desktop. Prepare that test identity separately.

## 2. Decide where the AVD resources belong

A landing zone gives the workload a governed place to run. In an existing organization, ask for the approved AVD workload subscription and the services available from the platform team.

Management groups organize subscriptions. Azure permissions assigned at a parent scope are inherited by its children. The diagram shows the four levels where an Azure permission can be assigned.

![Nested boxes with four levels: a management group contains two subscriptions, the subscriptions contain three resource groups, and the resource groups contain a virtual machine, a virtual network, a storage account and another virtual machine.](/img/avd/AVD-Post-03-Access-Scope-v2.png)

*The Azure RBAC scope levels: management group, subscription, resource group and resource. A role assigned at one level applies to everything below it. Drawn by the author from [Understand scope for Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview), which has its own diagrams to compare. Not an official Microsoft diagram. Icons: Microsoft Azure and Microsoft Entra architecture icons, used unmodified under the terms on Microsoft's icons page.*

The complete [Resource Organization](https://adnanasiddiqui.com/azure-landing-zone/resource-organization/) post covers the platform hierarchy. Here, record the specific subscription and resource groups your AVD deployment will use.

The existing development group inspected here is **rg-avd-dev**, in **East US**. Its tags include Environment: dev, Project: avd and ManagedBy: Terraform (a tool that builds Azure resources from configuration files). A tag is a label on a resource. A ManagedBy tag says how the owner intends to manage it, but the tag does not prove it. Check the real configuration before you change anything. Use your organization's naming standard when one exists.

If the platform team has provided a suitable group, open **Resource groups**, select it and verify the subscription, name and location. Record its owner.

![Resource group rg-avd-dev overview: location East US, tags Environment dev, ManagedBy Terraform, Project avd and Workload Azure Virtual Desktop; subscription name and subscription ID hidden](/img/avd/AVD-Post-03-resourcegroup-redacted.png)

*We inspected an existing group. We did not create it in this walkthrough. Its metadata location is East US.*



If no workload group exists, record the intended name and approved location. The Terraform deployment will create the group it manages. Keep a supplied group as an existing dependency in that design.

A resource group's region controls its metadata location; resources inside it can be in other regions. Use the same region for the group and its resources where you can, and choose each resource's location deliberately when it is deployed.

Keep resources that you intend to manage and retire together in the same group. Shared platform resources have a separate lifecycle: an AVD lab cleanup must not remove the shared hub, DNS or logging environment.

### Record the platform services the workload will use

A virtual network is the private network for Azure resources. A subnet is a section of that network. **DNS** resolves names to addresses. Before building hosts, record which network and name-resolution service they will use.

1. Open the existing workload's VM **Overview** and read **Virtual network/subnet**. Here, avdsh-01 uses **vnet-avd-dev/snet-sessionhosts** (the VM overview is not pictured).
2. Open that VNet and check its region and **DNS servers**. This lab uses East US and **Azure provided DNS service**.
3. Record the dependencies below with the people responsible for them. For a personal lab, you may own each area. In an organization, use the platform team's approved services and record their owners.

![Virtual network vnet-avd-dev overview: location East US, one subnet and Azure provided DNS service; subscription name and network IDs hidden](/img/avd/AVD-Post-03-network-ready-redacted.png)

*The existing VNet is in East US and uses Azure-provided DNS. The screenshot shows the top of the VNet overview only. This is an inventory check, not a connectivity test.*

| Dependency | Preparation decision |
|---|---|
| Session-host network | Record the VNet, subnet, region and network owner. The virtual network must be in the same Azure region as the session hosts. Confirm available address space before adding hosts. |
| DNS and identity | Record the DNS service. If the chosen design uses AD DS or Entra Domain Services, confirm access to the required domain controllers and DNS servers. |
| Outbound access | Identify who owns outbound routing and filtering. The later network build must allow the required AVD endpoints. |
| Applications and profiles | Identify the application/data locations and intended profile-storage service. Record who supplies their access and connectivity. |
| Monitoring | Agree where AVD diagnostics will be collected and who reviews alerts. Reuse an approved logging destination where suitable. |

**Our starting point:** the existing VNet is identified. In our check it had no peerings configured (a peering is a link that lets two virtual networks communicate directly), so we have not established a shared hub dependency. The peerings list and the VM overview are not pictured above. The VM overview flagged default outbound access. Default outbound access means Azure gives a VM a public outbound IP address automatically when no explicit outbound method is set. That address is owned by Microsoft and can change without notice. Subnets in new virtual networks created with the API version released after 31 March 2026 are private by default, and existing virtual networks are not changed. A later networking step will select and validate an explicit outbound design. Do not treat this inventory as proof of enterprise network readiness.

## 3. Confirm the user's licensing before desktop deployment

An Azure subscription pays for infrastructure. AVD access rights are a separate licensing decision.

For Windows 10 or Windows 11 desktops used for internal commercial purposes, these licenses make a user eligible:

| Eligible license family | Listed options |
|---|---|
| Microsoft 365 | E3, E5, A3, A5, F3, Business Premium, Student Use Benefit |
| Windows Enterprise | E3 or E5 |
| Windows Education | A3 or A5 |
| Windows VDA | Per user |

Confirm the exact eligible product assigned to every test user. Similar product names are easy to confuse: the list names Microsoft 365 E3, not Office 365 E3, so check the exact product name on the user.

Contractors working for an organization can fall under internal commercial use. Selling application access to customers is a different scenario: external commercial use has per-user access pricing, a pay-as-you-go charge for each external user, billed by enrolling an Azure subscription. Internal means your own staff and contractors. External means your customers use your application. Do not select that pricing simply because a user is a contractor or guest. Windows Server hosts have separate RDS licensing requirements.

AVD access licensing also does not remove the Azure charges for VMs, disks, storage and networking.

### Existing user: inspect the assignment

1. In the Azure portal, open **Microsoft Entra ID > Users**, select the candidate user and open **Licenses**.
2. Read the product, state and assignment path. This is a read-only inspection.
3. For assignments or errors that need fixing, use the Microsoft 365 admin center: **Users > Active users > select the user > Licenses and Apps**. Use the appropriate licensing administrator account.
4. Before assigning a product, check available seats, the user's usage location (the country or region set on the account; an invalid one can make an assignment fail) and the reported error.


![Licenses page of the test user in Microsoft Entra reading No license assignments found, with a note that changes are made in the M365 admin center; account name and directory name hidden](/img/avd/AVD-Post-03-license-redacted-v2.png)

*The selected user shows No license assignments found. This does not confirm production AVD licensing.*

### Confirm the Dev/Test route used here

This development subscription shows offer ID **MS-AZR-0063P**. Visual Studio subscribers can use Azure Dev/Test credits to run Azure Virtual Desktop workloads, but no page I read states which offer ID those credit subscriptions carry, so the link between this offer ID and the Dev/Test benefit is unconfirmed. We read the actual offer ID, rather than relying on the subscription name or a dev tag.

1. Open **Subscriptions > selected subscription > Overview**.
2. Read **Offer ID** and **Status**. Compare the offer with the published Azure Dev/Test terms.
3. Confirm what the users will do. In an Azure Dev/Test subscription, users may connect without a separate license to run acceptance tests or give feedback. Be aware that the page for Visual Studio subscribers says Azure Dev/Test credits can pay for Azure Virtual Desktop usage but that access still requires eligible user licenses, so the two pages need reconciling for a Visual Studio subscription.

![Subscription overview with status Active and Offer and Offer ID rows present; the subscription name, subscription ID, directory, offer name and offer ID are hidden](/img/avd/AVD-Post-03-offer-redacted.png)

*The subscription overview shows status Active. The offer name and offer ID are hidden here, because the offer is unconfirmed licensing detail that this figure does not establish.*

**Our result:** the subscription shows offer MS-AZR-0063P. If that offer counts as an Azure Dev/Test subscription, the test user may be able to connect for acceptance tests without a separate license; confirm this in the Azure Dev/Test terms before relying on it. The test user still has zero assigned product licenses; no Microsoft 365 license was assigned. No page I read states that this offer qualifies, so treat it as unconfirmed. For a production deployment, confirm the eligible user entitlement before providing desktops.

### New user: confirm the licensing route first

If the user does not exist yet, confirm the eligible product and an available seat with the licensing owner. User creation and assignment follow the identity decision. Record this as planned, rather than already assigned.

For Windows Enterprise, Education or VDA arrangements managed outside this screen, obtain confirmation from the licensing owner.

## 4. Check the administrator's permissions at the right scope

There are two administration systems to distinguish. **Microsoft Entra roles** manage directory tasks, such as creating users. **Azure RBAC roles** manage Azure resources, such as a host pool or VM. RBAC means role-based access control.

An Azure subscription Owner is not automatically a Microsoft Entra user administrator. A Microsoft Entra Global Administrator does not automatically receive access to every Azure resource.

For the later standard-management AVD deployment, check the following permissions or their equivalent. This table is for these tasks; networking, storage and additional integrations have their own access requirements.

| Task | Access to check |
|---|---|
| Create host pools, workspaces and application groups | Desktop Virtualization Contributor on the target resource group or subscription. |
| Create session-host VMs | Virtual Machine Contributor on the target resource group or subscription. |
| Assign users/groups to an application group | Microsoft.Authorization/roleAssignments/write at that scope. User Access Administrator and Owner include it. |
| Register a resource provider | register/action at subscription scope; included in Contributor and Owner. |
| Create a budget on the resource group | Contributor, Cost Management Contributor or Owner on that resource group. |
| Create the test user | User Administrator in the Microsoft Entra directory. |
| Create/manage the ordinary test security group | Groups Administrator or User Administrator in the Microsoft Entra directory. |

The account you inspect below is the human administrator. Later, we will separately check the identity used by Terraform and the operations its deployment needs. A deployment identity is the user, application or managed identity under which the code runs.

### Inspect the access you already have

1. Open the target subscription or resource group.
2. Select **Access control (IAM) > Check access**. Read your assignments in the current view. If your portal shows the previous layout, select the link under Check access that offers the previous view.
3. Read both direct and inherited assignments. Record the role and where it was assigned.
4. If your organization uses eligible PIM roles, activate the approved role for the task. PIM is Privileged Identity Management: a process for activating eligible privileged access when needed.



![Access control (IAM) page with three active assignments: Owner on this resource, Owner inherited from a management group and User Access Administrator inherited from root; membership and subscription name hidden](/img/avd/AVD-Post-03-iam-redacted.png)

*The current view shows direct Owner, inherited Owner and inherited User Access Administrator assignments. Read the Scope column, not just the role name.*

**What this tells us:** this lab administrator has broad access. The portal also flags elevated access at root scope. These existing assignments are evidence of the current environment, not a production permission template. Have the access owner review unnecessary elevation; grant the deployment identity only the operations and scope it needs.

**Check the result:** access covers the scope where you will deploy. A role on one resource group does not grant access to a neighboring group. Checking a parent scope also does not list assignments made only on its child resources.

If something is missing, give the access owner the task, required permission and target scope. Use the narrowest scope that supports the work. The [Identity and Access](https://adnanasiddiqui.com/azure-landing-zone/identity-and-access-in-the-landing-zone/) post explains the shared access foundation.

## 5. Prepare the test user's group membership

Use an existing suitable identity before creating another account. **Active Directory Domain Services (AD DS)** is the Windows domain directory. A synchronized user has an identity maintained in another directory and synchronized into Microsoft Entra ID. A cloud-only user is created directly in Entra ID.

1. Open **Microsoft Entra ID > Users** in the verified tenant and select the test user.
2. Record its sign-in name, called the **user principal name (UPN)**, and object ID privately.
3. Open **Properties** and check the identity's source. Here, the test user shows **On-premises sync enabled: Yes**. We reuse this synchronized account. The Properties tab is not pictured; the screenshot below shows the Overview tab.
4. Check its directory roles and licensing route. Use a non-administrator for desktop testing.

![Test user overview: account enabled, 1 group membership, 0 assigned roles and 0 assigned licenses; account name, user principal name and object ID hidden](/img/avd/AVD-Post-03-user-redacted.png)

*The test account is Enabled, has one group membership, zero assigned directory roles and zero assigned product licenses. Whether the Dev/Test route above covers the planned acceptance test is still to be confirmed.*

### Check what the group already grants

1. Open **Microsoft Entra ID > Groups > All groups** and select **AVD_Users**.
2. Check that this is the intended security group. Its membership type is **Assigned**.
3. Open **Azure role assignments** before adding a user. Understand the permissions the user will receive through this group.

![AVD_Users Azure role assignments: Desktop Virtualization User on an application group, Storage File Data SMB Share Contributor on a storage account and Virtual Machine User Login on two virtual machines](/img/avd/AVD-Post-03-group-access-redacted.png)

*These assignments already existed. Adding the test user did not create new role assignments.*

| Existing role | Scope in this environment |
|---|---|
| Desktop Virtualization User | Application group avd-dag-avd-dev |
| Virtual Machine User Login | Session-host VM avdsh-01 |
| Virtual Machine User Login | Session-host VM avdsh-02 |
| Storage File Data SMB Share Contributor | Storage account avddevprofiles00001 (the screenshot cuts off the share name) |

These are different access layers: the published desktop, Windows sign-in and the profile share. Their presence is useful preparation; successful sign-in and profile creation still need a functional test.

### Add the selected user and verify the saved result

1. In **AVD_Users**, open **Members > Add members**.
2. Search for the test user's account name. Match the account against the private identity record before selecting it.
3. Select the account, then **Select** to save the membership.
4. Refresh **Members** and check that the test user appears in the saved member list. The screenshot below hides the account names.

![AVD_Users Members page listing five direct members of type User; all five account names are covered by grey boxes; the Email column is empty](/img/avd/AVD-Post-03-members-redacted.png)

*The group now contains five members. Their account names are covered with solid boxes. This is the saved result.*

For a fresh environment, creating a security group and adding a user does not grant desktop access. The required assignments must be configured for the chosen identity, session-host and storage design. We will explain those decisions in the following posts. Here, we reused an existing access group after inspecting its assignments.

## 6. Prepare the subscription for the workload

A **resource provider** makes a service's resource types available to an Azure subscription. AVD uses **Microsoft.DesktopVirtualization**.

1. Open **Subscriptions**, then the verified subscription.
2. Select **Resource providers** and search for **Microsoft.DesktopVirtualization**.
3. If it is **NotRegistered**, select it and **Register**, using an account with subscription-level registration permission.
4. Refresh and check for **Registered**.



![Resource providers list filtered to Microsoft.DesktopVirtualization with status Registered; subscription name hidden](/img/avd/AVD-Post-03-provider-redacted.png)

*Microsoft.DesktopVirtualization was already Registered. No registration change was required.*

Register the providers required by the actual deployment; do not register every service as a preparation shortcut.

### Check quota in the intended host region

A **quota** is an allocation limit. For VM vCPUs, both the total regional quota and the selected VM-family quota matter. Existing consumption uses part of each allowance.

1. From the subscription, open **Usage + quotas**. You can also use **Quotas > My quotas** to inspect quotas across subscriptions.
2. Filter to **Compute** and the intended host region.
3. Search for **Total Regional vCPUs**, then separately check the family you plan to use. A VM family is a group of VM sizes that share one quota. Record usage, limit and remaining allowance.

Our existing session host **avdsh-01** is in **East US**, using **Standard D4s v5** with four vCPUs. We checked the corresponding **Standard DSv5 Family vCPUs** quota in that same region.

![Usage + quotas filtered to Compute in East US: Total Regional vCPUs 8 of 20 (40%) and Total Regional Spot vCPUs 0 of 20; subscription name hidden](/img/avd/AVD-Post-03-quota-redacted.png)

*East US: Total Regional vCPUs shows 8 of 20 used, leaving 12. The Spot allowance is a separate row.*

4. Keep the same region selected, then search for the matching VM family. Do not use another family's allowance.

![Usage + quotas filtered to Compute in East US: Standard DSv5 Family vCPUs 8 of 20 (40%); subscription name hidden](/img/avd/AVD-Post-03-quota-family-redacted.png)

*East US: Standard DSv5 Family vCPUs also shows 8 of 20 used, leaving 12.*

For example, adding two more 4-vCPU hosts would require eight additional vCPUs. At this check, both allowances have room for that increase. This is quota arithmetic, not a user-capacity or production sizing recommendation. Existing consumption is already included; do not count the existing hosts again as new capacity.

Quota and Azure capacity are separate. Available quota does not guarantee that a VM size can be allocated in the selected region or zone. Recheck both quota tiers if the later design changes the region or VM family.

### Create and verify the workload budget

Our agreed budget is **$106 per billing month** for **rg-avd-dev**. This is the amount chosen for this development environment, not a recommended production budget.

1. Open **Resource groups > rg-avd-dev > Budgets**. Check the resource-group scope before selecting **Add**.
2. Enter **budget-avd-dev**. Select **Billing month** and enter **106 USD**.
3. Check the evaluation start and expiry dates. The saved budget uses the billing period starting **18 September 2026** and expires **17 September 2028**. Choose dates appropriate to your own environment.
4. Continue to the alert settings and enter the following conditions.

| Alert type | Threshold | Amount |
|---|---|---|
| Actual cost | 80% | $84.80 |
| Actual cost | 100% | $106.00 |
| Forecast cost | 100% | $106.00 |

5. Add the agreed cost owner's email recipient. We used the signed-in owner's address; it is hidden in the published evidence. No action group (a saved list of people or tools to notify) was selected.
6. Select **Create**. Open **budget-avd-dev** from the saved budget list and verify its scope, amount, reset period, alert conditions and recipient.

![Budget summary for budget-avd-dev: scope rg-avd-dev, 106 USD, resets billing month, created 9/18/2026, expires 9/17/2028, evaluated spend 0.00 USD](/img/avd/AVD-Post-03-budget.png)

*The saved budget is scoped to rg-avd-dev, with a $106 amount and a billing-month reset. The portal rounds the 80% amount to $85 in its alert display.*

![Budget alert conditions: actual cost 80% ($85), actual cost 100% ($106), forecasted cost 100% ($106), action group None; recipient email hidden; subscription name hidden](/img/avd/AVD-Post-03-budget-alerts-redacted.png)

*The saved configuration contains 80% and 100% actual-cost alerts, a 100% forecast alert and an email recipient. The recipient's address is hidden. The header of this screenshot reads Subscription, but the Scope row inside the budget reads rg-avd-dev (Resource group).*

**Read the scope carefully:** this budget covers the workload resource group. Resources in other groups, shared platform services and separate licensing costs need their own cost ownership and appropriate budget scopes. This is not a budget for every cost associated with AVD.

A billing month can differ from a calendar month for Visual Studio subscriptions. Use the selected reset period when interpreting an alert. Cost data can take 8 to 24 hours to appear, and budgets are evaluated every 24 hours. A newly created budget showing zero evaluated spend does not prove the resources have incurred no charges.

A budget sends alerts; it does not stop consumption. The cost owner must review the alert and act. Keep a retirement plan for the lab and a cost-review process for production. Record this as an existing portal-managed budget so a later Terraform deployment does not create a duplicate.

## 7. Check policies and record the preparation result

**Azure Policy** evaluates resources against assigned rules. An **initiative** groups several policies. An assignment specifies where those rules apply. A rule that audits a resource is different from one that denies a deployment.

### Read the rules that apply to the workload

1. Open **Subscriptions > selected subscription > Policies**, then **Assignments**.
2. Check the scope and filters. Include applicable parent assignments when reviewing the workload's rules.
3. Open each relevant assignment. Read its scope, excluded scopes, enforcement mode and parameters. Check any exemptions that apply.
4. Record region, tag and resource-type requirements when they are assigned. Use these values in the later deployment configuration.
5. Open **Compliance** to inspect reported findings. A successful deployment does not mean the environment meets every policy.

![Azure Policy Assignments page at subscription scope: 1 total assignment, 1 initiative assignment (ASC Default) and 0 policy assignments; subscription name hidden](/img/avd/AVD-Post-03-policy-redacted.png)

*The checked subscription view shows one initiative assignment, ASC Default, and zero standalone policy assignments.*

**Our result:** the assignment detail page (not pictured) describes ASC Default as the default security initiative of Microsoft Defender for Cloud (formerly Security Center). It has subscription scope, no excluded scopes and Default enforcement. The assignment list did not show separate region, required-tag or allowed-resource-type assignments. Existing tags alone are not evidence of tag enforcement.

The subscription Compliance view reported the initiative as **Non-compliant**. This preparation check is not a production compliance sign-off. Review the relevant findings with the security owner before production use. We did not change policies or create exemptions to hide findings.

### Keep one readiness record

Keep IDs and private addresses in your build notes. The table below records what we actually checked or changed, and where the next design decision belongs.

| Preparation item | Result in this walkthrough |
|---|---|
| Tenant and subscription | Directory association checked; subscription Active. |
| Workload placement | Existing rg-avd-dev inspected; East US metadata location and development tags recorded. |
| Licensing route | Offer MS-AZR-0063P read from the portal; Dev/Test eligibility still to be confirmed against the Azure Dev/Test terms. The test user has no assigned product license. Production needs eligible entitlement. |
| Administrator access | Existing direct and inherited assignments inspected. Broad lab access is not the production role design. Terraform access is checked when the infrastructure code is prepared. |
| Test identity and group | Existing synchronized test user reused; saved membership in AVD_Users verified. Existing group assignments inspected. |
| AVD provider | Microsoft.DesktopVirtualization Registered. |
| Region and VM-family quota | East US regional and Standard DSv5 allowances each show 8 of 20 used; 12 vCPUs remain at this check. |
| Platform dependencies | Existing vnet-avd-dev/snet-sessionhosts and Azure-provided DNS recorded. Identity, outbound connectivity and logging decisions feed the following posts. |
| Policy check | ASC Default audit initiative inspected; non-compliance reported. No production compliance approval claimed. |
| Cost controls | Saved rg-avd-dev budget: $106 per billing month, three alert conditions and owner email recipient verified. |

You now have the deployment context, test identity, cost control and existing dependencies recorded. Next, choose the supported identity model and plan the network. Recheck quota if that design changes the region or VM family.

## 8. Resolve readiness checks and continue

| What you see | What to inspect first |
|---|---|
| The subscription is missing | Current directory, subscription filters and your access to that subscription |
| CLI shows another subscription | Explicitly select the intended subscription and inspect az account show again |
| User creation is unavailable | Directory role, not just an Azure subscription role |
| You can create resources but cannot assign access | Role-assignment permission at the intended scope |
| A license assignment fails | Available seats, usage location and the reported assignment error |
| The group exists but the user is absent | Membership in that exact tenant and group |
| Registration is denied | Subscription-level provider-registration permission |
| Planned VM deployment exceeds quota | Both total regional and VM-family allowances |
| Deployment is denied by policy | The reported assignment, scope, effect and parameters; work with its owner |

Keep this readiness record for the next posts. This walkthrough changed the selected user’s group membership and created a workload budget. Existing infrastructure and provider registration were inspected. Preserve shared platform services during any later cleanup.

For production, confirm production licensing and approved permissions for the selected design. The preparation completed here does not prove a successful desktop sign-in or working profile storage; those checks belong to the deployment and validation steps later in the series.

Next: [Choose the Right Identity Model for Azure Virtual Desktop](/azure-virtual-desktop/choose-the-right-identity-model/).

Go deeper: [How Azure Virtual Desktop Fails](/azure-virtual-desktop/how-azure-virtual-desktop-fails/).

## Sources

[Prerequisites](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites), [licensing](https://learn.microsoft.com/en-us/azure/virtual-desktop/licensing) and [built-in roles for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/virtual-desktop).
