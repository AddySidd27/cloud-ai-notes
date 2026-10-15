// Presentation metadata only. Keyed by article order. The article text itself is never edited here.
const published = "2026-10-07";
export default {
  201: { tags: ["Windows 365", "Cloud PC", "Fundamentals"], published: "2026-10-11" },
  202: { tags: ["Windows 365", "Pilot planning"], published: "2026-10-11" },
  203: { tags: ["Windows 365", "Networking"], published: "2026-10-11" },
  204: { tags: ["Windows 365", "Provisioning"], published: "2026-10-11" },
  205: { tags: ["Windows 365", "Connection"], published: "2026-10-11" },
  206: { tags: ["Windows 365", "Intune"], published: "2026-10-11" },
  "206.5": { tags: ["Windows 365", "Restore", "Recovery"], published: "2026-10-15" },
  207: { tags: ["Windows 365", "Security"], published: "2026-10-11" },
  208: { tags: ["Windows 365", "ANC troubleshooting"], published: "2026-10-11" },
  209: { tags: ["Windows 365", "Operations"], published: "2026-10-11" },
  101: { tags: ["AVD", "Fundamentals"], published: "2026-10-11" },
  102: { tags: ["AVD", "Architecture"], published: "2026-10-11" },
  103: { tags: ["AVD", "Deployment preparation"], published: "2026-10-11" },
  104: { tags: ["AVD", "Identity", "Microsoft Entra"], published: "2026-10-11" },
  106: { tags: ["AVD", "Host pools", "Capacity planning", "Images"], published: "2026-10-12" },
  105: { tags: ["AVD", "Networking", "Hub-and-spoke"], published: "2026-10-11" },




  1: { tags: ["Landing zone", "Fundamentals"], published },
  2: { tags: ["Platform landing zone", "Ownership"], published },
  3: { tags: ["Tenant", "Billing", "Management groups", "Subscriptions"], published },
  4: { tags: ["Operating model"], published },
  5: { tags: ["Requirements", "Compliance", "Cost"], published },
  6: { tags: ["Billing", "Microsoft Entra", "Tenant"], published },
  7: { tags: ["Identity", "Azure RBAC", "Microsoft Entra"], published },
  8: { tags: ["MFA", "Conditional Access", "PIM", "Privileged access"], published },
  9: { tags: ["Management groups", "Resource organization"], published },
  10: { tags: ["Networking", "Hub-and-spoke", "Virtual WAN"], published },
  11: { tags: ["Security", "Zero Trust", "Key Vault"], published: "2026-10-08" },
  13: { tags: ["Monitoring", "Azure Monitor", "Backup and recovery"], published: "2026-10-08" },
  14: { tags: ["Governance", "Azure Policy", "Cost management"], published: "2026-10-08" },
  15: { tags: ["DevOps", "Infrastructure as code", "CI/CD"], published: "2026-10-08" },
  16: { tags: ["Landing zone", "Migration", "Platform engineering"], published: "2026-10-08" },
  61: { tags: ["Rollout", "Landing zone", "Platform engineering"], published: "2026-10-09" },
  62: { tags: ["Rollout", "Migration", "Landing zone"], published: "2026-10-09" },
  63: { tags: ["Use cases", "Landing zone", "Management groups"], published: "2026-10-14" },
  // Which articles sit on the homepage in "Featured". Edit the numbers to change it.
  featured: [10, 1, 8],
  // Homepage "Architecture and engineering" plates: area label and the article whose diagram is shown.
  plates: [
    { area: "Networking", order: 10, img: "post-10-hub-spoke-and-virtual-wan.svg" },
    { area: "Identity", order: 7, img: "post-07-roles-groups-scopes.svg" },
    { area: "Resource organization", order: 9, img: "post-09-management-group-hierarchy.svg" },
  ],
};
