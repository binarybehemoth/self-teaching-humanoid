# The Self-Teaching Humanoid

The open companion repository for the book *The Self-Teaching Humanoid*
by Chong Lip Phang.

This is a **faithful, runnable scaffold** of the complete system the book describes —
a humanoid robot that learns broadly, teaches and is taught by others, improves
itself, and does so in the open and in service of the people around it.

> **What this is, and is not.** This repository is the *skeleton and blueprint* of the
> system — its architecture, interfaces, schemas, and safety structure, with working
> examples — organised so that every concept in the book has an inspectable home in the
> code. It is **not** a finished, deployable, production-grade humanoid. A production
> robot is the work of a large team over years, and no repository could hand that over.
> See `docs/SCOPE.md` for an honest account of what is and is not here.

## The architecture, mirrored in the layout

The repository is a monorepo whose top-level directories mirror the book's structure:

| Directory     | Contains                                             | In the book        |
|---------------|------------------------------------------------------|--------------------|
| `body/`       | ROS 2 nodes and the hardware-abstraction layer       | Parts I–IV         |
| `learning/`   | Broad- and effective-learning pipelines              | Parts V–VII, XI–XIV|
| `mind/`       | Planner, policy, memory, and self-model              | Parts VIII–X       |
| `safety/`     | Monitor, constitution, and human override            | Parts VIII–X       |
| `platform/`   | Skill interface, marketplace, and standard layer     | Parts XV–XVII      |
| `backend/`    | Services and the API gateway (FastAPI)               | Parts XVIII–XX     |
| `frontend/`   | Studio, marketplace, and dashboard surfaces          | Parts XVIII–XX     |
| `schemas/`    | Every JSON schema defined across the book            | throughout         |
| `examples/`   | Runnable, end-to-end demonstrations                  | throughout         |

`safety/` is deliberately kept as its own first-class module. The whole system's
trustworthiness rests on it, and it is meant to be changed only deliberately and with
review — never as a casual side effect of improving something else.

## Quickstart — run an end-to-end example (no dependencies)

The core of the system runs on the Python standard library alone, so you can watch the
whole flow — perceive, plan, safety-check, act, learn — immediately:

```bash
git clone https://github.com/clphang/self-teaching-humanoid.git
cd self-teaching-humanoid

python3 examples/end_to_end/clear_a_table.py     # the whole system in one script
python3 examples/end_to_end/teach_a_skill.py     # teach, publish, install, use
python3 examples/skills/water_plants.py          # a composed skill (Ch 51)
```

These examples drive a **pure-Python simulated robot** (`body/sim_robot.py`), so no
hardware and no external packages are required to see the system work.

## Running the full stack (back end + front ends + simulated robot)

To bring up the back-end services, the web surfaces, and a simulated robot together:

```bash
# with Docker
docker compose up

# or locally
pip install -r requirements.txt
python3 -m backend.app          # serves the API + static front ends on :8000
```

Then open:

- Teaching studio   — <http://localhost:8000/studio>
- Skill marketplace — <http://localhost:8000/market>
- Fleet dashboard   — <http://localhost:8000/fleet>

## The safety architecture

Every action a robot takes passes the **safety monitor** (`safety/monitor.py`) before it
reaches the actuators. The monitor sits at the seam between decision and motion, so it
catches an unsafe command whatever its origin — a flawed plan, a bad marketplace skill,
or an errant learned behaviour. The **human override** is always reachable. This is a
faithful illustration of the *design*; a safety system for a physical robot among real
people requires validation and assurance far beyond any open scaffold. Treat the safety
module with the seriousness the book argues for.

## License

Released under the Apache License 2.0. See `LICENSE`. Free to run, study, modify, and
build upon.

## A note from the book

> Build on this system in the spirit it was built: keep the safeguards intact and take
> them seriously; be honest about what your robots can and cannot do; respect the people
> whose data teaches them and whose spaces they share; and hold, above every other
> objective, the wellbeing of the humans your machines will touch.

Now go build.
