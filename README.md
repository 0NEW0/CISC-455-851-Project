# CISC-455-851-Project

# Student Study Schedule Optimization

## 1. Project Overview

The goal of this project is to optimize a student's weekly study schedule using a **Genetic Algorithm (GA)**.

The algorithm scores schedules by deadlines, task priorities, and daily workload. It also penalizes occupied unavailable slots and short Project sessions.

The schedule covers Monday to Friday, with four one-hour slots per day and **20 slots per week**. Each run marks two slots on different weekdays as unavailable.

## 2. Problem Definition

We use four sample tasks with different priorities, deadlines, and required study hours.

| Task ID | Task Name | Hours | Priority | Deadline |
|---|---|---|---|---|
| A | Assignment | 4 | 1 (Low) | Wednesday |
| B | Project | 5 | 3 (High) | Thursday |
| C | Essay | 3 | 2 (Medium) | Thursday |
| D | Exam Review | 3 | 3 (High) | Friday |

**Basic Settings:**
- Available days: Monday to Friday
- Study slots per day: 4
- Duration per slot: 1 hour
- Total scheduled time: 20 hours
- Total required study time: 15 hours
- Free slots: 5, of which 2 must cover the unavailable slots to avoid a penalty
- Project sessions: at least 2 consecutive hours on the same day

Deadlines are represented using numbers from 0 (Monday) to 4 (Friday). Each task should be completed by the end of its deadline day.

## 3. Chromosome Representation

Each chromosome represents a complete weekly study schedule.

- **Genotype:** A list of 20 genes, with each gene representing a one-hour time slot.
- **Gene Values:** A, B, C, D, or Free.
- **Phenotype:** A weekly timetable showing when each task is scheduled.
- **Constraints:** Each task must appear exactly as many times as its required hours.

For example, Task A must appear 4 times, Task B 5 times, Task C 3 times, Task D 3 times, and Free 5 times.

## 4. Schedule Representation and Fitness (Parts 1 and 2)

- [Step 1 — Schedule representation](step1_problem_representation/README.md) builds the initial population, displays weekly schedules, and samples two unavailable slots on different weekdays. The slots stay fixed for each run and can be reproduced with its seed.
- [Step 2 — Fitness evaluation](step2_fitness_function/README.md) validates the chromosome and scores the schedule. `evaluate_fitness()` returns the penalty breakdown, and `fitness_function()` returns the score the GA maximizes.

```text
fitness = -(1000 * deadline_penalty + priority_penalty + 5 * balance_penalty
            + 1000 * unavailable_slot_conflicts + 20 * short_sessions)
```

Detailed documentation for each step is in its corresponding directory.

## 5. Genetic Algorithm and Experiments (Parts 3–5)

- **Part 3: Genetic operators.** Tournament selection chooses parents. Two crossover strategies and swap mutation produce offspring while preserving task hours. See the [operator design report](step3_genetic_operators/REPORT.md).
- **Part 4: GA implementation & Advanced Strategies.** The core GA (`run_ga()`) uses a population of 50, 100 generations, and elitist survival. To add "healthy complexity" and enhance the core search process, we engineered three advanced EA strategies: **Memetic Local Search**, **Island Model Migration**, and **Adaptive Penalties**. 
  - *For a comprehensive breakdown of the two-phase experimental methodology, algorithmic design, and the trade-offs of each advanced strategy, please refer to the detailed **[Step 4 Report](step4_ga_implementation/README_step4.md)**.*
- **Part 5: Experiments and visualization.** `visualize.py` runs parameter sweeps (population size, mutation rate, crossover rate, elite count) and robustness tests. See the [experiment report](step5_experiments_visualization/README_part5.md).

**Experiment method:** Each parameter setting uses the same 20 distinct seeds. The script averages the trials' best fitness separately for each generation, starting at generation 0, and prints the highest-scoring individual schedule. The five robustness plots show individual seeds.

## 6. Project Progress

| Part | Component | Status |
|---|---|---|
| 1 | Problem & Representation | Completed |
| 2 | Fitness Function | Completed |
| 3 | Genetic Operators | Completed |
| 4 | GA Implementation | Completed |
| 5 | Experiments & Visualization | Completed |

## Python Package Layout and Execution

Open the repository folder in VS Code and run the following in a terminal at the repository root. `uv sync --locked` installs the dependencies, including Matplotlib and NumPy, into `.venv`.

```sh
uv sync --locked
uv run python -m step4_ga_implementation.genetic_algorithm
uv run python -m unittest discover -s tests -p "test_*.py" -t . -v
uv run python -m step5_experiments_visualization.visualize
```

If the environment already exists, you can run the tests or visualization with its Python interpreter directly. In Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -t . -v
.\.venv\Scripts\python.exe -m step5_experiments_visualization.visualize
```

Use `python -m` from the repository root so Python can find sibling packages such as `Shared`. Close each plot window to continue to the next figure. The automated tests cover the genetic operators, the GA, and trial aggregation. Run the visualization separately to view the plots.

To refresh the five sets of PNGs and schedule logs without opening plot windows, run `uv run python -m step5_experiments_visualization.visualize --save`.
