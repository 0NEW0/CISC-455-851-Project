"""Plot the constrained GA experiments and report the schedules they select."""

import argparse
from contextlib import redirect_stdout
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from step1_problem_representation.schedule_data import DAYS, display_schedule
from step4_ga_implementation import genetic_algorithm as ga


FIGURES_DIR = Path(__file__).parent / "Figures from Tests"
RATES = (1, 0.5, 0.25, 0.125, 0.0625)
REQUIREMENTS = (
    ("All deadlines met", "deadline_penalty"),
    ("No unavailable-slot conflicts", "unavailable_slot_conflicts"),
    ("No short Project sessions", "short_sessions"),
)


def plot_data(description, best_fitness, *, trials=None, output_path=None):
    fig, ax = plt.subplots()
    ax.plot(range(len(best_fitness)), best_fitness, marker="o", markersize=3, color="#007D82")
    ax.set_title(f"Best Fitness by Generation: {description}")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness" if trials is None else f"Mean Best Fitness ({trials} seeds)")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    try:
        if output_path is None:
            plt.show()
        else:
            fig.savefig(output_path, dpi=160)
    finally:
        plt.close(fig)


def print_result(result):
    parameters = result["parameters"]
    slots = ", ".join(f"{DAYS[day]} slot {slot + 1}" for day, slot in parameters["unavailable_slots"])
    penalties = result["best_breakdown"]
    print(f"Best schedule: seed {parameters['seed']}, generation {result['best_generation']}, "
          f"fitness {result['best_fitness']:g}")
    print(f"Unavailable slots: {slots}")
    print(f"Penalties: deadline={penalties['deadline_penalty']}, "
          f"slot conflicts={penalties['unavailable_slot_conflicts']}, short sessions={penalties['short_sessions']}, "
          f"priority={penalties['priority_penalty']}, balance={penalties['balance_penalty']:g}")
    display_schedule(result["best_chromosome"])
    print()


def robustness_test(generations=100, *, output_dir=None):
    print(f"Robustness: five individual seeds, {generations} generations\n")
    for seed in range(1, 6):
        result = ga.run_ga(seed=seed, generations=generations)
        path = output_dir / f"Seed_{seed}.png" if output_dir is not None else None
        plot_data(f"Seed {seed}", result["best_history"], output_path=path)
        print_result(result)


def _parameter_test(label, parameter, values, figure_names, generations, trials, output_dir):
    if trials < 1:
        raise ValueError("At least one trial is required.")

    print(f"{label}: seeds 1–{trials}, {generations} generations per run\n")
    for value, filename in zip(values, figure_names, strict=True):
        description = f"{label} {value}"
        print(description)
        results = [ga.run_ga(seed=seed, generations=generations, **{parameter: value})
                   for seed in range(1, trials + 1)]
        histories = [result["best_history"] for result in results]
        mean_history = [mean(scores) for scores in zip(*histories, strict=True)]
        breakdowns = [result["best_breakdown"] for result in results]
        for name, penalty in REQUIREMENTS:
            print(f"{name}: {sum(b[penalty] == 0 for b in breakdowns)}/{trials}")
        all_met = sum(all(b[penalty] == 0 for _, penalty in REQUIREMENTS) for b in breakdowns)
        print(f"All three requirements met: {all_met}/{trials}")
        print(f"Mean final best fitness: {mean_history[-1]:.2f}")
        path = output_dir / filename if output_dir is not None else None
        plot_data(description, mean_history, trials=trials, output_path=path)
        print_result(max(results, key=lambda result: result["best_fitness"]))


def population_test(generations=100, trials=20, *, output_dir=None):
    values = (5, 10, 20, 40, 80)
    names = [f"Pop_{value}.png" for value in values]
    _parameter_test("Population Size", "population_size", values, names, generations, trials, output_dir)


def mutation_test(generations=100, trials=20, *, output_dir=None):
    names = [f"Mut_{rate * 100:g}.png" for rate in RATES]
    _parameter_test("Mutation Rate", "mutation_rate", RATES, names, generations, trials, output_dir)


def crossover_test(generations=100, trials=20, *, output_dir=None):
    names = [f"Cross_{rate * 100:g}.png" for rate in RATES]
    _parameter_test("Crossover Rate", "crossover_rate", RATES, names, generations, trials, output_dir)


def elite_test(generations=100, trials=20, *, output_dir=None):
    values = (0, 1, 2, 4, 8)
    names = ["elite_0.png", *(f"Elite_{count}.png" for count in values[1:])]
    _parameter_test("Elite Count", "elite_count", values, names, generations, trials, output_dir)


def main(output_dir=None):
    experiments = (
        (robustness_test, "Robustness", "Robustness Schedules.txt"),
        (population_test, "Population", "Population Schedules.txt"),
        (mutation_test, "Mutation", "Mutation Schedules.txt"),
        (crossover_test, "Crossover", "Cross_Schedules.txt"),
        (elite_test, "Elite", "Elite Schedules.txt"),
    )
    for experiment, folder, log_name in experiments:
        if output_dir is None:
            experiment()
        else:
            destination = output_dir / folder
            destination.mkdir(parents=True, exist_ok=True)
            print(f"Saving {folder} results to {destination}", flush=True)
            with (destination / log_name).open("w", encoding="utf-8", newline="\n") as log, redirect_stdout(log):
                experiment(output_dir=destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true", help="Refresh PNGs and schedule logs under Figures from Tests.")
    args = parser.parse_args()
    main(FIGURES_DIR if args.save else None)
