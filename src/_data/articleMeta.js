// Presentation metadata only. Keyed by article order. The article text itself is never edited here.
const published = "2026-10-07";
export default {
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
  // Which articles sit on the homepage in "Featured". Edit the numbers to change it.
  featured: [10, 1, 8],
  // Homepage "Architecture and engineering" plates: area label and the article whose diagram is shown.
  plates: [
    { area: "Networking", order: 10, img: "post-10-hub-spoke-and-virtual-wan.svg" },
    { area: "Identity", order: 7, img: "post-07-roles-groups-scopes.svg" },
    { area: "Resource organization", order: 9, img: "post-09-management-group-hierarchy.svg" },
  ],
};
