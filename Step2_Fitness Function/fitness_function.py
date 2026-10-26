"""Evaluate weekly study schedules. Higher fitness values are better.

Run this file directly to evaluate and display a random schedule.
"""

from collections import Counter
import importlib.util
from pathlib import Path

_DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "Step1_Problem & Representation"
    / "schedule_data.py"
)
_spec = importlib.util.spec_from_file_location("schedule_data", _DATA_PATH)
_schedule_data = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_schedule_data)

DAYS = _schedule_data.DAYS
SLOTS_PER_DAY = _schedule_data.SLOTS_PER_DAY
TASKS = _schedule_data.TASKS

DEADLINE_WEIGHT = 1000
PRIORITY_WEIGHT = 1
BALANCE_WEIGHT = 5


def validate_chromosome(chromosome):
    """Raise ValueError unless the schedule has exactly the required slots."""
    total_slots = len(DAYS) * SLOTS_PER_DAY
    expected = Counter({task_id: task["hours"] for task_id, task in TASKS.items()})
    free_slots = total_slots - sum(expected.values())
    if free_slots < 0:
        raise ValueError("Tasks exceed available study time.")
    expected["Free"] = free_slots

    if len(chromosome) != total_slots:
        raise ValueError(f"Chromosome must contain exactly {total_slots} slots.")
    if any(not isinstance(gene, str) or gene not in expected for gene in chromosome):
        raise ValueError("Chromosome contains an unknown task or invalid gene.")
    if Counter(chromosome) != expected:
        raise ValueError(f"Incorrect task counts; expected {dict(expected)}.")


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
    schedule = _schedule_data.create_chromosome()
    _schedule_data.display_schedule(schedule)
    print("Fitness evaluation:", evaluate_fitness(schedule))
