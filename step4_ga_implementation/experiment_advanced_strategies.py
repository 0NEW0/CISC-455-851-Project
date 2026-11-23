"""
Master Experiment Script for Advanced GA Strategies.
Runs 4 strategies (Baseline + 3 Advanced) across multiple seeds and provides
comprehensive statistical comparison for the final presentation.

Run from the repository root with:
    uv run python -m step4_ga_implementation.experiment_advanced_strategies
"""

from statistics import mean, median
from step4_ga_implementation.strategy_runner import run_advanced_ga

SEEDS = range(1, 21)  # 20 seeds for statistical significance
GENERATIONS = 100
STRATEGIES = ["baseline", "memetic", "island", "adaptive"]


def run_strategy(strategy_name):
    """Run one strategy across all seeds and collect metrics."""
    results = []
    for seed in SEEDS:
        result = run_advanced_ga(strategy=strategy_name, seed=seed, generations=GENERATIONS)
        breakdown = result['best_breakdown']
        
        results.append({
            'seed': seed,
            'best_fitness': result['best_fitness'],
            'best_generation': result['best_generation'],
            'final_best': result['best_history'][-1],
            'deadline_penalty': breakdown['deadline_penalty'],
            'slot_conflicts': breakdown['unavailable_slot_conflicts'],
            'short_sessions': breakdown['short_sessions'],
        })
    return results


def print_strategy_results(strategy_name, results):
    """Print detailed results for one strategy."""
    print(f"\n{'='*70}")
    print(f"STRATEGY: {strategy_name.upper()}")
    print(f"{'='*70}")
    
    best_fitnesses = [r['best_fitness'] for r in results]
    best_generations = [r['best_generation'] for r in results]
    final_bests = [r['final_best'] for r in results]
    
    deadline_violations = sum(1 for r in results if r['deadline_penalty'] > 0)
    slot_violations = sum(1 for r in results if r['slot_conflicts'] > 0)
    session_violations = sum(1 for r in results if r['short_sessions'] > 0)
    
    print(f"Runs: {len(results)}")
    print(f"Best Fitness:     mean={mean(best_fitnesses):.1f}, median={median(best_fitnesses):.1f}")
    print(f"Best Generation:  mean={mean(best_generations):.1f}, min={min(best_generations)}, max={max(best_generations)}")
    print(f"Final Best:       mean={mean(final_bests):.1f}, median={median(final_bests):.1f}")
    print(f"\nConstraint Violations (out of {len(results)} runs):")
    print(f"  Deadline violations:      {deadline_violations}/{len(results)}")
    print(f"  Slot conflicts:           {slot_violations}/{len(results)}")
    print(f"  Short sessions:           {session_violations}/{len(results)}")


def print_comparison_table(all_results):
    """Print a clean comparison table of all strategies."""
    print("\n" + "="*90)
    print("COMPARISON TABLE: ALL STRATEGIES")
    print("="*90)
    print(f"{'Strategy':<15} {'Best Fitness':<15} {'Best Gen':<12} {'Final Best':<12} {'Deadline':<10} {'Slots':<8} {'Sessions':<10}")
    print("-"*90)
    
    for strategy in STRATEGIES:
        results = all_results[strategy]
        best_fitnesses = [r['best_fitness'] for r in results]
        best_generations = [r['best_generation'] for r in results]
        final_bests = [r['final_best'] for r in results]
        
        deadline_violations = sum(1 for r in results if r['deadline_penalty'] > 0)
        slot_violations = sum(1 for r in results if r['slot_conflicts'] > 0)
        session_violations = sum(1 for r in results if r['short_sessions'] > 0)
        
        print(f"{strategy:<15} {mean(best_fitnesses):<15.1f} {mean(best_generations):<12.1f} "
              f"{mean(final_bests):<12.1f} {deadline_violations:<10} {slot_violations:<8} {session_violations:<10}")
    
    print("="*90)


def main():
    print("="*90)
    print("ADVANCED GA STRATEGIES COMPARISON")
    print(f"Running {len(STRATEGIES)} strategies across {len(SEEDS)} seeds, {GENERATIONS} generations each")
    print("="*90)
    
    all_results = {}
    for strategy in STRATEGIES:
        print(f"\nRunning {strategy}...")
        results = run_strategy(strategy)
        all_results[strategy] = results
        print_strategy_results(strategy, results)
    
    print_comparison_table(all_results)
    print("\n Experiment complete! Use these results for your presentation.")
    print("="*90)


if __name__ == "__main__":
    main()