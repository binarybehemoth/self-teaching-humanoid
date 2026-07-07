# Scope — what this repository is, and is not

This repository is the open companion to the book *The Self-Teaching
Humanoid*. It is a **faithful, runnable scaffold** of the complete system the book
describes — not a finished, deployable, production-grade humanoid.

## What IS here

- The **complete architecture** of the book, made runnable: the five layers (body,
  broad + effective learning, mind, platform) plus the safety spine, with clean
  interfaces between them.
- A **real, working safety architecture** — a monitor that gates every action at the
  seam between decision and motion, a constitution, and a human override.
- The **skill interface** a developer writes to, with capability negotiation and
  composition (the `WaterPlants` example is the worked example from Ch 51).
- A **back end** (FastAPI API gateway + services) and **front-end surfaces** (studio,
  marketplace, dashboard).
- Every **JSON schema** defined across the book.
- **Runnable end-to-end examples** driving a pure-Python simulated robot, so the whole
  flow — perceive, plan, safety-check, act, learn — can be seen on one computer with no
  hardware and no external packages.

## What is NOT here (and cannot be)

- A **production-grade physical humanoid**. That is the work of a large team over years.
- The **enormous trained models** that real perception and vision-language-action
  policies require — those come only from enormous data. The `mind/` components here are
  transparent stand-ins that make the architecture runnable, not trained models.
- **Hardened commercial reliability**, or **drivers for any specific commercial robot**.
- A **certified, deployment-ready safeguard**. The safety module is a faithful
  illustration of the *design*. A safety system suitable for a physical robot operating
  among real people requires validation, testing, and assurance far beyond any open
  scaffold. **Treat the safety systems with the seriousness the book argues for.**

## How to think about it

The repository is the **skeleton and the blueprint**, not the finished building. Its
value is that every concept in the book has a concrete, inspectable counterpart
you can read, run, and change — a place to start, structured to mirror the book.

Build on it in the spirit it was built: keep the safeguards intact and take them
seriously; be honest about what your robots can and cannot do; respect the people whose
data teaches them and whose spaces they share; and hold, above every other objective,
the wellbeing of the humans your machines will touch.
