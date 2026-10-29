"""Genetic operators for weekly study schedule optimization."""

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
