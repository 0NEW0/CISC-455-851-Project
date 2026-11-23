"""Step 4: complete Genetic Algorithm for the weekly study schedule.

Run from the repository root with:
    python -m step4_ga_implementation.genetic_algorithm
"""

import random
import sys
from functools import partial

from step1_problem_representation.schedule_data import (
    DAYS, choose_unavailable_slots, create_population, display_schedule,
)
from step2_fitness_function.fitness_function import evaluate_fitness, fitness_function
from step3_genetic_operators.genetic_operators import crossover, mutate, select_parent

# ---------------------------------------------------------------------------
# Parameter choices
# ---------------------------------------------------------------------------
POPULATION_SIZE = 50
GENERATIONS = 100
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.3
TOURNAMENT_SIZE = 3
ELITE_COUNT = 2
CROSSOVER_STRATEGY = "two_point_repair"

SURVIVAL_SCHEMES = ("elitist", "mu_comma_lambda", "mu_plus_lambda", "steady_state")
SURVIVAL = "elitist"


def _make_offspring(population, count, crossover_rate, mutation_rate,
                    tournament_size, crossover_strategy, rng, score,
                    repair_function=None):
    """Create `count` children: tournament selection -> crossover -> mutation -> repair."""
    offspring = []
    while len(offspring) < count:
        parent1 = select_parent(population, score, rng, tournament_size)
        parent2 = select_parent(population, score, rng, tournament_size)
        child1, child2 = crossover(
            parent1, parent2, crossover_rate, rng, crossover_strategy
        )
        
        # Mutate child 1
        child1 = mutate(child1, mutation_rate, rng)
        if repair_function is not None:
            child1 = repair_function(child1, rng, score)
        offspring.append(child1)
        
        if len(offspring) < count:
            # Mutate child 2
            child2 = mutate(child2, mutation_rate, rng)
            if repair_function is not None:
                child2 = repair_function(child2, rng, score)
            offspring.append(child2)
            
    return offspring


def _rank(chromosomes, score):
    """Return (fitness, chromosome) pairs sorted from best to worst."""
    return sorted(
        ((score(c), c) for c in chromosomes),
        key=lambda pair: pair[0],
        reverse=True,
    )


def run_ga(
    population_size=POPULATION_SIZE,
    generations=GENERATIONS,
    crossover_rate=CROSSOVER_RATE,
    mutation_rate=MUTATION_RATE,
    tournament_size=TOURNAMENT_SIZE,
    elite_count=ELITE_COUNT,
    crossover_strategy=CROSSOVER_STRATEGY,
    survival=SURVIVAL,
    seed=None,
    *,
    use_constraints=True,
    # --- NEW ADVANCED HOOKS ---
    repair_function=None,
    score_override=None,
    generation_callback=None,
):
    """Run the GA and return a dictionary of results."""
    if not isinstance(population_size, int) or population_size < 2:
        raise ValueError("Population size must be an integer of at least 2.")
    if not isinstance(generations, int) or generations < 1:
        raise ValueError("Generations must be a positive integer.")
    if not isinstance(elite_count, int) or not 0 <= elite_count < population_size:
        raise ValueError("Elite count must be between 0 and population size - 1.")
    if not isinstance(tournament_size, int) or not 1 <= tournament_size <= population_size:
        raise ValueError("Tournament size must be between 1 and population size.")
    if survival not in SURVIVAL_SCHEMES:
        raise ValueError(f"Survival must be one of {SURVIVAL_SCHEMES}.")

    # Draw once from a separate stream so the slots stay fixed across generations.
    unavailable_slots = choose_unavailable_slots(seed)
    scored_slots = unavailable_slots if use_constraints else None
    
    # --- HOOK: Score Override ---
    if score_override is not None:
        score = score_override
    elif use_constraints:
        score = partial(fitness_function, unavailable_slots=scored_slots)
    else:
        score = fitness_function
        
    rng = random.Random(seed)
    if seed is not None:
        random.seed(seed)  # Part 1 uses the global random module

    # Include repair_function in the settings tuple passed to _make_offspring
    offspring_settings = (crossover_rate, mutation_rate, tournament_size,
                          crossover_strategy, rng, score, repair_function)
                          
    population = create_population(population_size)
    best_chromosome, best_fitness, best_generation = None, float("-inf"), 0
    best_history, average_history = [], []

    for generation in range(generations + 1):
        # --- HOOK: Generation Callback (e.g., Island Migration) ---
        if generation_callback is not None:
            population = generation_callback(population, generation, rng)

        # Evaluate each schedule once per generation.
        scored = _rank(population, score)
        gen_best_fitness, gen_best = scored[0]
        best_history.append(gen_best_fitness)
        average_history.append(sum(s for s, _ in scored) / len(scored))
        if gen_best_fitness > best_fitness:
            best_fitness, best_chromosome = gen_best_fitness, gen_best.copy()
            best_generation = generation

        if generation == generations:
            break

        # Build the next generation with the chosen survival scheme.
        if survival == "elitist":
            population = [c.copy() for _, c in scored[:elite_count]] + _make_offspring(
                population, population_size - elite_count, *offspring_settings
            )
        elif survival == "mu_comma_lambda":
            population = _make_offspring(population, population_size, *offspring_settings)
        elif survival == "mu_plus_lambda":
            children = _make_offspring(population, population_size, *offspring_settings)
            pool = sorted(
                scored + [(score(c), c) for c in children],
                key=lambda pair: pair[0],
                reverse=True,
            )
            population = [c for _, c in pool[:population_size]]
        else:  # steady_state: 2 children at a time replace the 2 worst
            ranked = scored
            for _ in range(population_size // 2):
                kids = _make_offspring(
                    [c for _, c in ranked], 2, *offspring_settings
                )
                ranked = sorted(
                    ranked[:-2] + [(score(k), k) for k in kids],
                    key=lambda pair: pair[0],
                    reverse=True,
                )
            population = [c for _, c in ranked]

    return {
        "best_chromosome": best_chromosome,
        "best_fitness": best_fitness,
        "best_breakdown": evaluate_fitness(best_chromosome, unavailable_slots=scored_slots),
        "best_generation": best_generation,
        "best_history": best_history,
        "average_history": average_history,
        "parameters": {
            "population_size": population_size,
            "generations": generations,
            "crossover_rate": crossover_rate,
            "mutation_rate": mutation_rate,
            "tournament_size": tournament_size,
            "elite_count": elite_count,
            "crossover_strategy": crossover_strategy,
            "survival": survival,
            "seed": seed,
            "use_constraints": use_constraints,
            "unavailable_slots": unavailable_slots,
            "python_version": sys.version.split()[0],
        },
    }


if __name__ == "__main__":
    result = run_ga()
    print("Parameters:", result["parameters"])
    for day, slot in result["parameters"]["unavailable_slots"]:
        print(f"Unavailable slot: {DAYS[day]}, slot {slot + 1}")
    print("Best fitness per generation (first 5):", result["best_history"][:5])
    print("Best fitness per generation (last 5):", result["best_history"][-5:])
    print("Best found in generation:", result["best_generation"])
    print("Best fitness:", result["best_fitness"])
    print("Penalty breakdown:", result["best_breakdown"])
    display_schedule(result["best_chromosome"])