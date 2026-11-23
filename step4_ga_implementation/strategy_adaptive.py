"""
Strategy 3: Adaptive Penalties (Dynamic Fitness Landscape)
Dynamically adjusts penalty weights over generations to balance exploration vs exploitation.
"""

from step2_fitness_function.fitness_function import evaluate_fitness


def adaptive_fitness_wrapper(chromosome, unavailable_slots, generation, total_generations, 
                             base_deadline_weight=1000, base_unavailable_weight=1000):
    """
    Fitness function with adaptive penalty weights that change over generations.
    """
    progress = generation / total_generations if total_generations > 0 else 1.0
    scaling_factor = 0.1 + 0.9 * (progress ** 2)
    
    adaptive_deadline_weight = base_deadline_weight * scaling_factor
    adaptive_unavailable_weight = base_unavailable_weight * scaling_factor
    
    evaluation = evaluate_fitness(chromosome, unavailable_slots=unavailable_slots)
    
    cost = (
        adaptive_deadline_weight * evaluation["deadline_penalty"]
        + 1 * evaluation["priority_penalty"]
        + 5 * evaluation["balance_penalty"]
        + adaptive_unavailable_weight * evaluation["unavailable_slot_conflicts"]
        + 20 * evaluation["short_sessions"]
    )
    
    return -cost