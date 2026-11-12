## Part 4 — GA Implementation

### Files added in this part

| File | What it is |
|---|---|
| `step4_ga_implementation/genetic_algorithm.py` | The complete GA. `run_ga()` connects Parts 1 to 3 and returns the best schedule and the fitness history. This is the final solution. |
| `step4_ga_implementation/compare_survival.py` | The experiment script. It runs the four survival schemes on 30 seeds each and prints the comparison table. |
| `step4_ga_implementation/__init__.py` | Empty file that makes the folder a Python package, like the other steps. |
| `tests/test_ga.py` | 12 tests for `run_ga()`. |

### How `run_ga()` works

Each generation the GA scores every schedule, keeps the 2 best unchanged (elitism), and fills the rest of the population with children. Each child is made by tournament selection of two parents, crossover, and swap mutation, all from Part 3. After 100 generations it returns the best schedule, its penalty breakdown, and the best and average fitness of every generation (the Part 5 plots use these).

Default settings: population 50, 100 generations, crossover rate 0.8, mutation rate 0.3, tournament size 3, 2 elite schedules. These are starting values and were not tuned. `run_ga(seed=<number>)` makes a run repeatable, including the initial population.

### Why we ran an experiment

The Part 3 operators say how children are made, but the GA also has to decide **which schedules survive into the next generation**. Our first version used elitism because it is the simple standard choice, but we did not know if the choice mattered. So we implemented the other common survival schemes from the course and compared them. `run_ga(survival=...)` selects the scheme:

| Scheme | How it is done in the code |
|---|---|
| `elitist` (default) | Copy the 2 best schedules, then make 48 children. The new population is the 2 elites plus the 48 children. |
| `mu_comma_lambda` | Make 50 children. The new population is only the children, so the old population is discarded completely (no elitism). |
| `mu_plus_lambda` | Make 50 children, put them in one pool with the 50 parents, sort by fitness, and keep the best 50. |
| `steady_state` | Repeat 25 times per generation: make 2 children, remove the 2 worst schedules, and add the 2 children. After the loop the population is the new generation. |

In every scheme about 50 children are made per generation, so the work per generation is similar. We call 25 steps of `steady_state` one generation so the history lists line up with the other schemes.

### Experiment setup

`compare_survival.py` does this for each scheme:

- It calls `run_ga(seed=s, survival=scheme)` for the seeds 0 to 29. Everything else uses the default settings. Using the same seed gives all schemes the same starting population.
- It checks when the best fitness first reaches **-65**.
- It measures the time of each run with `time.perf_counter()` and reports the median.
- It counts every call to the fitness function by temporarily replacing `fitness_function` with a counting wrapper. This count includes the evaluations made inside tournament selection.

### Results (30 seeds per scheme)

| Scheme | Runs reaching -65 | Avg. generation reached | Slowest run | Best at gen. 100 (avg.) | Population mean at gen. 100 (avg.) | Median time per run | Fitness evaluations per run |
|---|---|---|---|---|---|---|---|
| `elitist` | 30/30 | 26.4 | 56 | -65.0 | -223.0 | 1.65 s | 19,450 |
| `mu_comma_lambda (μ,λ)` | 30/30 | 35.5 | 76 | -65.1 | -250.5 | 1.71 s | 20,050 |
| `mu_plus_lambda (μ+λ)` | 30/30 | 27.3 | 69 | -65.0 | -65.0 | 1.79 s | 25,050 |
| `steady_state` | 30/30 | 22.1 | 60 | -65.0 | -69.7 | 1.80 s | 25,050 |

Times were measured on one machine and will differ on other machines. The evaluation counts do not depend on the machine.

### What we observed and why

**1. All four schemes solved the problem in every run.** The search space has about 195.5 billion arrangements, but the fitness only depends on which day each task hour is on, not on the order inside a day. That leaves fewer than 11 million different day assignments, and only 2 of them are optimal. With a population of 50 and 100 generations, the GA has enough chances to find one. 

**2. Without elitism (`mu_comma_lambda`) the best fitness can get worse, and it was the slowest.** This was expected. In a (μ,λ) scheme the parents are thrown away, so a very good schedule only survives if its children are also good. Crossover and mutation usually make a good schedule worse, not better. Our results show this: the average best at generation 100 is -65.1, so some runs had reached -65 and lost it again. Elitism removes this risk.

**3. `mu_plus_lambda` lost almost all variety.** In a (μ+λ) scheme parents and children compete, so only the best schedules survive. This gives strong selection pressure, and the population fills with copies of the best schedules. Our results match this: at generation 100 the population mean is exactly -65.0, so every schedule was optimal. That is premature convergence. 

**4. `elitist` keeps a low population mean on purpose.** Its mean stayed around -223 because crossover and mutation keep creating worse children, while the 2 elite schedules keep the best result safe. This is the balance between exploration (new schedules) and exploitation (keeping the best). Selection pressure is lower than in `mu_plus_lambda`, so more variety is kept.

**5. `steady_state` was the fastest in generations (22.1 on average).** We think this is because a new child can be chosen as a parent right away, in the next step, instead of waiting for the next generation. It also replaces only the 2 worst schedules, so the good ones stay. We did not test this explanation, so it is a likely reason, not a proven one. The gaps between schemes are a few generations and the slowest runs overlap, so with 30 seeds we do not claim a clear winner.

**6. Running time barely separates the schemes.** The medians are between 1.65 s and 1.80 s, a difference of about 9%, even though `mu_plus_lambda` and `steady_state` use about 29% more fitness evaluations (25,050 vs. 19,450). We profiled one run and found that about 90% of the time is spent in `validate_chromosome`, which `select_parent` calls on the whole population every time (as the Part 3 report notes). Every scheme makes about the same number of selections, so this overhead is almost the same for all of them and hides the extra evaluations. The evaluation count is the fairer measure of cost.

### Limitations of the experiment

- The problem is small and every scheme reaches the optimum, so the experiment shows differences in speed and behavior, not which scheme is better in general.
- We used 30 seeds (in the experment code) and one set of parameters. The ranking of the schemes could change with other population sizes or rates.
- The schemes do not use exactly the same number of fitness evaluations. `mu_plus_lambda` and `steady_state` use about 29% more than `elitist`.
- Running times are machine dependent and mostly measure the validation overhead, not the GA itself.
- We tested only the default crossover (`count_preserving_crossfill`).

### What we chose and why

We kept **`elitist`** as the default:

- It reached the optimum in all 30 runs.
- The best fitness never goes down, so the Generation vs. Best Fitness plot is easy to read and explain.
- It keeps more variety than `mu_plus_lambda`.
- It uses fewer fitness evaluations than `mu_plus_lambda` and `steady_state`.
- `steady_state` was a little faster in generations, but the gap is small, it costs more evaluations, and it makes "one generation" less clear.

### How to run

Run everything from the repository root.

**The final solution only** (runs the GA once with seed 42 and prints the best schedule):

```powershell
python -m step4_ga_implementation.genetic_algorithm
```

**The survival experiment** (prints the results table; takes a few minutes):

```powershell
python -m step4_ga_implementation.compare_survival
```

**All tests** (Parts 1 to 4):

```powershell
python -B -m unittest discover -s tests -p "test_*.py" -t . -v
```

With `uv`, put `uv run` in front of each command.
