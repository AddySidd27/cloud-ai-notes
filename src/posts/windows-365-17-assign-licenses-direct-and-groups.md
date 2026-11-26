---
title: "Assign Windows 365 Licenses: Direct Assignment and Groups"
seoTitle: "Assign Windows 365 Licenses: Direct and Group-Based"
layout: post.njk
permalink: /windows-365/assign-licenses/
order: 216
part: 17
tags: w365-series
deck: "Assign a Windows 365 license to a user or to a group, know the group licensing limits, and keep the license and the provisioning policy group in step."
---

Before a user can use a Cloud PC, someone must assign a Windows 365 license to that user. This article is for the administrator who does that. It shows the ways to assign the license, the portal steps for a single user and for a group, the rules and limits for group licensing, and how the license links to the provisioning policy group.

A Cloud PC is also tied to a provisioning policy. Provisioning policies require users to be part of specific Microsoft Entra ID groups to receive their Cloud PCs. So a user needs two things: a license, and a place in the group that the policy is assigned to. The Cloud PC needs both, so check both.

It covers Windows 365 Enterprise. Windows 365 Flex works differently, and that part is short. The article does not repeat which other licenses each user needs or how Flex licenses are counted. The [licensing article](/windows-365/licensing/) covers both.

![Requirement 1: a Windows 365 Enterprise license reaches the user by direct assignment or by group-based licensing. Requirement 2: the user is a member of the group that a provisioning policy is assigned to. With both in place the Cloud PC shows Provisioned. If the license or the policy link is removed, the Cloud PC keeps working for seven days in a grace period, then it is deprovisioned.](/img/windows-365/windows-365-assign-licenses.svg)

*Source: [Assign licenses](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses), [Assign or unassign licenses to a group in the Microsoft 365 admin center](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-group-licenses?view=o365-worldwide) and [Troubleshoot Windows 365 Enterprise Cloud PC grace period issues](https://learn.microsoft.com/en-us/troubleshoot/windows-365/troubleshoot-windows-365-enterprise-cloud-pcs-grace-period-issue).*

## Key terms

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop that Windows 365 gives to a user. |
| Windows 365 Enterprise | The Windows 365 edition this article covers. Before a user can use a Cloud PC, you assign a Windows 365 license to that user. |
| Windows 365 Flex | An edition whose licenses are assigned to your tenant and shared across Cloud PCs. The [editions article](/windows-365/editions/) explains the editions and modes. |
| Tenant | Your organization's dedicated instance of Microsoft Entra ID. It holds the organization's users and groups. |
| Windows 365 license | The license a user needs before they can use a Windows 365 Enterprise Cloud PC. The portal calls it a product, a subscription or a license on different pages. |
| Role | An administrator role that decides what you can do in a portal, such as License Administrator. |
| Direct assignment | You assign the license to one user yourself. |
| Group-based licensing | You assign the license to a group. The members of the group get the license. |
| Microsoft 365 admin center | The portal where you manage licenses. |
| Microsoft Entra admin center | The portal for Microsoft Entra ID, the Microsoft identity service that holds users and groups. |
| Microsoft Intune admin center | A third portal, where you manage Cloud PCs and provisioning policies. |
| Provisioning policy | The settings that tell Windows 365 how to create Cloud PCs for the users in a group. See the [provisioning article](/windows-365/provision/). |
| Nested group | A group that contains other groups. Group-based licensing does not support them. |
| Usage location | A setting on the user that says where the user is. Some Microsoft services are not available in all locations. |
| Reprocess | A button that asks group-based licensing to try the assignment again. |
| Grace period | Seven days during which a Cloud PC keeps working after its license or policy link is removed. After that it is deprovisioned. |
| Deprovisioned | The Cloud PC is removed from your environment. This deletes the operating system and data, and it cannot be undone. |
| Provisioned | A Cloud PC status. You see it in the **Status** column of **All Cloud PCs** in the Intune admin center. |

## Ways to assign a Windows 365 Enterprise license

You can use any of these methods:

| Method | Use it for |
|---|---|
| Microsoft 365 admin center | Individual users |
| Microsoft Entra admin center | Group license assignments |
| PowerShell or Microsoft Graph | Direct licenses for a list of individual users, with scripts or the Graph interface instead of a portal |

You can also assign licenses to groups in the Microsoft 365 admin center. The portal steps below use it for both a user and a group, so you stay in one portal.

You need Windows 365 licenses that are not yet assigned. If there are not enough, assignment fails with a Not enough licenses error (see the error table below). The [licensing article](/windows-365/licensing/) explains what to buy.

### Windows 365 Flex

Flex licenses are assigned to your tenant and shared across Cloud PCs. You assign them by selecting a Microsoft Entra group when you create the provisioning policy. The [editions article](/windows-365/editions/) explains the Flex modes.

## Assign a license to a user

You must be at least a License Administrator.

1. Sign in to the Microsoft 365 admin center.
2. Go to **Billing** > **Licenses**.
3. On the **Subscriptions** tab, select the Windows 365 license you want to assign.
4. On the **License details** page, select the **Users** tab, then select **Assign licenses**.
5. In the **Assign licenses to users** pane, type a name and choose it from the results. You can add up to 20 users at a time.
6. To assign or remove access to specific items in the license, select **Turn apps and services on or off**.
7. Select **Assign**, then close the right pane.

## Assign a license to a group

You must be at least a Groups Administrator, License Administrator or User Administrator. You can use security groups, mail-enabled groups or Microsoft 365 groups. This is about the license. The group that a provisioning policy uses is covered in the [provisioning article](/windows-365/provision/).

1. Sign in to the Microsoft 365 admin center.
2. Go to **Billing** > **Licenses**.
3. On the **Licenses** page, select **Assign licenses**.
4. In the side panel, search for the group and select its name from the list.
5. Select the subscription the licenses should come from.
6. To assign or remove access to specific items in the license, select **Turn apps and services on or off**.
7. Select **Assign licenses**.

You can also start from the product. Select the Windows 365 license on the **Subscriptions** tab, open the **Groups** tab, and select **Assign licenses**. Search for the group, select its name from **Suggested groups**, then select **Assign**.

To remove a group license, go to **Billing** > **Licenses**, select the product, find the group in the list, select the three dots on its row, select **Unassign**, and confirm.

## Group-based licensing rules and limits

| Rule or limit | What it means |
|---|---|
| Nested groups | Not supported. If you assign a license to a nested group (a group that contains other groups), only users in the first-level group get the license. |
| Usage location | Before a license can be assigned to a user, the administrator must specify the user's location. With group-based licensing, a user with no location gets the location of the tenant. |
| Large groups | Changing licenses for a large group, such as 100,000 users, can affect performance. In high load, license changes and membership changes can take a long time to process. |
| Number of groups (Microsoft 365 admin center) | You can assign licenses to a maximum of 20 groups at a time. |
| Reprocess (Microsoft 365 admin center) | **Reprocess** tries up to 20 users at a time. |
| Long lists (Microsoft 365 admin center) | The lists of users who did and did not get licenses show 999 users at a time. Scroll to the bottom to load the next set. |

If your users are in several locations, set the location when you create each user.

## When group assignment fails

A group license error is not shown at once, the way a direct assignment error is. Group-based licensing records the failure on the user and shows it later in the portal.

To see errors:

1. In the Microsoft 365 admin center, go to **Billing** > **Licenses**.
2. Select the product.
3. Select the **Errors & issues** tab. It lists the users with problems.
4. Select a user to see the error type.

Common group licensing errors and their fixes (a selection):

| Error | Problem | Fix |
|---|---|---|
| Not enough licenses | There are not enough available licenses for one of the products assigned to the group. | Buy more licenses, remove unused direct assignments, or free licenses from other groups or users. |
| Usage location isn't allowed | Some Microsoft services are not available in all countries or regions. The user's usage location is either missing or set to an unsupported location. | Set the correct usage location on the user, or remove users in unsupported locations from the licensed group. If a user has no usage location, group-based licensing uses the tenant location. |
| Conflicting service plans | A service plan in one product conflicts with a service plan already assigned to the user through another product. | Disable one conflicting plan, remove the redundant direct license, or adjust the group license assignment. |
| More than one product license assigned to a group | If one product fails because of insufficient licenses, conflicts or dependency issues, the other products in that group might not be assigned either. | Inspect the affected users and determine which product caused the failure. |

You might need to reprocess after you fix the cause:

1. Go to **Billing** > **Licenses**.
2. Select the license product with the problem.
3. Select **Errors & Issues**.
4. Correct the cause for each group or user listed.
5. Select the affected group or user and choose **Reprocess**.

## Move a user between licensed groups

When you move a user from one licensed group to another, the order matters. If you remove the user from the old group first, the user is unlicensed until group-based licensing finishes the new group. In large tenants or under high load, that can last longer than expected.

1. Add the user to the new group first.
2. Confirm the new license shows on the user's **Licenses** page.
3. Remove the user from the old group.

Resizing a Cloud PC whose user has a group license has its own steps. The [Cloud PC lifecycle article](/windows-365/cloud-pc-lifecycle/) covers them.

## The license and the provisioning policy group

A Windows 365 license is not enough on its own. The Cloud PC is tied to two things:

1. The license assignment, direct or from a group.
2. The connection to the provisioning policy. The user must be a member of a group that is assigned to the policy.

(The other licenses a user needs are in the [licensing article](/windows-365/licensing/).)

If either one is lost, the Cloud PC enters a grace period. This happens when:

- the user is removed from the group that gives the license,
- the direct license is removed from the user, or
- the user is removed from the group assigned to the provisioning policy.

The Cloud PC keeps working for seven days. Then it is deprovisioned, which deletes its operating system and data and cannot be undone. Reassign the license and the group membership within that time. How to bring a Cloud PC back and how to end a grace period early are in the [grace period article](/windows-365/grace-period-unused-licenses/).

This part is about the policy side, not the license. It uses a different portal, the Microsoft Intune admin center. To assign the policy to a group again:

1. Select **Devices** > **Windows 365**, then **Provisioning policies**.
2. Open the policy and, under **Assignments**, select **Edit**.
3. Select **Add groups**, choose the groups, then select **Select**.
4. Select **Next** and **Update**.

Nested groups are not currently supported for the policy assignment either.

To add a user to the group, sign in to the Microsoft Intune admin center and select **Groups** > **All groups**. Choose the group, select **Members** > **Add members**, add the users who need Cloud PCs, and select **Select**.

## Common mistakes

- **Using a nested group for the license.** Only users in the first-level group get the license.
- **Leaving usage location empty on a user who gets the license from a group.** The user gets the tenant location. Some services are not available in all locations.
- **Not having enough licenses for the group.** This is one of the group licensing errors. Check **Errors & issues**.
- **Removing a user from the old group before the new one has applied.** The user is unlicensed until processing finishes.
- **Fixing the cause but not reprocessing.** You might need to select **Reprocess** after you fix the cause.
- **Assuming a license is enough.** The user must also be in the group assigned to the provisioning policy.

## How to validate this in your environment

1. In the Microsoft 365 admin center, go to **Billing** > **Licenses** and select the Windows 365 product. Check that the user or the group is licensed.
2. Open the **Errors & issues** tab and confirm no users are listed for the product.
3. Confirm the user's **Licenses** page shows the Windows 365 license.
4. In the Intune admin center, open **Devices** > **Windows 365** > **Provisioning policies**, open the policy, and confirm the user's group is listed under **Assignments**.
5. Open **All Cloud PCs** and check in the **Status** column that the Cloud PC shows **Provisioned**.
6. For a group move, follow add, confirm, remove, and check the user's **Licenses** page after each step.

## Sources

- [Assign licenses](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses)
- [Assign or unassign licenses to a group in the Microsoft 365 admin center](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-group-licenses?view=o365-worldwide)
- [Troubleshoot Windows 365 Enterprise Cloud PC grace period issues](https://learn.microsoft.com/en-us/troubleshoot/windows-365/troubleshoot-windows-365-enterprise-cloud-pcs-grace-period-issue)
