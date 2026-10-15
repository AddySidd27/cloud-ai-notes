export default {
  name: "AdnanSiddiqui.com",
  tagline: "Cloud architecture. Engineering. Real-world technology.",
  description: "Deep technical guides, architecture insights, hands-on engineering and practical solutions across Azure, AVD, Windows 365, Citrix, AWS and modern infrastructure.",
  url: process.env.SITE_URL || "https://adnanasiddiqui.com",
  repo: "https://github.com/AddySidd27/Azure_landing_zone",
  author: "Adnan Ahmed",
  role: "Senior Solutions Architect",
  featured: 63, // article order number shown as the feature on the home page; it needs a diagram
  credentials: [],
  certifications: [
    { code: "MCT", name: "Microsoft Certified Trainer", issuer: "Microsoft" },
    { code: "ASA", name: "Microsoft Certified: Azure Solutions Architect Expert", issuer: "Microsoft" },
    { code: "AVD", name: "Microsoft Certified: Azure Virtual Desktop Specialty (AZ-140)", issuer: "Microsoft" },
    { code: "AZ-104", name: "Microsoft Certified: Azure Administrator Associate", issuer: "Microsoft" },
    { code: "CCP-V", name: "Citrix Certified Professional – Virtualization (CCP-V)", issuer: "Citrix" },
    { code: "CCA-V", name: "Citrix Certified Associate – Virtualization (CCA-V)", issuer: "Citrix" },
  ],
  bio: "I design and explain Azure landing zones and end-user computing platforms. Each article starts from the basics, defines every term, and is checked against Microsoft Learn before it goes out.",
  year: new Date().getFullYear(),
};
