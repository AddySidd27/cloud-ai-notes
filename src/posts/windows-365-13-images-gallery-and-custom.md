---
title: "Windows 365 Images: Gallery Images and Custom Images"
layout: post.njk
permalink: /windows-365/images/
order: 212
part: 13
tags: w365-series
deck: "Choose between a gallery image and a custom image, add a custom image in Intune, and know what happens to existing Cloud PCs when you change the image."
---

A Cloud PC is built from an image. This article is for administrators who must decide which image a provisioning policy should use. You will be able to compare gallery and custom images, check what a custom image must meet, add one in Intune, pick it in a policy, and predict what a later image change does to Cloud PCs that already exist.

This article covers Windows 365 Enterprise. The [provision article](/windows-365/provision/) already walks through a policy with a gallery image, so this article does not repeat that walkthrough. It goes deeper on the image itself.

## Key terms

- **Cloud PC:** a Windows desktop that Windows 365 hosts for a user. The user can connect to it from anywhere, on any device.
- **Microsoft Intune admin center:** the web portal where you manage Windows 365. This article calls it Intune.
- **Image:** a saved copy of a Windows installation that Windows 365 uses as the starting point for every new Cloud PC.
- **Gallery image:** an image that Microsoft supplies in the Windows 365 gallery. You choose it while you create a provisioning policy.
- **Custom image:** an image that you build yourself and upload to Windows 365.
- **Provisioning policy:** the set of rules, including the image, that tells Windows 365 how to build Cloud PCs for the users in a group.
- **Provisioning:** the automatic building of a Cloud PC.
- **Reprovision:** delete a Cloud PC and build a new one from the current provisioning policy.
- **Virtual machine (VM):** a computer that runs as software in Azure. A Cloud PC is a VM.
- **Azure subscription:** the Azure account area where your Azure resources, such as a managed image, live and are billed.
- **Azure region:** a datacenter location in Azure.
- **Generalized image:** an image prepared so it can be used to create many machines.
- **Generation 2 (Gen2):** the newer type of virtual machine image. New custom images must use it.
- **Managed image:** an image stored in Azure, captured from a generalized VM.
- **Azure Compute Gallery:** an Azure service that stores and organizes images. A custom image can come from here instead of a managed image.
- **Image definition and image version (Azure Compute Gallery):** the image definition is the gallery entry that contains your image. An image version is one specific image inside that definition.
- **Trusted Launch:** an Azure security type for virtual machines. You choose the security type when you create a VM or an image definition. It matters here because an Azure Compute Gallery image must use Trusted Launch, and a managed image must not.
- **Service principal:** the identity that a service uses to get access to your Azure resources.
- **Microsoft Entra join:** the Cloud PC joins Microsoft Entra ID directly.
- **Microsoft Entra hybrid join:** the Cloud PC joins your Active Directory domain, which is synced to Microsoft Entra ID. You pick the join type in the provisioning policy.
- **Azure network connection:** a link between Cloud PCs and your on-premises resources.
- **Single-session and multi-session:** single-session Windows serves one user per VM. Multi-session editions of Windows 10 and Windows 11 are built for several users and cannot be used for Windows 365 custom images.
- **OS disk and data disk:** the OS disk holds Windows. A data disk is an extra disk attached to the VM.
- **Recovery partition:** a separate hidden area on the OS disk used for Windows repair.
- **N and LTSC editions:** N editions are Windows without some media features. LTSC is the long term service channel edition of Windows.
- **Co-management:** a device that is managed by both Intune and Configuration Manager.

## The two kinds of image

![Flow from gallery images and custom images into a provisioning policy, then to Cloud PCs. Custom images come from a managed image or an Azure Compute Gallery image, are added in Intune and checked by Windows 365. Changes apply to new or reprovisioned Cloud PCs only.](/img/windows-365/windows-365-images.svg)

*Source: [Device images overview](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images), [Add or delete custom device images](https://learn.microsoft.com/en-us/windows-365/enterprise/add-device-images) and [Edit provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/edit-provisioning-policy).*

| Compare | Gallery image | Custom image |
|---|---|---|
| Who builds it | Microsoft | You |
| Where you find it | In the policy, on the Image page | In Intune under Custom images, after you add it |

If no gallery image meets your needs, you can upload up to 20 of your own custom images. Windows 365 suggests using one of the Cloud PC gallery images as a starting template for a custom image.

## Gallery images

The gallery has Windows Enterprise images. They are replicated to all Azure regions, so provisioning is quick. Each one has some audit policies already turned on, such as account policies, logon and logoff, object access and policy change.

There are three sets of images to choose from:

1. **With preinstalled Microsoft 365 Apps.** Microsoft 365 Apps and the Teams optimizations are already installed. Some Microsoft Edge and Outlook first-time settings are also preapplied.
2. **No preinstalled applications.** A plain image. Look for names without **M365 Apps**.
3. **Developer Configuration with preinstalled Microsoft 365 Apps.** It adds developer tools and settings, and sets up Windows Subsystem for Linux (WSL) with Ubuntu. It is not supported on 2 vCPU (two virtual CPU cores) or GPU licenses, because they do not support nested virtualization. You are responsible for managing and maintaining the third-party applications in it. They are not currently manageable through Intune as packaged applications. If you need Intune to manage them, uninstall them and redeploy them through Intune.

### How gallery images are updated

Supported gallery images are updated every month, after the Windows security patch release schedule. The update happens around the middle of the month. The updated image is available in Intune for provisioning around the end of the third week. Each one includes the Windows monthly update, Microsoft 365 Apps updates (the latest Monthly Enterprise Channel release), Microsoft Teams updates and Teams WebRTC redirector updates.

Newly provisioned Cloud PCs get the latest image automatically. For existing Cloud PCs, you get the update by reprovisioning.

## What an image must meet

Gallery images and custom images must both meet these rules. You check them yourself for a custom image that you build.

- A supported version of Windows 10 or Windows 11 Enterprise.
- Generation 2. Existing Gen1 custom images stay active, but new ones must be Gen2.
- A clean Windows install that was never joined to Active Directory or Microsoft Entra ID, never enrolled in Intune, and never enrolled for co-management.
- A generalized VM image.
- Single-session. Multi-session is not supported.
- No recovery partition.
- The default 64 GB OS disk size. Windows 365 adjusts the size to match the size in the license description.
- No data disks attached to the VM before you capture the image.
- No FSLogix components. FSLogix is a profile tool used with Azure Virtual Desktop.
- No more than 3,000 apps in the Start menu.

A custom image has more rules:

- It must exist in an Azure subscription.
- It must be stored as a managed image, or in an Azure Compute Gallery with the security type set to Trusted Launch.
- It must not contain Azure Virtual Desktop components, such as the Remote Desktop Agent Boot Loader and the Remote Desktop Services Infrastructure Agent. Azure Virtual Desktop is a separate Microsoft desktop service.
- A custom image that includes Teams needs extra optimization steps (see [Create a Cloud PC custom image that supports Microsoft Teams](https://learn.microsoft.com/en-us/windows-365/enterprise/create-custom-image-support-teams)).
- Images with disk encryption sets are not supported.

Some editions of Windows, such as N and LTSC, are not supported.

One detail is easy to miss. If you create a VM in Azure to build a managed image, choose the **Standard** security type when you create the VM. Managed images do not support Trusted Launch VMs. If you import from an Azure Compute Gallery instead, the image definition must have Trusted Launch enabled.

Building the image is outside this article. To make a managed image from a generalized VM, see [Create a managed image of a generalized VM in Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/capture-image-resource).

## Add a custom image in Intune

Before you start, you need a generalized Gen2 image in an Azure subscription that meets the rules above, either as a managed image or in an Azure Compute Gallery. There are two ways to add it. Both start in the [Microsoft Intune admin center](https://intune.microsoft.com/).

### From an Azure managed image

1. Go to **Devices** > **Provision Cloud PCs** > **Custom images** > **Add** > **Managed image**.
2. In the **Add image** pane, enter the **Image name**. It appears in the Custom images list.
3. Enter the **Image version** in the format Major.Minor.Patch, for example 0.0.1 or 1.5.13. This is a version label that Windows 365 shows in the Custom images list.
4. Choose the **Subscription** the image came from.
5. Choose the **Source Image**. The list shows the images in that subscription that meet the prerequisites.
6. Select **Add**.

### From an Azure Compute Gallery

First give the **Windows 365** service principal the **Compute Gallery Image Reader** role on the gallery. Its application ID is 0af06dc6-e4b5-4f28-818e-e78e62d137a5. In some organizations this application is named **Cloud PC**. You need an account that can create role assignments on the gallery, such as Owner, User Access Administrator or Role Based Access Control Administrator.

1. In the [Azure portal](https://portal.azure.com), open the Azure Compute Gallery that contains your image.
2. Select **Access control (IAM)** > **Add** > **Add role assignment**.
3. Assign the role. For detailed steps, see [Assign Azure roles using the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal).
4. Select **Review + assign**.

The image definition must have these options: x64, Windows, and security type Trusted Launch.

Then add the image in Intune:

1. Go to **Devices** > **Provision Cloud PCs** > **Custom images** > **Add** > **Azure Compute Gallery image**.
2. Enter the **Image name** and the **Image version** (Major.Minor.Patch). These two show in the Custom images list. This version label is separate from the gallery image version in step 5.
3. Choose the **Subscription** of the gallery.
4. Choose the **Azure Compute Gallery**. The **Image definition** fills in automatically.
5. Choose the gallery **Image version** that you want to upload.
6. Adding a scope tag is optional.

### What Windows 365 does with the upload

Windows 365 copies the image to a temporary subscription. It then checks that the image meets the requirements and deploys a virtual machine to confirm the image can boot and be provisioned as a Cloud PC. For Microsoft Entra hybrid join, it copies the image to every Azure region where you have an Azure network connection. For Microsoft Entra join, it copies the image to the provisioned region during provisioning.

The image shows up when you select an image for a provisioning policy only after the upload succeeds.

Storing a managed image in Azure has storage costs. You can delete the managed image from Azure after it has uploaded successfully to Intune.

## Choose the image in a provisioning policy

Create a policy, or edit one, and go to the **Image** page of the policy wizard. Set **Image type**:

- **Gallery image:** choose **Select**, pick an image from the gallery, then choose **Select** again.
- **Custom image:** choose **Select**, pick an image from the list, then choose **Select** again. The list shows the images you added in Intune.

Select **Next** to continue. See [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) for the other pages of the wizard.

## What happens when you change the image later

To change the image on an existing policy, open **Devices** > **Provision Cloud PCs** > **Provisioning policies**, select the policy, and under **Properties** select **Edit** next to **Image**.

Saving the change does not touch the Cloud PCs that already exist. Only Cloud PCs that are newly provisioned, or reprovisioned, use the new image. To move an existing Cloud PC to the new image, you must reprovision it.

| Situation | What happens |
|---|---|
| A new user is assigned to the policy and has a valid Cloud PC license | The Cloud PC is built with the changed image |
| Existing Cloud PC, policy image changed | No change until it is reprovisioned |
| Existing Cloud PC is reprovisioned | It is deleted and rebuilt from the current policy |

Reprovisioning wipes the user's Cloud PC. The user is signed out, and all data, apps and customizations are deleted. The user gets a new Cloud PC, often with a new device name. The Cloud PC must have the status **Failed** or **Provisioned**. In Intune, go to **Devices** > **All Devices**, choose the Cloud PC, select **Reprovision**, then select **Yes**. Tell users first and make sure important data is backed up. The [Cloud PC lifecycle article](/windows-365/cloud-pc-lifecycle/) covers reprovisioning in more detail, and the [Reprovision a Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/reprovision-cloud-pc) page lists which actions do and do not trigger it.

A point-in-time restore, a resize and a restart do not reprovision the Cloud PC. Neither does changing the policy by itself.

For Windows 365 Flex in shared mode, the rule is different. After you change the image, use **Reprovision** on the policy page. Without that bulk reprovision, the new image does not apply to new Cloud PCs added to the pool or to Cloud PCs that you reprovision one at a time.

## Delete a custom image

Go to **Devices** > **Provision Cloud PCs** > **Custom images**, select the check box next to the image, select **Delete**, then confirm. You cannot delete an image that a provisioning policy uses. Delete the policy first, then the image. Check which Cloud PCs the policy serves before you delete it.

## Common mistakes

- Building the custom image from a machine that was joined to a domain or enrolled in Intune. The image must never have been joined or enrolled.
- Choosing a Trusted Launch VM when building a managed image. Use the Standard security type for a managed image. Trusted Launch is for the Azure Compute Gallery image definition.
- Forgetting the Compute Gallery Image Reader role for the Windows 365 service principal.
- Leaving a data disk attached, a recovery partition in place, or FSLogix or Azure Virtual Desktop components in the image.
- Using a multi-session, N or LTSC edition of Windows.
- Changing the image in the policy and expecting existing Cloud PCs to update. They do not until you reprovision them.
- Going straight to the policy after you add an image. The image appears in the policy only after the upload succeeds.
- Reprovisioning without warning the user. All local data is deleted.
- Trying to delete an image that a policy still uses.

## How to validate this in your environment

1. In Intune, open **Devices** > **Provision Cloud PCs** > **Custom images**. Confirm your image is listed with the right name and version. Wait for the upload to finish.
2. Open or create a provisioning policy. On the **Image** page, set **Image type** to **Custom image** and confirm the image appears in the list.
3. Before any change, note the image on the policy under **Properties** > **Image**.
4. After you edit the image, confirm an existing Cloud PC is unchanged.
5. Add a test user to a group that the policy is assigned to, and give that user a Cloud PC license. Provisioning starts automatically. Sign in and look for something that exists only in the new image, such as an app you added.
6. Only on a disposable test Cloud PC, run **Reprovision** and confirm the rebuilt Cloud PC has the same difference. Do not do this on the only working Cloud PC.

## Sources

- [Device images overview](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images)
- [Add or delete custom device images](https://learn.microsoft.com/en-us/windows-365/enterprise/add-device-images)
- [Edit provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/edit-provisioning-policy)
