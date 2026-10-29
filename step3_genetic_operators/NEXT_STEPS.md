# Integration and Next Steps

Part 3 is implemented and tested. See [REPORT.md](REPORT.md) for design decisions and evidence. Parts 4 and 5 remain to be developed.

## Part 4: Integrate the Operators

```python
select_parent(population, fitness_function, random_number_generator, tournament_size=3)
crossover(parent1, parent2, crossover_rate, random_number_generator,
          strategy="count_preserving_crossfill")
mutate(chromosome, mutation_rate, random_number_generator)
```

Use strategy="count_preserving_crossfill" or strategy="two_point_repair". Pass scalar fitness: larger scores are better, including negative values. Do not use the detailed evaluation dictionary or assume that zero fitness is reachable. For a population below 3, supply a smaller tournament size.

Use one generator per run. This fragment assumes a valid population already exists:

```python
import random
from step2_fitness_function.fitness_function import fitness_function
from step3_genetic_operators.genetic_operators import select_parent, crossover, mutate

random_number_generator = random.Random(851)
parent1 = select_parent(population, fitness_function, random_number_generator)
parent2 = select_parent(population, fitness_function, random_number_generator)
children = crossover(parent1, parent2, 0.8, random_number_generator,
                     strategy="count_preserving_crossfill")
children = [mutate(child, 0.1, random_number_generator) for child in children]
```

Rates 0.8 and 0.1 are illustrative, not tuned recommendations. Operators already apply probabilities; do not repeat those checks in the GA loop. Mutation rate means the chance of one swap per chromosome.

Part 4 must implement generation management, population-size preservation (including odd sizes), replacement, any elitism, stopping conditions, and fitness history. Separate parent calls may choose the same individual. Unchanged offspring and neutral mutations are intentional. Catch ValueError only when there is a defined recovery or user-message policy.

### Reproducible Initialization

Part 1 still uses global random.shuffle. A proposed change is to pass the same generator through create_population and create_chromosome; this is not implemented. Until initialization is controlled, seeding only the operators does not reproduce the full run.

Record seeds, settings, Python version, and code revision. Reproduction assumes compatible software and identical inputs and call sequences. The two crossover strategies consume different random draws, so a shared seed does not synchronize all later choices across strategies.

## Part 5: Compare and Visualize

Compare both crossover strategies with equivalent starting populations, several seeds, fixed budgets, and fixed remaining settings for the first comparison. Then investigate parameter interactions if needed.

Report best-fitness distributions, frequency of on-time solutions, convergence, and diversity. Include generation-versus-fitness plots and the best weekly schedule. Genotype diversity can be inflated by within-day permutations that do not change fitness. Repair-effect metrics require additional instrumentation; the current interface does not expose them.

Do not infer operator superiority from unit tests or one successful run. The model does not include prerequisites, session continuity, or within-day preferences.

## Package Layout and Execution

Step packages are step1_problem_representation, step2_fitness_function, step3_genetic_operators, step4_ga_implementation, and step5_experiments_visualization. Shared validation remains in Shared/chromosome_validation.py. Update external scripts or editor launch paths that use the previous folder names.

Run from the repository root using module execution:

```powershell
python -m step1_problem_representation.schedule_data
python -m step2_fitness_function.fitness_function
python -B -m unittest discover -s tests -p "test_*.py" -t . -v
```

VS Code uses unittest, start directory tests, pattern test_*.py, and top-level directory '.'. Refresh the Testing panel after changes. Run the 31-test suite after integration changes.
