"""
Strategy 2: Island Model GA (Multi-Population with Migration)
Maintains multiple independent populations (islands) that evolve separately.
Every `migration_interval` generations, the best individuals migrate to the 
next island, injecting fresh genetic diversity and preventing premature convergence.
"""

import random
import sys
from functools import partial

from step1_problem_representation.schedule_data import choose_unavailable_slots, create_population
from step2_fitness_function.fitness_function import evaluate_fitness, fitness_function
from step4_ga_implementation.genetic_algorithm import (
    _make_offspring, _rank, SURVIVAL_SCHEMES
)


def run_island_ga(
    num_islands=3,
    migration_interval=10,
    migrants_count=2,
    population_size=50,
    generations=100,
    crossover_rate=0.8,
    mutation_rate=0.3,
    tournament_size=3,
    elite_count=2,
    crossover_strategy="two_point_repair",
    survival="elitist",
    seed=None,
    *,
    use_constraints=True,
    repair_function=None,
    score_override=None,
):
    if survival not in SURVIVAL_SCHEMES:
        raise ValueError(f"Survival must be one of {SURVIVAL_SCHEMES}.")

    rng = random.Random(seed)
    if seed is not None:
        random.seed(seed)

    unavailable_slots = choose_unavailable_slots(seed)
    scored_slots = unavailable_slots if use_constraints else None
    
    if score_override is not None:
        score = score_override
    elif use_constraints:
        score = partial(fitness_function, unavailable_slots=scored_slots)
    else:
        score = fitness_function

    offspring_settings = (crossover_rate, mutation_rate, tournament_size,
                          crossover_strategy, rng, score, repair_function)

    islands = [create_population(population_size) for _ in range(num_islands)]
    best_chromosome, best_fitness, best_generation = None, float("-inf"), 0
    best_history, average_history = [], []

    for generation in range(generations + 1):
        gen_best_fitness = float("-inf")
        gen_sum_fitness = 0
        total_individuals = 0

        for island_idx in range(num_islands):
            population = islands[island_idx]
            scored = _rank(population, score)
            
            if scored[0][0] > gen_best_fitness:
                gen_best_fitness = scored[0][0]
            gen_sum_fitness += sum(s for s, _ in scored)
            total_individuals += len(scored)

            if scored[0][0] > best_fitness:
                best_fitness = scored[0][0]
                best_chromosome = scored[0][1].copy()
                best_generation = generation

            if generation == generations:
                continue

            if survival == "elitist":
                next_pop = [c.copy() for _, c in scored[:elite_count]] + _make_offspring(
                    population, population_size - elite_count, *offspring_settings
                )
            elif survival == "mu_comma_lambda":
                next_pop = _make_offspring(population, population_size, *offspring_settings)
            elif survival == "mu_plus_lambda":
                children = _make_offspring(population, population_size, *offspring_settings)
                pool = sorted(scored + [(score(c), c) for c in children], key=lambda p: p[0], reverse=True)
                next_pop = [c for _, c in pool[:population_size]]
            else:
                ranked = scored
                for _ in range(population_size // 2):
                    kids = _make_offspring([c for _, c in ranked], 2, *offspring_settings)
                    ranked = sorted(ranked[:-2] + [(score(k), k) for k in kids], key=lambda p: p[0], reverse=True)
                next_pop = [c for _, c in ranked]
            
            islands[island_idx] = next_pop

        best_history.append(gen_best_fitness)
        average_history.append(gen_sum_fitness / total_individuals if total_individuals > 0 else 0)

        # --- MIGRATION PHASE ---
        if generation > 0 and generation % migration_interval == 0 and generation < generations:
            for i in range(num_islands):
                source_island_idx = i
                target_island_idx = (i + 1) % num_islands
                
                source_scored = _rank(islands[source_island_idx], score)
                migrants = [c.copy() for _, c in source_scored[:migrants_count]]
                
                target_scored = _rank(islands[target_island_idx], score)
                islands[target_island_idx] = [c for _, c in target_scored[migrants_count:]] + migrants

    return {
        "best_chromosome": best_chromosome,
        "best_fitness": best_fitness,
        "best_breakdown": evaluate_fitness(best_chromosome, unavailable_slots=scored_slots),
        "best_generation": best_generation,
        "best_history": best_history,
        "average_history": average_history,
        "parameters": {
            "strategy": "island_model",
            "num_islands": num_islands,
            "migration_interval": migration_interval,
            "migrants_count": migrants_count,
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