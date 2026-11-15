// A series groups articles. The tag must match the tag in the articles' front matter.
export default [
  {
    slug: "azure-landing-zone",
    tag: "alz",
    category: "azure",
    name: "Azure Landing Zone",
    title: "Azure Landing Zone Engineering Series",
    short: "What an Azure landing zone is and how to plan one, from ownership and identity to networking and rollout.",
    blurb: "This series explains what an Azure landing zone is and how to plan one. It covers who owns what, identity, how resources are organized, networking, security and rollout. It is for people who are new to Azure landing zones. Each article explains its terms before using them and lists its sources at the end.",
  },
  { slug: "azure-virtual-desktop", tag: "avd-series", category: "avd", name: "Azure Virtual Desktop", title: "Azure Virtual Desktop Engineering Series", short: "How Azure Virtual Desktop is built, how it fails, and how to plan identity, networking, profiles and images.", blurb: "This series explains Azure Virtual Desktop (AVD). You will learn how it is built, how it fails, and how to plan identity, access, licensing, clients, networking, profiles and images. It is for engineers who run or plan to run AVD. Some articles include screenshots from a real environment. Each article says what was tested and what was not." },
  { slug: "windows-365-enterprise", tag: "w365-series", category: "windows-365", name: "Windows 365", title: "Windows 365 Enterprise Engineering Series", short: "A Windows 365 Cloud PC from licensing and network choices to Intune management, for a first pilot.", blurb: "This series follows a Windows 365 Cloud PC from licensing and network choices to setup, Intune management and daily operations. It is for admins planning a first pilot. Each article says what I tested and what I did not." },
  { slug: "terraform-labs", tag: "terraform-lab", category: "labs", name: "Terraform labs", title: "Terraform Labs for Azure Virtual Desktop", short: "Terraform projects that build Azure Virtual Desktop environments, with the code, a diagram and the steps to run and check each one.", blurb: "These labs build Azure Virtual Desktop environments from Terraform code. Each article explains what the code creates, how to run it, the steps you finish by hand, how to check the result, and what you would change before production use. The code is in the article or in a GitHub repository." },
  { slug: "azure-basics-labs", tag: "azure-basics-lab", category: "labs", name: "Azure basics labs", title: "Azure Basics Labs for Beginners", short: "Short hands-on labs on the Azure basics you need before Azure Virtual Desktop: accounts, identity, MFA, networking, virtual machines, storage and monitoring.", blurb: "These labs teach the Azure basics you need before you build Azure Virtual Desktop. Each lab is mostly steps: do it in the portal, repeat it with the Azure CLI, and use Terraform where it helps. Each one has a diagram, a check, a cleanup, and a note on where the same skill is used in Azure Virtual Desktop. Do them in order in a test tenant, not a work tenant." },
];
