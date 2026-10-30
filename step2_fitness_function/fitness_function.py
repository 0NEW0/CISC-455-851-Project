"""Evaluate schedules. Run from the repository root with python -m step2_fitness_function.fitness_function."""

from Shared.chromosome_validation import validate_chromosome
from step1_problem_representation.schedule_data import (
    DAYS, SLOTS_PER_DAY, TASKS, create_chromosome, display_schedule,
)

DEADLINE_WEIGHT = 1000
PRIORITY_WEIGHT = 1
BALANCE_WEIGHT = 5


def evaluate_fitness(chromosome):
    """Return the fitness and its unweighted penalty components.

    Deadline penalty: sum of days late for every task hour. The deadline day
    itself is allowed. Priority penalty: priority times day index for every
    task hour, encouraging important work earlier in the week. Balance penalty:
    squared deviations from the average daily study hours.

    With the current data, priority <= 140 and balance <= 12. A deadline
    weight of 1000 therefore makes every on-time schedule outrank every late
    schedule. Reassess weights if task data or other weights change.
    """
    validate_chromosome(chromosome)
    daily_hours = [0] * len(DAYS)
    deadline_penalty = 0
    priority_penalty = 0

    for index, task_id in enumerate(chromosome):
        if task_id == "Free":
            continue
        day = index // SLOTS_PER_DAY
        task = TASKS[task_id]
        daily_hours[day] += 1
        deadline_penalty += max(0, day - task["deadline"])
        priority_penalty += task["priority"] * day

    average_hours = sum(task["hours"] for task in TASKS.values()) / len(DAYS)
    balance_penalty = sum((hours - average_hours) ** 2 for hours in daily_hours)
    fitness = -(
        DEADLINE_WEIGHT * deadline_penalty
        + PRIORITY_WEIGHT * priority_penalty
        + BALANCE_WEIGHT * balance_penalty
    )
    return {
        "fitness": fitness,
        "deadline_penalty": deadline_penalty,
        "priority_penalty": priority_penalty,
        "balance_penalty": balance_penalty,
    }


def fitness_function(chromosome):
    """Return a scalar score for GA selection or maximization."""
    return evaluate_fitness(chromosome)["fitness"]


if __name__ == "__main__":
    schedule = create_chromosome()
    display_schedule(schedule)
    print("Fitness evaluation:", evaluate_fitness(schedule))
