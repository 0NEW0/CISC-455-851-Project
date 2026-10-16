# CISC-455-851-Project

# Student Study Schedule Optimization

## Problem Definition
The goal is to optimize a student's weekly study schedule using a Genetic Algorithm (GA).

The schedule covers Monday to Friday, with 4 one-hour study slots per day, giving a total of 20 available slots.

There are four tasks with different priorities, deadlines, and required study hours.

## Chromosome Representation
- **Genotype:** A list of 20 genes, where each gene represents a one-hour time slot.
- **Gene Values:** A, B, C, D, or Free.
- **Phenotype:** A weekly timetable showing when each task is scheduled.
- **Constraints:** Each task must appear exactly as many times as its required hours.

## Initial Population
The `create_chromosome()` function generates a random weekly schedule.

The `create_population(size)` function generates multiple random schedules for the initial population.

## Optimization Goal
The GA aims to find a schedule that considers task priorities, meets deadlines, and balances workload across the week.
