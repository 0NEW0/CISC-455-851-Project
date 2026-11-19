"""Evaluate schedules. Run from the repository root with python -m step2_fitness_function.fitness_function."""

from itertools import groupby

from Shared.chromosome_validation import validate_chromosome
from step1_problem_representation.schedule_data import (
    DAYS, SLOTS_PER_DAY, TASKS, choose_unavailable_slots, create_chromosome, display_schedule,
)

DEADLINE_WEIGHT = 1000
PRIORITY_WEIGHT = 1
BALANCE_WEIGHT = 5
UNAVAILABLE_SLOT_WEIGHT = 1000
SHORT_SESSION_WEIGHT = 20


def evaluate_fitness(chromosome, *, unavailable_slots=None):
    """Return the fitness and its unweighted penalty components.

    Deadline penalty: sum of days late for every task hour. The deadline day
    itself is allowed. Priority penalty: priority times day index for every
    task hour, encouraging important work earlier in the week. Balance penalty:
    squared deviations from the average daily study hours.

    Pass zero-based (day, slot) pairs to include the new scheduling rules.
    Each occupied unavailable slot and each short same-day study block add
    a penalty. Omit unavailable_slots to reproduce the original score.
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
    cost = (
        DEADLINE_WEIGHT * deadline_penalty
        + PRIORITY_WEIGHT * priority_penalty
        + BALANCE_WEIGHT * balance_penalty
    )
    penalties = {
        "deadline_penalty": deadline_penalty,
        "priority_penalty": priority_penalty,
        "balance_penalty": balance_penalty,
    }

    if unavailable_slots is not None:
        conflicts = sum(
            chromosome[day * SLOTS_PER_DAY + slot] != "Free"
            for day, slot in unavailable_slots
        )
        short_sessions = 0
        for start in range(0, len(chromosome), SLOTS_PER_DAY):
            day_slots = chromosome[start:start + SLOTS_PER_DAY]
            for task_id, session in groupby(day_slots):
                if task_id == "Free":
                    continue
                minimum_hours = TASKS[task_id].get("min_session_hours", 1)
                if minimum_hours > 1 and sum(1 for _ in session) < minimum_hours:
                    short_sessions += 1

        penalties["unavailable_slot_conflicts"] = conflicts
        penalties["short_sessions"] = short_sessions
        cost += UNAVAILABLE_SLOT_WEIGHT * conflicts + SHORT_SESSION_WEIGHT * short_sessions

    return {"fitness": -cost, **penalties}


def fitness_function(chromosome, *, unavailable_slots=None):
    """Return a scalar score for GA selection or maximization."""
    return evaluate_fitness(chromosome, unavailable_slots=unavailable_slots)["fitness"]


if __name__ == "__main__":
    schedule = create_chromosome()
    unavailable_slots = choose_unavailable_slots()
    for day, slot in unavailable_slots:
        print(f"Unavailable slot: {DAYS[day]}, slot {slot + 1}")
    display_schedule(schedule)
    print("Fitness evaluation:", evaluate_fitness(schedule, unavailable_slots=unavailable_slots))
