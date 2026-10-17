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

## 4. Current Implementation — Part 1 Completed

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

## 5. Remaining Project Components

### Part 2 — Fitness Function
- Evaluate schedules based on priorities, deadlines, and workload balance.
- Apply penalties for undesirable schedules.

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
| 2 | Fitness Function | To Do |
| 3 | Genetic Operators | To Do |
| 4 | GA Implementation | To Do |
| 5 | Experiments & Visualization | To Do |

