---
title: "Start Here: How This Blog Works and What to Read First"
seoTitle: "Start Here: What to Read First"
slug: "start-here"
series: "Start Here"
part: ""
post_number: 0
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/azure/architecture/landing-zones/azure-virtual-desktop/design-guide"
    checked_on: "2026-10-13"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-desktop/overview"
    checked_on: "2026-10-13"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone"
diagrams: []
production_section_written_by_addy: false
layout: post.njk
permalink: "/start-here/"
order: 0
deck: "This blog teaches Azure Landing Zone and Azure Virtual Desktop in a fixed order, so you can start with no background and build up to both, one step at a time."
next_num: ""
next_title: ""
---



## Pick your route

- **I have 15 minutes, or I am new:** start with [What Is an Azure Landing Zone](/azure-landing-zone/what-is-an-azure-landing-zone/), then follow the series in order.
- **After you finish the series:** [the greenfield rollout post](/azure-landing-zone/greenfield-rollout/) if you are starting fresh, or [the brownfield rollout post](/azure-landing-zone/brownfield-rollout/) if you already have an Azure environment. They use words defined in the earlier posts.
- **I already know landing zones:** go straight to the AVD series when it starts.

## Who this is for

- Engineers and architects who run, or are about to run, Azure Virtual Desktop (AVD), Microsoft's service that runs Windows desktops and apps on Azure.
- People who know some Azure and want the foundation done properly before they build workloads on it.
- Anyone preparing for work or exams around AVD and Azure architecture.

You do not need to know either topic. Each post explains its new words first. The blog is a guided reading of the official documentation, not a replacement for it.

## The three series

- **Azure Landing Zone.** What it is, the eight design areas, and what to build first.
- **Azure Virtual Desktop.** Planned, not started yet: fundamentals, identity, network, host pools, user profiles, images and apps, then operating AVD.
- **Azure Landing Zone: operate it.** How to roll a landing zone out in a new environment (greenfield) or an existing one (brownfield), and how to keep it up to date later.

## Why the landing zone comes first

A workload is an application or service you run in the cloud, and AVD is one. An Azure landing zone is the prepared Azure environment that workloads run in. It provides the foundation for cloud workloads such as AVD and defines components like governance, security, networking, identity and operations. The AVD reference implementation also requires a platform landing zone to be deployed first, so the blog builds AVD on top of the foundation. Security is covered inside each topic, not left to the end.

## How each post is built

Each post opens with a one-sentence summary, explains the topic in plain words with terms defined first, and shows a diagram. It then lists common mistakes, what I have seen in my own projects (it says so when I have nothing to report), the matching repo file, the official pages it is based on (with the month I checked them), and what comes next.

My rules:

- Facts come from official Microsoft documentation. If a statement is my own explanation, the post says so.
- If a feature is in Preview, the post says so, and I check it again before publishing.
- If a post uses a fictional case study, it is labelled fictional. It is a worked example, not customer work.
- Diagrams are simplified redrawings, using Microsoft's official icons. Where the official documentation has a diagram for the topic, mine follows its layout; where it has none, the layout is mine and the caption says so. Each caption links to the original page. They are not official Microsoft diagrams.

## How the repo labs fit in

[Azure_landing_zone](https://github.com/AddySidd27/Azure_landing_zone) is my public learning and reference lab, built with Terraform. It is not production-ready and it is not the official accelerator. Use it to see how the parts fit together, and use the official accelerator for real environments. [lab-vs-enterprise.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/lab-vs-enterprise.md) lists what a personal lab can and cannot reproduce, and [learning-path.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/learning-path.md) gives a suggested reading order.

No post includes a real deployment yet, and the repo's status table says real-deployment evidence is not published. Hands-on evidence from real runs will be added as it is produced. Where a post covers something the repo does not have yet, I add the file when the post goes out. The AVD repo link will be added here when that series starts.

## About me

I am Addy (Adnan Ahmed), a Senior Solutions Architect with 15 years in enterprise IT. A separate About page has more.

## Sources

Microsoft Learn, checked October 2026: [AVD landing zone design guide](https://learn.microsoft.com/azure/architecture/landing-zones/azure-virtual-desktop/design-guide) · [What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview)

The series structure, reading order and rules are my own plan.

## Start reading

[What Is an Azure Landing Zone](/azure-landing-zone/what-is-an-azure-landing-zone/)
