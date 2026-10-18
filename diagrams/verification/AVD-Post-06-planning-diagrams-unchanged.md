# Post 6 planning diagrams: checked, unchanged

Files: AVD-Post-06-published-resource-relationships, image-release-plan, storage-relationship, load-test-plan and company-pool-plan (.png) in `src/img/avd/`. All five are the author's planning diagrams, kept as they are and not redrawn.

## Learn references
- [Azure Virtual Desktop terminology](https://learn.microsoft.com/en-us/azure/virtual-desktop/environment-setup)
- [Prerequisites](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites)
- [Store FSLogix profile containers](https://learn.microsoft.com/en-us/azure/virtual-desktop/store-fslogix-profile)

## Verification checklist
- [x] Application group assigned to one workspace; app group draws on one host pool; users assigned on the app group.
- [x] Pooled hosts are updated by redeploying from updated images; personal hosts are assigned to one user.
- [x] Profile containers live on Azure Files or Azure NetApp Files, separate from the pooled VM OS disk (Learn also lists Storage Spaces Direct, so the list is not exhaustive).
- [x] Pool sizing arithmetic in the company pool plan re-computed: 1,800+2,200+700+300 = 5,000; 67x18 = 1,206; 46x24 = 1,104; 119 pooled + 1,000 personal = 1,119.

## Assumptions and design choices (not Learn requirements)
- Waves, approval gates, user densities, personas, GPU choice, load-test tooling and sign-off are the author's design choices.

## Unresolved questions for review
- The image release plan's 'replicate to target region' and the load test plan's PerfMon step have no supporting page among those the reviewer fetched; add a Compute Gallery or performance counter citation, or keep them as the author's.

## Recheck, 18 October 2026
This diagram was not changed in the Learn recheck pass. Its earlier record stands, and it was not re-compared against a Learn picture in this pass.
