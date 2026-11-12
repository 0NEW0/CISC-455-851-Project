"""Step 4: complete Genetic Algorithm for the weekly study schedule.

Run from the repository root with:
    python -m step4_ga_implementation.genetic_algorithm
"""

import random
import sys

from step1_problem_representation.schedule_data import create_population, display_schedule
from step2_fitness_function.fitness_function import evaluate_fitness, fitness_function
from step3_genetic_operators.genetic_operators import crossover, mutate, select_parent

# ---------------------------------------------------------------------------
# Parameter choices
# These are reasonable starting values, NOT tuned or proven optimal. Each has
# a short reason so it can be explained and defended.
# ---------------------------------------------------------------------------
# 50 schedules: the search space is about 20!/(4!5!3!3!5!) = 195,545,750,400
# (~1.96e11) arrangements, so 50 gives some diversity while 100 generations
# still run in a fraction of a second.
POPULATION_SIZE = 50
# Project requirement: roughly 100 generations. This is also the only stopping
# condition (fixed budget), which keeps runs comparable for Step 5.
GENERATIONS = 100
# High rate: recombining good schedules is the main source of progress.
CROSSOVER_RATE = 0.8
# mutate() applies ONE swap per chromosome with this probability. A moderate
# rate keeps diversity without constantly destroying good schedules.
MUTATION_RATE = 0.3
# Size 3 gives moderate selection pressure (best of 3 random individuals).
TOURNAMENT_SIZE = 3
# Elitism (used by the "elitist" scheme): the best 2 schedules are copied
# unchanged, so the best fitness can never get worse between generations.
ELITE_COUNT = 2
# Step 3's default strategy; both strategies always keep task counts valid.
CROSSOVER_STRATEGY = "count_preserving_crossfill"

# How the next population is chosen ("survival scheme"):
#   elitist          keep the best ELITE_COUNT, fill the rest with children (default)
#   mu_comma_lambda  only children survive (no elitism)
#   mu_plus_lambda   parents and children compete, the best population_size survive
#   steady_state     make 2 children at a time, replace the 2 worst
# Every scheme creates about population_size children per generation, so they
# use almost the same number of fitness evaluations.
SURVIVAL_SCHEMES = ("elitist", "mu_comma_lambda", "mu_plus_lambda", "steady_state")
SURVIVAL = "elitist"


def _make_offspring(population, count, crossover_rate, mutation_rate,
                    tournament_size, crossover_strategy, rng):
    """Create `count` children: tournament selection -> crossover -> mutation."""
    offspring = []
    while len(offspring) < count:
        parent1 = select_parent(population, fitness_function, rng, tournament_size)
        parent2 = select_parent(population, fitness_function, rng, tournament_size)
        child1, child2 = crossover(
            parent1, parent2, crossover_rate, rng, crossover_strategy
        )
        offspring.append(mutate(child1, mutation_rate, rng))
        if len(offspring) < count:
            offspring.append(mutate(child2, mutation_rate, rng))
    return offspring


def _rank(chromosomes):
    """Return (fitness, chromosome) pairs sorted from best to worst."""
    return sorted(
        ((fitness_function(c), c) for c in chromosomes),
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
):
    """Run the GA and return a dictionary of results.

    Population management: generational replacement. The default scheme is
    "elitist": each new generation = the elite_count best schedules (copied) +
    children made by tournament selection -> crossover -> swap mutation. The
    population size stays constant. See SURVIVAL_SCHEMES for the alternatives.
    elite_count is only used by the "elitist" scheme.

    Reproducibility: if seed is given, both the operators' random generator and
    Python's global random module (used by Part 1 to build the initial
    population) are seeded, so the same seed reproduces the whole run.

    Returned keys (for Step 5):
        best_chromosome      best schedule found (list of 20 genes)
        best_fitness         its fitness (higher is better, <= 0)
        best_breakdown       its penalty components from evaluate_fitness()
        best_generation      generation in which the best schedule first appeared
        best_history         best fitness per generation, index 0 = initial
                             population (length generations + 1)
        average_history      average fitness per generation, same indexing
        parameters           settings used, including seed and Python version
    """
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

    rng = random.Random(seed)
    if seed is not None:
        random.seed(seed)  # Part 1 uses the global random module

    offspring_settings = (crossover_rate, mutation_rate, tournament_size,
                          crossover_strategy, rng)
    population = create_population(population_size)
    best_chromosome, best_fitness, best_generation = None, float("-inf"), 0
    best_history, average_history = [], []

    for generation in range(generations + 1):
        # Evaluate each schedule once per generation.
        scored = _rank(population)
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
                scored + [(fitness_function(c), c) for c in children],
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
                    ranked[:-2] + [(fitness_function(k), k) for k in kids],
                    key=lambda pair: pair[0],
                    reverse=True,
                )
            population = [c for _, c in ranked]

    return {
        "best_chromosome": best_chromosome,
        "best_fitness": best_fitness,
        "best_breakdown": evaluate_fitness(best_chromosome),
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
            "python_version": sys.version.split()[0],
        },
    }


if __name__ == "__main__":
    result = run_ga(seed=42)
    print("Parameters:", result["parameters"])
    print("Best fitness per generation (first 5):", result["best_history"][:5])
    print("Best fitness per generation (last 5):", result["best_history"][-5:])
    print("Best found in generation:", result["best_generation"])
    print("Best fitness:", result["best_fitness"])
    print("Penalty breakdown:", result["best_breakdown"])
    display_schedule(result["best_chromosome"])