---
title: "Key Vault and Managed Identity: Let a VM Read a Secret Without a Password"
seoTitle: "Azure Key Vault and Managed Identity for Beginners"
layout: post.njk
permalink: "/azure-basics-labs/key-vault-managed-identity/"
order: 325
tags: [azure-basics-lab]
deck: "You store a demo secret in Azure Key Vault and read it from inside your Windows VM, using the VM's own identity instead of a password."
description: "Beginner Azure lab: create a Key Vault with Azure RBAC, store a demo secret, and read it from a Windows VM with its managed identity and the IMDS token endpoint."
---

By the end of this lab you will have a Key Vault with one demo secret in it, and your Windows VM from Lab 12 will read that secret by itself. No password, key or connection string is saved on the VM to make that work.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn. There is no Terraform in this lab, because I could not check the Key Vault Terraform resources against Learn.

Azure Key Vault is a service that stores sensitive values, such as passwords and keys, and decides who may read them. A managed identity is a sign-in that Azure creates and looks after for a resource, such as a VM. You will use both.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway Azure account.
- [Lab 2: Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/): you need Cloud Shell or the CLI for the CLI part.
- [Lab 3: Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): `rg-azb-core` and the budget stay in place.
- [Lab 7: RBAC roles](/azure-basics-labs/rbac-roles/): you have seen a role assignment before. This lab uses it twice.
- [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the Windows VM `vm-azb-win01` in `rg-azb-lab`, with its system-assigned managed identity turned on. You sign in to it the same way as in that lab. Lab 12 told you to remove the RDP rule (`allow-rdp-my-ip`) from the network security group `nsg-azb-vm` at the end. To connect now, add that rule again for your current public IP address, as Lab 12 showed, and remove it again in "Clean up".
- Time: about 40 minutes, plus a few minutes of waiting for a role to take effect.
- Cost: Key Vault is billed by use, so a few calls in this lab cost very little. The VM from Lab 12 keeps costing money while it runs, so start it before you begin and deallocate it at the end. See the [Key Vault pricing page](https://azure.microsoft.com/pricing/details/key-vault/) for current figures.
- Role: Owner on the subscription or on `rg-azb-lab`. Learn says you must be able to write role assignments, and names Owner and User Access Administrator as roles that can.
- Use the same region you picked in Lab 8, in every step.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top right of the portal before you change anything.
- Store a demo value only. Never type a real password, key or token into this vault.
- Do not turn on purge protection. Learn says it cannot be turned off again, by anyone, and then you cannot delete the vault for good until the retention time ends. This lab does not need it.
- Leave the network access settings of the vault at their defaults.
- Do not paste the access token from the VM into chats, tickets or notes. It is a working credential for a short time.
- Azure already requires MFA for portal and CLI changes. Expect the MFA prompt when you sign in as an admin.

## What the lab builds

![A left-to-right diagram. You, as a Key Vault Secrets Officer, create a demo secret in a key vault in the resource group rg-azb-lab. A Windows VM with a system-assigned managed identity and the role Key Vault Secrets User asks the local identity endpoint at 169.254.169.254 for a token, then sends the token to the key vault and gets the secret back.](/img/basics/key-vault-managed-identity.svg)

*Source: [Provide access to Key Vault keys, certificates, and secrets with Azure RBAC](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide), [Use a Windows VM system-assigned managed identity to access Azure Key Vault](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/tutorial-windows-managed-identities-vm-access), [How to use managed identities for Azure resources on an Azure VM to acquire an access token](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token) and [Key Vault soft-delete overview](https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### Part 1: Check the VM identity and create the vault

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant name at the top right.
2. Start the VM from Lab 12 if it is stopped. Open it, then go to **Security** > **Identity**. On the **System assigned** tab, check that **Status** is **On**. If it is **Off**, select **On** and **Save**. Learn describes this page for turning the identity on.

**Idea 1: secret, key and certificate.** A key vault holds three kinds of object. A **secret** is any value you want to keep tight, such as a password or a connection string. Key Vault returns the value to whoever is allowed to read it. A **key** is a cryptographic key used to encrypt, decrypt or sign. Learn says Key Vault is designed so the key itself is not handed out. A **certificate** is an X.509 certificate that Key Vault can renew. Learn says that when you create one, Key Vault also creates a key and a secret with the same name. This lab uses a secret only.

3. In the portal search box, type **Key vaults** and open it. Select **Create**. If the portal sends you to **Create a resource** and asks for **Key Vault**, pick that and select **Create**.
4. On the first page, set:
   - **Subscription**: your test subscription.
   - **Resource group**: `rg-azb-lab`.
   - **Key vault name**: a name of your own, 3 to 24 characters, letters, digits and hyphens. Key vault names are unique across all of Azure, so add five random digits, for example `kv-azb-48213`. If the portal says the name is taken, pick other digits. Write the name down.
   - **Region**: the region you chose for all labs.
   - **Pricing tier**: Standard.
5. Look for the setting that says how access is controlled. Some versions of the page call the tab **Access configuration**. Choose **Azure role-based access control**, not **Vault access policy**. Learn says newer vaults use Azure RBAC by default, but pick it on purpose and read the setting before you go on.
6. Open the **Recovery options** tab, if the page has one. Soft-delete is on and cannot be turned off. Leave **purge protection** unticked. Leave the retention days as they are.
7. Do not change the **Networking** tab. Select **Review + create**, then **Create**. When it finishes, select **Go to resource** and note the **Vault URI**. It looks like `https://<vault-name>.vault.azure.net/`.

Check: on the vault's **Overview** page you see your vault name and Vault URI. Under **Settings** > **Properties** (the name can vary) the permission model reads Azure role-based access control.

### Part 2: Give yourself a data role and add the secret

**Idea 2: management plane and data plane.** Learn splits access to a vault in two. The **control plane** (management plane) is where you manage the vault itself: create it, delete it, change its settings. The **data plane** is where you work with what is inside: read and write secrets, keys and certificates. They are controlled separately. The Owner and Contributor roles work on the control plane, so they do not let you read or write a secret. Learn says that with an Azure RBAC vault, Owner or Contributor do not give access to secret values, and `az keyvault secret set` fails with a Forbidden error for them. You need a data-plane role. Two are used here:

- **Key Vault Secrets Officer**: any action on secrets, except managing permissions. For you.
- **Key Vault Secrets User**: read secret contents. For the VM. It cannot write.

An Owner can give themselves the data role, as you do next. That is allowed, and it is a separate step on purpose.

8. In your vault, open **Access control (IAM)**. Select **Add** > **Add role assignment**.
9. On the **Role** tab, search for **Key Vault Secrets Officer**, select it, then **Next**.
10. On the **Members** tab, leave **Assign access to** on **User, group, or service principal**. Select **Select members**, find your admin account, select it, then **Select**.
11. Select **Review + assign** twice.
12. Wait one to five minutes. Learn says a role can take a few minutes to take effect, and a Forbidden error right after assigning usually means it has not reached the vault yet.
13. Open **Objects** > **Secrets**. Select **Generate/Import**. Set **Upload options** to **Manual**. For **Name** type `demo-secret`. Learn says a secret name is 1 to 127 characters, starts with a letter, and uses only letters, digits and hyphens. For **Value** type `demo-value-not-a-password`. Leave the rest as it is and select **Create**.
14. Select `demo-secret`, then the current version. Select **Show Secret Value**. You should see your demo value.

Check: the secret list shows `demo-secret` as enabled, and **Show Secret Value** works for you. If you see an authorization error, wait a few more minutes and refresh the page. Learn says browsers cache and a refresh may be needed.

### Part 3: Give the VM's identity the reader role

**Idea 3: managed identity.** Normally a program that wants a secret needs a password to ask for it, and that password has to be stored somewhere. That is the problem Key Vault is meant to remove, and a plain password would bring it back. With a managed identity, Azure creates an identity for the VM in Microsoft Entra ID and looks after its credentials. Your code on the VM asks a local address, `169.254.169.254`, for a token. That address is the Azure Instance Metadata Service (IMDS), and only the VM itself can reach it. The token proves who the VM is. Nothing is stored on the VM. Learn says Azure rotates the identity for you and recommends this way of signing in to Key Vault. One thing to know: Learn says all code running on the VM can ask for that token, so the security boundary is the VM.

15. In your vault, open **Access control (IAM)** again. Select **Add** > **Add role assignment**.
16. On the **Role** tab, select **Key Vault Secrets User**, then **Next**.
17. On the **Members** tab, set **Assign access to** to **Managed identity**. Select **Select members**.
18. In the **Select managed identities** pane, choose your subscription, set the managed identity type to **Virtual machine** (the list may call it system-assigned managed identity, then pick the service), and select your Lab 12 VM. Select **Select**.
19. Select **Review + assign** twice.
20. Open **Role assignments** on the same IAM page. Check that you see **Key Vault Secrets Officer** for your account and **Key Vault Secrets User** for the VM.
21. Wait one to five minutes before the next part.

### Part 4: Read the secret from inside the VM

22. Connect to the VM the way you did in Lab 12 and open **Windows PowerShell**.
23. Ask IMDS for a token for Key Vault. Learn's example uses this call. The `Metadata` header is required, and must be the lower-case word `true`:

```powershell
$Response = Invoke-RestMethod -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net' -Method GET -Headers @{Metadata="true"}
$KeyVaultToken = $Response.access_token
```

24. Use the token to read the secret. Replace `<vault-name>` with your vault name:

```powershell
$Secret = Invoke-RestMethod -Uri "https://<vault-name>.vault.azure.net/secrets/demo-secret?api-version=2016-10-01" -Method GET -Headers @{Authorization="Bearer $KeyVaultToken"}
$Secret.value
```

Check: the last line prints `demo-value-not-a-password`. You got it with no password on the VM. If you see 403 Forbidden, the role has not taken effect yet. Wait two minutes and run step 24 again. If the token call fails, read "The most common mistake".

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/). Check the tenant and subscription first, then set the variables. Use your own region and your own five digits for the vault name.

```bash
az account show --query "{tenant:tenantId, subscription:name}" -o table

LOCATION="<your-region>"            # the one region you use for the whole series
RG="rg-azb-lab"
VM="vm-azb-win01"
VAULT="kv-azb-<5 random digits>"    # 3-24 characters, letters, digits, hyphens, unique in Azure
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

Wait one to five minutes, then add the secret and read it back:

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

Check: `az role assignment list --scope "$VAULT_ID" --query "[].{role:roleDefinitionName, who:principalName}" -o table` lists both roles. Then do steps 22 to 24 of the portal part inside the VM. Reading from inside the VM is the point of the lab, so there is no CLI version of it.

## Terraform

No Terraform in this lab. I could not check the Terraform resources for a key vault and a secret, or their RBAC settings, against Learn, and I do not want to give you code I have not checked. If you want the Terraform version later, start from [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/) and the provider documentation for the key vault resources.

## Check that it works

- The vault exists in `rg-azb-lab`, uses Azure role-based access control, and has no purge protection.
- `demo-secret` exists, and you could read it as yourself after the Officer role took effect.
- The IAM page shows Key Vault Secrets Officer for you and Key Vault Secrets User for the VM.
- Inside the VM, the token call returned a token and the secret call printed your demo value.
- You can explain why Owner on the resource group alone did not let you read the secret.

## The most common mistake

Assigning the VM (or yourself) a management role and expecting it to read secrets. Owner and Contributor manage the vault. They do not read or write what is inside it. Learn says you need a data-plane role such as Key Vault Secrets Officer or Key Vault Secrets User, and that role assignments can take a few minutes to work.

Three smaller ones, all with the same 403 or empty result:

- Calling the secret URL too soon after the role assignment. Wait, then retry.
- Leaving the vault on **Vault access policy**. The roles in this lab only work on vaults that use Azure role-based access control. Learn says changing the model makes the old access policies stop counting.
- Leaving out the `Metadata: true` header, or using `http://localhost`. Learn says a missing header gives a `bad_request_102` error. The token call also fails if the VM has no managed identity switched on.

## Clean up

First remove the RDP rule again, the same way as in Lab 12: open `nsg-azb-vm`, **Inbound security rules**, tick `allow-rdp-my-ip`, **Delete**. Sign out of the VM first.

Then delete the vault and nothing else. In the portal, open the vault and select **Delete**. In the CLI:

```bash
az keyvault delete --name "$VAULT" --resource-group "$RG"
```

Delete is not purge. Learn says soft-delete is on for every vault and cannot be turned off. A deleted vault stays recoverable for the retention time, 90 days unless you set another, and during that time nobody can create a vault with the same name. Learn also says role assignments on a soft-deleted vault are deleted, and they do not come back if you recover it. For a standard vault, Learn says a soft-deleted vault does not incur charges.

If you want the name back, or want the vault really gone, you can purge it, because purge protection is off. Learn says only the subscription owner or someone with the Key Vault Purge Operator role can purge, and that purge is immediate and cannot be undone.

- Portal: search for **Key vaults**, select **Manage deleted vaults** at the top, choose your subscription, tick your vault, and select **Purge**.
- CLI: `az keyvault list-deleted --resource-type vault`, then `az keyvault purge --name "$VAULT"`.

Keep for later labs:

- `rg-azb-lab` and the VM from Lab 12. Deallocate the VM when you stop for the day, as in [Lab 13: VM size, disk, stop and deallocate](/azure-basics-labs/vm-size-disk-stop-deallocate/). The managed identity stays on the VM. It costs nothing.
- `rg-azb-core`, the budget and the other items from earlier labs.

If you do not purge, write the vault name down. You cannot use it again for 90 days. [Lab 19](/azure-basics-labs/when-something-breaks/) lists the vault purge as one of its last cleanup steps.

## Where this is used in AVD

AVD deployments use the same two ideas: a Key Vault holds secrets such as a password, and a managed identity lets Azure reach that vault without a stored credential. The session host article lists a Key Vault with private network access as needing a managed identity. See [Create, Update and Replace Session Hosts](/azure-virtual-desktop/create-update-replace-session-hosts/). The golden image article describes Azure Image Builder creating a Key Vault during a build: [Build and Maintain a Golden Image](/azure-virtual-desktop/build-and-maintain-a-golden-image/).

## Next lab

[Lab 16: Log Analytics workspace and an alert](/azure-basics-labs/log-analytics-alert/) adds a place to collect logs and an alert that tells you when something happens.

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
- [Assign Azure roles using the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal)
- [Add role assignment conditions for Key Vault secrets by using Azure CLI](https://learn.microsoft.com/en-us/azure/key-vault/general/howto-abac-conditions-cli)
- [Azure built-in roles for Security](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/security)
