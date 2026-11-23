# Step 1 — Schedule representation

The timetable has 20 one-hour slots across five weekdays, with four slots per day. The sample tasks require 15 hours, leaving five slots free.

| ID | Task | Hours | Priority | Deadline |
| --- | --- | ---: | --- | --- |
| A | Assignment | 4 | 1 (low) | Wednesday |
| B | Project | 5 | 3 (high) | Thursday |
| C | Essay | 3 | 2 (medium) | Thursday |
| D | Exam Review | 3 | 3 (high) | Friday |

The genotype is a flat list in weekday and slot order. A gene is `A`, `B`, `C`, `D`, or `Free`. A valid chromosome contains exactly 4 A, 5 B, 3 C, 3 D, and 5 Free entries. The phenotype is the same schedule displayed as five rows of four slots. Days are indexed from 0 (Monday) to 4 (Friday), and a task may be scheduled on its deadline day.

Each GA run randomly marks one slot on each of two different weekdays as unavailable. The two slots stay fixed for the run and can be reproduced with its seed. A schedule avoids availability conflicts by leaving these slots free. A Project session must span at least two consecutive slots on the same day to avoid the short-session penalty. [Step 2](../step2_fitness_function/README.md) describes how these rules affect fitness.

## Implementation

In [schedule_data.py](schedule_data.py), `create_chromosome()` fills the required hours, adds free slots, then shuffles the slots. It raises `ValueError` if the task hours exceed the timetable. `create_population(size)` generates the initial population, and `display_schedule(chromosome)` prints the weekly timetable. `choose_unavailable_slots(seed)` returns two zero-based `(day, slot)` pairs.

[Shared chromosome validation](../Shared/chromosome_validation.py) checks the length, allowed gene values, and exact task and free-slot counts. The fitness function and genetic operators reuse this check.

## Run the example

From the repository root, run the module to see the unavailable slots, a sample schedule, and the initial population size.

```sh
uv run python -m step1_problem_representation.schedule_data
```
