# Genetic Operators Development Report

## Scope and Responsibilities

Part 3 implements tournament parent selection, two crossover strategies, and swap mutation for the weekly study schedule GA. All operators are implemented and verified by 31 unittest test methods on Python 3.13. Part 4 remains responsible for the complete GA, generations, replacement, elitism, and history. Part 5 remains responsible for experiments and visualization. No full GA performance or optimality claim is made.

## Representation and Shared Validation

Chromosomes contain 20 one-hour slots: A=4, B=5, C=3, D=3, Free=5. Validity means correct length, allowed labels, and exact counts. Deadlines are evaluated through fitness; a late schedule can be valid.

`Shared/chromosome_validation.py` owns the validator extracted from Part 2 without changing its rules. It returns None for valid input and raises ValueError otherwise. Both fitness and operators import it. Part 2 continues to expose the imported validator for compatibility.

The Step directories were renamed to valid Python package names:

- step1_problem_representation
- step2_fitness_function
- step3_genetic_operators
- step4_ga_implementation
- step5_experiments_visualization

Each package has __init__.py. Shared/__init__.py marks Shared as a regular package, and tests/__init__.py supports test discovery. These markers do not add paths to Python's search path. Internal imports are standard dotted imports; there is no importlib loading or sys.path modification. Run module commands from the repository root rather than executing nested files by path.

## Interface Contracts

```python
select_parent(population, fitness_function, random_number_generator, tournament_size=3)
crossover(parent1, parent2, crossover_rate, random_number_generator,
          strategy="count_preserving_crossfill")
mutate(chromosome, mutation_rate, random_number_generator)
```

Every returned chromosome is an independent list. Inputs are preserved, including when an operation is skipped. Gene values are immutable strings, so list copying is sufficient.

### Parent Selection

Validate the entire population before sampling. Require a nonempty population and an integer tournament size from 1 through population size; boolean sizes are rejected. Sample participants without replacement within a tournament. Evaluate only participants, maximize scalar fitness, and break best-score ties randomly. Return a copy of the winner. Separate calls can choose the same parent.

The default size 3 is an initial configuration, not an experimentally established optimum. Smaller populations require an explicit smaller size. Full-population validation on every call adds work proportional to population size and chromosome length. A future optimization must deliberately preserve or revise this contract and tests.

### Crossover

Validate rate, strategy, and both parents before randomness, including at rate zero. Rates are finite real numbers in [0, 1]; booleans, strings, None, NaN, and infinities are rejected with ValueError. Unknown strategies raise ValueError.

A zero rate returns copies without randomness. A rate of one always activates crossover without a probability draw. Intermediate rates activate when random() < crossover_rate. One probability decision applies to the pair. Sample two distinct boundaries from 0 through chromosome length and sort them. Segments are [start:end], with end exclusive. Both children share cuts and reverse parent roles. A full-length segment is allowed and returns parent-equivalent copies.

- count_preserving_crossfill: preserve the selected parent's segment in place. Compute remaining gene counts. Traverse the other parent circularly from end and fill empty positions circularly from end, accepting a label only while its count is still needed. The helper builds one child.
- two_point_repair: use one parent's segment and the other parent's outside positions. For each excess label, randomly sample only the necessary outside occurrences. Shuffle the missing-gene list and replace the selected positions. The copied segment is protected. Already-valid children require no repair randomness. The repair changes the minimum number of positions needed to restore counts and uses no fitness or deadline heuristic.

### Mutation

Validate the rate and chromosome even at zero rate. Rate rules match crossover. The rate is the probability of applying one swap to the entire chromosome, not a per-gene probability. Return a copy even when skipped. At rate one, always apply one swap; intermediate rates use one probability draw. Sample two distinct positions without replacement and swap their values.

Equal-label swaps and different-label swaps within the same day are allowed. The former may leave the chromosome unchanged; the latter preserves the current fitness. No rejection sampling forces a different label, different day, or improved score.

## Design Decisions and Course References

Lecture 6, Genetic Algorithm, slide 2 distinguishes representation-dependent variation from representation-independent selection. Slides 18-21 discuss crossover bias and the need for problem-dependent comparisons. Our task-day assignments matter, while within-day order does not affect the current fitness.

Lecture 4, Eight Queens, slide 8 presents cut and crossfill with one cut, a preserved prefix, and distinct values. count_preserving_crossfill is an adaptation: it uses two boundaries, an internal protected segment, circular filling, and repeated-label counts. It should not be described as the exact lecture operator.

Lecture 8, Permutation Representation, slides 2 and 8-13 assume distinct objects for conventional permutation crossovers. Direct PMX and edge crossover do not fit repeated task labels without adaptation. Slides 3-7 describe permutation mutation, including swap; slides 3-4 support one whole-chromosome mutation decision and a swap.

Lecture 9, Selection and Population Management, slides 15-16 describe tournament selection and the effects of size and replacement. Tournament selection avoids making selection pressure depend on the large magnitude difference between late and on-time fitness values.

Lecture 12, Parameter Setting, slides 6-7 identifies operator choice as a symbolic parameter and rates/tournament size as numeric parameters. Slide 13 motivates multiple runs and quality, speed, success, and robustness measurements. The strategy argument supports that comparison; neither crossover has been established as superior.

Source files: 4-EightQueens.pdf, 6-GA.pdf, 8-PermutationRep.pdf, 9-SelPop.pdf, and 12-ParameterSetting.pdf from the supplied CISC 851 lecture materials.

## TDD Development and Validation Results

Tests were written and executed before implementing missing behavior. Initial failures included absent interfaces, missing explicit validation, first-winner tie handling, and unimplemented active crossover/mutation. Each was followed by the necessary implementation and a passing suite. Tests for behavior already implemented passed immediately; no artificial Red phase was introduced.

Current suite: 31 test methods, some with multiple subtests:

| Area | Methods | Coverage |
|---|---:|---|
| Selection | 10 | Negative fitness, copies, ties, invalid inputs, tournament membership, real fitness, seeded reproduction |
| Crossover | 13 | Exact children for both strategies, protected segments, count repair, missing-label mixtures, no-repair cases, boundary and single-gene segments, rates, invalid inputs, seeded integration |
| Mutation | 7 | Zero and unit rates, exact swapped positions, neutral swaps, invalid inputs, intermediate-rate boundaries, seeded validity and reproduction |
| Full operator pipeline | 1 | Selection -> crossover -> mutation with both strategies, real fitness, input preservation, and seeded reproduction |

Controlled mocks verify exact decisions without flaky statistical assertions. Seeded integration uses seeds 7, 42, and 851 for both crossover strategies. The full pipeline repeats ten parent-pair operations per configuration and compares two identically initialized runs. This is operator integration, not a replacement or generation-management implementation.

Final verification: all 31 methods passed on Python 3.13. The suite was also rerun after final documentation/configuration cleanup. No commits were created during this work.

## Integration Guidelines for Parts 4 and 5

Use one generator per GA run:

```python
import random

from step2_fitness_function.fitness_function import fitness_function
from step3_genetic_operators.genetic_operators import select_parent, crossover, mutate

random_number_generator = random.Random(851)
parent1 = select_parent(population, fitness_function, random_number_generator)
parent2 = select_parent(population, fitness_function, random_number_generator)
child1, child2 = crossover(
    parent1, parent2, 0.8, random_number_generator,
    strategy="count_preserving_crossfill",
)
child1 = mutate(child1, 0.1, random_number_generator)
child2 = mutate(child2, 0.1, random_number_generator)
```

This fragment assumes a valid population already exists; it is not a full GA. Rates 0.8 and 0.1 are illustrative, not tuned recommendations. Do not apply crossover/mutation probabilities again in the GA loop. Use scalar fitness, where larger negative scores are better. Do not assume zero is reachable. Catch ValueError at an application boundary only when a defined recovery or user-message policy exists.

Part 1 still uses global random.shuffle and has not been changed to accept a generator. Passing the run's generator through create_population and create_chromosome remains a proposed integration change. Until then, seeding only operators does not reproduce initialization. The integration tests control initialization directly with their local generator.

Record seeds, configuration, Python version, and code revision. Reproduction assumes compatible software, identical inputs, and the same sequence of random calls. Different crossover strategies consume random draws differently, so sharing a seed does not synchronize all later random choices across strategies.

Part 5 should compare strategies using equivalent starting populations, fixed evaluation/generation budgets, several seeds, and fixed remaining parameters for the initial comparison. Report fitness distributions, on-time success, convergence, meaningful diversity, and repair effects. Report tuned parameter interactions if explored. Within-day permutations can inflate genotype diversity without changing schedule fitness. Instrumentation for repair metrics is not currently exposed by the operator interface and must be added separately if those metrics are collected.

## Execution

Run from the repository root:

```powershell
python -m step1_problem_representation.schedule_data
python -m step2_fitness_function.fitness_function
python -B -m unittest discover -s tests -p "test_*.py" -t . -v
```

VS Code uses unittest discovery from tests, pattern test_*.py, and top-level directory '.'. Refresh the Testing panel after changing files. Old launch paths referencing folders with spaces must be updated.

## Limitations and Remaining Work

The Part 3 operators are complete for the agreed scope. Parts 4 and 5 remain pending. No experiments establish superiority or global optimality. The representation and fitness do not model session continuity, task prerequisites, or within-day preferences. Neutral swaps, unchanged offspring, repeated parent selection, and full-length crossover segments are intentional. A future extension should change contracts and tests explicitly.
