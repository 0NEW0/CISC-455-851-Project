"""
Visualize generation vs. best fitness

Run from the repository root with:
    python -m step5_experiments_visualization.visualize

Tests ga on different types of tests:

- Robustness: Tests the GA on 5 different seeds to guarantee convergence
- Population: Tests the GA on 20 different seeds with modified population sizes
- Mutation: Tests the GA on 20 different seeds with modified mutation rates
- Crossover: Tests the GA on 20 different seeds with modified crossover rates
- Elite: Tests the GA on 20 different seeds with modified elite counts

All tests plot the average best_fitness compared to generation for each parameter change (besides robustness which does each seed once)

The program then displays the best schedule found 

"""

import matplotlib.pylab as plt
import numpy as np

from step1_problem_representation.schedule_data import display_schedule
from step4_ga_implementation import genetic_algorithm as ga

# plot_date plots Generation vs. Best Fitness to see how fast the algorithm finds a solution
def plot_data(description, best_fitness):
    generation = np.arange(1, len(best_fitness)+1)
    best_fitness = np.array(best_fitness)
    plt.plot(generation, best_fitness, marker='o', color='blue')
    plt.title(f"Generation vs. Best Fitness for {description}")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.grid(True)
    plt.show()

def robustness_test(generations=20):
        print("Testing Robustness...")
        for seed in range(1,6):
            print(f"Seed {seed}")
            result = ga.run_ga(seed=seed, generations=generations)
            description = "Seed " + str(seed)
            plot_data(description, result["best_history"])
            display_schedule(result["best_chromosome"])
        print("Robustness Testing Complete")

def population_test(generations=100, trials=20):
    print("Testing Population Size...")
    population_size = 5
    for _ in range(5):
        best_schedule = 0
        best_fitness = 0       
        print(f"Population size {population_size}")
        result = ga.run_ga(population_size=population_size, generations=generations, seed=1)
        best_schedule = result["best_chromosome"]
        best_schedule_fitness = result["best_fitness"]
        best_fitness = result["best_history"]
        for seed in range(1, trials):
            result = ga.run_ga(population_size=population_size, generations=generations, seed=seed)
            for i in range(len(best_fitness)):
                best_fitness[i] += result["best_history"][i]
            if result["best_fitness"] > best_schedule_fitness:
                best_schedule = result["best_chromosome"]
                best_schedule_fitness = result["best_fitness"]
        description = "Population Size " + str(population_size)
        plot_data(description, [x / generations for x in best_fitness])
        display_schedule(best_schedule)
        population_size *= 2
    print("Population Size Testing Complete")

def mutation_test(generations=20, trials=20):
    print("Testing Mutation Rate...")
    mutation_rate = 1
    for _ in range(5):
        best_schedule = 0
        best_fitness = 0       
        print(f"Mutation Rate {mutation_rate}")
        result = ga.run_ga(mutation_rate=mutation_rate, generations=generations, seed=1)
        best_schedule = result["best_chromosome"]
        best_schedule_fitness = result["best_fitness"]
        best_fitness = result["best_history"]
        for seed in range(1, trials):
            result = ga.run_ga(mutation_rate=mutation_rate, generations=generations, seed=seed)
            for i in range(len(best_fitness)):
                best_fitness[i] += result["best_history"][i]
            if result["best_fitness"] > best_schedule_fitness:
                best_schedule = result["best_chromosome"]
                best_schedule_fitness = result["best_fitness"]
        description = "Mutation Rate " + str(mutation_rate)
        plot_data(description, [x / generations for x in best_fitness])
        display_schedule(best_schedule)
        mutation_rate /= 2
    print("Mutation Rate Testing Complete")

def crossover_test(generations=20, trials=20):
    print("Testing Crossover Rate...")
    crossover_rate = 1
    for _ in range(5):
        best_schedule = 0
        best_fitness = 0       
        print(f"Crossover Rate {crossover_rate}")
        result = ga.run_ga(crossover_rate=crossover_rate, generations=generations, seed=1)
        best_schedule = result["best_chromosome"]
        best_schedule_fitness = result["best_fitness"]
        best_fitness = result["best_history"]
        for seed in range(1, trials):
            result = ga.run_ga(crossover_rate=crossover_rate, generations=generations, seed=seed)
            for i in range(len(best_fitness)):
                best_fitness[i] += result["best_history"][i]
            if result["best_fitness"] > best_schedule_fitness:
                best_schedule = result["best_chromosome"]
                best_schedule_fitness = result["best_fitness"]
        description = "Crossover Rate " + str(crossover_rate)
        plot_data(description, [x / generations for x in best_fitness])
        display_schedule(best_schedule)
        crossover_rate /= 2

def elite_test(generations=20, trials=20):
    print("Testing Elite Count...")
    elite_count = 0
    for _ in range(5):
        best_schedule = 0
        best_fitness = 0       
        print(f"Elite Count {elite_count}")
        result = ga.run_ga(elite_count=elite_count, generations=generations, seed=1)
        best_schedule = result["best_chromosome"]
        best_schedule_fitness = result["best_fitness"]
        best_fitness = result["best_history"]
        for seed in range(1, trials):
            result = ga.run_ga(elite_count=elite_count, generations=generations, seed=seed)
            for i in range(len(best_fitness)):
                best_fitness[i] += result["best_history"][i]
            if result["best_fitness"] > best_schedule_fitness:
                best_schedule = result["best_chromosome"]
                best_schedule_fitness = result["best_fitness"]
        description = "Elite Count " + str(elite_count)
        plot_data(description, [x / generations for x in best_fitness])
        display_schedule(best_schedule)
        elite_count = 1 if elite_count == 0 else elite_count*2

def main():
    robustness_test()
    population_test()
    mutation_test()
    crossover_test()
    elite_test()

if __name__ == "__main__":
    main()
