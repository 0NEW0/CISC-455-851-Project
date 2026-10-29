"""Genetic operators for weekly study schedule optimization."""

import math
from collections import Counter
from numbers import Real

from Shared.chromosome_validation import validate_chromosome


def select_parent(
    population,
    fitness_function,
    random_number_generator,
    tournament_size=3,
):
    """Return an independent copy of the winner, breaking fitness ties randomly.

    Validate every chromosome before sampling without replacement. Only sampled
    participants are scored. Raise ValueError for an empty population, invalid
    tournament size, or invalid chromosome. The default tournament size is 3;
    smaller populations must supply an explicit smaller size.
    """
    if not population:
        raise ValueError("Population must not be empty.")

    if not isinstance(tournament_size, int) or isinstance(tournament_size, bool):
        raise ValueError("Tournament size must be an integer.")
    if not 1 <= tournament_size <= len(population):
        raise ValueError("Tournament size must be between 1 and population size.")

    for chromosome in population:
        validate_chromosome(chromosome)

    participants = random_number_generator.sample(population, tournament_size)
    evaluated_participants = [
        (participant, fitness_function(participant))
        for participant in participants
    ]
    best_fitness = max(score for _, score in evaluated_participants)
    best_participants = [
        participant
        for participant, score in evaluated_participants
        if score == best_fitness
    ]
    if len(best_participants) == 1:
        selected_parent = best_participants[0]
    else:
        selected_parent = random_number_generator.choice(best_participants)
    return selected_parent.copy()


def crossover(
    parent1,
    parent2,
    crossover_rate,
    random_number_generator,
    strategy="count_preserving_crossfill",
):
    """Validate inputs and apply the selected crossover with the given probability.

    Rates must be finite real numbers in [0, 1], excluding booleans. Both
    parents and the strategy are validated even when the rate is zero.
    Both strategies preserve task counts and return independent children.
    """
    if (
        isinstance(crossover_rate, bool)
        or not isinstance(crossover_rate, Real)
        or not 0 <= crossover_rate <= 1
        or not math.isfinite(crossover_rate)
    ):
        raise ValueError("Crossover rate must be a finite number between 0 and 1.")
    if strategy not in ("count_preserving_crossfill", "two_point_repair"):
        raise ValueError("Unknown crossover strategy.")
    validate_chromosome(parent1)
    validate_chromosome(parent2)

    if crossover_rate == 0 or (
        crossover_rate < 1 and random_number_generator.random() >= crossover_rate
    ):
        return parent1.copy(), parent2.copy()
    start, end = sorted(random_number_generator.sample(range(len(parent1) + 1), 2))
    if strategy == "count_preserving_crossfill":
        return (
            _count_preserving_crossfill(parent1, parent2, start, end),
            _count_preserving_crossfill(parent2, parent1, start, end),
        )
    return (
        _two_point_crossover_with_repair(parent1, parent2, start, end, random_number_generator),
        _two_point_crossover_with_repair(parent2, parent1, start, end, random_number_generator),
    )


def _count_preserving_crossfill(segment_parent, donor_parent, start, end):
    """Build one child from validated parents and half-open segment [start:end].

    Preserve the segment in place. Traverse the donor and empty positions
    circularly from end, accepting genes only while their counts are needed.
    """
    size = len(segment_parent)
    child = [None] * size
    child[start:end] = segment_parent[start:end]
    remaining = Counter(segment_parent)
    remaining.subtract(segment_parent[start:end])
    empty_positions = iter(list(range(end, size)) + list(range(start)))
    for offset in range(size):
        gene = donor_parent[(end + offset) % size]
        if remaining[gene] > 0:
            child[next(empty_positions)] = gene
            remaining[gene] -= 1
    return child


def _two_point_crossover_with_repair(
    segment_parent, outside_parent, start, end, random_number_generator,
):
    """Build one child and repair only excess occurrences outside [start:end].

    Parents are already validated. For each excess task, sample the required
    number of outside positions. Shuffle missing genes before replacements.
    """
    child = outside_parent.copy()
    child[start:end] = segment_parent[start:end]
    expected = Counter(segment_parent)
    actual = Counter(child)
    repair_positions = []
    missing_genes = []
    for gene, required_count in expected.items():
        excess = actual[gene] - required_count
        if excess > 0:
            candidates = [
                index for index, value in enumerate(child)
                if value == gene and not start <= index < end
            ]
            repair_positions.extend(random_number_generator.sample(candidates, excess))
        elif excess < 0:
            missing_genes.extend([gene] * -excess)
    if missing_genes:
        random_number_generator.shuffle(missing_genes)
        for position, gene in zip(repair_positions, missing_genes):
            child[position] = gene
    return child


def mutate(chromosome, mutation_rate, random_number_generator):
    """Return a new chromosome, applying one swap with the given probability.

    Validate the chromosome even at rate zero. Sample two distinct positions
    without replacement; equal genes and fitness-neutral swaps are allowed.
    """
    if (
        isinstance(mutation_rate, bool)
        or not isinstance(mutation_rate, Real)
        or not 0 <= mutation_rate <= 1
        or not math.isfinite(mutation_rate)
    ):
        raise ValueError("Mutation rate must be a finite number between 0 and 1.")
    validate_chromosome(chromosome)
    mutated = chromosome.copy()
    if mutation_rate == 0 or (
        mutation_rate < 1 and random_number_generator.random() >= mutation_rate
    ):
        return mutated
    first, second = random_number_generator.sample(range(len(mutated)), 2)
    mutated[first], mutated[second] = mutated[second], mutated[first]
    return mutated
