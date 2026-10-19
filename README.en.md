# Stop Collecting Your 51st Roadmap

> A two-year computer-science learning map: from zero to building **AI applications with Java**.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)
[![Read Online](https://img.shields.io/badge/Read%20Online-GitHub%20Pages-blue)](https://chenguanji0711.github.io/java-to-ai-roadmap/)

**👉 Read online: [chenguanji0711.github.io/java-to-ai-roadmap](https://chenguanji0711.github.io/java-to-ai-roadmap/)**

> 中文版：[README.md](README.md) · 正文内容目前只有中文（`roadmap.md` / 在线阅读版），本页是英文项目说明。

---

## Two editions — pick by your situation

| | Long edition (default) | Intern sprint edition |
|---|---|---|
| Goal | Ship a system and explain your trade-offs | **Pass resume screening + technical interviews** |
| Timeline | 20–26 months | **8 / 16 / 24 weeks** |
| For | Beginners building a foundation | Anyone applying to internships in the next 3 months |
| Entry | [index.html](index.html) / [online](https://chenguanji0711.github.io/java-to-ai-roadmap/) | [intern.html](intern.html) / [online](https://chenguanji0711.github.io/java-to-ai-roadmap/intern.html) |
| PDF | [roadmap.pdf](roadmap.pdf) (35 pp) | [intern.pdf](intern.pdf) (21 pp) |

> The sprint edition is **not** an abridged long edition — it swaps the judging criteria.
> It drops long-horizon material (computer organization, JVM tuning, distributed systems, microservice stacks)
> and adds what only exists in 2026: how AI-assisted coding is actually evaluated, and how resume screening works.
> You can switch between the two from the top of either page.

---

## Who is this for

If three or more of these sound familiar, this repo is for you:

- You have bookmarked dozens of "roadmaps" but **don't know where to start**
- You know Java syntax, but Spring tutorials read like ancient Greek
- You memorized lots of interview trivia, but **freeze when asked "why"**
- You want to build AI apps, but every search returns "fine-tuning", "RAG", "agents" and you panic
- Every time you restart, you begin again with "variables and data types"

**It's not a discipline problem.** Most roadmaps tell you *what* to learn, never the three things that actually matter:

1. **Why this order** (so you can't tell what's skippable)
2. **When you're "done"** (so you never feel ready)
3. **What to do when stuck** (so one blocker ends the run)

This repo answers only those three questions.

---

## How it's different

| Typical roadmap | This one |
|---|---|
| Lists of topics and links | A **dependency graph** — every layer's "why" lives in the layer below |
| "Learn X" with no bar | An **exit exam** per stage: can't pass it, don't advance |
| Ordered by tech stack | Ordered by **capability chain**: language → data structures → systems → data → engineering → backend → AI |
| Assumes unlimited time | A timeline for **8–12 hours/week**, with a recovery plan for missed weeks |
| Jargon up front | A **plain-language glossary** (20 terms, one line each) |

The one line to remember: **each layer's "why" lives in the layer beneath it.**

---

## What's inside

| Section | What you get |
|---|---|
| 0. Self-check | Confirm this is written for you |
| 1. Five-minute version | Goal / route / time / acceptance criteria on one screen |
| 2. Provenance & edits | Which article it's based on, what I changed, and **what I explicitly rejected** |
| 3. The building metaphor | Nine stages = nine construction phases |
| 4. Why the order can't be flipped | Dependency graph + three "what breaks if you skip" examples |
| 5. How long it takes | Gantt chart: main track vs. parallel tracks |
| 6. The nine stages | P0–P8: why now / what to learn / what to avoid / exit exam / resources |
| 7. Plain-language glossary | JVM, B+ tree, RAG, embedding… one sentence each |
| 8. Learning with AI | 8 copy-paste dialogue templates + 3 anti-hallucination rules |
| 9. What "learned" means | Four levels (L1 recall → L4 rework) + three self-checks |
| 10. The daily 90 minutes | Loop diagram, 5-line journal, weekly/monthly review, recovery |
| 11. Three checklists | Must-learn / optional / not-yet — **tickable** |
| 12. Seven traps | Each with a concrete way out |

---

## Screenshots

![Hero](assets/01-hero.png)

![Dependency graph](assets/02-dependency-graph.png)

![Checklist](assets/03-checklist.png)

<details>
<summary>More screenshots (timeline / dark mode)</summary>

![Timeline](assets/04-timeline.png)

![Dark mode](assets/05-dark-mode.png)

</details>

---

## Three ways to use it

| You want to | Open |
|---|---|
| **Read** (recommended — colour, diagrams, interactive) | [`index.html`](index.html) or the [online version](https://chenguanji0711.github.io/java-to-ai-roadmap/) |
| **Edit / copy snippets / publish** | [`roadmap.md`](roadmap.md) (GitHub renders the alerts, tables, checkboxes and Mermaid diagrams) |
| **Print / offline / iPad** | [`roadmap.pdf`](roadmap.pdf) (38 pages) |
| **Look up details** | [`handbook.md`](handbook.md) — the denser reference manual |

> Bottom-right has a **🧠 AI templates** button: eight prompt templates for talking to an AI, with a keyword field that fills the placeholders, one-click copy, and a memory of the last one you used.
>
> The page opens with a **"this week: three things"** card — it picks the next three unfinished items of your current stage, swaps them in as you tick, and counts how many weeks you've kept going.
>
> `index.html` is a **single file with zero external dependencies**: CSS, JS and SVG are all inlined, so it works offline.
> Checklist progress is stored in `localStorage` — tick items, close, reopen, still there. **Export / import as JSON** to move progress between devices.

---

## Core claims

> **Each layer's "why" lives in the layer beneath it.**

> **You can skip the smart home, but not the plumbing.** (OS and networking are the plumbing.)

> **AI application development is 90% software engineering.** That's why AI comes last, not first.

> **Algorithms are the only fully parallel module** — start in week 3, run until the last day.

> The source article says "nobody checks whether you actually built the project; if you can talk your way through it, it's yours" — **I reject that.** In a long game you get exposed two questions deep, and worse, the mindset makes you skip the actual building.

---

## Version baseline (verified 2026-10)

| Component | Version | Note |
|---|---|---|
| JDK | **25 (LTS)** | Latest GA is 27 but **not LTS**; next LTS is 29 (2027-09) |
| Spring Boot | **4.1.x** | Pairs with Spring Framework 7.x |
| Spring AI | **2.0.x** | Officially supports Boot 4.0.x / 4.1.x |
| LangChain4j | **1.22.x** | Fast-moving |

> ⚠️ Version mismatch is the biggest invisible trap for self-learners: plenty of tutorials still target **Java 8 + Spring Boot 2.x**, while Boot 3 moved everything from `javax.*` to `jakarta.*`. **Trust official docs and official example repos; read blogs for ideas, not for code.**

---

## Source and changes

The skeleton comes from a Feishu article **《后端学习路线》** by 「花绿青」 (July 2026):
<https://my.feishu.cn/wiki/DtjfwF73JibHfdkxkfsc9CWQnlg>

That article is written from a **job-hunt sprint** perspective (3–6 months to a big-tech backend offer). This repo restructures it and is explicit about three deviations:

1. The goal changed from "pass the interview" to "**ship a system and explain your design trade-offs**";
2. The time scale stretched from 3–6 months to **20–26 months**;
3. The article ends with "to be continued: AI development" — **stage P7 (AI application development) is my extrapolation of its methodology, not original content**, and is marked as such in the text.

---

## Install as an app / read offline

`index.html` itself is still a **single file with zero external dependencies**. Two tiny PWA files make it installable:

| File | Purpose |
|---|---|
| `manifest.json` | Lets the browser treat it as an app, installable to the home screen |
| `sw.js` | Service worker — caches the page so it opens with no network |

- **iPhone**: open in Safari → Share → **Add to Home Screen**
- **Android**: open in Chrome → menu → **Install app**
- **Desktop Chrome / Edge**: click the install icon in the address bar

> You can delete both files; you just lose the "installable app" part.

---

## Contributing

- Dead links, outdated versions, factual mistakes → open an Issue
- Better resources (especially first-hand Chinese material) → send a PR
- Want to add your own notes → fork freely, attribution required

---

## License

[CC BY 4.0](LICENSE) © 2026 chenguanji0711

Copy, modify and redistribute freely (including commercially) — **keep attribution**.
Third-party articles, docs and images remain the property of their original authors.

---

## If this helped you

- ⭐ **Star the repo** — it helps other lost learners find it
- 🔗 **Send it to one friend who needs it** — more useful than bookmarking
- 🐛 **Found a dead link or outdated version?** Open an issue and I'll fix it
- 📅 The checklists get updated when JDK / Spring Boot / Spring AI ship major versions

> One person's learning path is often saved by someone else's roadmap.
