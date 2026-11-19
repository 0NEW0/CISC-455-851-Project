# Part 5: Experiments and Visualization

The five robustness and sweep experiments in the [figures and schedule logs](Figures%20from%20Tests) use the updated fitness function. It deducts 1,000 points per occupied unavailable slot and 20 per Project session shorter than two consecutive hours on the same day, in addition to the original penalties. Each run draws two unavailable slots on different weekdays. The slots stay fixed for the run and are reproducible from its seed. The saved results were generated with Python 3.14.3.

## Robustness and Parameter Sweeps

The robustness plots show five separate runs with seeds 1–5 and 20 generations each. All five selected schedules met all three requirements. In the [seed 1 example](Figures%20from%20Tests/Robustness/Seed_1.png), Monday slot 3 and Tuesday slot 1 were unavailable. That run first reached its best fitness of **−81 at generation 14**. It scheduled the Project in two blocks of 2 and 3 hours.

The four parameter sweeps use seeds 1–20 for each setting and average the per-generation best fitness, including generation 0. Population size runs for 100 generations. Mutation rate, crossover rate, and elite count run for 20. The schedule logs record the success counts, mean final best fitness, and the highest-scoring schedule for each setting, with its seed, unavailable slots, and penalty breakdown.

| Sweep | Settings in order | Runs meeting all three, out of 20 |
| --- | --- | --- |
| [Population size](Figures%20from%20Tests/Population/Population%20Schedules.txt) | 5, 10, 20, 40, 80 | 4, 15, 20, 20, 20 |
| [Mutation rate](Figures%20from%20Tests/Mutation/Mutation%20Schedules.txt) | 100%, 50%, 25%, 12.5%, 6.25% | 19, 19, 18, 17, 16 |
| [Crossover rate](Figures%20from%20Tests/Crossover/Cross_Schedules.txt) | 100%, 50%, 25%, 12.5%, 6.25% | 20, 15, 14, 13, 12 |
| [Elite count](Figures%20from%20Tests/Elite/Elite%20Schedules.txt) | 0, 1, 2, 4, 8 | 15, 19, 18, 19, 19 |

The runs cover one task set and a fixed set of seeds. The sweeps vary one parameter at a time and use two different generation budgets, so comparisons belong within each sweep. The results track which runs satisfy the requirements and the best scores the GA finds. The global optimum can depend on the unavailable slots.

## How to Run

From the repository root:

```sh
uv sync --locked
uv run python -m step5_experiments_visualization.visualize
```

Close each plot window to continue to the next plot. To regenerate the 25 sweep and robustness plots and the five schedule logs without opening windows:

```sh
uv run python -m step5_experiments_visualization.visualize --save
```

