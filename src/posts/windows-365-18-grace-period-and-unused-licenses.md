---
title: "Windows 365 Grace Period and Unused Licenses"
layout: post.njk
permalink: /windows-365/grace-period-unused-licenses/
order: 217
part: 18
tags: w365-series
deck: "Find Cloud PCs that nobody uses, understand what starts and ends a grace period, and remove or restore Cloud PCs on purpose."
---

Cloud PCs that people rarely use are a cost you can reduce. Two things help you do that. The first is the **grace period**, a short waiting time that starts when a Cloud PC loses its license or its link to a provisioning policy. The second is the **Cloud PC utilization report**, which shows which Cloud PCs are barely used.

This article is for administrators who run Windows 365 Enterprise. After reading it you can say what starts a grace period, bring a Cloud PC back, end a grace period on purpose for one or many Cloud PCs, and find Cloud PCs that are good candidates for clean-up. The three ways a grace period starts are described for Enterprise Cloud PCs. Bulk deprovisioning also applies to Flex Cloud PCs created in Dedicated mode. The utilization report lists Enterprise, Flex Dedicated and Flex Shared Cloud PCs.

The basic idea of a grace period, and how it fits with resize and reprovision, is in [The life of a Cloud PC](/windows-365/cloud-pc-lifecycle/). License types and how to count them are in [Windows 365 licensing](/windows-365/licensing/). Other Intune reports are in [Monitor Windows 365](/windows-365/monitoring/), and the full steps for assigning licenses are in [Assign Windows 365 licenses](/windows-365/assign-licenses/). This article does not repeat them. It adds the causes, the way back, the bulk steps and the clean-up routine.

## Key terms

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop that Windows 365 runs in the cloud for a user. |
| Grace period | Seven days in which a Cloud PC that lost its license or provisioning policy link keeps working before it is deprovisioned. |
| Deprovision | Remove the Cloud PC. The operating system and data are deleted and the Cloud PC is no longer available. |
| Provisioning policy | The set of settings Windows 365 uses to create Cloud PCs. It is assigned to Microsoft Entra ID groups. |
| Microsoft Entra ID group | A group of users in Microsoft Entra ID, the Microsoft identity service. Groups can carry licenses and receive provisioning policies. |
| Group-based licensing | Giving a license to a group so that every member gets it. |
| Direct assignment | Giving a license to one user by name. |
| Status | The state shown for each Cloud PC in the **Devices** > **Windows 365** > **All Cloud PCs** list in the Intune admin center, for example **In grace period** or **Provisioned**. |
| Provisioned | The status a Cloud PC should show after you fix the cause of a grace period. Users can sign in to it. |
| Intune admin center | The Microsoft Intune admin center, the web portal where you manage Cloud PCs and open the reports in this article. |
| Microsoft 365 admin center | The web portal where you assign Windows 365 licenses. |
| License Administrator | The lowest role that can assign licenses in the Microsoft 365 admin center. |
| Time connected | The hours a user was connected to a Cloud PC, as shown in the utilization report. |
| User UPN | The user's identifier, in the form of an email address. It is a column in the utilization report. |
| Histogram | A chart in the utilization report that counts Cloud PCs in each range of time connected. |
| Nested group | A group placed inside another group. |
| Flex | Windows 365 Flex is a Windows 365 offering. It is listed as Flex dedicated or Flex shared in the report. Bulk deprovision works for Flex Cloud PCs created in Dedicated mode. See [Windows 365 licensing](/windows-365/licensing/). |

## What starts a grace period

A Cloud PC enters a grace period when a valid Windows 365 license is removed from the user, or when the link between the user and the provisioning policy is broken. This can happen in three ways:

| What changed | Where the problem is |
|---|---|
| The user was removed from the group that gives them the license | Group-based license |
| The direct license assignment was removed from the user | Direct assignment |
| The user was removed from the group assigned to the provisioning policy that created the Cloud PC | Provisioning policy assignment |

The same happens if a group is removed from a provisioning policy: all Cloud PCs for the members of that group enter a seven-day grace period. This affects every member at once, so check before you change a policy assignment. These causes are described for Enterprise Cloud PCs.

![Three events start a seven-day grace period on an Enterprise Cloud PC: removal from the license group, removal of a direct license, or removal from the provisioning policy group. You restore the cause or deprovision. The utilization report helps find unused Cloud PCs.](/img/windows-365/windows-365-grace-period.svg)

*Source: [Troubleshoot Windows 365 Enterprise Cloud PC grace period issues](https://learn.microsoft.com/en-us/troubleshoot/windows-365/troubleshoot-windows-365-enterprise-cloud-pcs-grace-period-issue), [Deprovision or end grace period for Cloud PCs](https://learn.microsoft.com/en-us/windows-365/enterprise/end-grace-period) and [Cloud PC utilization report](https://learn.microsoft.com/en-us/windows-365/enterprise/report-cloud-pc-utilization).*

## How long it lasts and what the user can do

The grace period lasts seven days. During that time the Cloud PC stays operational and the user can continue to use it. When the seven days end, the user is logged off, loses access, and the Cloud PC is deprovisioned.

So a grace period is a time to fix a mistake, not a lock. If you want a user cut off at once, a grace period on its own does not do that.

## Bring a Cloud PC back

To return a Cloud PC to the **Provisioned** status, check two things: the original license assignment is in place, and the connection to the provisioning policy is in place.

### Put the license back

Sign in to the Microsoft 365 admin center as at least a License Administrator and go to **Billing** > **Licenses**. On the **Subscriptions** tab, select the Windows 365 license.

- **Group-based:** on the **License details** page, select the **Groups** tab, then **Assign licenses**. Search for the group, select its name, then select **Assign**.
- **Direct:** select the **Users** tab, then **Assign licenses**. Type a name and choose it from the results. You can add up to 20 users at a time. Then select **Assign**.

### Put the policy link back

Provisioning policies need users to be members of specific Microsoft Entra ID groups. Put back whichever link was removed.

1. Check that the user is in the group. Sign in to the Intune admin center and select **Groups** > **All groups**. Open the group that goes with the provisioning policy and select **Members** > **Add members**. Add the users who need Cloud PCs and select **Select**.
2. Check that the group is assigned to the policy. Select **Devices** > **Windows 365** > **Provisioning policies** and open the policy the Cloud PC was created from. If the group is missing, under **Assignments** select **Edit**, then **Add groups**, choose the group and select **Select**. Then select **Next** and **Update**.

Nested groups (a group inside another group) are not currently supported in policy assignments.

### Check that it worked

Open **Devices** > **Windows 365** > **All Cloud PCs** in the Intune admin center. Confirm the Cloud PCs show **Provisioned** and that users can sign in.

## End a grace period early

If a Cloud PC is no longer needed, you do not have to wait seven days. Ending the grace period is destructive. Tell the user first.

### One Cloud PC

1. Sign in to the Intune admin center and select **Devices** > **Windows 365** > **All Cloud PCs**.
2. In the **Status** column, select **In grace period**, then **Deprovision now**, then **Yes**.

After **Yes**, the Cloud PC starts deprovisioning, the user loses access, and the operating system and data are deleted. This cannot be undone. Back up anything that is needed before you start. If the original provisioning policy was replaced with a different policy, the Cloud PC is reprovisioned with the settings in the new policy. The other automatic steps are in [The life of a Cloud PC](/windows-365/cloud-pc-lifecycle/).

### Many Cloud PCs

Tell the users first. This is destructive. Bulk deprovision works for Enterprise Cloud PCs and Flex Cloud PCs in Dedicated mode that are in a grace period. Data on each Cloud PC is removed and the users lose access. There are two ways to start it.

| | Provisioning policy view | Intune Bulk Action Wizard |
|---|---|---|
| Start at | **Devices**, then in **Manage W365 Cloud PCs** select **Provision Cloud PCs** | **Devices** > **All devices** > **Bulk device actions** |
| Choose | An Enterprise or Flex Dedicated provisioning policy, then its **Devices** tab, then the Cloud PCs in grace period | **Windows** as OS, **Cloud PCs** as device type and **Deprovision** as action, then **Next**, then **Add devices** |
| Action | Select **Deprovision**. Selecting several Cloud PCs sends you to the Bulk Action Wizard | Select individual devices or devices targeted to a user group |
| Finish | **Next** to see your selection, **Next** to **Review + Create**, then **Create** | Same |

When you select **Create**, the Cloud PCs are deprovisioned, all data is lost and the action cannot be undone.

In the wizard, only Enterprise or Flex Dedicated Cloud PCs that are in a grace period appear, plus Windows 365 Reserve Cloud PCs. Select only Cloud PCs in a grace period. The **Deprovision** action can be blocked if you select a provisioned Cloud PC. This rule does not apply to Reserve Cloud PCs, which this article does not cover.

## Find Cloud PCs that nobody uses

Open the **Cloud PC utilization** report in the Intune admin center: **Devices** > **Cloud PC performance** > **Cloud PC utilization**. Reviewing Cloud PCs with low use can reduce costs in two ways:

- Reassign under-used Cloud PC licenses to users who will use them more.
- Find and deprovision Cloud PCs that stay inactive for a long time.

The report covers a timespan you choose: 28, 60 or 90 days. The histogram counts Cloud PCs by time connected for that timespan:

| Group | Time connected |
|---|---|
| High | More than 80 hours |
| Average | 40 to 80 hours |
| Low | Less than 40 hours |
| None | Zero hours |

The list shows **Device name**, **User UPN** (the user's identifier, in the form of an email address), **PC type**, **Time connected**, **Date last connected**, **Date created** and **Device type** (the offering: Enterprise, Flex dedicated or Flex shared). In the list, **Time connected** is the total hours over the last four weeks. **Date last connected** is the most recent connection or sign-out, within the last 60 days.

Use **Add filters** to filter by **PC type**, **Time connected** or **Date last connected**. For one Cloud PC, select **Reports** > **Cloud PC overview** > **Cloud PC utilization**, select the device, then **Performance (preview)**. The **Time connected** section shows its usage. Select **View report** for more.

**Deprovision now** and the bulk steps apply to Cloud PCs that are in a grace period. For an Enterprise Cloud PC you decide to remove, taking away its license or removing the user from the provisioning policy group puts it in a grace period (see the table above). Remove the user from the group, not the group from the policy, or every member's Cloud PC enters a grace period. When **Status** shows **In grace period**, use **Deprovision now** or the bulk steps.

## Clean-up checklist

1. Open the utilization report for 28 days. Read the **None** and **Low** ranges in the histogram, and use **Add filters** > **Time connected** to narrow the list.
2. For each one, check **Date last connected** and ask the user or manager if the Cloud PC is still needed.
3. If it is needed, leave it. If the license would be used more by someone else, reassign it.
4. If it is not needed, make sure the data is saved elsewhere and the user knows.
5. Remove the license, or remove the user from the provisioning policy group. Open **Devices** > **Windows 365** > **All Cloud PCs** until **Status** shows **In grace period**.
6. For each Cloud PC in a grace period, decide: restore or deprovision.
7. Restore: put back whichever was removed, the license, or the provisioning policy group membership or assignment. Then confirm the status is **Provisioned**.
8. Deprovision: use **Deprovision now**, or the bulk steps for many.
9. Confirm only Cloud PCs you intended were deprovisioned.

## Common mistakes

- **Using a grace period to cut off access.** The user keeps working for seven days.
- **Selecting Cloud PCs that are not in a grace period for bulk deprovision.** The action can be blocked.
- **Using Deprovision now without telling the user or saving data.** It deletes the operating system and data and cannot be undone.
- **Fixing only the license.** A Cloud PC also enters a grace period when the user leaves the provisioning policy group, so check both.
- **Using nested groups for policy assignment.** They are not currently supported.
- **Reading the report without checking the timespan.** The choices are 28, 60 or 90 days, so check which one is selected before you decide.

## How to validate this in your environment

Use a test user and a test Cloud PC only.

1. In the Microsoft 365 admin center, note how the test user gets the Windows 365 license: group-based or direct. Open **Billing** > **Licenses**, select the license and check the **Groups** and **Users** tabs.
2. In the Intune admin center, open **Groups** > **All groups** and confirm the test user is in the group for the provisioning policy. Open **Devices** > **Windows 365** > **Provisioning policies**, open the policy and check **Assignments**.
3. Remove the license from the test user. Open **Devices** > **Windows 365** > **All Cloud PCs** and look for **In grace period** in the **Status** column. Confirm the user can still use the Cloud PC.
4. Put the license back and confirm the status returns to **Provisioned**.
5. Open the utilization report. Pick 28 days and find the test Cloud PC. Check its **Time connected** and **Date last connected**. Try the **PC type**, **Time connected** and **Date last connected** filters.
6. Only if you want to test deletion, put the test Cloud PC in a grace period again and select **Deprovision now**. Confirm the Cloud PC is no longer available.
7. To see the bulk path without running it, open **Devices** > **All devices** > **Bulk device actions** and go as far as the **Add devices** step. Do not select **Create**.

## Sources

- [Deprovision or end grace period for Cloud PCs](https://learn.microsoft.com/en-us/windows-365/enterprise/end-grace-period)
- [Troubleshoot Windows 365 Enterprise Cloud PC grace period issues](https://learn.microsoft.com/en-us/troubleshoot/windows-365/troubleshoot-windows-365-enterprise-cloud-pcs-grace-period-issue)
- [Cloud PC utilization report](https://learn.microsoft.com/en-us/windows-365/enterprise/report-cloud-pc-utilization)
