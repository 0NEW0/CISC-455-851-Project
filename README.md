# CISC-455-851-Project

# Student Study Schedule Optimization

## 1. Project Overview

The goal of this project is to optimize a student's weekly study schedule using a **Genetic Algorithm (GA)**.

The algorithm aims to create a study schedule that considers task priorities, deadlines, and workload balance.

The schedule covers Monday to Friday, with 4 one-hour study slots per day, giving a total of **20 available slots per week**.

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
- Total available time: 20 hours
- Total required study time: 15 hours
- Remaining free time: 5 hours

Deadlines are represented using numbers from 0 (Monday) to 4 (Friday). Each task should be completed by the end of its deadline day.

## 3. Chromosome Representation

Each chromosome represents a complete weekly study schedule.

- **Genotype:** A list of 20 genes, with each gene representing a one-hour time slot.
- **Gene Values:** A, B, C, D, or Free.
- **Phenotype:** A weekly timetable showing when each task is scheduled.
- **Constraints:** Each task must appear exactly as many times as its required hours.

For example, Task A must appear 4 times, Task B 5 times, Task C 3 times, Task D 3 times, and Free 5 times.

## 4. Current Implementation — Parts 1 and 2 Completed

**File: `schedule_data.py`**

The following components have been implemented:

### 4.1 Sample Task Data
- Defined available study days and time slots.
- Created four sample tasks with required hours, priorities, and deadlines.

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

**Note:** Initial schedules are randomly generated and may not satisfy all deadlines. The fitness function and genetic operators will be responsible for evaluating and improving these schedules.

### 4.5 Chromosome Validation
**File:** `step2_fitness_function/fitness_function.py`

**Function:** `validate_chromosome(chromosome)`

- Reuses the task data and study settings from Part 1.
- Checks that the chromosome contains exactly 20 valid slots.
- Checks that each task and Free appear exactly as many times as required.
- Raises a `ValueError` for invalid chromosomes so missing task hours cannot improve fitness.

### 4.6 Fitness Evaluation
**Function:** `evaluate_fitness(chromosome)`

- Evaluates a schedule using three penalty components:
  - **Deadline penalty:** Sums the days late for each scheduled task hour. Study on the deadline day is allowed.
  - **Priority penalty:** Sums task priority multiplied by the scheduled day index (Monday = 0). This encourages higher-priority work earlier in the week.
  - **Balance penalty:** Sums squared differences between daily study hours and the average of 3 hours per day.
- Combines the penalties using the following formula:

```text
fitness = -(1000 * deadline_penalty + priority_penalty + 5 * balance_penalty)
```

- Returns the fitness value and all three unweighted penalty components in a dictionary.
- Higher fitness values indicate better schedules; scores are nonpositive.
- With the current task data, priority penalty is at most 140 and balance penalty is at most 12. The deadline weight of 1000 ensures every on-time schedule scores higher than every late schedule.

**Note:** The priority rule assumes important tasks should be scheduled earlier. Weights should be reassessed if task data or scoring preferences change.

### 4.7 GA Fitness Interface and Example
**Function:** `fitness_function(chromosome)`

- Returns only the scalar fitness value for use by the Genetic Algorithm.
- Supports selection methods based on score comparisons, such as tournament or rank selection. Roulette-wheel selection requires a suitable score transformation to positive weights.
- Running `fitness_function.py` directly displays a random weekly schedule and its fitness breakdown.

### 4.8 Fitness Verification
- Checked a manually calculated schedule score and workload balance penalties.
- Checked deadline-day acceptance and penalties for task hours scheduled one or two days late.
- Checked rejection of incorrect lengths, unknown genes, and incorrect task counts.
- Evaluated 1,000 random schedules generated by Part 1 and checked consistency between the detailed evaluation and scalar fitness interface.

## 5. Remaining Project Components

### Part 3 — Genetic Operators
- Implement selection, crossover, and mutation.
- Maintain valid chromosome representations.

### Part 4 — GA Implementation
- Combine the previous components into a complete Genetic Algorithm.
- Run the algorithm for approximately 100 generations.
- Record the best fitness value for each generation.

### Part 5 — Experiments & Visualization
- Test the completed algorithm.
- Plot Generation vs. Best Fitness.
- Display the best weekly study schedule.
- Analyze the results and limitations.

## 6. Project Progress

| Part | Component | Status |
|---|---|---|
| 1 | Problem & Representation | Completed |
| 2 | Fitness Function | Completed |
| 3 | Genetic Operators | To Do |
| 4 | GA Implementation | To Do |
| 5 | Experiments & Visualization | To Do |


## Python Package Layout and Execution

The five Step directories use lowercase names with underscores and contain __init__.py package markers. Shared validation lives in `Shared/chromosome_validation.py`. Internal imports use standard Python imports; no dynamic loading or sys.path modifications are needed.

Run commands from the repository root:

```powershell
python -m step1_problem_representation.schedule_data
python -m step2_fitness_function.fitness_function
python -m unittest discover -s tests -p "test_*.py" -t . -v
```

Use module execution (`python -m`) rather than running nested files directly. See `step3_genetic_operators/REPORT.md` for integration guidance.
