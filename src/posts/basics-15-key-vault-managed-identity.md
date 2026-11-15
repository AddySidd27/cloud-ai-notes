---
title: "Key Vault and Managed Identity: Let a VM Read a Secret Without a Password"
seoTitle: "Azure Key Vault and Managed Identity for Beginners"
layout: post.njk
permalink: "/azure-basics-labs/key-vault-managed-identity/"
order: 325
tags: [azure-basics-lab]
deck: "You store a demo secret in Azure Key Vault and read it from inside your Windows VM, using the VM's own identity instead of a password."
description: "Beginner Azure lab: create a Key Vault with Azure RBAC, store a demo secret, and read it from a Windows VM with its managed identity, no password."
---

By the end of this lab you will have a Key Vault with one demo secret in it, and your Windows VM from Lab 12 will read that secret by itself. No password, key or connection string is saved on the VM to make that work.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn. There is no Terraform in this lab, because I could not check the Key Vault Terraform resources against Learn.

Azure Key Vault is a service that stores sensitive values, such as passwords and keys, and decides who may read them. A managed identity is a sign-in that Azure creates and looks after for a resource, such as a VM. You will use both.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway Azure account.
- [Lab 2: Azure Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/): you need Cloud Shell or the CLI for the CLI part.
- [Lab 3: Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): `rg-azb-core` with `ag-azb-email`, and the budget `budget-azb-core` on the subscription, stay in place.
- [Lab 7: Azure RBAC roles](/azure-basics-labs/rbac-roles/): you have seen a role assignment before. This lab uses it twice.
- [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the Windows VM `vm-azb-win01` in `rg-azb-lab`, with its system-assigned managed identity turned on.
- Time: about 40 minutes, plus a few minutes of waiting for a role to take effect.
- Cost: Key Vault is billed by use, so a few calls in this lab cost very little. The VM bills for compute while it runs, so this lab starts it only for Part 4 and stops it at the end. See the [Key Vault pricing page](https://azure.microsoft.com/pricing/details/key-vault/) for current figures.
- Role: Owner on the subscription or on `rg-azb-lab`. Learn says you must be able to write role assignments, and names Owner and User Access Administrator as roles that can.
- Use your region from the notes sheet in [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/), in every step.

**State of your resources**

| | At the start | At the end |
| --- | --- | --- |
| VM `vm-azb-win01` | Stopped (deallocated), as Labs 12 to 14 leave it. Parts 1 to 3 do not need it running. | Stopped (deallocated) |
| Rule `allow-rdp-my-ip` in `nsg-azb-vm` | Not there. You add it only if you use the Remote Desktop route in Part 4. | Not there |
| Public IP `pip-azb-win01` | Exists. It stays. | Exists |
| New in this lab | Nothing | Nothing. The key vault is deleted and purged in "Clean up". |

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top right of the portal before you change anything.
- Store a demo value only. Never type a real password, key or token into this vault.
- Do not turn on purge protection. Learn says it cannot be turned off again, by anyone, and then you cannot delete the vault for good until the retention time ends. This lab does not need it.
- Pick a vault name you do not mind losing for a while. A deleted vault keeps its name for 90 days unless you purge it. "Clean up" purges it.
- Leave the network access settings of the vault at their defaults.
- Do not paste the access token from the VM into chats, tickets or notes. It is a working credential for a short time.
- Azure already requires MFA for portal and CLI changes. Expect the MFA prompt when you sign in as an admin.

## What the lab builds

![A numbered diagram. Step 1: you, with the role Key Vault Secrets Officer, create a demo secret in the key vault in the resource group rg-azb-lab. Step 2: the Windows VM asks its local identity endpoint at 169.254.169.254 for a token. Step 3: Microsoft Entra ID issues the token for the VM's system-assigned managed identity. Step 4: the VM sends the token to the key vault, which allows the read because the VM identity has the role Key Vault Secrets User, and returns the secret value. No password is stored on the VM.](/img/basics/key-vault-managed-identity.svg)

*Source: [Provide access to Key Vault keys, certificates, and secrets with Azure RBAC](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide), [Use a Windows VM system-assigned managed identity to access Azure Key Vault](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/tutorial-windows-managed-identities-vm-access), [How to use managed identities for Azure resources on an Azure VM to acquire an access token](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token) and [Key Vault soft-delete overview](https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Idea 1: what a key vault holds.** A key vault holds secrets (passwords, connection strings), keys and certificates. This lab uses one secret. A secret is any value you want to keep tight. Key Vault returns it only to whoever is allowed to read it.

### Part 1: Check the VM identity and create the vault

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant name at the top right.
2. Open the VM `vm-azb-win01`, then go to **Security** > **Identity**. You can read this page while the VM is stopped. On the **System assigned** tab, check that **Status** is **On**. If it is **Off**, select **On** and **Save**.
3. In the portal search box, type **Key vaults** and open it. Select **Create**. If the portal sends you to **Create a resource** and asks for **Key Vault**, pick that and select **Create**.
4. On the first page, set:
   - **Subscription**: your test subscription.
   - **Resource group**: `rg-azb-lab`.
   - **Key vault name**: a name of your own, 3 to 24 characters, letters, digits and hyphens. It must start with a letter, end with a letter or a digit, and not have two hyphens in a row. Key vault names are unique across all of Azure, so add five random digits, for example `kv-azb-48213`. If the portal says the name is taken, pick other digits. Write the name down.
   - **Region**: the region you chose for all labs.
   - **Pricing tier**: Standard.
5. Open the **Access configuration** tab (if your page has no such tab, look on **Basics**). Choose **Azure role-based access control**, not **Vault access policy**. Newer vaults use Azure RBAC by default, but pick it on purpose and read the setting before you go on.
6. Open the **Recovery options** tab, if the page has one. Soft-delete is on and cannot be turned off. Leave **purge protection** unticked. Leave the retention days as they are.
7. Do not change the **Networking** tab. Select **Review + create**, then **Create**. When it finishes, select **Go to resource** and note the **Vault URI**. It looks like `https://<vault-name>.vault.azure.net/`.

Check: on the vault's **Overview** page you see your vault name and Vault URI. Under **Settings** > **Properties** (the name can vary) the permission model reads Azure role-based access control.

### Part 2: Give yourself a data role and add the secret

**Idea 2: management plane and data plane.** Access to a vault is split in two. The **control plane** (management plane) is where you manage the vault itself: create it, delete it, change its settings. The **data plane** is where you work with what is inside: read and write secrets, keys and certificates. They are controlled separately. Owner and Contributor work on the control plane, so on an Azure RBAC vault they do not let you read or write a secret, and `az keyvault secret set` fails with a Forbidden error for them. You need a data-plane role. Two are used here:

- **Key Vault Secrets Officer**: any action on secrets, except managing permissions. For you.
- **Key Vault Secrets User**: read secret contents. For the VM. It cannot write.

An Owner can give themselves the data role, as you do next. That is allowed, and it is a separate step on purpose.

8. In your vault, open **Access control (IAM)**. Select **Add** > **Add role assignment**.
9. On the **Role** tab, search for **Key Vault Secrets Officer**, select it, then **Next**.
10. On the **Members** tab, leave **Assign access to** on **User, group, or service principal**. Select **Select members**, find your admin account, select it, then **Select**.
11. Select **Review + assign** twice.
12. Wait three minutes. If step 13 gives an authorization error, refresh, wait two more minutes and try again. Do not add the role twice.

    Optional, to see the point of Idea 2: before the role has taken effect, or with an account that has only Owner, **Objects** > **Secrets** shows an authorization error. Owner manages the vault. It does not read what is inside.
13. Open **Objects** > **Secrets**. Select **Generate/Import**. Set **Upload options** to **Manual**. For **Name** type `demo-secret`. For **Value** type `demo-value-not-a-password`. Leave the rest as it is and select **Create**.
14. Select `demo-secret`, then the current version. Select **Show Secret Value**. You should see your demo value.

Check: the secret list shows `demo-secret` as enabled, and **Show Secret Value** works for you. If you see an authorization error, wait a few more minutes and refresh the page.

### Part 3: Give the VM's identity the reader role

**Idea 3: managed identity.** Normally a program that wants a secret needs a password to ask for it, and that password has to be stored somewhere. That is the problem Key Vault is meant to remove, and a plain password would bring it back. With a managed identity, Azure creates an identity for the VM in Microsoft Entra ID and looks after its credentials. Your code on the VM asks a local address, `169.254.169.254`, for a token. That address belongs to the Azure Instance Metadata Service (IMDS), and only the VM itself can reach it. Microsoft Entra ID issues the token. It proves who the VM is. Nothing is stored on the VM. One thing to know: all code running on the VM can ask for that token, so the security boundary is the VM.

15. In your vault, open **Access control (IAM)** again. Select **Add** > **Add role assignment**.
16. On the **Role** tab, select **Key Vault Secrets User**, then **Next**.
17. On the **Members** tab, set **Assign access to** to **Managed identity**. Select **Select members**.
18. In the **Select managed identities** pane, choose your subscription. In the **Managed identity** drop-down choose **Virtual machine**, then tick `vm-azb-win01`. Select **Select**.
19. Select **Review + assign** twice.
20. Open **Role assignments** on the same IAM page. Check that you see **Key Vault Secrets Officer** for your account and **Key Vault Secrets User** for the VM.
21. Wait three minutes before the next part.

### Part 4: Read the secret from inside the VM

The two commands in this part must run on the VM, not in your browser or Cloud Shell. The address `169.254.169.254` only answers from inside the VM. Start the VM first:

22. Open `vm-azb-win01` > **Overview** > **Start**. Wait until the status says **Running** (two to three minutes).

23. Choose how to run the two scripts in steps 24 and 25 on the VM:
    - **Way A: Run command (no sign-in, no RDP rule).** On the VM, open **Operations** > **Run command** > **RunPowerShellScript**. Paste both scripts together into the box, replace `<vault-name>` with your vault name, and select **Run**. The output window shows the result. If it shows an error instead of the secret, use Way B.
    - **Way B: Remote Desktop.** Follow "Connect again later" in [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/): look up your public IP address again, add `allow-rdp-my-ip` to `nsg-azb-vm` for that address only, connect, and sign in as `testuser1` or `azureuser`. In the Remote Desktop window, open **Windows PowerShell** and run the two scripts one after the other.

24. Ask IMDS for a token for Key Vault. The `Metadata` header is required, and must be the lower-case word `true`:

```powershell
$Response = Invoke-RestMethod -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net' -Method GET -Headers @{Metadata="true"}
$KeyVaultToken = $Response.access_token
```

Check: run `$KeyVaultToken.Length`. A long number means you have a token. An empty result or a red error means the call failed: read "The most common mistake". Never paste the token anywhere.

25. Use the token to read the secret. Replace `<vault-name>` with your vault name:

```powershell
$Secret = Invoke-RestMethod -Uri "https://<vault-name>.vault.azure.net/secrets/demo-secret?api-version=2016-10-01" -Method GET -Headers @{Authorization="Bearer $KeyVaultToken"}
$Secret.value
```

Check: the last line prints `demo-value-not-a-password`. You got it with no password on the VM. If you see 403 Forbidden, with text like "Caller is not authorized to perform action on resource", the role has not taken effect yet. Wait two minutes and run step 25 again.

Look at what you typed. There was no password, key or connection string in either command. The VM proved who it was with its identity. In AVD you will rely on the same pattern.

Do not stop here. Go to "Clean up" now, so the VM does not keep running.

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/). Check the tenant and subscription first, then set the variables. Anything in ALL CAPS or after a `#` comment is yours to change. Run `echo "$VAULT"` before you use the variable. If Cloud Shell restarts, set the variables again.

```bash
az account show --query "{tenant:tenantId, subscription:name}" -o table

RG="rg-azb-lab"
VM="vm-azb-win01"
LOCATION=$(az vm show --resource-group "$RG" --name "$VM" --query location -o tsv)   # same region as the VM
VAULT=kv-azb-48213   # replace 48213 with five digits of your own; 3-24 characters, unique in Azure
echo "$LOCATION $VAULT"
```

Create the vault. The `--enable-rbac-authorization true` setting is in Learn's own examples. Do not add `--enable-purge-protection`.

```bash
az keyvault create --name "$VAULT" --resource-group "$RG" --location "$LOCATION" --enable-rbac-authorization true
VAULT_ID=$(az keyvault show --name "$VAULT" --resource-group "$RG" --query id -o tsv)
```

Give yourself Key Vault Secrets Officer. This command is the one from Learn's Bicep and ARM quickstarts:

```bash
az role assignment create --role "Key Vault Secrets Officer" \
  --assignee-object-id $(az ad signed-in-user show --query id -o tsv) \
  --assignee-principal-type User \
  --scope "$VAULT_ID"
```

Wait three minutes, then add the secret and read it back:

```bash
az keyvault secret set --vault-name "$VAULT" --name "demo-secret" --value "demo-value-not-a-password"
az keyvault secret show --vault-name "$VAULT" --name "demo-secret" --query "value" -o tsv
```

Give the VM's identity Key Vault Secrets User:

```bash
VM_PRINCIPAL=$(az vm show --resource-group "$RG" --name "$VM" --query identity.principalId -o tsv)
az role assignment create --role "Key Vault Secrets User" \
  --assignee-object-id "$VM_PRINCIPAL" \
  --assignee-principal-type ServicePrincipal \
  --scope "$VAULT_ID"
```

If `$VM_PRINCIPAL` is empty, the VM has no system-assigned identity. Run `az vm identity assign --name "$VM" --resource-group "$RG"` (Learn's command), and read the `systemAssignedIdentity` value it prints.

Check: `az role assignment list --scope "$VAULT_ID" --query "[].{role:roleDefinitionName, who:principalName}" -o table` lists both roles. Then do steps 22 to 25 of the portal part (start the VM, then run the scripts on the VM). Reading from inside the VM is the point of the lab, so there is no CLI version of it.

## Terraform

No Terraform in this lab. I could not check the Terraform resources for a key vault and a secret, or their RBAC settings, against Learn, and I do not want to give you code I have not checked. If you want the Terraform version later, start from [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/) and the provider documentation for the key vault resources.

## Check that it works

- The vault exists in `rg-azb-lab`, uses Azure role-based access control, and has no purge protection.
- `demo-secret` exists, and you could read it as yourself after the Officer role took effect.
- The IAM page shows Key Vault Secrets Officer for you and Key Vault Secrets User for the VM.
- On the VM, the token call returned a token and the secret call printed your demo value.
- You can explain why Owner on the resource group alone did not let you read the secret.

## The most common mistake

Assigning the VM (or yourself) a management role and expecting it to read secrets. Owner and Contributor manage the vault. They do not read or write what is inside it. You need a data-plane role such as Key Vault Secrets Officer or Key Vault Secrets User, and role assignments can take a few minutes to work.

Three smaller ones, all with the same 403 or empty result:

- Calling the secret URL too soon after the role assignment. Wait, then retry.
- Leaving the vault on **Vault access policy**. The roles in this lab only work on vaults that use Azure role-based access control. Changing the model makes the old access policies stop counting.
- Leaving out the `Metadata: true` header, or using `http://localhost`. Learn says a missing header gives a `bad_request_102` error. The token call also fails if the VM has no managed identity switched on.

## Clean up

Do these three steps in this order. The lab ends with the VM stopped.

1. If you used Way B (Remote Desktop): sign out of the VM (do not just lock it), then open `nsg-azb-vm` > **Inbound security rules**, tick `allow-rdp-my-ip` and select **Delete**. If you used Way A, there is no rule to delete.
2. Delete the vault, then purge it. In the portal, open the vault and select **Delete**. In the CLI (set `RG` and `VAULT` again first if Cloud Shell restarted):

   ```bash
   az keyvault delete --name "$VAULT" --resource-group "$RG"
   az keyvault list-deleted --resource-type vault
   az keyvault purge --name "$VAULT"
   ```

   Delete is not purge. Soft-delete is on for every vault and cannot be turned off, so a deleted vault stays recoverable for the retention time (90 days unless you set another) and keeps its name. Purge removes it for good and cannot be undone. It works here because purge protection is off. Only the subscription owner or someone with the Key Vault Purge Operator role can purge. Role assignments on a soft-deleted vault are deleted and do not come back if you recover it.

   Portal purge: search for **Key vaults**, select **Manage deleted vaults** (if you do not see it, look in the toolbar menu), choose your subscription, select your vault and use the purge option. The CLI commands above are the sure way. `az keyvault list-deleted` should show nothing for your vault afterwards.
3. Stop the VM: open `vm-azb-win01`, select **Stop**, and read the status. It must say **Stopped (deallocated)**.

End state: VM Stopped (deallocated), no `allow-rdp-my-ip` rule.

The vault is gone and the public IP `pip-azb-win01` is still there. Keep `rg-azb-lab` and the VM (Lab 12), and `rg-azb-core`, the budget `budget-azb-core` and the other items from earlier labs. The managed identity stays on the VM and costs nothing. If you stop the series here, [Lab 19](/azure-basics-labs/when-something-breaks/) has the full clean up.

## Where this is used in AVD

AVD deployments use the same two ideas: a Key Vault holds secrets such as a domain-join or local admin password, and a managed identity lets Azure reach that vault without a stored credential. The session host article lists a Key Vault with private network access as needing a managed identity. See [Create, Update and Replace Session Hosts](/azure-virtual-desktop/create-update-replace-session-hosts/). The golden image article describes Azure Image Builder creating a Key Vault during a build: [Build and Maintain a Golden Image](/azure-virtual-desktop/build-and-maintain-a-golden-image/).

## Next lab

[Lab 16: Log Analytics and a heartbeat alert](/azure-basics-labs/log-analytics-alert/) adds a place to collect logs and an alert that tells you when something happens.

## Sources

- [Provide access to Key Vault keys, certificates, and secrets with Azure role-based access control](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide)
- [Plan for Azure RBAC as the default access control model in Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/access-control-default)
- [Quickstart: Create a key vault using the Azure portal](https://learn.microsoft.com/en-us/azure/key-vault/general/quick-create-portal)
- [Quickstart: Set and retrieve a secret from Azure Key Vault using the Azure portal](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-portal)
- [Quickstart: Set and retrieve a secret from Azure Key Vault using Azure CLI](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-cli)
- [Azure Key Vault keys, secrets, and certificates overview](https://learn.microsoft.com/en-us/azure/key-vault/general/about-keys-secrets-certificates)
- [Azure Key Vault basic concepts](https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts)
- [Azure Key Vault soft-delete overview](https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview)
- [Azure Key Vault recovery management with soft delete and purge protection](https://learn.microsoft.com/en-us/azure/key-vault/general/key-vault-recovery)
- [Tutorial: Use a Windows VM system-assigned managed identity to access Azure Key Vault](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/tutorial-windows-managed-identities-vm-access)
- [How to use managed identities for Azure resources on an Azure VM to acquire an access token](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token)
- [Configure managed identities for Azure resources on a VM using the Azure portal](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/qs-configure-portal-windows-vm)
- [Run scripts in your Windows VM by using action Run Commands](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/run-command)
- [Assign Azure roles using the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal)
- [Add role assignment conditions for Key Vault secrets by using Azure CLI](https://learn.microsoft.com/en-us/azure/key-vault/general/howto-abac-conditions-cli)
- [Azure built-in roles for Security](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/security)
