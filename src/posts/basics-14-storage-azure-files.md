---
title: "Storage Account and Azure Files Share with Identity-Based Access"
seoTitle: "Azure Files Share with Entra Sign-In: Beginner Lab"
layout: post.njk
permalink: "/azure-basics-labs/storage-azure-files/"
order: 324
tags: [azure-basics-lab]
deck: "You create a storage account and an Azure Files share, give the TestUsers group access with an Azure role, and mount the share from your Lab 12 VM without using an account key."
description: "Hard beginner Azure lab: create a storage account and file share, turn on Entra Kerberos, assign a share role, avoid the MFA error 1327 and mount the share."
---

By the end of this lab you will have a storage account and a file share in `rg-azb-lab`. Microsoft Entra Kerberos will be switched on for the account. Kerberos is a sign-in system that uses tickets. You do not need to know more yet. The `TestUsers` group will have an Azure role on the share, and your test user will have mounted the share as a drive on the Lab 12 VM, signed in with the Entra identity and not with an account key.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn. No Terraform is included, so none was run either.

This is a hard lab. There are many small steps, and each one must be done. If one is skipped, the mount fails with an error that does not name the missing step. It has two halves. Part A (Parts 1 to 5) happens in the portals and needs no VM. Part B (Part 6) happens on the VM. Between them there is a checkpoint where you can stop safely. Read the whole lab once before you start.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway tenant and subscription.
- [Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the user `testuser1` and the group `TestUsers`. The user must be a cloud-only user, which means it exists only in Microsoft Entra ID and is not synced from an on-premises Active Directory.
- [Lab 7: Azure RBAC roles](/azure-basics-labs/rbac-roles/): you give a role to a group in this lab, the same way as there.
- [Lab 8: Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/): the resource group `rg-azb-lab`.
- [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the VM `vm-azb-win01`, joined to Microsoft Entra ID, where you mount the share. It runs Windows Server 2025, which is on Learn's list of operating systems for cloud-only users. If your client were Windows 11, check the build list on Learn's Entra Kerberos page. You also need the local admin password for `azureuser` from Lab 12 and your route (A, B or C) from [Lab 11](/azure-basics-labs/your-pc-and-remote-desktop-clients/).
- The state the VM is in: after [Lab 13](/azure-basics-labs/vm-size-disk-stop-deallocate/) the VM is **Stopped (deallocated)** and there is no RDP rule. Part A does not need the VM. Part B starts with a numbered list that starts the VM, adds the rule and connects ("Connect again later" in Lab 12).
- Roles: Owner on `rg-azb-lab` (as in Lab 7) to assign Azure roles, and an administrator who can grant admin consent in Entra (Global Administrator works). The account you created in Lab 1 is normally a Global Administrator. The `azureuser` account from Lab 12 is the administrator on the VM.
- Your region from the notes sheet in [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/) (the same one as `vnet-azb`). Keep the storage account in the same region as the VM.
- Time: about 2 hours, including the waits. Cost: small if you clean up on time. The share stays almost empty. Check the current prices on the [Azure Files pricing page](https://azure.microsoft.com/pricing/details/storage/files/). A budget from Lab 3 only warns, it does not stop anything.
- Billing right now: the VM disk and `pip-azb-win01` (VM deallocated). New in this lab: a storage account, and the VM running for about an hour in Part B.

State at the start: VM Stopped (deallocated), no RDP rule. At the end: VM Stopped (deallocated) again, RDP rule removed, storage account and share kept.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name before you change anything.
- Do not use the storage account keys for this test. A key gives administrator rights on all files in the share and on everything else in the account. If you ever connected to the share with a key from the VM, unmount it and remove the saved key first, because the old connection gets in the way of the new one. If the mount fails, do not reach for the key. Fix the cause (see "The most common mistake").
- Azure CLI 2.76 or newer.
- Public network access stays on in this lab, so the VM can reach the account. That is a test setting. [Lab 18: Private endpoint and private DNS](/azure-basics-labs/private-endpoint-dns/) closes it. Do not put real files on this share.
- Only one identity source can be on for a storage account. This lab uses Microsoft Entra Kerberos.
- For cloud-only users, Learn lists Windows 11 Enterprise or Pro and Windows Server 2025, with the latest cumulative updates. Windows Server 2022 is listed only for hybrid users. The client must be Microsoft Entra joined. If you built your VM from a Windows Server 2022 image, build a Windows Server 2025 VM before you continue.
- The VM needs a temporary RDP rule while you work, as in Lab 12. You remove it again in the cleanup.
- Do not edit the Entra app that Azure creates for the account, except for the changes in this lab. Learn warns that other edits can cause errors.

## What the lab builds

![Step 1: testuser1 signs in to the VM vm-azb-win01, which asks Microsoft Entra ID for a Kerberos ticket for the storage account. Step 2: Entra ID returns the ticket. Step 3: the VM mounts the file share azbshare in the storage account stazb-digits over SMB on port 445. The role Storage File Data SMB Share Contributor, given to the group TestUsers on the share, decides what the user may do. A Conditional Access box points at Entra ID and says that no MFA policy may cover the storage account app. Entra ID and the users belong to the tenant. The VM and the storage account are in the resource group rg-azb-lab.](/img/basics/storage-azure-files.svg)

*Source: [Create an Azure classic file share](https://learn.microsoft.com/en-us/azure/storage/files/storage-how-to-create-file-share), [Enable Microsoft Entra Kerberos authentication for hybrid and cloud-only identities on Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable), [Assign share-level permissions for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-assign-share-level-permissions) and [Mount SMB Azure file share on Windows](https://learn.microsoft.com/en-us/azure/storage/files/storage-how-to-use-files-windows). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Part A: the Azure side (Parts 1 to 5, about 50 minutes, no VM needed)**

**Background: account, share and the other services.** A storage account is the top-level resource: it has a name, a region and a bill. Inside it you use services. Azure Files is a file server in the cloud. It uses SMB, the Windows file-sharing protocol, so Windows can show it as a drive letter. A file share is one shared folder inside the account. So the order is: account, then Azure Files service, then share, then folders and files. The account name must be 3 to 24 characters, only numbers and lowercase letters, and unique across all of Azure. That is why `storage` or `files` is already taken.

**Background: which type.** Two choices set the price: HDD or SSD, and how you pay. This lab uses HDD, LRS and pay-as-you-go, so an almost empty share costs almost nothing. LRS (locally redundant storage) keeps three copies in one data centre. It is the cheapest redundancy and is enough for a test. Premium (SSD) bills for reserved size from day one: do not pick it here. For a real share, read the Azure Files pricing page first.

### Part 1: Create the storage account and the share

1. Sign in to the [Azure portal](https://portal.azure.com) as your administrator. Check the tenant and subscription name at the top right.
2. Search for **Storage accounts** and select it. Select **+ Create**.
3. On the **Basics** tab set:
   - **Subscription**: your test subscription.
   - **Resource group**: `rg-azb-lab`.
   - **Storage account name**: `stazb` followed by five random digits, for example `stazb48213`. The portal tells you if the name is taken. Write the name down. You use it in almost every later step.
   - **Region**: the region you use for everything.
   - **Primary service**: **Azure Files**.
   - **Media tier**: **HDD (standard)**.
   - **File share billing**: **Pay-as-you-go file shares**.
   - **Redundancy**: **LRS**.
4. Leave the **Advanced**, **Networking**, **Data protection**, **Security** and **Encryption** tabs at their defaults. Public network access is **Enable** by default. That is fine for now.
5. Select **Review + create**, read the summary, then select **Create**. When the deployment is complete, select **Go to resource**.
6. In the service menu, under **Data storage**, select **Classic file shares**. Select **+ Classic file share**. (Some Learn pages call the menu item **File shares**.)
7. On the **Basics** tab set **Name** to `azbshare`. A share name uses lowercase letters, numbers and single hyphens. Leave **Access tier** at **Transaction optimized**.
8. Select the **Backup** tab. Clear **Enable backup**. A backup creates more resources that you would have to clean up, and this lab does not need it.
9. Select **Review + create**, then **Create**.

Check: under **Classic file shares** you see `azbshare`. On the account's **Overview** page, **Account kind** shows StorageV2 and the redundancy shows locally-redundant storage (LRS).

### Part 2: Turn on Microsoft Entra Kerberos

**Background: three things must agree.** For the mount to work, three things have to be right, checked one after the other:

1. **Who are you?** Entra ID has to give your user a Kerberos ticket for the storage account. This needs the account setting, an admin consent, a tag, a client setting on the VM and a Conditional Access exclusion. These are Parts 2, 3, 4 and 6.
2. **May you open the share?** An Azure role on the share (Part 5). With no role, access is denied.
3. **What can you do inside?** Windows permissions (ACLs) on folders and files. This lab does not change ACLs.

Learn lists limits you must know. Microsoft Entra Kerberos on Azure Files supports cloud-only identities in the public Azure cloud only. It does not support cross-tenant access. And you cannot use Windows File Explorer or `icacls` to set ACLs for cloud-only users.

10. Go to your storage account. In the service menu, under **Data storage**, select **Classic file shares**.
11. Next to **Identity-based access**, select the status, which reads **Not configured**.
12. Under **Microsoft Entra Kerberos**, select **Set up**.
13. Select the **Microsoft Entra Kerberos** checkbox.
14. Leave both boxes (domain name and domain GUID) empty. They are for companies that sync a local domain.
15. Select **Save**.

Check: go back to **Classic file shares**. **Identity-based access** now shows **Configured**.

### Part 3: Admin consent and the cloud-only group tag

Turning on Kerberos makes Azure create an app in your tenant. It is named `[Storage Account] <your-storage-account-name>.file.core.windows.net`. Two settings on it are required for cloud-only users.

16. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com) as Global Administrator. Check the tenant name.
17. Open **Entra ID** > **App registrations**. Select **All applications**. If the list is empty or the app is missing, wait a minute and refresh.
18. Select the app named `[Storage Account] <your-storage-account-name>.file.core.windows.net`.
19. Under **Manage**, select **API permissions**.
20. Select **Grant admin consent for** your directory name. This grants three permissions (openid, profile and User.Read) for all accounts in the directory. Select **Yes**.
21. Under **Manage**, select **Manifest**. The manifest is the app's settings file in JSON.
22. In the manifest editor, find the line `"tags": [],`. Change it to `"tags": ["kdc_enable_cloud_group_sids"],`. If `tags` already has values, add a comma and the new value inside the square brackets, for example `"tags": ["existing","kdc_enable_cloud_group_sids"]`. If the manifest page shows two tabs, use the one that contains the word `tags`. Select **Save**. If Save fails with an error, you probably lost a comma or a quote.

Why step 22: a Kerberos ticket can hold at most 1,010 group identifiers. For cloud-only users the ticket must carry the Entra group identifiers too, and Learn calls this tag mandatory for cloud-only identities. Without it, authentication fails.

Check: the **API permissions** page shows the three permissions with a status that says admin consent was granted. Reopen the manifest and read that `tags` holds `kdc_enable_cloud_group_sids`.

### Part 4: Keep MFA away from the storage app (the trap)

Learn says Microsoft Entra Kerberos does not support MFA for Azure file shares. If a Conditional Access policy that requires MFA covers the storage account app, you cannot reach the share, and `net use` fails with:

`System error 1327: Account restrictions are preventing this user from signing in. For example: blank passwords aren't allowed, sign-in times are limited, or a policy restriction has been enforced.`

That message names blank passwords and sign-in times, and neither is the cause. The cause is the MFA policy.

The policy from [Lab 6: Conditional Access](/azure-basics-labs/conditional-access/) targets only the two AVD apps, never **All resources**, so it does not hit the storage app. The danger is any other policy that targets **All resources** and requires MFA.

23. In the Entra admin center, open **Entra ID** > **Conditional Access** > **Policies**.
24. If the list is empty, or no policy that is **On** or **Report-only** targets **All resources** (older name: **All cloud apps**) with an MFA requirement, write "none" in your notes and go on to Part 5.
25. If one does, follow the box below.

**Only if you have such a policy.** Open the policy, then **Target resources** > **Exclude** tab > **Select excluded cloud apps**. Search for `[Storage Account] <your-storage-account-name>.file.core.windows.net`, select it and **Save**. If the app is not in the picker, stop. Do not widen or turn off the policy to get around it. Read the "Disable multifactor authentication on the storage account" section of Learn's page for Azure Files.

Check: no policy that requires MFA covers the storage app, or the app is listed under that policy's excluded apps.

### Part 5: Give TestUsers the role on the share

26. In the Azure portal, open your storage account, then **Classic file shares**, then select `azbshare`.
27. Select **Access Control (IAM)**.
28. Select **Add**, then **Add role assignment**.
29. On the **Role** tab, search for and select **Storage File Data SMB Share Contributor**. It gives read, write and delete access on files and directories in Azure Files. Select **Next**.
30. Keep **Assign access to** at **User, group, or service principal**. Select **+ Select members**, search for `TestUsers`, and select the group. Select **Select**.
31. Select **Review + assign**, then **Review + assign** again. If your page shows **Save** instead, select that.

A share-level permission change usually takes effect within 30 minutes, and sometimes longer. Do the VM steps below first. They take a while.

Check: on the **Role assignments** tab of the share, `TestUsers` appears with **Storage File Data SMB Share Contributor**.

### Checkpoint A: safe to stop here

The VM is still off, so nothing is billing for compute. Check each line before you start Part B:

| Check | Where to look |
|---|---|
| The account exists and `azbshare` is listed | Storage account > **Classic file shares** |
| Identity-based access shows **Configured** | Storage account > **Classic file shares** |
| Admin consent is granted | Entra admin center > the `[Storage Account]` app > **API permissions** |
| The tag is in the manifest | The same app > **Manifest** |
| `TestUsers` has the role | `azbshare` > **Access Control (IAM)** > **Role assignments** |

**Part B: on the VM (Part 6, about 60 minutes)**

### Part 6: Prepare the VM and mount the share

Get onto the VM. This is the routine from "Connect again later" in [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/), with the local administrator first.

- a) Start the VM. Portal: **Virtual machines** > `vm-azb-win01` > **Start**. Wait for **Running**. CLI: `az vm start --resource-group rg-azb-lab --name vm-azb-win01`.
- b) Look up your public IP again on the PC you connect from.
- c) Add the rule `allow-rdp-my-ip` to `nsg-azb-vm`: priority 1000, source your IP only, as in Lab 12 Part 5.
- d) Download the RDP file again (**Connect** > **Native RDP** > **Download RDP File**), or use the one you saved. Route C: open Remote Desktop Connection instead, type the VM's public IP as the computer, and leave the web account box unticked (the local account does not use it).
- e) Open it. When Windows asks for credentials, select **More choices**, then **Use a different account**.
- f) User name `vm-azb-win01\azureuser`, and the password from Lab 12. Do steps 32 to 35 below as this local administrator.
- g) Restart the VM from inside (step 36).
- h) After the restart, reconnect as `testuser1` (step 38).

32. In PowerShell (Run as administrator), check that the two services Learn lists as required are running:

    ```powershell
    Get-Service WinHttpAutoProxySvc, iphlpsvc
    ```

    Both must show **Running**. If one is stopped, start it. Do not disable the whole `WinHttpAutoProxySvc` service.
33. In the same PowerShell window, tell Windows to ask for the Entra Kerberos ticket at sign-in. The registry value is the way a single test VM can do it:

    ```powershell
    reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Kerberos\Parameters /v CloudKerberosTicketRetrievalEnabled /t REG_DWORD /d 1
    ```

34. Check it. The value shows `0x1`.

    ```powershell
    reg query HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Kerberos\Parameters /v CloudKerberosTicketRetrievalEnabled
    ```

35. Test that the VM can reach the storage account on port 445, which SMB uses. Replace `<your-storage-account-name>` with `stazb` plus your five digits, and remove the brackets:

    ```powershell
    Test-NetConnection -ComputerName <your-storage-account-name>.file.core.windows.net -Port 445
    ```

    `TcpTestSucceeded` must say `True`. If it says `False`, your network or a rule on the VM blocks port 445. Check the NSG from Lab 9 for a rule that denies outbound traffic.
36. Restart the VM from the Start menu. The setting needs a restart or a policy refresh.
37. Wait until the role in Part 5 has had time to apply. If you assigned it less than 30 minutes ago, wait. Do not change anything while waiting.
38. Reconnect with the same RDP file. This time choose **More choices** > **Use a different account** and sign in as `AzureAD\testuser1@yourtenant.onmicrosoft.com` (routes A and B), or use the web account setting with `testuser1@yourtenant.onmicrosoft.com` (route C, as in Lab 12). Use a fresh sign-in after every change above, so the ticket is new.
39. Open a normal **Command Prompt** (do not choose **Run as administrator**, and do not use PowerShell). Mount the share:

    ```
    net use Z: \\<your-storage-account-name>.file.core.windows.net\azbshare
    ```

    There is no user name and no password: Windows uses your sign-in. Do not add `/user:` and do not paste a key. Use another drive letter if `Z:` is taken.
40. You should see `The command completed successfully.` Write a test file and list the drive:

    ```
    echo hello > Z:\test.txt
    dir Z:\
    ```

You just opened a cloud file share with your Entra identity and no key. It is the same idea AVD profiles use. If you can map the share but cannot write at the root, the share permission or the Windows permissions on the share are the cause: look at Learn's pages on share-level permissions and Windows ACLs. If `net use` fails and you want to compare, the share's **Connect** page in the portal can generate the command. Choose **Active Directory or Microsoft Entra**, never **Storage account key**.

Check: `dir Z:\` lists `test.txt`, and `net use` shows `Z:` as connected.

## Steps with the Azure CLI

Do Part 1, the account setting and the role from the command line. Admin consent, the manifest tag, the Conditional Access exclusion and everything on the VM stay in the portal and on the VM.

Start with the variables. Use Cloud Shell from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/) in Bash. If Cloud Shell was closed or timed out, run this block again before the Clean up commands.

```bash
RG="rg-azb-lab"
LOCATION=$(az network vnet show --resource-group $RG --name vnet-azb --query location -o tsv)
SA="stazb$(shuf -i 10000-99999 -n 1)"   # stazb plus five digits; the name must be unique in Azure
SHARE="azbshare"
echo "$LOCATION"
echo "$SA"                         # write this name down
```

Write the name down. If you run the block again, set `SA=stazb12345` yourself, with your own digits from the first run.

Check the tenant and subscription first, and check that the name is free:

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
az storage account check-name --name "$SA" --query "{free:nameAvailable, reason:reason}" -o table
```

Check: `free` says `True`.

Create the account with the standard (HDD), LRS, pay-as-you-go type, and then the share:

```bash
az storage account create \
  --resource-group "$RG" \
  --name "$SA" \
  --location "$LOCATION" \
  --kind StorageV2 \
  --sku Standard_LRS \
  --https-only true \
  --min-tls-version TLS1_2 \
  --output none

az storage share-rm create \
  --resource-group "$RG" \
  --storage-account "$SA" \
  --name "$SHARE" \
  --access-tier TransactionOptimized \
  --output none
```

`StorageV2` with `Standard_LRS` is Learn's combination for HDD pay-as-you-go with local redundancy. The share has no `--quota`. A pay-as-you-go share without a quota can grow to the account's maximum, and the quota does not change the bill.

Check: `az storage share-rm show --resource-group "$RG" --storage-account "$SA" --name "$SHARE" --query name -o tsv` prints `azbshare`.

Turn on Microsoft Entra Kerberos:

```bash
az storage account update \
  --resource-group "$RG" \
  --name "$SA" \
  --enable-files-aadkerb true \
  --output none
```

Check: `az storage account show --resource-group "$RG" --name "$SA" --query azureFilesIdentityBasedAuthentication` prints a result that names `AADKERB`. If the field is empty, wait a minute and run it again, then look in the portal at **Classic file shares** > **Identity-based access**.

Now stop and do Part 3 (admin consent and the tag) and Part 4 (Conditional Access) in the portal. Then assign the role. For a group, use the group's object ID:

```bash
GROUP_ID=$(az ad group show --group "TestUsers" --query id -o tsv)
SCOPE="$(az storage account show --resource-group "$RG" --name "$SA" --query id -o tsv)/fileServices/default/fileshares/$SHARE"

az role assignment create \
  --role "Storage File Data SMB Share Contributor" \
  --assignee-object-id "$GROUP_ID" \
  --assignee-principal-type Group \
  --scope "$SCOPE"
```

Check: `az role assignment list --scope "$SCOPE" -o table` shows the role for the group. Then continue with Part 6 in the portal steps.

## Terraform

No Terraform block in this lab. [Deploy an AVD Quick Lab with Terraform](/terraform-labs/avd-quick-lab/) builds this same kind of account and share with Terraform. It marks the steps that still need the portal, which are the admin consent, the tag and the Conditional Access exclusion.

## Check that it works

- `azbshare` exists in your storage account, and the account shows **Identity-based access: Configured** with Microsoft Entra Kerberos.
- The app `[Storage Account] <name>.file.core.windows.net` has admin consent and the tag `kdc_enable_cloud_group_sids` in its manifest.
- No Conditional Access policy that requires MFA covers the storage app.
- `TestUsers` has **Storage File Data SMB Share Contributor** on the share.
- As `testuser1` on the VM, `net use Z: \\<name>.file.core.windows.net\azbshare` completes, and `Z:\test.txt` exists.
- You did not copy or type an account key anywhere.

If it fails, match the message to the layer:

| What you see | Layer | Likely cause | What to do |
|---|---|---|---|
| System error 1327 | 1, ticket | An MFA policy covers the storage app. | Part 4. |
| Access is denied, or it asks for a user name and password | 1 or 2 | The role is missing or has not applied yet, the Kerberos setting on the client is missing, or the tag is missing. | Check the role (Part 5). If you assigned it recently, wait 10 minutes and retry. Check the registry value (step 34), check the tag (step 22), restart and sign in fresh. |
| The network path was not found, or a timeout | Network | Port 445 is blocked, or the name is wrong. | Step 35. Check the account name. |
| Mounts but cannot write | 3, Windows permissions | The share-level or file-level permission is too narrow. | Check the role, then Learn's page on Windows ACLs. |
| The portal says identity-based authentication is not configured | 1 | Part 2 was not saved. | Repeat Part 2. |

## The most common mistake

Reaching for the account key when the mount fails. The portal offers it as an option, and it works, and it hides the real fault. A mount with a key proves nothing about the Entra setup, and the key opens the whole account. Fix the cause instead. The cause is nearly always one of three: the MFA exclusion (error 1327), the role that has not applied yet, or the missing tag for cloud-only users.

## Clean up

Keep the account and the share if you do [Lab 15](/azure-basics-labs/key-vault-managed-identity/) to [Lab 18](/azure-basics-labs/private-endpoint-dns/). Lab 18 locks the account down and uses it.

On the VM, delete the test file on the `Z:` drive and unmount it:

```
del Z:\test.txt
net use Z: /delete
```

Then do these four things, in this order:

1. Sign out of the VM from the Start menu (do not lock).
2. Remove the RDP rule `allow-rdp-my-ip` from `nsg-azb-vm` (Lab 12 Clean up shows how).
3. Stop the VM: **Stop** in the portal, or `az vm deallocate --resource-group rg-azb-lab --name vm-azb-win01`. Check that the status reads **Stopped (deallocated)**.
4. Route C only: leave the `hosts` line for now.

End state: VM Stopped (deallocated), no `allow-rdp-my-ip` rule.

At the start of Lab 15 you follow "Connect again later" in Lab 12 again.

Keep for later labs: the storage account, `azbshare`, the role assignment, the app settings, the VM `vm-azb-win01` (Stopped (deallocated)) and its public IP `pip-azb-win01`.

Stopping after this lab? Delete the storage account (**Storage accounts** > your account > **Delete**). Then open **Entra ID** > **App registrations** > **All applications**, search for `[Storage Account]`, and if the app for your account is still listed after the account is gone, delete it. If you delete only the share and not the account, the share keeps being billed for its stored data for 7 days, because soft delete is on by default. Delete the whole account instead.

At the end of the series, [Lab 19: When something breaks](/azure-basics-labs/when-something-breaks/) deletes everything in `rg-azb-lab` together, which includes the account:

```bash
az group delete --name "rg-azb-lab"
```

## Where this is used in AVD

In AVD, user profiles with FSLogix are stored on a share like this one, and the session hosts reach it with the same Kerberos ticket and the same role. In the AVD portal you will see the share path in the FSLogix setting (`VHDLocations`). Large companies often sync users from on-premises Active Directory. That path needs a domain controller and is not in this series. Read [How FSLogix Profile Containers Work](/azure-virtual-desktop/how-fslogix-profile-containers-work/) for what a profile container is, and [Choose Storage and Set Access for FSLogix Profile Containers](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/) for the storage choice, the two permission layers and where the Learn pages disagree about cloud-only users and FSLogix. This lab tests Azure Files with a cloud-only user. It does not test FSLogix.

## Next lab

[Lab 15: Key Vault and managed identity](/azure-basics-labs/key-vault-managed-identity/) stores a secret and lets the VM read it without a password, which is another case where the identity does the work and not a key.

## Sources

- [Create an Azure classic file share](https://learn.microsoft.com/en-us/azure/storage/files/storage-how-to-create-file-share)
- [Enable Microsoft Entra Kerberos authentication for hybrid and cloud-only identities on Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable)
- [Assign share-level permissions for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-assign-share-level-permissions)
- [Configure directory-level and file-level permissions for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-configure-file-level-permissions)
- [Mount SMB Azure file share on Windows](https://learn.microsoft.com/en-us/azure/storage/files/storage-how-to-use-files-windows)
- [Understand Azure Files billing](https://learn.microsoft.com/en-us/azure/storage/files/understanding-billing)
- [Introduction to Microsoft Entra Kerberos](https://learn.microsoft.com/en-us/entra/identity/authentication/kerberos)
- [Prerequisites for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites)
- [Store FSLogix profile containers on Azure Files using Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/virtual-desktop/create-profile-container-azure-ad)
- [Require multifactor authentication for all users](https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-all-users-mfa-strength)
- [Configure network endpoints for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-networking-endpoints)
