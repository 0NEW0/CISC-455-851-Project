"""
Visualize generation vs. best fitness

Run from the repository root with:
    python -m step5_experiments_visualization.visualize

Tests ga on the same seed 20 times. It takes the average best fitness over all runs at each generation.
It then plots the results to visualize how fast the algorithm converges on average

"""

import matplotlib.pylab as plt
import numpy as np

from step1_problem_representation.schedule_data import display_schedule
from step4_ga_implementation import genetic_algorithm as ga

# plot_date plots Generation vs. Best Fitness to see how fast the algorithm finds a solution
def plot_data(seed, best_fitness):
    generation = np.arange(1, len(best_fitness)+1)
    best_fitness = np.array(best_fitness)
    plt.plot(generation, best_fitness, marker='o', color='blue')
    plt.title(f"Generation vs. Best Fitness for Seed {seed}")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.grid(True)
    plt.show()


# run_trials returns the average best_fitness of each generation based on the seed and number of trials provided
def run_trials(seed, trial_count):
    best_fitness = []
    best_schedule = 0
    max_schedule_fitness = 0
    print("Testing...")
    for trial in range(20):
            print(f"Trial {trial+1}")
            result = ga.run_ga(seed=seed)
            if not best_fitness:
                best_fitness = result["best_history"]
                best_schedule = result["best_chromosome"]
                best_schedule_fitness = result["best_fitness"]
            else:
                for i in range(len(best_fitness)):
                    best_fitness[i] += result["best_history"][i]
                if result["best_fitness"] > best_schedule_fitness:
                     best_schedule = result["best_chromosome"]
                     best_schedule_fitness = result["best_fitness"]
    return [x / trial_count for x in best_fitness], best_schedule

def main():
    # Sets a random seed that remains consistent throughout all tests (seed is kept small for better readability on graph)
    seed = np.random.randint(0,30)
    # Sets the number of times the ga is run
    trial_count = 20
    # Tests the ga on the particular seed for the given number of trials
    best_fitness, best_schedule = run_trials(seed, trial_count)
    # Plots the average best fitness value per generation
    plot_data(seed, best_fitness)
    # Displays the schedule of the best schedule
    display_schedule(best_schedule)

if __name__ == "__main__":
    main()