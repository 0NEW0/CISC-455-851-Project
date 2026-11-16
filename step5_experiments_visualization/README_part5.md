# Part 5 - Experiments Visualization

## Files added in this part

| File | What it is |
| ---- | ---------- |
| visualize.py | Runs 5 different tests on the GA algorithm and displays best fitness per generation and best schedule from each test|
| Figures From Tests | Holds graphs of best fitness per generation from each trial run |

## Robustness Tests

The algorithm successfully found valid schedules for all tested random seeds, demonstrating strong robustness. Most seeds converged within four generations, although one seed required seventeen generations before finding a valid solution. This suggests that while convergence is generally very fast, random factors can still have a noticeable impact on convergence speed.

To account for these occasional slower runs, a generation limit of 100 was retained. This limit provides more than enough opportunity for convergence while maintaining reasonable computation times on typical hardware.

## Population Size Tests

Population size had a significant impact on convergence speed. Smaller populations generally required substantially more generations to find valid schedules. In particular, a population size of 5 failed to converge within the 100-generation limit on average.

As population size increased, convergence became considerably faster. A population size of 80 converged after approximately 4 generations on average, demonstrating the advantage of maintaining a larger pool of candidate solutions. Larger populations provide greater genetic diversity, increasing the likelihood of useful traits being combined into valid schedules.

However, larger populations also require more computation per generation. To balance computational cost with reliable convergence, a population size of 50 was selected.

## Mutation Rate Tests

Higher mutation rates generally resulted in faster convergence. Mutation rates above 12.5% converged after approximately 5 generations on average, while mutation rates of 12.5% and below required approximately 7 generations.

This behaviour may be explained by mutations occurring within highly fit individuals. These mutations can introduce missing schedule components and produce fully valid schedules more quickly than relying solely on crossover and selection.

While very high mutation rates can disrupt promising solutions, moderate mutation rates appeared to provide enough exploration to discover valid schedules efficiently. A mutation rate of 30% was selected because it balanced exploration while still promoting rapid convergence.

## Crossover Rate Tests

Crossover rate had a much stronger impact on convergence speed compared to mutation rate. Higher crossover rates consistently produced faster convergence, with a crossover rate of 100% converging after approximately 4 generations on average. In contrast, crossover rates of 12.5% and below required approximately 8 generations on average.

Since crossover combines genetic information from two highly fit individuals, higher crossover rates increase the likelihood of producing offspring that meets our scheduling requirements. This allows the population to create complete schedules more quickly.

A crossover rate of 80% was selected because it provided most of the observed speed benefits while still allowing some offspring to be generated without crossover, preserving additional opportunities for exploration.

## Elite Count Tests

Varying the elite count produced little observable impact on convergence speed or schedule diversity. Across all tested elite counts, the algorithm converged in approximately one generation and produced similar schedules.

These results suggest that elitism is not a major factor for this particular scheduling problem. Nevertheless, an elite count of 2 was selected to ensure that high-quality solutions are preserved between generations without significantly reducing population diversity.

## Overall Findings

Across all experiments, the algorithm consistently found valid schedules under a wide range of parameter settings. The primary differences between configurations were observed in convergence speed rather than the ability to find a solution.

Population size, mutation rate, and crossover rate all influenced how quickly valid schedules were discovered. Larger populations, higher mutation rates, and higher crossover rates generally led to faster convergence. Elite count had little measurable impact on performance.

Based on the experimental results, the final parameter settings were:

- **Population Size:** 50
- **Mutation Rate:** 30%
- **Crossover Rate:** 80%
- **Elite Count:** 2
- **Generation Limit:** 100

These settings provided a balance between convergence speed, computational efficiency, solution quality, and reliability across multiple runs.

# How to Run

From the repository root with:
```java
python -m step5_experiments_visualization.visualize
```
