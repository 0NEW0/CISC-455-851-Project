# Part 5 - Experiments Visualization

## Files added in this part

| File | What it is |
| ---- | ---------- |
| visualize.py | Runs 5 different tests on the GA algorithm and displays best fitness per generation and best schedule from each test|
| Figures From Tests | Holds graphs of best fitness per generation from each trial run |

## Test Results

### Robustness Tests

The algorithm successfully found valid schedules for all tested random seeds. Most seeds converged within four generations; however, Seed 4 required seventeen generations before finding a valid solution. This suggests that while convergence is generally very fast, random initialization can still have a noticeable impact on convergence speed. Therefore, a generation limit of 100 was retained to ensure reliable convergence across a wide range of runs while maintaining reasonable computation times.

Across different seeds, many of the best schedules assigned tasks to similar days while varying only the time slots. This suggests that the algorithm may be converging toward a limited region of the solution space. Additional testing of selection pressure would be needed to determine whether this behaviour is caused by premature convergence or by characteristics of the scheduling problem itself.

### Population Tests

Population size testing produced some of the most interesting results. All tested population sizes ranging from 5 to 80 individuals were able to converge within 20 generations. On average, most population sizes converged within approximately 3 generations, although the population size of 20 required around 12 generations to converge.

Smaller populations appeared to produce a wider variety of final schedules, with tasks often being assigned to different days rather than simply different time periods. However, convergence behaviour was less predictable compared to larger populations. Larger populations produced more consistent convergence behaviour but generally generated schedules with similar overall structures.

Since all population sizes were able to find valid schedules, population size primarily affected convergence consistency rather than solution quality. A population size of 50 was selected because it provided predictable convergence behaviour while maintaining reasonable computation times.

### Mutation Rate Tests

Mutation rate had a noticeable effect on convergence speed. Higher mutation rates generally converged later in the run, averaging approximately 4 generations before finding a valid schedule, while lower mutation rates converged more quickly with an average of approximately 2 generations.

This behaviour is expected because higher mutation rates increase exploration by introducing additional changes into the population. While this can improve diversity, it can also disrupt high-quality schedules before they can be refined further. Lower mutation rates allow promising schedules to be preserved and exploited more effectively, resulting in faster convergence.

One unexpected observation was that lower mutation rates appeared to produce slightly more diverse schedules than higher mutation rates. However, the differences were small and not significant enough to draw strong conclusions. A mutation rate of 30% was selected because it provided a balance between maintaining diversity and preserving promising solutions.

### Crossover Rate Tests

Higher crossover rates consistently resulted in faster convergence. The highest crossover rates converged in approximately one generation on average, while the lowest crossover rates required around three generations.

Unlike mutation rate, crossover rate did not appear to significantly affect schedule diversity. Similar scheduling patterns emerged regardless of the crossover probability used. The primary impact of crossover was on the speed at which high-quality solutions were discovered.

A crossover rate of 80% was selected because it consistently produced rapid convergence while maintaining solution quality. A higher crossover rate increases the likelihood that useful portions of successful schedules are combined, improving the algorithm's ability to exploit promising solutions.

### Elite Count Tests

Changing the elite count produced little measurable impact on convergence speed or schedule diversity. All tested elite counts converged within approximately one generation, and the resulting schedules exhibited similar characteristics.

These results suggest that elitism is not a major factor for this particular scheduling problem. Nevertheless, an elite count of 2 was selected as a conservative setting to ensure that high-quality schedules are preserved between generations without significantly reducing population diversity.

## Overall Findings

Across all experiments, the genetic algorithm consistently found valid schedules regardless of parameter settings. Differences between configurations primarily affected convergence speed rather than the ability to find a solution.

The results suggest that the scheduling problem is well suited to a genetic algorithm and does not present a particularly difficult search landscape under the tested constraints. Parameter tuning was therefore most useful for improving computational efficiency and convergence consistency rather than improving final solution quality.

Based on the experimental results, the final parameter settings were:

- Population Size: **50**
- Mutation Rate: **30%**
- Crossover Rate: **80%**
- Elite Count: **2**
- Generation Limit: **100**

These settings provided a balance between convergence speed, solution diversity, computational cost, and reliability.

# How to Run

From the repository root with:
```java
python -m step5_experiments_visualization.visualize
```
