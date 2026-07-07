# Examples

Runnable demonstrations. The end-to-end examples need **nothing beyond the Python
standard library** — they drive a pure-Python simulated robot (`body/sim_robot.py`), so
you can see the whole system work on one computer with no hardware.

```bash
python3 examples/end_to_end/clear_a_table.py   # the whole system: perceive->plan->safety-check->act->learn
python3 examples/end_to_end/teach_a_skill.py   # teach -> publish -> install -> use (the platform loop)
python3 examples/skills/water_plants.py        # a composed skill (Ch 51 worked example)
```

`clear_a_table.py` also demonstrates the safety monitor doing its job: unsafe motions
near a person are vetoed, and the human override halts everything.
