"""
Master Wrapper for Advanced GA Strategies.
Provides a unified interface to run the baseline or any advanced strategy.
"""

from . import genetic_algorithm as ga
from . import strategy_memetic
from . import strategy_island
from . import strategy_adaptive


def run_advanced_ga(strategy="baseline", **kwargs):
    """Unified interface to run the baseline or any advanced strategy."""
    if strategy == "baseline":
        return ga.run_ga(**kwargs)
        
    elif strategy == "memetic":
        kwargs["repair_function"] = strategy_memetic.memetic_repair
        return ga.run_ga(**kwargs)
        
    elif strategy == "island":
        return strategy_island.run_island_ga(**kwargs)
        
    elif strategy == "adaptive":
        return _run_adaptive_ga(**kwargs)
        
    else:
        raise ValueError(f"Unknown strategy: {strategy}. Choose from ['baseline', 'memetic', 'island', 'adaptive']")


def _run_adaptive_ga(
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
    **kwargs
):
    """Run GA with adaptive penalty weights."""
    from step1_problem_representation.schedule_data import choose_unavailable_slots
    
    unavailable_slots = choose_unavailable_slots(seed)
    
    # Note: For simplicity in this prototype, we apply the adaptive wrapper 
    # at generation 0. A fully dynamic version would update the generation 
    # counter via the generation_callback hook.
    score_override = lambda chromosome: strategy_adaptive.adaptive_fitness_wrapper(
        chromosome, unavailable_slots, 0, generations
    )
    
    return ga.run_ga(
        population_size=population_size,
        generations=generations,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        tournament_size=tournament_size,
        elite_count=elite_count,
        crossover_strategy=crossover_strategy,
        survival=survival,
        seed=seed,
        use_constraints=use_constraints,
        repair_function=repair_function,
        score_override=score_override,
    )