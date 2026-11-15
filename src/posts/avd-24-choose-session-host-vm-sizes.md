---
title: "Choose Session Host VM Sizes: Compute, GPU, Disks and Quota"
seoTitle: "Choose AVD Session Host VM Sizes: GPU, Disks, Quota"
layout: post.njk
permalink: "/azure-virtual-desktop/choose-session-host-vm-sizes/"
order: 124
part: 24
tags: [avd-series]
# PENDING: publication date and final slug/order approval; the date lives in src/_data/articleMeta.js
deck: "Read a VM size name, start from the sizing guidelines, decide if you need a GPU, choose the OS disk and security type, and check quota before a deployment fails."
description: "How to choose an Azure Virtual Desktop session host VM size: the sizing guidelines, GPU sizes, OS disks, Trusted launch, and quota and capacity checks."
---

You have decided who the users are for Azure Virtual Desktop (AVD), which apps they run and how many sessions you expect. The next question is which virtual machine (VM) to buy. That is the topic of this article.

[The host pool planning article](/azure-virtual-desktop/plan-your-host-pools/) shows how to group users, test with real work and count hosts. This article starts after that. It covers how to read a VM size name, what the sizing guidelines say, when you need a GPU, which disk and security options matter, and how to check quota and capacity so a deployment does not fail halfway. How to create and replace the hosts is in [the session host lifecycle article](/azure-virtual-desktop/create-update-replace-session-hosts/).

## Key terms

| Term | Meaning |
|---|---|
| Session host | A virtual machine (VM) that runs the user's desktop or apps. |
| Host pool | A group of session hosts that users connect to. |
| Single-session and multi-session | On a single-session host, one user is signed in at a time. This is the case in a personal host pool, where each user gets their own session host. On a multi-session host, several users are signed in at the same time. This is the case in a pooled host pool, where users share session hosts, with Windows 11 Enterprise multi-session. |
| vCPU | A virtual processor. With hyper-threading (one core runs two tasks at once), one physical core can appear as two vCPUs. |
| VM size, series and family | A size is one VM configuration, such as Standard_D8s_v5. A series is a group of sizes with similar hardware. A family is a group of series for a type of work, such as general purpose or GPU. |
| GPU | A graphics processing unit. It draws and encodes pictures much faster than the CPU can. |
| OS disk | The disk that holds Windows and the apps installed on that session host. |
| Temporary disk | A disk on the physical server that runs the VM. Its data can be lost, for example when the VM is moved or deleted. |
| Ephemeral OS disk | An OS disk placed on the VM's local storage instead of on remote Azure storage. It is not kept when the VM is deleted or reimaged. |
| Generation 2 VM | A newer VM generation. Trusted launch works only with Generation 2 VMs. |
| Trusted launch | A VM security setting that protects the boot process. It uses Secure Boot and a virtual Trusted Platform Module (vTPM). Secure Boot checks that only trusted software starts. A vTPM is a virtual chip that stores keys and boot measurements. |
| Quota | How many vCPUs or VMs your subscription is allowed to deploy in a region. A deployment fails if it goes over quota. |
| Capacity | The compute that Azure actually has free in a region or zone. Quota does not guarantee it. |
| Premium SSD and Standard SSD | Two types of Azure disk. Premium SSD is faster. |
| Azure Files | A shared network file store in Azure. AVD profiles are often kept there. |
| Breadth-first and depth-first | Two ways to load balance users. Breadth-first sends each new user to the VM with the fewest sessions. Depth-first fills one VM before it uses the next. |
| NVMe | A very fast type of disk storage. |
| Availability zone | A separate datacenter location inside one Azure region. |
| Session host configuration | A host pool setting that lets AVD create and update session hosts for you. See the lifecycle article. |
| RemoteApp and desktop app group | A desktop app group gives users a full desktop. A RemoteApp group gives users single apps. |
| Snapshot | A saved copy of a disk at one moment. |
| Intune and Group Policy | Two tools that push settings to many computers. |
| AVD Insights | An AVD monitoring dashboard in the Azure portal. |
| Autoscale | An Azure Virtual Desktop feature that scales session hosts up and down on a schedule to match demand. |
| Scaling plan | The schedule and rules that autoscale follows. |
| Savings plan and reserved instance | Two ways to pay less for compute. You agree to use Azure for a set time, and the price drops. |
| Reimage | Rebuild a VM from its image. |
| Deallocated | A VM that is stopped and no longer billed for compute. |
| Frame encoding and codec | Before the session picture is sent to the user, it is compressed. The method is called a codec. AVC/H.264 and HEVC/H.265 are two codecs. |

![Four steps. 1: know the workload (light, medium, heavy or power; single-session or multi-session). 2: choose the VM: size, GPU (optional), OS disk and security type. 3: Azure checks quota and capacity. If both are fine, it creates the VM and you go to step 4. If not, go back to step 2 and change the size, zone or region, or request more quota. 4: after it runs, measure with AVD Insights, use autoscale, and use savings plans or reserved instances.](/img/avd/AVD-Session-Host-VM-Size.svg)

*Source: [Session host virtual machine sizing guidelines](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/virtual-machine-recs), [Check vCPU quotas](https://learn.microsoft.com/en-us/azure/virtual-machines/quotas) and [Enable GPU acceleration for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/graphics-enable-gpu-acceleration). The documentation has no single diagram of these steps, so the layout is simplified.*

## Start from the sizing guidelines

The documentation has a page of session host sizing guidelines. It says its examples are generic and only for initial estimates, and that you should scale the deployment to what your users need.

For a single-session host, the page recommends at least two physical CPU cores per VM, typically four vCPUs with hyper-threading. That means two cores run as about four vCPUs. It gives these examples:

| Workload type | Minimum vCPU, RAM and OS storage | Example Azure sizes |
|---|---|---|
| Light | 2 vCPUs, 8 GB RAM, 32 GB storage | D2s_v5, D2s_v4 |
| Medium | 4 vCPUs, 16 GB RAM, 32 GB storage | D4s_v5, D4s_v4 |
| Heavy | 8 vCPUs, 32 GB RAM, 32 GB storage | D8s_v5, D8s_v4 |

For a multi-session host, the page also gives users per vCPU. [The host pool planning article](/azure-virtual-desktop/plan-your-host-pools/) already covers that table. Here we look only at the minimum VM and example sizes:

| Workload type | Minimum vCPU, RAM and OS storage | Example Azure sizes |
|---|---|---|
| Light, medium and heavy | 8 vCPUs, 16 GB RAM, 32 GB storage | D8s_v5, D8s_v4, F8s_v2, D8as_v4, D16s_v5, D16s_v4, F16s_v2, D16as_v4 |
| Power | 6 vCPUs, 56 GB RAM, 340 GB storage | D16ds_v5, D16s_v4, D16as_v4, NV6, NV16as_v4 |

NV6 is a first-generation NV size. It is in the sizing page but not in the GPU table later in this article, so check that table before you use it.

The page suggests at least 30 GB of profile storage for each user in both tables. The size names are explained in the next section. The examples are v4 and v5 sizes. The pages used for this article do not say which newer series are supported, so check any size you choose against the unsupported list below. Then test it (judgement).

### Few big VMs or many small VMs

The page gives clear advice about size for multi-session hosts:

- A VM should have at least four cores. Windows needs at least two threads running at the same time for some drawing work. With only two cores and several users, the screen and apps become unstable.
- Do not go above 32 cores. The page says more cores mean more effort to keep them in step. After about 16 cores the gain is small. Two 16-core VMs give a better experience than one 32-core VM.
- With 20 or more users on one VM, several smaller VMs would perform better than one or two large ones. Breadth-first load balancing spreads users across VMs. Depth-first fills one VM before it uses the next.
- Many small VMs are easier to switch off. A large VM nearly always has someone signed in, so you cannot shut it down to save money or to update it.

### What changes when you add CPU or memory

The page lists the main factors in capacity. In short:

- Doubling the cores does not double the number of users. The page gives a scaling factor of about 1.5 to 1.9, and says it is higher when you start with few cores. Going from 4 to 8 cores gains more than going from 8 to 16.
- Memory can matter more than CPU when it is the limit. The page says going from 8 GB to 16 GB can more than double the users you can support.
- Signing in uses a lot of CPU. Plan for the busiest sign-in time, such as 9 AM, and not only for the steady state.
- Running on a VM costs capacity. The sizing page reports 15–20% less capacity than a physical server with no VM, based on internal testing. It says response times can be 10–20% higher.
- Fast storage helps apps that use the disk a lot. The page suggests SSD or NVMe drives (fast disks).
- Network delay, packet loss and jitter also change the experience. [The bandwidth and latency article](/azure-virtual-desktop/plan-bandwidth-latency-and-quality-of-service/) covers them.

## Read a VM size name

A size name packs several facts into letters. The naming page gives this pattern: family, optional subfamily, number of vCPUs, optional extra letters for features, and a version.

| Part | Example | What it means |
|---|---|---|
| Family | D | A group of sizes for a type of work. D is general purpose, with a balanced ratio of CPU to memory. F is compute optimized, with more CPU for each unit of memory. E is memory optimized, with more memory for each CPU. N is GPU. |
| Subfamily | NV | In N sizes, a second letter marks the type. V means visualization and graphics optimized. C means compute intensive. |
| vCPUs | 8 | The number of vCPUs. |
| Feature letters | a, d, s | `a` is an AMD processor. `d` means the VM has a local temporary disk. `s` means it can use Premium SSD disks. `l` means low memory. `p` means an ARM-based processor. |
| Version | v5 | The version of the series. |

So Standard_D8s_v5 is a general purpose VM with 8 vCPUs that can use Premium SSD disks, in version 5. Standard_D16ds_v5 adds a local temporary disk. Standard_NV16as_v4 is a graphics-optimized N size with 16 vCPUs and an AMD processor, in version 4.

The letters matter for AVD in three ways. A `d` in the name means the size has a local temporary disk. An ephemeral OS disk can use that disk, or the VM's cache. Some older sizes, such as Standard_D8s_v3, have a temporary disk even without a `d`, so the letters are only a hint. Check the size's specification. A `p` size is ARM-based, which AVD does not support for session hosts. An N size is the way to get a GPU.

## What AVD does not support

The prerequisites page lists what you cannot use as a session host:

- 32-bit operating systems.
- N, KN, LTSC and other Windows editions that the page does not list.
- Ultra disks as the OS disk type.
- Ephemeral OS disks for Azure VMs. The pages disagree: this page says not supported, but the AVD ephemeral page says AVD supports them. See the section on OS disks and the table at the end.
- Virtual Machine Scale Sets.
- Arm64-based Azure VMs.

The supported systems for session hosts are Windows 11 and Windows 10 Enterprise and Enterprise multi-session, and Windows Server 2016, 2019, 2022 and 2025, in each case 64-bit. [The image article](/azure-virtual-desktop/build-and-maintain-a-golden-image/) covers the image.

## When you need a GPU

By default, a remote session is drawn by the CPU, even on a VM that has a GPU. The GPU page says GPU acceleration has three parts:

- **GPU-accelerated app rendering.** Apps use the GPU to draw their graphics.
- **GPU-accelerated frame encoding.** RDP encodes each picture before it sends it to the user. With a GPU, this uses AVC/H.264 or HEVC/H.265. The page says it gives higher frame rates and a better experience, but can use more network bandwidth and more session host and client resources.
- **Full-screen video encoding.** This uses the H.264/AVC 444 graphics mode, or HEVC when HEVC encoding is on.

The sizing page adds a reason to look at GPUs even without graphics apps: on a VM with no GPU, RDP encodes pictures in software and shares CPU time with everything else. If a user's screens together are bigger than 3840 × 2160 pixels (4K), the page says this can cause block artifacts, pixelation, frozen frames and cache corruption. The page then suggests a GPU-enabled session host.

The page lists these sizes. The list may change, so check the page. A series name such as NVv4 groups sizes such as Standard_NV16as_v4.

| Azure VM series | GPU app rendering | GPU frame encoding |
|---|---|---|
| NVv3-series | Supported | HEVC/H.265 and AVC/H.264 |
| NVv4-series | Supported | AVC/H.264 |
| NVadsA10 v5-series | Supported | HEVC/H.265 and AVC/H.264 |
| NCasT4_v3-series | Supported | HEVC/H.265 and AVC/H.264 |

Notes from the page:

- The NC, NCv2, NCv3, ND and NDv2 series are not generally appropriate as session hosts. They are meant for compute work such as machine learning and do not accelerate most apps or the Windows user interface.
- NVIDIA sizes include a GRID license (NVIDIA's license for sharing a GPU between users) for 25 users at the same time.
- Bigger GPUs are likely to give a better experience for the same number of users. Smaller and fractional (shared) GPU sizes let you tune cost and quality more finely.
- You must install the graphics driver yourself, and only drivers distributed by Azure are supported. For NVIDIA sizes it must be the GRID driver, not the CUDA driver.
- You turn on the features with a policy in Intune or Group Policy, then restart the session host. The policy names include "Use hardware graphics adapters for all Remote Desktop Services sessions" and "Configure H.264/AVC hardware encoding for Remote Desktop connections". The page warns that if you turn on "Prioritize H.264/AVC 444 Graphics mode" but not the hardware encoding policy, the CPU may still do the encoding.
- HEVC/H.265 needs more: Windows 10 or 11, a desktop app group (RemoteApp is not supported), and a client with HEVC decoding and a supported app. It also needs NVIDIA GRID driver 16.2 (537.13) or later on NVIDIA sizes, multimedia redirection turned off on the session host, and the policy "Configure H.265/HEVC hardware encoding for Remote Desktop Connections" under the Azure Virtual Desktop administrative template.

To check that it works, open Task Manager in the session and look at the GPU, or open Connection Information and look for "Codecs Used: HEVC". The page also names Event Viewer events: ID 170 for AVC hardware encoding and ID 162 for the full-screen profile in use.

## Choose the OS disk

Each session host has an OS disk that holds Windows and the apps you install on that host. The sizing tables ask for 32 GB of OS storage as a minimum, and 340 GB for the power workload. The user's profile is not on this disk. It lives on shared storage such as Azure Files, as the host pool article explains.

**Ephemeral OS disks.** The AVD page on ephemeral OS disks says AVD now supports them, but its notes still say "during preview" for the limits below. The What's new page called this a public preview in October 2025 and said "now available" in June 2026. The prerequisites page and the AVD FAQ still say they are not supported. The AVD ephemeral OS disk page says they suit hosts that keep no user data on the disk. They give lower latency and faster reimaging (rebuilding the VM from the image). The pages disagree, so check the current status before you use them. What to know:

- They are supported only in pooled host pools that use a session host configuration. [The lifecycle article](/azure-virtual-desktop/create-update-replace-session-hosts/) explains session host configurations.
- During the preview, only the Standard SSD disk type is supported. Premium SSD and NVMe are not. It is not supported in Azure Government during the preview.
- The Windows image must fit in the VM's temporary disk (or its cache). The page gives an example: a 127 GiB Windows 11 multi-session marketplace image fits on the 200 GiB temporary disk of Standard_D8s_v3. GiB is a slightly bigger unit than GB (1 GiB is about 1.07 GB).
- The VM cannot be deallocated. It can only be restarted, reimaged or deleted. The page therefore recommends dynamic autoscale with "Minimum percentage of active hosts" set to 100%, so that scaling only creates and deletes hosts.
- Snapshots, image capture, Azure Disk Encryption, Azure Backup and Azure Site Recovery are not supported.
- The Learn troubleshooting page for ephemeral OS disks says to keep user profiles in FSLogix profile containers (profiles stored on shared storage), because the OS disk is not kept when the host is rebuilt.

## Security type and image generation

When you create a host pool, you choose a security type for the session hosts: Standard, Trusted launch virtual machines, or Confidential virtual machines (VMs with extra hardware protection for data in use; not covered in this article). Choosing Trusted launch selects Secure Boot and the vTPM for you. Choosing Confidential also turns on integrity monitoring.

The Trusted launch page says it is the default for newly created Generation 2 VMs when the image, disk and size all support it. It works only with Generation 2 VMs, a supported size and a supported operating system image. A few Generation 2 sizes do not support it. The Trusted launch FAQ shows how to check a size:

```powershell
$region = "centralus"
$vmSize = "Standard_D8s_v5"
(Get-AzComputeResourceSku | where {$_.Locations.Contains($region) -and ($_.Name -eq $vmSize) })[0].Capabilities
```

Change the first two values to yours. If the output includes `TrustedLaunchDisabled True`, that Generation 2 size does not support Trusted launch. If the size is Generation 2 and there is no `TrustedLaunchDisabled` line, the size supports it.

Size, image and disk must also fit together. The troubleshooting page for session host configurations gives example errors such as `ComputeSkuIncompatibleWithImageHyperVGeneration` and `ImageDiskTypeIncompatible`, and says to check the prerequisites when the combination of size, disk, image and virtual network is not compatible. The virtual network must also be in the same Azure region as the session hosts.

## Check quota and capacity

A deployment can fail even when the size is right. There are two separate checks.

**Quota.** Quota is your subscription's permission to deploy vCPUs or VMs. The vCPU quota has two levels in each region: Total Regional vCPUs, and a limit for each VM size family. A new VM must fit in both, or the deployment is not allowed. The page also says quota counts cores that are in use, allocated and deallocated, so a stopped VM still uses quota. GPU sizes have their own family lines in the usage list, for example NV.

**Capacity.** Capacity is what Azure has available in the region or zone. The page says that even with enough quota, a deployment can fail because Azure does not have enough capacity for that size. In that case, try another size, zone or region. To make sure a size is available, the page points to on-demand capacity reservation (you pay to have Azure keep that VM size free for you).

The AVD troubleshooting page lists errors for size and region combinations, such as `VmSkuNotAvailableInRegion`, `VmSkuNotAvailableInRegionDueToRestriction` and `AvailabilityZoneNotAvailable`. It suggests the `Get-AzComputeResourceSku` cmdlet to see restrictions. To see your usage and limits:

```powershell
Get-AzVMUsage -Location "Central US"
```

```azurecli
az vm list-usage --location "Central US" -o table
```

More points from the documentation:

- The limit on session hosts you can create in one step differs by page: 400 on the regional host pools page, 500 on the session host configuration deployment page, and about 132 for each template run in the FAQ (800 template objects, about 6 per VM). Quota can lower all of them. Check the page for your method.
- When you run a session host update, the service checks the subnet and the core quota first. The check does not guarantee capacity during the update, so the page says to keep the batch size within the remaining quota.
- The prerequisites page says West US 3 is not supported for host pools that use a session host configuration. Regions can change. Checking the page first is my advice (judgement).

## Keep the cost down

The documentation says the VM instances are usually the biggest part of the cost of session hosts. These are the levers it describes:

- **Autoscale.** A scaling plan starts and stops hosts to match demand. You cannot use autoscale and the older Azure Automation scaling tool on the same host pool.
- **Savings plans and reserved VM instances.** The cost page says you can use either to reduce compute cost.
- **AVD Insights.** Its utilization view shows when sessions peak and when hosts sit idle. The page says this can show where to use a scaling plan, resize VMs or reduce the number of hosts.

## A simple way to choose

This order is my own method, not a documented procedure (judgement):

1. Start from the user group, the apps and the number of users that the host pool plan gives you.
2. Pick candidate sizes from the sizing guidelines. The sizing page gives two ranges, 6 to 24 vCPUs in one place and 4 to 24 in another. I use 4 to 24 as a working range for multi-session hosts (judgement). The multi-session table suggests 8 or more for most workloads. Using only a few different sizes keeps things simple (judgement).
3. Decode the name. Check that the size is not Arm64 or otherwise unsupported.
4. Decide if you need a GPU, an ephemeral OS disk or a security type other than Standard.
5. Check the region, the quota for the size family and the capacity, with a small test deployment.
6. Test with real work. Watch CPU, memory and input delay, as the host pool article describes.
7. Write down the size, the reasons and the tests, so that the next change starts from facts.

## Where the documentation differs

| # | Topic | What the pages say | What to do |
|---|---|---|---|
| 1 | Ephemeral OS disks | The prerequisites page and the FAQ list ephemeral OS disks for Azure VMs as not supported. The AVD ephemeral OS disk page says AVD supports them, with limits marked "during preview", for pooled host pools with a session host configuration. The What's new pages say public preview (October 2025) and now available (June 2026). | Not resolved. The article describes the AVD page and tells you to confirm the current status before use. |
| 2 | Smallest multi-session VM | The sizing table gives 8 vCPUs as the minimum for light, medium and heavy workloads. The text says four cores is the lowest recommended number, and 6 vCPUs is the minimum for power work. | These do not clash. Four cores is the lowest a stable multi-session VM should have. Eight vCPUs is where the table starts for light, medium and heavy work. Start at 8 or more and test. |
| 3 | Upper and lower size limit | The same page says vCPUs in one place and cores in another: it first says to limit VM size to between 6 and 24 vCPUs, and later gives 4 to 24 cores as the recommended range. | The checklist uses 4 to 24 as a working range (judgement). |

## Common mistakes

- **Taking the guideline table as a final size.** The page calls its examples generic and for initial estimates only.
- **Choosing one big VM.** A big VM is harder to shut down and, above about 16 cores, adds less capacity for each core.
- **Choosing a GPU VM without the driver or the policy.** The session is still drawn by the CPU until you install the driver and turn on the policy.
- **Choosing an NC, NCv2, NCv3, ND or NDv2 series size for graphics.** The page says they do not accelerate most apps or the Windows interface. NCasT4_v3 is the listed exception.
- **Expecting a stopped VM to free quota.** Deallocated VMs still count.
- **Putting profiles on an ephemeral OS disk.** The disk is erased when the host is rebuilt.
- **Checking quota only when the deployment fails.** Check both quota levels and the capacity first.

## How to check a setup

1. Look up the VM size in the sizing guidelines. Compare the vCPUs and memory with the workload you tested.
2. Run `Get-AzVMUsage -Location "<region>"` and compare the usage with the number of vCPUs you plan to add. Check Total Regional vCPUs and the size family line.
3. Run the `Get-AzComputeResourceSku` check for your size and region. Look for restrictions, and for `TrustedLaunchDisabled` if you plan to use Trusted launch.
4. For a GPU host, open Task Manager in a session and confirm the GPU is in use. Look for "Codecs Used: HEVC" in Connection Information if you enabled HEVC.
5. For an ephemeral OS disk, open the session host in the portal and confirm that its disk is ephemeral. Check that the scaling plan keeps 100% of hosts active.
6. After the first week with real users, open AVD Insights. Compare CPU, memory and input delay with your plan and change one thing at a time.

## Sources

[Session host virtual machine sizing guidelines](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/virtual-machine-recs), [Enable GPU acceleration for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/graphics-enable-gpu-acceleration) and [Check vCPU quotas](https://learn.microsoft.com/en-us/azure/virtual-machines/quotas).

The article also uses these Microsoft Learn pages: the AVD prerequisites, the AVD ephemeral OS disk page, the Learn troubleshooting page for ephemeral OS disks, the Azure VM naming conventions, the Azure VM sizes overview, the Trusted launch page and FAQ, and the AVD troubleshooting pages for session host configurations.
