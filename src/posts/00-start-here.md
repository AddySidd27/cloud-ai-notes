---
title: "Start Here: How This Blog Works and What to Read First"
slug: "start-here"
series: "Start Here"
part: ""
post_number: 0
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/azure/architecture/landing-zones/azure-virtual-desktop/design-guide"
    checked_on: "2026-10-07"
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



## Who this is for

- Engineers and architects who run, or are about to run, Azure Virtual Desktop (AVD). AVD is Microsoft's service for delivering Windows desktops and apps from Azure.
- People who know some Azure and want the foundation done properly before they build workloads on it.
- Anyone preparing for work or exams around AVD and Azure architecture.

You do not need to know either topic. Each post explains its new words first and uses only ideas from that post or the posts before it.

## Why Azure Landing Zone comes first

A workload is an application or service you run in the cloud, and AVD is one. An Azure landing zone is the prepared Azure environment that workloads run in. An Azure landing zone provides the foundation for cloud workloads such as AVD, and defines components like governance, security, networking, identity and operations. So the blog starts with the foundation, then builds AVD on top of it.

## The three series

- **Azure Landing Zone.** What it is, the eight design areas, and what to build first.
- **Azure Virtual Desktop.** Planned topics: fundamentals, identity, network, host pools, user profiles, images and apps, then operating AVD.
- **Azure Landing Zone: operate it.** A greenfield rollout (a new environment), a brownfield rollout (an environment that already exists) and keeping the landing zone up to date (running and improving it after it is built).

The order of the landing zone posts is fixed. The Azure Virtual Desktop series gets its own check against the official documentation before it starts, and any change will be noted here.

## How to read it

Read the Azure Landing Zone series first, in order, starting with "What Is an Azure Landing Zone". Then read the Azure Virtual Desktop series, then the operate series last, once you have seen both.

If you already know landing zones, you can jump straight to the Azure Virtual Desktop series.

## Security is built in, not added at the end

Security is not left to the end. In the landing zone series it appears in identity, privileged access, the Security design area and security operations. The Azure Virtual Desktop series will cover security topics in the same way.

## How each post is built

Every post starts with the situation you will run into, then explains the topic in plain words, shows a diagram, lists the mistakes to check for first, and links the exact repo file with the lab or reference. At the end it lists the Microsoft pages it is based on, with the month I checked them, and says what comes next.

My rules:

- Facts come from official Microsoft documentation. If a statement is my own explanation, the post says so.
- If a feature is in Preview, the post says so, and I check it again before publishing.
- If a post uses a fictional case study, it is labelled fictional. It is a worked example, not customer work.
- Diagrams are simplified redrawings, using Microsoft's official icons. Where the official documentation has a diagram for the topic, mine follows its layout; where it has none, the layout is mine and the caption says so. Each caption links to the original page. They are not official Microsoft diagrams.

## The code and labs

Most posts have a matching file in this public repo. Where a post covers something the repo does not have yet, I add the file when the post goes out:

- [Azure_landing_zone](https://github.com/AddySidd27/Azure_landing_zone): the landing zone guide and labs

The Azure Virtual Desktop repo link will be added here when that series starts.

## About me

I am Addy (Adnan Ahmed), a Senior Solutions Architect. A separate About page has more.

## Sources

Microsoft Learn, checked October 2026: [AVD landing zone design guide](https://learn.microsoft.com/azure/architecture/landing-zones/azure-virtual-desktop/design-guide)

The series structure, reading order and rules are my own plan.

## Start reading

[What Is an Azure Landing Zone](/azure-landing-zone/what-is-an-azure-landing-zone/)
