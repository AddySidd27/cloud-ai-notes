---
title: "Platform Automation and DevOps"
slug: "platform-automation-and-devops"
series: "Azure Landing Zone"
part: ""
post_number: 15
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/platform-automation-devops"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/automation"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/infrastructure-as-code-updates"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/implementation-options"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/devops-principles-and-practices"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/devops-teams-topologies"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/development-strategy-development-lifecycle"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/environments"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/development-strategy-test-driven-development"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/security-considerations-overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/security-considerations-tools"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/testing-approach"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-areas"
    checked_on: "2026-10-08"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/platform-automation-devops.md"
diagrams:
  - file: "../diagrams/post-15-test-driven-development-cycle.svg"
    type: learn-layout-redraw
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/development-strategy-test-driven-development (picture test-driven-development-process.png, read from the MicrosoftDocs GitHub source)"
    source: "../diagrams/post-15-test-driven-development-cycle.drawio"
production_section_written_by_addy: true
layout: post.njk
permalink: "/azure-landing-zone/platform-automation-and-devops/"
order: 15
deck: "The Platform automation and DevOps design area of an Azure landing zone is about building, changing and running the landing zone through code, review and automatic pipelines, instead of clicking in the portal."
next_num: "16"
next_title: "Minimum Viable Platform Landing Zone: What to Build First"
tags: [alz]
---



## 1. The problem

In the earlier posts you made many decisions: management groups, identity, networks, security, monitoring and policy. Someone has to turn those decisions into real Azure resources. And the landing zone does not stand still. Policies are updated, subscriptions are added, and fixes are needed.

If a person does all of this by hand in the portal, no one can see what was changed, who approved it, or why two environments look different.

Microsoft's Platform automation and DevOps design area asks how to deploy and manage the landing zone with code, review and automation. On the design areas page, Learn lists it last (letter I). Its goal is to line up your DevOps ways of working with the landing zone's whole life: creating it (provisioning), managing it, changing it over time (evolution) and running it (operations). Learn says this uses "extreme automation" and Infrastructure as Code.

In this post, "Learn" means the Microsoft Learn website. The post follows Learn's pages for this design area: the overview, automation, using infrastructure as code to update, the implementation options, DevOps principles, team topologies, the development lifecycle, environments, the testing approach, test-driven development, and the two security pages. Learn's overview groups its pages in four parts: Platform automation, DevOps, Development strategy and Security. I cover the implementation options and the infrastructure as code page early, because they explain the tools.

## 2. Simple explanation

### Words you need first

Earlier posts defined these words: landing zone, design area, platform team, workload, subscription, subscription vending, Azure Policy, Azure RBAC, Microsoft Entra ID, Microsoft Entra tenant, multifactor authentication (MFA), Active Directory, Privileged Identity Management (PIM), service principal, managed identity, Azure Key Vault, Microsoft Defender for Cloud, Microsoft Sentinel, SIEM, Log Analytics workspace, Conditional Access, least privilege, configuration drift, Terraform, Sandbox, DeployIfNotExists (DINE), and Canary environment.

The words below are new, or are explained more fully here. Each is in plain words, based on Microsoft Learn. Where a row says "my plain words", the explanation is mine, not Microsoft's.

**Code and review**

| Word | What it means |
|---|---|
| Infrastructure as code (IaC) | My plain words: describing Azure resources in code files, so they can be deployed the same way every time. |
| Declarative and imperative | Microsoft says IaC is declarative: you describe the end result, and the tool brings the real state in line with it. Scripts, for example in Azure CLI or Azure PowerShell (command-line tools for Azure), are imperative: you list the steps to run, and the result depends on the state before. |
| Bicep | My plain words: Microsoft's language for describing Azure resources as code. Learn calls it a domain-specific language for deploying Microsoft-developed Azure resources. |
| Everything as Code (EaC) | Microsoft's name for keeping all of it in code, not only the resources. Learn lists Infrastructure as Code, Policy as Code, Configuration as Code, Deployment as Code and Documentation as Code. |
| Policy as Code (PaC) | Microsoft's name for deploying and managing Azure Policy through IaC. |
| Version control, Git and repository | My plain words: version control keeps every change to your code with its history. Git is the version control system Learn recommends. A repository (repo) is the place where one project's code and history live. |
| Commit | My plain words: one saved set of changes in Git. |
| Branch, merge and `main` | My plain words: a branch is a separate line of changes. Merging joins a branch's changes into another branch. `main` is the name of the main branch. |
| Pull request and branch policy | My plain words: a pull request asks the team to review a branch before it is merged. Microsoft describes a branch policy as a rule that protects an important branch, for example a minimum number of reviewers. |
| Trunk-based development and feature branch | Microsoft says that in trunk-based development, developers commit to a single branch, which helps continuous integration. My plain words: a feature branch is a short branch for one change, merged back to `main`. |
| Squash | My plain words: joining all the small saves of a branch into one save. Learn says a squash merge adds all file changes to a single new commit on the default branch. |
| Peer review and the 4-eyes principle | Microsoft says teams can follow the 4-eyes principle: code changes are never made alone. Peer programming or peer review means a second person sees each change. |
| Backlog | My plain words: the list of work the team plans to do. |
| Technical debt | My plain words: work you owe later, such as a quick fix that was not reviewed. Microsoft warns that too much of it slows the team down. |
| Exemption | My plain words: a way for a workload team to ask to skip one policy rule, after approval. |

**Pipelines and tools**

| Word | What it means |
|---|---|
| CI/CD and pipeline | My plain words: continuous integration (CI) means every code change automatically triggers checks and test deployments. Continuous delivery (CD) means the tested change is deployed to an environment. A pipeline is the automatic process that runs these steps. |
| Azure DevOps and GitHub | My plain words: two services that host Git repositories and run pipelines. |
| DevOps agent (runner) | My plain words: the machine that runs a pipeline job. GitHub calls it a runner. Microsoft says Microsoft-hosted agents are kept up to date by Microsoft, and you set up and manage self-hosted agents yourself. |
| Static analysis, linter and unit test | My plain words: static analysis and a linter read your code and flag mistakes without running it. A unit test is a small automatic check of one part. |
| What-if and plan | Bicep what-if and Terraform plan show what a deployment would create, change or delete, before it runs. |
| Accelerator | Microsoft's ready-made tool that deploys the reference architecture. There is an IaC accelerator (Bicep or Terraform) and a portal accelerator. |
| Azure Verified Modules (AVM) | Microsoft's reusable, customizable building blocks for Bicep or Terraform. You can use them alone or inside the accelerator. |
| ClickOps | Microsoft's word for creating and managing resources by clicking in portals, consoles and wizards. |
| Extreme automation and self-healing | Microsoft's phrases. Extreme automation means automating everything: provisioning, configuration, platform management and the creation of landing zone subscriptions for workload teams. Self-healing is my plain words for a platform that fixes itself, for example by redeploying from code. |
| Single source of truth | Microsoft's phrase for the code system that shows what is running in each environment. |

**Teams, environments and testing**

| Word | What it means |
|---|---|
| DevOps | Microsoft says it is the union of people, processes and technology that provides continuous value to development and operations. |
| Workload team and enabling team | Platform and workload teams were defined earlier. Learn adds a third type: enabling teams, which help other teams close skill gaps, for example in DevOps. |
| Environment | A separate place to build, test or release. Learn names Development, Test, Staging, UAT (user acceptance test, where end users check the system) and Production. |
| Definition of done (DoD) and acceptance criteria | The DoD is a simple agreement between the platform team and other teams on what the landing zone must include. Acceptance criteria are the checks that show a feature is done. |
| Test-driven development (TDD) and refactor | A process where you write the test first and then the code. Microsoft calls the cycle red/green: a failing test is red, a passing test is green. To refactor means to clean up the code without changing what it does. |
| Azure Resource Graph | My plain words: a service to query the resources you have deployed. Learn says it can run data-driven tests on a landing zone. |

**Signing in and protecting the tools**

| Word | What it means |
|---|---|
| Entitlement management and access package | My plain words: a Microsoft Entra feature that gives people time-limited sets of access, called access packages. |
| Application registration and user-assigned managed identity | Two kinds of identity for a pipeline. An application registration is how a service principal is created in Microsoft Entra ID. A user-assigned managed identity is a managed identity you create as its own Azure resource. |
| Service connection | In Azure DevOps, a wrapper for the identity in Azure that a pipeline uses to deploy. |
| OpenID Connect (workload identity federation) | A way for a pipeline to sign in to Azure without a stored password or secret. Microsoft says to use it for deployment identities. |
| Claim | My plain words: a piece of information about who or what is signing in. GitHub's claims include the environment and the workflow. |
| Secret scanning and dependency scanning | My plain words: secret scanning looks for passwords in code. Dependency scanning checks the libraries your code uses for known problems. |
| Secure admin workstation (SAW) | Microsoft's name for a hardened (locked down) machine used to deploy changes to high-risk and production environments. |
| Lateral movement | My plain words: an attacker moving from one account or machine to another. |

### What the design area covers

| Part | The question it answers |
|---|---|
| Platform automation | How do you deploy and run the landing zone through code and pipelines? |
| Implementation options | Which accelerator or tool do you start with? |
| Using IaC to update | Why use IaC to keep the landing zone up to date? |
| DevOps | How do you organize the teams and measure success? |
| Development strategy | How do you handle repositories, branches, builds, environments, rollback and tests? |
| Security | How do you protect the DevOps tools and pipelines themselves? |

### Platform automation

Microsoft says the ability to make changes at scale through a set, automated process helps the organization go beyond the baseline that security, governance and management create. Its automation considerations are:

- **Everything as Code.** Teams can then see which resources are deployed, track changes and control which ones reach production.
- **The 4-eyes principle.** Use Git repositories and branch policies to enforce peer review, for example a minimum number of approvals before a merge into a protected branch.
- **CI/CD.** Every code change should start checks such as static code analysis, validation and test deployments. Microsoft calls testing early "fail fast" or "shift-left testing".
- **Deploy after review.** After changes are approved and merged into `main`, the CD process deploys them to production.
- **Extreme automation.** The aim is a platform that is self-healing and gives self-service to workload teams. Microsoft says this frees the platform team from deploying and managing the platform by hand, so it has more time to build more automation.
- **Emergency fixes.** Teams can use PIM eligible permissions (permissions you must ask for first) to get access for a fix, and later bring the fix back to code to limit drift. Or they can use code for a quick fix. Always put quick fixes in the backlog and rework them later.
- **Azure Policy as code.** Policies can automate things such as log collection. Many Policy as Code frameworks have an exemption process, so plan for workload teams to ask for exemptions.

*A note on Post 14.* Post 14 says the DINE guidance tells most customers to use DINE and Modify policies. The automation page says something that sounds different. It says to use policy-driven governance to tell workload teams when they deploy something that breaks a security control, and to consider the `deny` effect for this. It says to avoid `modify` effects here, because a policy that changes a setting at deployment makes the real resource differ from what the team's code says.

Learn does not say how the two fit. My reading: the DINE page says DINE and Modify deploy only supporting settings, never the workload resources themselves, and the automation page is about a workload team's own code drifting from what is deployed. Check both pages when you choose.

**Learn's platform automation recommendations:**

- Follow Everything as Code, and keep all the code types in version control.
- Use the 4-eyes principle with peer review.
- Adopt a branching strategy and set branch policies, so changes are merged through pull requests.
- Use CI/CD to test and deploy to different environments.
- Automate everything, including the creation of landing zone subscriptions for workload teams.
- Use the accelerator that matches your team's skills.
- Use a layered approach to add what the accelerator does not cover.
- Use code for quick fixes, and register them in the backlog.
- Manage Azure Policy as code, and set up an exemption process. Be ready to unblock teams when needed.
- Use policy-driven governance to block deployments that do not meet a security control.

### Implementation options

Microsoft says the platform landing zone can be deployed in two main ways:

- **IaC approach (recommended).** Use the platform landing zone accelerator with Azure Verified Modules for Terraform or Bicep. You can use the modules alone or inside the accelerator.
- **Portal approach.** The platform landing zone accelerator in the Azure portal works best for organizations without IaC skills, or those who prefer a visual way.

The IaC accelerator sets up a continuous delivery environment, and supports Azure DevOps and GitHub for version control, pipelines and runners. It works in four phases:

| Phase | What you do |
|---|---|
| 0. Planning | Choose the IaC language and the version control system. |
| 1. Prerequisites | Set up the credentials and subscriptions for the deployment. |
| 2. Bootstrap | Run the PowerShell module to bootstrap the Azure environment and the version control system. |
| 3. Run | Customize the code to your needs, then start the CI/CD pipelines to deploy the platform landing zone. |

**The portal accelerator.** Microsoft says it gives less flexibility and scalability than the IaC options, and that updates and version control are hard to manage without IaC. It suggests moving to IaC when possible.

**Which team starts where.** Learn says new teams that are used to the portal can start with the portal accelerator (a ClickOps approach), and later add Azure CLI, PowerShell or IaC as skills grow. Teams with established skills should rely heavily on IaC, and run all operations through the pipeline instead of using personal accounts.

**Layers.** Microsoft says IaC-based accelerators have a limited management scope. If you use one, start with the accelerator, then add a layer of automation for what your workload teams need, for example domain controller deployment for legacy applications.

### Why use IaC to update a landing zone

Microsoft says organizations should plan to deploy their landing zone with IaC. If you already built resources by hand, you must first describe them in code, because you need to map the existing resources to the desired state. The benefits Learn lists:

- **Less effort.** The tool can show what would change before you deploy (what-if or plan), so you can see how resources are set today and how an update will change them.
- **Fewer errors.** Programmatic deployments change only what is defined and have preview options, which reduces outages from failed or incomplete changes.
- **Version control and history.** Changes go through branches, and the history shows what was deployed and when. You can deploy to a test environment until you are ready to merge.
- **Testing environments.** The same definition can deploy a second environment. Learn's example is trying the Premium Azure Firewall tier in a test environment before changing production.
- **Catching drift.** The next IaC run shows where the real state differs from the code. IaC tools detect and repair drift, but Learn says they might not address all issues.

**Repository structure.** Learn says to:
- use trunk-based development with feature branches, so all changes merge back to `main` before deploying to any environment;
- use the same code for all environments, with variables to tell them apart;
- never copy and paste code between folders or branches, because this leads to drift between environments;
- run Terraform plan or Bicep what-if against all environments, including production, in a pull request. Learn says separate read-only identities make this safe.

**Hardening IaC deployments.** Learn says to:
- always deploy through continuous delivery pipelines, and avoid running deployments from local developer machines or unmanaged devices;
- use separate identities for plan or what-if (read access) and for apply or deploy (write access);
- use human approval gates for the production deploy stage, and check the plan or what-if output;
- use governed pipelines: a template stored and managed in a central place, so all deployments follow the same guardrails.

**Changes outside the code.** Learn says to make them only in an emergency, and to take care with accounts that can make them, such as PIM. The next IaC run will flag the difference. Learn also says changes made in the portal are cumbersome to bring back into code.

### DevOps: framework, metrics, tools and teams

Learn says that in a landing zone, DevOps is the framework that guides the team that owns the landing zone's whole life.

**Framework and metrics.**
- Define a DevOps framework, or line it up with your organization's DevOps and cloud adoption strategy, and connect it to your business strategy.
- Set metrics to improve DevOps performance, and make key metrics visible to everyone. For software delivery, Learn names four: Lead Time for Change (the time from idea to production), Deployment Frequency (deployments per day to production), Mean Time to Restore (the time to restore service after an incident) and Change Fail Percentage (the share of changes to production that lead to a failure). Learn also names quality metrics and business outcome metrics.
- Decide which practices to start with, based on current skills, and make a roadmap. Microsoft says using a DevOps model everywhere at once does not instantly create capable teams, so make a plan to grow skills.

**Tools.**
- Choose a set of DevOps tools that fits the framework. Avoid many different tools, because they add complexity. These are only examples from Learn, by stage: for planning, Azure Boards and GitHub; for CI and testing, Azure Repos and GitHub Repos; for CD, Azure Pipelines and GitHub Actions, with Bicep, Pulumi and Terraform listed as IaC tools under CD; for operations, Azure Automation and Azure Monitor. Learn has more examples for each stage.

**Teams.** Learn's team topologies page sets three roles:

| Team type | What Learn says |
|---|---|
| Platform team | Build a team with people from IT, security, compliance and the business. Give it company-wide functions that need to be done the same way, such as policy management, subscription provisioning, identity policies, network management and platform monitoring. Build the platform to reduce the load on workload teams, with self-service and clear guardrails. |
| Workload teams | Give them ownership of the application lifecycle. Control them with policy and Azure RBAC, not with paperwork. Do not force them to use centralized artifacts or provisioning pipelines. Set clear boundaries between the platform team and workload teams. |
| Enabling teams | Use them to close skill gaps, for example in DevOps, with time-bound support and coaching. Build reusable templates and libraries, and encourage InnerSourcing (teams contribute improvements back to shared assets), such as Azure Verified Modules. |

### Development strategy

Learn's development lifecycle page has five topics: repository, branches, automated builds, deployment and rollback. These are its recommendations, with a few considerations where noted.

#### Repository
- Use Git as the version control system.
- Use private repositories to build the landing zone. Use public repositories only for non-confidential material such as automation examples, public documentation and open-source collaboration material.
- Use an IaC approach to deploy, manage and govern cloud resources.
- *Considerations:* understand mono-repo (all code in one repository) versus multirepo (one repository per project), and set repository permissions.

#### Branches
- Adopt trunk-based development.
- Use consistent branch names, and set permissions on who can read and update a branch.
- Set branch policies: pull requests for merges into `main`, a minimum number of reviewers, a reset of approval votes when the source branch changes (votes to reject or wait stay), automatic reviewers, and a check that comments are resolved.
- Use squash as the merge strategy.

#### Automated builds
- Use CI to build and test code every time someone commits changes.
- Include unit tests for IaC (for example the Bicep linter or the ARM template test toolkit, which checks Azure's older template format) and for application code.
- Use Microsoft-hosted agents if possible. Learn says they give isolation and a clean virtual machine for each run.
- When you connect Azure DevOps or GitHub to Azure, define the scope so the connection reaches only the resources it needs.
- Use Key Vault secrets so credentials are not hard-coded.

#### Deployment
- Use CD so code is always ready to deploy to production-like environments.
- Use environments. Learn says they give deployment history, traceability of commits and work items (the tasks linked to each change), resource health and security.
- Add IaC pre-deployment checks (Bicep what-if, ARM what-if or Terraform plan) to preview what a resource would create, modify or delete.

#### Rollback
- Learn suggests a rollback plan, which means going back to a known good state. This is a consideration. Its recommendation is to use Git's undo features to revert changes to committed files, discard uncommitted changes or reset a branch.

#### Environments
Learn describes four common tiers: Development, Test, Staging and Production, with an optional UAT environment. Its points for a landing zone:
- Test environments let platform developers try changes before production. Keep environments as similar as possible, because differences cause configuration drift, which Microsoft says can cause data loss, slower deployments and failures.
- Use IaC to reduce drift between environments.
- Use checks on test results to control the move from development to production, and let failing tests stop the change.
- Always have at least one test environment, use separate service principals for test and production, and use automated checks and approvals before any change to an environment.
- The environments page says the testing approach page describes two ways to test platform changes: copy the management group hierarchy into a Canary and a Production environment, or use Sandbox subscriptions. I checked the testing approach page. It says this guidance is for platform-level changes only, such as management groups, policies and role assignments. It says this is not a common pattern for most customers and is not mandatory. It warns that if you deploy by portal, the canary and production environments may drift out of sync, and suggests moving to IaC.

#### Test-driven development
Learn says TDD means writing the tests before the code. The cycle (Figure 1) has five steps:
1. **Create a test.** Define a test that checks the acceptance criteria for a feature.
2. **Test the landing zone.** Run the new test and the existing ones. If the feature does not exist yet, the new test should fail.
3. **Expand and refactor the landing zone.** Add the code for the feature, and clean it up.
4. **Deploy the landing zone** to a controlled test or sandbox environment.
5. **Test the landing zone** again. When all tests pass, the feature is done.

You repeat the cycle until the full definition of done is met. Learn says Azure Policy is the main mechanism for testing the acceptance criteria in the DoD, and that built-in policy initiatives can test and enforce the whole DoD. It says Azure Resource Graph can run data-driven tests on what is deployed.

### Security for DevOps platforms

Microsoft says it keeps the underlying cloud infrastructure secure, but you must configure security for your own Azure DevOps organizations and GitHub. Learn groups its points like this.

#### Who can get in
- **Restrict access to the tools.** Use least privilege through Microsoft Entra ID. Use entitlement management for time-limited access packages, and PIM for just-in-time promotion to administrator roles. Consider turning off permission inheritance in Azure DevOps. For most platform team members, Learn says the Basic access level and the Contributor group at project level are enough in Azure DevOps, and a team with write access to the landing zone repository is enough in GitHub. Check that branch policies stop the Contributor group from skipping them in pull requests.
- **Restrict repository, branch and pipeline access.** This protects against unwanted or harmful changes, and stops a compromised pipeline from reaching other projects, pipelines and repositories. Learn suggests securing YAML pipelines (pipelines written as text files) step by step.
- **Choose the agent for your security needs.** Microsoft-hosted agents need no upgrades or maintenance. Self-hosted agents give more room for guardrails and can reach private networks.
- **Protect admin accounts.** The RBAC page says that for highly privileged accounts in Active Directory, credentials should not be synchronized to Microsoft Entra ID, and the reverse, to reduce lateral movement. It suggests Conditional Access policies that require multifactor authentication for Azure DevOps.

#### How pipelines sign in to Azure
- **Use secure, scoped identities.** Use a user-assigned managed identity or an application registration (service principal), never a user account. Use OpenID Connect, never client secrets or certificates. Make a separate identity for each application and environment, and a separate read-only identity for plan and what-if. Scope each identity to the subscriptions or resource groups it needs. Deploy the identities through IaC in a secure subscription vending process.
- **In Azure DevOps:** always use a service connection with OpenID Connect. Create approvals on the service connection, not on environments, because Learn says environment approvals can be bypassed in code (someone who can edit the pipeline file could skip them). Use required templates (governed pipelines) on the service connection.
- **In GitHub Actions:** use OpenID Connect and create approvals on a GitHub Actions environment. Learn also says to add the `environment` claim and the `job_workflow_ref` claim to the identity's federated credential, and to use `repository_owner_id` and `repository_id` instead of `repository`. This limits the identity to one environment, one workflow and one repository, even if the repository is renamed.
- **Use a secret store.** Avoid secrets where you can. If you cannot, never hard-code them in code or documents. Keep them in a store such as Azure Key Vault.

*Note from Learn:* the lifecycle page speaks of service connections and GitHub secrets, while the security page says to avoid secrets and use OpenID Connect. Follow the security page.

#### Checks and watching
- **Use hardened workstations.** Use secure admin workstations to deploy changes to high-risk and production environments.
- **Scan and test.** Use static code analysis, unit tests, secret scanning and dependency scanning in your pipelines. Microsoft Defender for Cloud and GitHub Advanced Security can help.
- **Watch audit events.** For Azure DevOps, review the audit events and stream them to a Log Analytics workspace or a SIEM such as Microsoft Sentinel. The RBAC page suggests Sentinel rules that alert on improper use of permissions.

## 3. Diagram

Microsoft Learn has a picture of the test-driven development cycle for a landing zone. I redrew it with the same layout.

**Figure 1. The test-driven development cycle.**

![Test-driven development cycle for an Azure landing zone. A box, Definition of done, with an arrow labelled Acceptance criteria points into a cycle of five circles that go clockwise: create a test, test the landing zone, expand and refactor the landing zone, deploy the landing zone, test the landing zone, and back to create a test.](/diagrams/post-15-test-driven-development-cycle.svg)

*Simplified diagram, redrawn by me from the Microsoft Learn picture, with the same layout. The picture has no icons. Not an official Microsoft diagram. The picture does not show the red and green tests.*

Learn has other pictures on these pages: a map of Azure tools for test-driven development, and two example DevOps toolchain pictures. I did not redraw those. The toolchain examples are in the text above.

## 4. What I have seen in production

### Mistakes to check for first

These come from Microsoft's recommendations, one line each. The next part says which ones I saw myself.

**Deployments**
- **Staying on portal clicks.** Microsoft says the portal accelerator is less flexible and scalable, and that updates and version control are hard without IaC.
- **Deploying from a laptop.** Microsoft says to always deploy through continuous delivery pipelines.
- **Copying code between folders for each environment.** Microsoft says this causes drift between environments, and to use the same code with variables.
- **No test environment.** Microsoft says to have at least one.

**Identities**
- **Using a user account, or a secret, for deployments.** Microsoft says to use scoped managed identities or service principals with OpenID Connect.
- **One identity for plan and apply, or for all environments.** Microsoft says to use separate identities per application and environment, and a read-only one for plan and what-if.
- **Approvals only on the environment in Azure DevOps.** Microsoft says to put them on the service connection, because environment approvals can be bypassed in code.

**Process**
- **Changes made outside the code.** Microsoft says to do this only in an emergency. The next IaC run will flag the difference, and bringing portal changes back into code is hard work.
- **Quick fixes that never reach the backlog.** Microsoft says to register them, to limit technical debt.
- **No policy exemption process.** Microsoft says to plan for workload teams to ask for exemptions.

### From my own projects

I saw these from the list above in my own projects:

- Staying on portal clicks. This was a real problem.
- Deploying from a laptop. This was a real problem.
- No test environment. This was a real problem.
- One identity for plan and apply, or for all environments. This was a real problem.
- Approvals only on the environment in Azure DevOps. This was a real problem.
- Changes made outside the code. This was a real problem.
- No policy exemption process. This was a real problem.

I did not mark the other three items from the list as something I saw. I leave out project details.

## 5. Repo

- Platform automation and DevOps: the decisions to make, my delivery flow, the controls from Learn, and my own practice (my short checklist): [platform-automation-devops.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/platform-automation-devops.md)

## 6. Sources

Microsoft Learn, checked October 2026: [Design area: Platform automation and DevOps](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/platform-automation-devops) · [Platform automation](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/automation) · [Use infrastructure as code to update an Azure landing zone](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/infrastructure-as-code-updates)

