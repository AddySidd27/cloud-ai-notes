---
title: "Windows 365 Enterprise: Operate, Roll Out and Extend"
seoTitle: "Windows 365: Operate, Roll Out and Extend"
layout: post.njk
permalink: /windows-365/operate-and-extend/
order: 209
part: 10
tags: w365-series
deck: "Move from one verified pilot to a supportable service, then evaluate Boot, Switch and Offline as separate exercises."
---

A Cloud PC pilot becomes a service when someone owns assignment, support, updates, recovery and cost. Preserve the pilot's evidence, then expand in small groups with a clear rollback decision for each wave.

## Write the operating record

| Area | Record before rollout |
| --- | --- |
| Eligibility | Who approves a license and group membership change |
| Provisioning | Policy owner, image, join type, network and region |
| User support | Connection method, error capture and escalation path |
| Endpoint management | Configuration, application, update and compliance owners |
| Recovery | Restore decision owner, user data location and service expectations |
| Cost | Seat inventory, unused licenses and any customer Azure infrastructure |

When a new user joins, check the license and group, then watch provisioning and first connection. When a user leaves, follow the organization's retention and offboarding process before changing licensing. Do not treat a portal deletion as a harmless housekeeping step: it may affect data and recovery windows. Test the support process with one real ticket before expanding to the next group.

## Walk one user through the service

1. **Joiner:** approve the user and license, add the user to the intended pilot group, and check the provisioning and first-session result. Save timestamps and owner.
2. **Mover:** document the new requirements before changing group or policy targeting. Check the effect on the existing Cloud PC and data first; a network or region move is a separate planned action.
3. **Support:** ask the user for the exact client, error, time and last successful sign-in. Check service status, Cloud PC state, device check-in and the matching sign-in event before taking a remote action.
4. **Leaver:** follow the organization's retention and recovery policy, record the license and Cloud PC state, then deprovision only through an approved offboarding workflow.

The [editable joiner/mover/leaver draw.io source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/source/09-joiner-mover-leaver-lifecycle.drawio) and [Cloud PC operations source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/source/10-cloud-pc-lifecycle-operations.drawio) show the decision paths. They are design diagrams, not evidence of a completed leaver or restore test.

In my pilot, a [controlled restart and reconnect](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-07-controlled-restart.md) was recorded on October 7. This verifies the specific user-facing action described there. It does not prove point-in-time restore, resize, reprovision or a full offboarding sequence. Microsoft's [remote actions reference](https://learn.microsoft.com/en-us/windows-365/enterprise/remotely-manage-cloud-pc) explains the supported actions and where to check their statuses.

## Roll out in waves

Start with the pilot user, add a small group with varied applications, then widen only after connection, management and support results are recorded. For each wave, track assigned licenses, provisioned Cloud PCs, connection failures, policy conflicts and time to resolve. Keep known gaps visible. A progress dashboard should distinguish **planned**, **configured**, **observed** and **blocked**; it should not convert a written procedure into a completed lab.

My [complete learning journey](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/00-complete-learning-journey.md) links the 15 use cases and their evidence limits. The [validation status](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) is the place to check what was actually seen. The existing Microsoft-hosted Cloud PC provides a useful management pilot, while the separate ANC test remains unresolved.

## Optional experiences belong after the core pilot

Windows 365 Boot, Switch and Offline are distinct user experiences with device, client and service prerequisites. Evaluate each against the current Microsoft Learn instructions, a supported device, an explicit success test and a recovery route. Do not present an optional experience as working merely because a Cloud PC exists. Record a separate test for its launch, reconnect behavior and policy impact.

This series is a starting route, not a claim that every optional feature and destructive recovery action has been performed in my tenant. Use its worksheets to reproduce the steps, and compare each portal choice with the linked current product documentation.

Return to [Start Here](/windows-365/start-here/) or explore the [engineering repository](https://github.com/AddySidd27/Windows365-enterprise-engineering).

### Microsoft Learn

- [Windows 365 deployment guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-management)
- [Windows 365 Cloud PC lifecycle](https://learn.microsoft.com/en-us/windows-365/enterprise/lifecycle)
- [Windows 365 documentation](https://learn.microsoft.com/en-us/windows-365/)
