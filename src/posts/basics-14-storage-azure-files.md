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

By the end of this lab you will have a storage account and a file share in `rg-azb-lab`. Microsoft Entra Kerberos will be switched on for the account. The `TestUsers` group will have an Azure role on the share, and your test user will have mounted the share as a drive on the Lab 12 VM, signed in with the Entra identity and not with an account key.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn. No Terraform is included, so none was run either.

This is a hard lab. There are many small steps, and each one must be done. If one is skipped, the mount fails with an error that does not name the missing step. Read the whole lab once before you start.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway tenant and subscription.
- [Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the user `testuser1` and the group `TestUsers`. The user must be a cloud-only user, which means it exists only in Microsoft Entra ID and is not synced from an on-premises Active Directory.
- [Lab 7: RBAC roles](/azure-basics-labs/rbac-roles/): you give a role to a group in this lab, the same way as there.
- [Lab 8: Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/): the resource group `rg-azb-lab`.
- [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the VM `vm-azb-win01`, joined to Microsoft Entra ID, where you mount the share. It runs Windows Server 2025, which is on Learn's list of operating systems for cloud-only users (see "Safety first" below). After [Lab 13](/azure-basics-labs/vm-size-disk-stop-deallocate/) it is deallocated, so you start it in Part 6. You also need the local admin password for `azureuser` from Lab 12 and the RDP steps from Lab 12 Part 5 and Part 6.
- Roles: you need an administrator who can assign Azure roles on `rg-azb-lab` (Owner, as in Lab 7), and a Global Administrator for the admin consent step. The `azureuser` account from Lab 12 is the administrator on the VM.
- The same region you chose in Lab 8. Use it for everything here. Keep the storage account in the same region as the VM.
- Time: about 90 minutes, including the waits. Cost: small if you clean up on time. The share stays almost empty, and the type used here bills for what you store, plus transactions. Check the current prices on the [Azure Files pricing page](https://azure.microsoft.com/pricing/details/storage/files/). A budget from Lab 3 only warns, it does not stop anything.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name before you change anything.
- Do not use the storage account keys for this test. A key is an administrator key for the whole account. Learn says it gives administrator rights on all files in the share and on everything else in the account. If you ever connected to the share with a key from the VM, Learn says to unmount and remove the saved key first, because the old connection gets in the way of the new one.
- Do not sign in with `az login --use-device-code`.
- Azure CLI 2.76 or newer.
- Public network access stays on in this lab, so the VM can reach the account. That is a test setting. [Lab 18: Private endpoint and DNS](/azure-basics-labs/private-endpoint-dns/) closes it. Do not put real files on this share.
- Only one identity source can be on for a storage account. This lab uses Microsoft Entra Kerberos. Do not switch it on together with another source.
- Windows versions. For cloud-only users Learn lists Windows 11 Enterprise or Pro (single or multi-session) and Windows Server 2025, with the latest cumulative updates. Windows 10 and Windows Server 2022 are listed only for hybrid users. The client must be Microsoft Entra joined or Microsoft Entra hybrid joined. The Lab 12 VM is Windows Server 2025 and Entra joined, so it fits. If you built your VM from a Windows Server 2022 image instead, do not continue with the cloud-only test. Build a Windows Server 2025 or Windows 11 VM, or use the hybrid path at the end.
- The VM needs a temporary RDP rule while you work, as in Lab 12. You remove it again in the cleanup.
- Do not edit the Entra app that Azure creates for the account, except for the changes in this lab. Learn warns that other edits can cause errors.

## What the lab builds

![A left-to-right diagram inside the resource group rg-azb-lab. A storage account contains a file share. The test user on the Lab 12 Windows VM mounts the share over SMB on port 445. Microsoft Entra ID issues the Kerberos ticket, and the Azure role Storage File Data SMB Share Contributor on the share decides whether the user may read and write.](/img/basics/storage-azure-files.svg)

*Source: [Create an Azure classic file share](https://learn.microsoft.com/en-us/azure/storage/files/storage-how-to-create-file-share), [Enable Microsoft Entra Kerberos authentication for hybrid and cloud-only identities on Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable), [Assign share-level permissions for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-assign-share-level-permissions) and [Mount SMB Azure file share on Windows](https://learn.microsoft.com/en-us/azure/storage/files/storage-how-to-use-files-windows). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Idea 1: storage account, file share and the other services.**

A storage account is the top-level resource. Learn calls it a shared pool of storage, IOPS and throughput. It holds your data, and you pay and set the region, redundancy and network rules at this level. The account is not a place where you put files directly.

Inside it you create services. In the create wizard Learn lists the choices for **Primary service** as Azure Blob Storage or Azure Data Lake Storage, Azure Files, and Other (tables and queues). In plain words: blobs hold objects such as pictures and backups, you reach them through a web address. Tables and queues are for applications. Azure Files is a file server in the cloud. It uses SMB, the Windows file-sharing protocol, so Windows can show it as a drive letter.

A file share is one shared folder inside the account. One account can hold many shares. So the order is: account, then Azure Files service, then share, then folders and files.

The account name has rules. Learn says it must be 3 to 24 characters, only numbers and lowercase letters, and unique across all of Azure. That is why `storage` or `files` is already taken. The share name has other rules: lowercase letters, numbers and single hyphens, starting and ending with a letter or number, and no two hyphens in a row.

**Idea 2: which type to choose.**

Two choices set the price: the media tier and the billing model. The media tier is HDD (called **Standard** in the portal) or SSD (called **Premium**). SSD gives steady high speed and low delay. HDD costs less and is meant for general use. Redundancy says how many copies Azure keeps. LRS (locally redundant storage) keeps three copies in one data centre in one region. It is the cheapest choice, and it is enough for a test.

Learn lists three billing models. With **provisioned** billing (v1 and v2) you pay for the size you reserve, even if the share is empty. For SSD provisioned v1, Learn gives a minimum of 100 GiB. For provisioned v2, it gives a range that starts at 32 GiB. With **pay-as-you-go** (HDD only) you pay for what you store, plus transactions and data transfer.

Learn recommends provisioned v2 for new deployments. This lab uses HDD, LRS and pay-as-you-go anyway. That is my choice for a throwaway test: an almost empty share costs almost nothing. For a real share you would follow Learn's advice and look at provisioned v2. Premium (SSD) is for shares that need low delay. It is not needed here, and you pay for the reserved size from the first day.

### Part 1: Create the storage account and the share

1. Sign in to the [Azure portal](https://portal.azure.com) as your administrator. Check the tenant and subscription name at the top right.
2. Search for **Storage accounts** and select it. Select **+ Create**.
3. On the **Basics** tab set:
   - **Subscription**: your test subscription.
   - **Resource group**: `rg-azb-lab`.
   - **Storage account name**: use the series pattern: `stazb` followed by five random digits, for example `stazb48213`. Learn's rule is 3 to 24 lowercase letters and numbers. The portal tells you if the name is taken. Write the name down. You use it in almost every later step.
   - **Region**: the region you use for everything.
   - **Primary service**: **Azure Files**.
   - **Media tier**: **HDD (standard)**.
   - **File share billing**: **Pay-as-you-go file shares**.
   - **Redundancy**: **LRS**.
4. Leave the **Advanced**, **Networking**, **Data protection**, **Security** and **Encryption** tabs at their defaults. On the **Networking** tab, public network access is **Enable** by default. That is fine for now.
5. Select **Review + create**, read the summary, then select **Create**. When it says the deployment is complete, select **Go to resource**.
6. In the service menu, under **Data storage**, select **Classic file shares**. Some Learn pages still call this menu item **File shares**. Select **+ Classic file share**.
7. On the **Basics** tab set **Name** to `azbshare`. Leave **Access tier** at **Transaction optimized**.
8. Select the **Backup** tab. Learn says backup is on by default for an SMB share. Clear **Enable backup**. A backup creates more resources that you would have to clean up, and this lab does not need it.
9. Select **Review + create**, then **Create**.

Check: under **Classic file shares** you see `azbshare`. On the account's **Overview** page, **Account kind** shows StorageV2 and the redundancy shows locally-redundant storage (LRS).

### Part 2: Turn on Microsoft Entra Kerberos

**Idea 3: three things must agree.**

For the mount to work, three separate things have to be right, and they are checked one after the other:

1. **Who are you?** Microsoft Entra ID has to give your user a Kerberos ticket for the storage account. Kerberos is a sign-in system based on tickets. Learn says that with Microsoft Entra Kerberos, Entra ID issues the tickets, and for cloud-only users the file share no longer needs a domain controller. This is the part that needs the account setting, an admin consent, a tag, the client setting and a Conditional Access exclusion.
2. **May you open the share?** An Azure role on the share, the share-level permission. Learn says that when no role is assigned, access is denied. The default share-level permission starts at **None**.
3. **What can you do inside?** Windows permissions (ACLs) on folders and files. Learn says that if the share-level and the file-level permission differ, the more restrictive one applies. Learn lists the root of a new share with `NT AUTHORITY\Authenticated Users` set to Modify, so a user who passes step 2 can normally write at the root. This lab does not change ACLs.

**The limit you must know before you start.** Learn says that Azure Files with Microsoft Entra Kerberos supports cloud-only identities in the public Azure cloud, not in Azure US Government or Azure operated by 21Vianet. It says it does not support cross-tenant access, and that guest users from other tenants are supported only for FSLogix on Azure Virtual Desktop. It also says that you cannot use Windows File Explorer or `icacls` to set ACLs for cloud-only users. You use the portal or a PowerShell module instead.

There is a second limit about AVD profiles, and the Learn pages do not agree on it. The AVD prerequisites page says that to use FSLogix with Microsoft Entra joined session hosts, the user accounts must be hybrid identities. The Azure Files page and the AVD page "Store FSLogix profile containers on Azure Files using Microsoft Entra ID" both describe cloud-only identities as supported for FSLogix. The Microsoft Entra Kerberos introduction page still labels cloud-only support as preview, and the other two pages carry no label. This lab tests Azure Files with a cloud-only user. It does not test FSLogix. See [Choose Storage and Set Access for FSLogix Profile Containers](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/) for how the pages differ, and check them again before you plan anything real.

10. Go to your storage account. In the service menu, under **Data storage**, select **Classic file shares**.
11. Next to **Identity-based access**, select the status, which reads **Not configured**.
12. Under **Microsoft Entra Kerberos**, select **Set up**.
13. Select the **Microsoft Entra Kerberos** checkbox.
14. Leave the domain name and domain GUID boxes empty. Learn says they are optional and only for hybrid users who will set file permissions with File Explorer.
15. Select **Save**.

Check: go back to **Classic file shares**. **Identity-based access** now shows **Configured**.

### Part 3: Admin consent and the cloud-only group tag

Turning on Kerberos makes Azure create an app in your tenant. It is named `[Storage Account] <your-storage-account-name>.file.core.windows.net`. Two settings on it are required for cloud-only users.

16. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com) as Global Administrator. Check the tenant name.
17. Open **Entra ID** > **App registrations**. Select **All applications**. If the list is empty or the app is missing, wait a minute and refresh.
18. Select the app named `[Storage Account] <your-storage-account-name>.file.core.windows.net`.
19. Under **Manage**, select **API permissions**.
20. Select **Grant admin consent for** your directory name. Learn says this grants three permissions (openid, profile and User.Read) for all accounts in the directory. Select **Yes**.
21. Under **Manage**, select **Manifest**. The manifest is the app's settings file in JSON.
22. Find the `tags` property. Add the value `"kdc_enable_cloud_group_sids"` to it. If the property already holds values, add this one to the list and keep the others. Select **Save**.

Why step 22: Learn says a Kerberos ticket can hold at most 1,010 group identifiers. For cloud-only users the ticket must carry the Entra group identifiers too, and Learn calls this tag mandatory for cloud-only identities. Without it, authentication fails.

Check: the **API permissions** page shows the three permissions with a status that says admin consent was granted for your directory. Reopen the manifest and read that `tags` holds `kdc_enable_cloud_group_sids`.

### Part 4: Keep MFA away from the storage app (the trap)

Learn says Microsoft Entra Kerberos does not support MFA for Azure file shares. If a Conditional Access policy that requires MFA covers the storage account app, you cannot reach the share, and `net use` fails with:

`System error 1327: Account restrictions are preventing this user from signing in. For example: blank passwords aren't allowed, sign-in times are limited, or a policy restriction has been enforced.`

That message names blank passwords and sign-in times, and neither is the cause. The cause is the MFA policy.

The policy from [Lab 6: Conditional Access](/azure-basics-labs/conditional-access/) targets only the two AVD apps, never **All resources**, so it does not hit the storage app. The danger is any other policy in your tenant that targets **All resources** and requires MFA, for example one you made after Lab 6 from Learn's "Require multifactor authentication for all users" page. Learn's Azure Files page says to exclude the storage app from such policies.

23. In the Entra admin center, open **Entra ID** > **Conditional Access** > **Policies**.
24. Read the list. For each policy that is **On** or **Report-only**, open it and read **Target resources**. Write down any policy that includes **All resources** (older name: **All cloud apps**) and requires MFA or an authentication strength. Lab 6 deletes its own policy at the end, so you may see an empty list.
25. If there is none, you are done with this part. Write "no all-resources MFA policy" in your notes.
26. If there is one, open it. Under **Target resources**, look for the **Exclude** tab, and select **Select excluded cloud apps** or the option with a similar name. Search for `[Storage Account] <your-storage-account-name>.file.core.windows.net`. Select the app and save.
27. If the app does not appear in the picker, stop. Do not widen or turn off the policy to get around it. Read the "Disable multifactor authentication on the storage account" section of the Learn page for Azure Files and look for the supported way to add it.

Check: for every all-resources MFA policy, the storage account app is listed under the excluded apps.

### Part 5: Give TestUsers the role on the share

28. In the Azure portal, open your storage account, then **Classic file shares**, then select `azbshare`.
29. Select **Access Control (IAM)**.
30. Select **Add**, then **Add role assignment**. Learn words this step as **Add a role assignment**.
31. On the **Role** tab, search for and select **Storage File Data SMB Share Contributor**. Learn says it gives read, write and delete access on files and directories in Azure Files. Select **Next**.
32. Keep **Assign access to** at **User, group, or service principal** (Learn's name: Microsoft Entra user, group, or service principal). Select **+ Select members**, search for `TestUsers`, and select the group. Select **Select**.
33. Select **Review + assign**, then **Review + assign** again. If your page shows **Save** instead, select that.

Learn says a share-level permission change usually takes effect within 30 minutes, and sometimes longer. Do the VM steps below first. They take a while, and the wait may be over by then.

Check: on the **Role assignments** tab of the share, `TestUsers` appears with **Storage File Data SMB Share Contributor**.


### Part 6: Prepare the VM and mount the share

These steps run on the Lab 12 VM. First start it (it is deallocated after Lab 13): in the portal open the VM and select **Start**, or run `az vm start --resource-group rg-azb-lab --name vm-azb-win01`. Then add the temporary RDP rule for your own IP address as in Lab 12 Part 5, and download the RDP file as in Lab 12 Part 6. Do Steps 34 to 38 as the local administrator, then restart and sign in as the test user.

To sign in as `azureuser`, open the RDP file, and when Windows asks for credentials select **More choices**, then **Use a different account**. Learn's connect page says a local account is entered as the VM name, a backslash and the user name, so type `vm-azb-win01\azureuser` and the password from Lab 12. If you used the web account setting in Lab 12 (case B), untick it for this sign-in, because a local account does not use it.

34. Open **PowerShell** as administrator. Check that the two services Learn lists as required are running:

    ```powershell
    Get-Service WinHttpAutoProxySvc, iphlpsvc
    ```

    Both must show **Running**. If one is stopped, start it. Do not disable the whole `WinHttpAutoProxySvc` service. Learn says it does other work too.
35. Tell Windows to ask for the Entra Kerberos ticket at sign-in. Learn gives three ways: Intune, Group Policy, or a registry value. The registry value is the one a single test VM can use. Run this in an elevated Command Prompt:

    ```
    reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Kerberos\Parameters /v CloudKerberosTicketRetrievalEnabled /t REG_DWORD /d 1
    ```

36. Check it:

    ```
    reg query HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Kerberos\Parameters /v CloudKerberosTicketRetrievalEnabled
    ```

    The value shows `0x1`.
37. Test that the VM can reach the storage account on port 445, which SMB uses. Learn gives this command:

    ```powershell
    Test-NetConnection -ComputerName <your-storage-account-name>.file.core.windows.net -Port 445
    ```

    `TcpTestSucceeded` must say `True`. If it says `False`, your network or a rule on the VM blocks port 445. Check the NSG from Lab 9 for a rule that denies outbound traffic.
38. Restart the VM. Learn says the setting needs a policy refresh or a restart.
39. Wait until the role in Part 5 has had time to apply. If you assigned it less than 30 minutes ago, wait.
40. Sign in to the VM as `testuser1`, the way Lab 12 did (`AzureAD\testuser1@yourtenant.onmicrosoft.com`, or the web account setting in case B). Learn says to sign in to the client with the identity that has the permissions. Use a fresh sign-in after every change above, so the ticket is new.
41. Open **Command Prompt** (not PowerShell). Mount the share:

    ```
    net use Z: \\<your-storage-account-name>.file.core.windows.net\azbshare
    ```

    Learn's form for a domain-joined or Entra-joined machine has no user name and no password. Windows uses your sign-in. Do not add `/user:` and do not paste a key. Use a drive letter that is free, if `Z:` is taken.
42. The command should say that it completed successfully. Write a test file:

    ```
    echo hello > Z:\test.txt
    dir Z:\
    ```

Another way, from the portal: open the share, select **Connect**, choose the drive letter, set **Authentication method** to **Active Directory or Microsoft Entra**, select **Show script**, copy it and run it on the VM. Do not choose **Storage account key**. If the portal says identity-based authentication is not configured, go back to Part 2.

A PowerShell form also exists. `New-PSDrive -Name Z -PSProvider FileSystem -Root "\\<your-storage-account-name>.file.core.windows.net\azbshare" -Persist -Scope global`. Learn's own script for this form also has a `cmdkey` line. Use `net use` for this lab. Learn says that when you mount with PowerShell, Command Prompt and File Explorer do not see the drive.

Check: `dir Z:\` lists `test.txt`, and `net use` shows `Z:` as connected.

## Steps with the Azure CLI

Do Part 1, the account setting and the role from the command line. Admin consent, the manifest tag, the Conditional Access exclusion and everything on the VM stay in the portal and on the VM. I did not find a Learn page that gives a CLI command for those, and the Conditional Access exclusion has no CLI form in the Learn pages used here.

Start with the variables. Use Cloud Shell from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/) in Bash.

```bash
RG="rg-azb-lab"
LOCATION="<your-region>"          # the one region you chose for all labs
SA="stazb$(shuf -i 10000-99999 -n 1)"   # stazb plus five digits; the name must be unique in Azure
SHARE="azbshare"
echo "$SA"                         # write this name down
```

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

`StorageV2` with `Standard_LRS` is Learn's combination for HDD pay-as-you-go with local redundancy. The share has no `--quota`. Learn says a pay-as-you-go share without a quota can grow to the account's maximum, and that the quota does not change the bill.

Check: `az storage share-rm show --resource-group "$RG" --storage-account "$SA" --name "$SHARE" --query name -o tsv` prints `azbshare`.

Turn on Microsoft Entra Kerberos (Learn's command):

```bash
az storage account update \
  --resource-group "$RG" \
  --name "$SA" \
  --enable-files-aadkerb true \
  --output none
```

Check: `az storage account show --resource-group "$RG" --name "$SA" --query azureFilesIdentityBasedAuthentication` prints a result that names `AADKERB`. If the field is empty, wait a minute and run it again, then look in the portal at **Classic file shares** > **Identity-based access**.

Now stop and do Part 3 (admin consent and the tag) and Part 4 (Conditional Access) in the portal. Then assign the role. Learn's command gives the role to a sign-in name. For a group, use the group's object ID:

```bash
GROUP_ID=$(az ad group show --group "TestUsers" --query id -o tsv)
SCOPE="$(az storage account show --resource-group "$RG" --name "$SA" --query id -o tsv)/fileServices/default/fileshares/$SHARE"

az role assignment create \
  --role "Storage File Data SMB Share Contributor" \
  --assignee-object-id "$GROUP_ID" \
  --assignee-principal-type Group \
  --scope "$SCOPE"
```

Check: `az role assignment list --scope "$SCOPE" -o table` shows the role for the group. Then continue with Part 6 in the portal steps, from Step 34.

### If you have hybrid identities

Skip this if your users are cloud-only. I have not run this path, and the lab above does not need it.

A hybrid identity is a user that exists in on-premises Active Directory Domain Services (AD DS) and is synced to Microsoft Entra ID with Microsoft Entra Connect Sync or Microsoft Entra Cloud Sync. What changes, according to Learn:

- You need AD DS and one of the two sync tools. Create the users, and also the groups you give roles to, in Active Directory, and sync them to Entra ID. Learn says a group must be created in AD to get the role for hybrid users. The cloud-only group tag from Part 3 is not needed for hybrid users. Learn marks it mandatory only for cloud-only identities.
- The client list is longer. It also includes Windows 10 Enterprise or Pro, version 2004 or later with current updates, and Windows Server 2022 with current updates. Clients must be Microsoft Entra joined or hybrid joined. They cannot be joined to Microsoft Entra Domain Services, or to AD only.
- The parts that stay the same: Kerberos switched on in the portal, admin consent, the MFA exclusion, the client registry value, the share role (given to the synced group) and the 30-minute wait.
- To set file and folder permissions with `icacls` or File Explorer, you need a Windows machine with an unimpeded network path to a domain controller. For this, Learn says you can enter the domain name and domain GUID in Part 2. This lab does not set folder permissions.

## Terraform

No Terraform block in this lab. The Terraform resources for a storage account with Microsoft Entra Kerberos and a share are not in the provider documentation I checked, and I did not want to write them from memory. [Deploy an AVD Quick Lab with Terraform](/terraform-labs/avd-quick-lab/) builds this same kind of account and share with Terraform. It marks the steps that still need the portal, which are the admin consent, the tag and the Conditional Access exclusion.

## Check that it works

- `azbshare` exists in your storage account, and the account shows **Identity-based access: Configured** with Microsoft Entra Kerberos.
- The app `[Storage Account] <name>.file.core.windows.net` has admin consent and the tag `kdc_enable_cloud_group_sids` in its manifest.
- No Conditional Access policy that requires MFA covers the storage app.
- `TestUsers` has **Storage File Data SMB Share Contributor** on the share.
- As `testuser1` on the VM, `net use Z: \\<name>.file.core.windows.net\azbshare` completes, and `Z:\test.txt` exists.
- You did not copy or type an account key anywhere.

If it fails, match the message:

| What you see | Likely cause | What to do |
|---|---|---|
| System error 1327 | An MFA policy covers the storage app. | Part 4. |
| Access is denied, or the command asks for a user name and password | The role is missing or has not applied yet, or the Kerberos setting on the client is missing, or the cloud-only tag is missing. | Check the role (Part 5), wait up to 30 minutes, check the registry value (Step 36), check the tag (Step 22), restart and sign in fresh. |
| The network path was not found, or a timeout | Port 445 is blocked, or the name is wrong. | Step 37. Check the account name. |
| A message that identity-based authentication is not configured (portal Connect page) | Part 2 was not saved. | Repeat Part 2. |

## The most common mistake

Reaching for the account key when the mount fails. The portal offers it as an option, and it works, and it hides the real fault. A mount with a key proves nothing about the Entra setup, and the key opens the whole account. Fix the cause instead. The cause is nearly always one of three: the MFA exclusion (error 1327), the role that has not applied yet, or the missing tag for cloud-only users.

## Clean up

If you do [Lab 18: Private endpoint and DNS](/azure-basics-labs/private-endpoint-dns/), keep the account and the share. Lab 18 locks the account down and uses it.

On the VM, delete the test file on the `Z:` drive and unmount it when you are done:

```
del Z:\test.txt
net use Z: /delete
```

Then sign out of the VM, remove the RDP rule `allow-rdp-my-ip` from `nsg-azb-vm` (Lab 12 Clean up shows how), and deallocate the VM so it does not bill for compute (`az vm deallocate --resource-group rg-azb-lab --name vm-azb-win01`, or **Stop** in the portal, and check the status reads **Stopped (deallocated)**).

Keep for later labs: the storage account, `azbshare`, the role assignment, the app settings, the VM `vm-azb-win01` (deallocated) and its public IP `pip-azb-win01`.

At the end of the series, in the cleanup of [Lab 19: When something breaks](/azure-basics-labs/when-something-breaks/), delete everything in `rg-azb-lab` together, which includes the account. In the portal: **Resource groups** > `rg-azb-lab` > **Delete resource group**, then type the name. With the CLI:

```bash
az group delete --name "rg-azb-lab"
```

Then open **Entra ID** > **App registrations** > **All applications** and search for `[Storage Account]`. If the app for your account is still there, check that the storage account is gone before you delete it. I did not find a Learn page that says what happens to this app when the account is deleted, so look.

If you delete only the share and not the account: the share keeps being billed for its stored data for the retention days, because soft delete is on by default (7 days). Learn says deleted shares are billed on their used capacity during that time. Delete the whole account instead, or turn soft delete off first.

## Where this is used in AVD

In AVD, user profiles with FSLogix are stored on a share like this one, and the session hosts reach it with the same Kerberos ticket and the same role. Read [How FSLogix Profile Containers Work](/azure-virtual-desktop/how-fslogix-profile-containers-work/) for what a profile container is, and [Choose Storage and Set Access for FSLogix Profile Containers](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/) for the storage choice, the two permission layers and the places where the Learn pages disagree about cloud-only users.

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
