"""Compare the survival schemes of run_ga over many seeds.

Run from the repository root with:
    python -m step4_ga_implementation.compare_survival

All other settings stay at their defaults; only `survival` and the seed change.
For every scheme it reports:
  - how many runs reached the optimal fitness and how fast (in generations)
  - the best and mean fitness in the last generation
  - the median running time of one run (machine dependent, use as a rough guide)
  - the average number of fitness evaluations per run (machine independent).
    This counts every call to the fitness function, including the ones made
    inside tournament selection.
"""

import time
from statistics import mean, median

from step4_ga_implementation import genetic_algorithm as ga

SEEDS = range(30)
TARGET = -65  # optimal fitness, confirmed by brute force (see README)


def first_generation_at_target(history):
    for generation, value in enumerate(history):
        if value >= TARGET:
            return generation
    return None


def run_scheme(scheme):
    """Run one scheme for every seed; return results, times and evaluation counts."""
    original = ga.fitness_function
    calls = [0]

    def counting_fitness(chromosome):
        calls[0] += 1
        return original(chromosome)

    ga.fitness_function = counting_fitness  # run_ga looks this name up at call time
    results, times, evaluations = [], [], []
    try:
        for seed in SEEDS:
            calls[0] = 0
            start = time.perf_counter()
            results.append(ga.run_ga(seed=seed, survival=scheme))
            times.append(time.perf_counter() - start)
            evaluations.append(calls[0])
    finally:
        ga.fitness_function = original
    return results, times, evaluations


def main():
    print(f"{len(SEEDS)} seeds per scheme, target fitness {TARGET}")
    print(f"{'scheme':<17}{'reached':>8}{'avg gen':>9}{'max gen':>9}"
          f"{'final best':>12}{'final mean':>12}{'median s':>10}{'evaluations':>13}")
    for scheme in ga.SURVIVAL_SCHEMES:
        results, times, evaluations = run_scheme(scheme)
        gens = [first_generation_at_target(r["best_history"]) for r in results]
        reached = [g for g in gens if g is not None]
        print(
            f"{scheme:<17}{len(reached):>5}/{len(SEEDS)}"
            f"{mean(reached) if reached else float('nan'):>9.1f}"
            f"{max(reached) if reached else float('nan'):>9}"
            f"{mean(r['best_history'][-1] for r in results):>12.1f}"
            f"{mean(r['average_history'][-1] for r in results):>12.1f}"
            f"{median(times):>10.3f}"
            f"{mean(evaluations):>13,.0f}"
        )


if __name__ == "__main__":
    main()