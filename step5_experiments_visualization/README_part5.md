# Part 5: Experiments and Visualization

## Files added in this part

| File | What it is |
| ---- | ---------- |
| `visualize.py` | Runs the five experiments, plots fitness by generation, and prints the best schedule for each setting. |
| [`Figures from Tests`](Figures%20from%20Tests) | Contains the 25 regenerated plots and five schedule logs. |

## Experiment Method

Each parameter setting uses the same 20 distinct seeds (1–20). The plots show the arithmetic mean of the 20 trials' best fitness at each generation, starting at generation 0. The population-size sweep runs for 100 generations; the other experiments run for 20. The five robustness plots show individual runs. Each printed schedule comes from the highest-scoring individual trial for that setting. The saved results were generated with Python 3.14.3.

An on-time schedule has no deadline penalty. The optimal fitness for this model is `-65`. The results below count these outcomes separately. Where a median generation is reported, it is calculated among runs that reached the stated target within the budget.

## Robustness Tests

All five seeds found on-time schedules by generation 3. Seeds 1–5 first did so at generations 1, 1, 2, 0, and 3, respectively. Two runs reached `-65` within 20 generations: seed 1 at generation 18 and seed 2 at generation 13.

## Population Size Tests

| Population size | On-time runs | Median first on-time generation | Runs reaching `-65` | Mean final best fitness |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 17/20 | 34 | 1/20 | -219.40 |
| 10 | 20/20 | 12 | 12/20 | -65.95 |
| 20 | 20/20 | 3 | 16/20 | -65.40 |
| 40 | 20/20 | 2 | 20/20 | -65.00 |
| 80 | 20/20 | 1 | 20/20 | -65.00 |

Of the two settings that reached the optimum in every run, size 80 reached it at median generation 22 and size 40 at median generation 31.5. A larger population also evaluates more schedules per generation; this comparison does not measure elapsed time.

## Mutation Rate Tests

All mutation rates produced on-time schedules for all 20 seeds, with median first on-time generations between 1 and 2. The 50% setting reached the optimum most often (9/20), followed by 25% (6/20). The 6.25% setting reached it once. Increasing the mutation rate did not consistently increase the number of optimal results.

## Crossover Rate Tests

All crossover rates produced on-time schedules for all 20 seeds. The median first on-time generation was 2 at 25%, 50%, and 100%, compared with 3 at 12.5% and 3.5 at 6.25%. The 100% setting reached the optimum in 6/20 runs; the 6.25%, 12.5%, and 25% settings each did so in 2/20 runs.

## Elite Count Tests

All elite counts produced an on-time schedule for all 20 seeds, with median first on-time generations between 1.5 and 2. Reaching the optimum was less common: 2/20 runs reached it with no elites, compared with 7/20 with two elites. This sweep did not measure schedule diversity.

## Overall Findings

Finding an on-time schedule was much more common than finding an optimal one. The results describe this task, these seeds, and these budgets. They do not establish an optimal joint setting. Step 4 retains its original defaults:

- **Population Size:** 50
- **Mutation Rate:** 30%
- **Crossover Rate:** 80%
- **Elite Count:** 2
- **Generation Limit:** 100

## How to Run

From the repository root:

```sh
uv sync --locked
uv run python -m step5_experiments_visualization.visualize
```

Close each plot window to continue to the next plot.
