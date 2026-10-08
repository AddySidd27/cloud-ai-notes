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



## 1. Who this is for

- Engineers and architects who run, or are about to run, Azure Virtual Desktop (AVD). AVD is Microsoft's service for delivering Windows desktops and apps from Azure.
- People who know some Azure and want the foundation done properly before they build workloads on it.
- Anyone preparing for work or exams around AVD and Azure architecture.

You do not need to know either topic. Each post explains its new words first and uses only ideas from that post or the posts before it.

## 2. Why Azure Landing Zone comes first

A workload is an application or service you run in the cloud, and AVD is one. An Azure landing zone is the prepared Azure environment that workloads run in. Microsoft's AVD landing zone guidance says an Azure landing zone provides the foundation for cloud workloads such as AVD, and defines components like governance, security, networking, identity and operations. So the blog starts with the foundation, then builds AVD on top of it.

## 3. The three series

| Series | What it covers | Posts (planned) |
|---|---|---|
| 1. Azure Landing Zone (posts 1 to 20) | What it is, the eight design areas Microsoft Learn names, how to build it safely, and how AVD fits in as a workload | 20 |
| 2. Azure Virtual Desktop (posts 21 to 60) | Planned topics: fundamentals, identity, network, host pools, user profiles, images and apps, then operating AVD | 40 |
| 3. ALZ Operate (posts 61 to 63) | Day-2 operations, greenfield rollout and brownfield rollout | 3 |

The order and titles of Series 1 and 3 are fixed. Day-2 operations means running the environment after it is built. Greenfield means a new environment, and brownfield means one that already exists. Series 2 gets its own check against Microsoft Learn before it starts, and any change will be noted here.

## 4. How to read it

1. Read Series 1 from post 1 in order. Posts 1 to 15 are the concepts. Posts 16 to 18 are about building it, and posts 19 and 20 connect AVD to it.
2. Read Series 2 from the start. It is planned to begin with what AVD is, then identity, network, host pools, profiles, and images and apps, then operations.
3. Read Series 3 (posts 61 to 63) last, once you have seen both.

If you already know landing zones, you can jump to Series 2, post 21. Check post 19 first: it connects the two.

## 5. Security is built in, not added at the end

Security is not left to the end. In Series 1 it appears in identity, privileged access (post 8), the Security design area (post 11) and security operations (post 12). Series 2 will cover security topics in the same way, and its exact list is set when that series is checked.

## 6. How I write each post

Every post follows the same six steps, then points to the next post:

1. The problem
2. A simple explanation
3. A diagram
4. What I have seen in production
5. The exact repo file with the lab or reference
6. Sources: up to three Microsoft Learn pages the post is based on, with the month I checked them

My rules:

- Facts come from Microsoft Learn. If a statement is my own explanation, the post says so.
- If a feature is in Preview, the post says so, and I check it again before publishing.
- If a post uses a fictional case study, it is labelled fictional. It is a worked example, not customer work.
- Diagrams are simplified redrawings based on Microsoft Learn, using Microsoft's official icons. Where Learn has a diagram for the topic, mine follows its layout; where it has none, the layout is mine and the caption says so. Each caption links to the Learn page. They are not official Microsoft diagrams.

## 7. The code and labs

Most posts have a matching file in this public repo. Where a post covers something the repo does not have yet, I add the file when the post goes out:

- [Azure_landing_zone](https://github.com/AddySidd27/Azure_landing_zone): the landing zone guide and labs

The Azure Virtual Desktop repo link will be added here when Series 2 starts.

## 8. About me

I am Addy (Adnan Ahmed), a Senior Solutions Architect. A separate About page has more.

## 9. Sources

Microsoft Learn, checked October 2026: [AVD landing zone design guide](https://learn.microsoft.com/azure/architecture/landing-zones/azure-virtual-desktop/design-guide)

The series structure, reading order and rules are my own plan.

## Start reading

[Post 1: What Is an Azure Landing Zone](/azure-landing-zone/what-is-an-azure-landing-zone/)
