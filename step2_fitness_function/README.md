# Step 2 — Fitness evaluation

[fitness_function.py](fitness_function.py) validates the chromosome before scoring it, so a schedule must include every required task hour. The GA maximizes the score, which is the negative weighted sum of these penalties.

| Penalty | Weight | How it is calculated |
| --- | ---: | --- |
| Deadline | 1,000 | Sum the days late for each scheduled task hour. Work on the deadline day incurs zero penalty. |
| Priority | 1 | Sum the task priority times its scheduled weekday index for each study hour. This favors scheduling higher-priority work earlier. |
| Workload balance | 5 | Sum the squared deviations from the average of three study hours per day. |
| Unavailable-slot conflicts | 1,000 | Count the unavailable slots occupied by any task. |
| Short sessions | 20 | Count Project blocks shorter than two consecutive hours within the same day. |

```text
fitness = -(1000 * deadline_penalty + priority_penalty + 5 * balance_penalty
            + 1000 * unavailable_slot_conflicts + 20 * short_sessions)
```

The deadline and availability terms carry the largest weights. The current weights reflect the [sample tasks and scheduling rules](../step1_problem_representation/README.md).

## GA interface

- `evaluate_fitness(chromosome, unavailable_slots=slots)` returns the fitness and its unweighted penalty breakdown.
- `fitness_function(chromosome, unavailable_slots=slots)` returns the scalar score used by the GA.
- Supply the run’s two zero-based `(day, slot)` pairs to apply the availability and session-length penalties. Omitting `unavailable_slots` uses the original three-term score for baseline comparisons.

The [GA tests](../tests/test_ga.py) cover fixed-seed reproduction and the effect of the availability and session-length penalties on schedule selection.

## Run the example

From the repository root, run the module to print the sampled unavailable slots, a random weekly schedule, and its fitness breakdown.

```sh
uv run python -m step2_fitness_function.fitness_function
```
