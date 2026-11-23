"""
Strategy 1: Memetic Algorithm (Local Search / Hill Climbing)
Applies a local search repair to each mutated child to fine-tune the schedule.
Instead of relying purely on random mutation, this actively tries to improve 
the child by testing random swaps and keeping the ones that increase fitness.
"""

def memetic_repair(chromosome, rng, score, max_attempts=20):
    """
    Try to improve the chromosome by performing random swaps and keeping improvements.
    This acts as a local search (hill climbing) step after mutation.
    """
    best_chromosome = chromosome.copy()
    best_fitness = score(best_chromosome)
    
    for _ in range(max_attempts):
        candidate = best_chromosome.copy()
        # Pick two distinct random positions
        i, j = rng.sample(range(len(candidate)), 2)
        
        # Swap the genes
        candidate[i], candidate[j] = candidate[j], candidate[i]
        
        # Evaluate the new candidate
        candidate_fitness = score(candidate)
        
        # If it's better, keep it and continue searching from this new peak
        if candidate_fitness > best_fitness:
            best_chromosome = candidate
            best_fitness = candidate_fitness
            
    return best_chromosome