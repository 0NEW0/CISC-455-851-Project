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

Part 1 is implemented in [`schedule_data.py`](step1_problem_representation/schedule_data.py). Part 2 is implemented in [`fitness_function.py`](step2_fitness_function/fitness_function.py).

The following components have been implemented:

### 4.1 Sample Task Data
- Defined available study days and time slots.
- Created four sample tasks with required hours, priorities, and deadlines.
- Draws two unavailable slots on different weekdays once per GA run. A fixed seed reproduces the draw.

### 4.2 Chromosome Generation
**Function:** `create_chromosome()`

- Creates a chromosome containing all required task hours.
- Adds free slots to reach 20 total slots.
- Randomly shuffles the chromosome to generate a weekly schedule.
- Raises an error if the required hours exceed the available time.

### 4.3 Initial Population
**Function:** `create_population(size)`

- Generates multiple random chromosomes.
- Each chromosome represents a possible weekly study schedule.
- Provides the initial population for the Genetic Algorithm.

### 4.4 Schedule Display
**Function:** `display_schedule(chromosome)`

- Converts a chromosome into a readable weekly schedule.
- Displays the four study slots for each day from Monday to Friday.

**Note:** Randomly generated schedules satisfy the task-hour counts. The fitness function then checks deadlines, availability, session length, and the other scoring criteria.

### 4.5 Chromosome Validation
**File:** [`Shared/chromosome_validation.py`](Shared/chromosome_validation.py)

**Function:** `validate_chromosome(chromosome)`

- Reuses the task data and study settings from Part 1.
- Checks that the chromosome contains exactly 20 valid slots.
- Checks that each task and Free appear exactly as many times as required.
- Raises a `ValueError` for invalid chromosomes so missing task hours cannot improve fitness.

### 4.6 Fitness Evaluation
**Function:** `evaluate_fitness(chromosome, unavailable_slots=slots)`

- Use the two `(day, slot)` pairs for the current run. Both indexes start at zero.
- Evaluates a schedule using five penalty components:
  - **Deadline penalty:** Sums the days late for each scheduled task hour. Study on the deadline day is allowed.
  - **Priority penalty:** Sums task priority multiplied by the scheduled day index (Monday = 0). This encourages higher-priority work earlier in the week.
  - **Balance penalty:** Sums squared differences between daily study hours and the average of 3 hours per day.
  - **Unavailable-slot conflicts:** Counts unavailable slots assigned to any task.
  - **Short sessions:** Counts Project sessions shorter than two consecutive hours on the same day.
- Combines the penalties using the following formula:

```text
fitness = -(1000 * deadline_penalty + priority_penalty + 5 * balance_penalty
            + 1000 * unavailable_slot_conflicts + 20 * short_sessions)
```

- Returns the fitness value and all five unweighted penalty components in a dictionary.
- Higher fitness values indicate better schedules; scores are nonpositive.
- With the current task data, a schedule with zero deadline and unavailable-slot penalties scores higher than one with either violation. A short Project session carries a smaller penalty.

**Note:** The priority rule assumes important tasks should be scheduled earlier. Weights should be reassessed if task data or scoring preferences change.

### 4.7 GA Fitness Interface and Example
**Function:** `fitness_function(chromosome, unavailable_slots=slots)`

- Returns only the scalar fitness value for use by the Genetic Algorithm.
- Supports selection methods based on score comparisons, such as tournament or rank selection. Roulette-wheel selection requires a suitable score transformation to positive weights.
- Running `python -m step2_fitness_function.fitness_function` from the repository root displays the sampled unavailable slots, a random weekly schedule, and its fitness breakdown.

### 4.8 Fitness Verification
- Checked a manually calculated schedule score and workload balance penalties.
- Checked deadline-day acceptance and penalties for task hours scheduled one or two days late.
- Checked rejection of incorrect lengths, unknown genes, and incorrect task counts.
- Evaluated 1,000 random schedules generated by Part 1 and checked consistency between the detailed evaluation and scalar fitness interface.
- Verified that the new penalties change which schedule the GA prefers and that a fixed seed reproduces the unavailable slots and results.

## 5. Genetic Algorithm and Experiments (Parts 3–5)

- **Part 3: Genetic operators.** Tournament selection chooses parents. Two crossover strategies and swap mutation produce offspring while preserving task hours. See the [operator design report](step3_genetic_operators/REPORT.md).
- **Part 4: GA implementation.** `run_ga()` defaults to a population of 50, 100 generations, 80% crossover, 30% mutation, and 2 elites. It returns the best schedule and each generation's best and average fitness. The initial population is generation 0. See the [GA and survival strategies report](step4_ga_implementation/README_step4.md).
- **Part 5: Experiments and visualization.** `visualize.py` runs five experiments with the updated fitness function: random seeds, population size, mutation rate, crossover rate, and elite count. The population-size sweep runs for 100 generations; the other experiments run for 20. See the [experiment report](step5_experiments_visualization/README_part5.md).

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
