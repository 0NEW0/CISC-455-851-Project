"""Validate chromosome structure using the task configuration from Part 1."""

from collections import Counter

from step1_problem_representation.schedule_data import DAYS, SLOTS_PER_DAY, TASKS


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
