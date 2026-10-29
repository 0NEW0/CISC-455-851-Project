# Genetic Operators Development Report

## Scope and Status

Tournament selection is implemented. Crossover, mutation, the complete GA, and experiments remain pending. All code, comments, docstrings, and this report are in English.

## Shared Validation and Package Structure

`Shared/chromosome_validation.py` owns `validate_chromosome`. Its logic was extracted unchanged from Part 2. It returns None for a valid chromosome and raises ValueError for incorrect length, unknown genes, or incorrect task counts. Required counts are A=4, B=5, C=3, D=3, Free=5. Late schedules can still be valid.

Parts 2 and 3 use:

```python
from Shared.chromosome_validation import validate_chromosome
```

Part 2 still exposes the imported validator for compatibility with existing callers. Task configuration remains in Part 1.

### Package Names and Imports

The Step folders were renamed to valid Python package names:

- step1_problem_representation
- step2_fitness_function
- step3_genetic_operators
- step4_ga_implementation
- step5_experiments_visualization

Each contains an __init__.py package marker. Shared/__init__.py marks Shared as a regular package; tests/__init__.py supports test discovery. These files contain package docstrings and do not add paths to Python's search path.

Internal dependencies now use normal imports. The validator imports settings from step1_problem_representation.schedule_data. Part 2 imports those settings and display/generation helpers directly. Part 3 imports the shared validator. All importlib loaders and sys.path modifications were removed from project Python files, including tests.

Run from the repository root using module execution:

```powershell
python -m step1_problem_representation.schedule_data
python -m step2_fitness_function.fitness_function
python -m unittest discover -s tests -p "test_*.py" -t . -v
```

Running nested files directly by path is no longer the supported entry point. Future developers should use dotted package imports and python -m from the root. Editor launch configurations and external scripts using old folder paths must be updated. VS Code unittest settings use tests as the start directory and the repository root as the top-level directory.

## Interface Contracts

```python
select_parent(population, fitness_function, random_number_generator, tournament_size=3)
```

The method validates every chromosome before sampling, including individuals outside the tournament. Empty populations and invalid tournament sizes raise ValueError. The size must be an integer from 1 through population size; booleans are rejected.

Participants are sampled without replacement within a tournament. Only participants receive fitness evaluations. Larger scalar scores win, and ties are resolved randomly among the best participants. An independent list copy is returned. Separate calls may select the same individual.

Validating the full population on each call adds work proportional to population size and chromosome length. Any later validation-once optimization must deliberately revise or preserve this contract and its tests.

## Design Decisions

Tournament selection controls pressure through tournament size without depending on the large score-scale difference between late and on-time schedules. Random tie-breaking matters because the fitness ignores within-day order. These are design reasons, not proof of superiority over rank or roulette selection. The default size 3 is an experimental starting point.

Crossover and mutation will control their occurrence probabilities internally. Part 4 must not repeat those probability checks. Their implementations remain pending.

## TDD Development and Validation Results

Tests preceded implementation of missing behavior. Tests for existing behavior passed without unnecessary source changes. The Shared extraction was a behavior-preserving refactoring protected by the suite.

The 10 test methods cover negative scores, independent copies, random ties, empty populations, noninteger sizes, out-of-range sizes, sampled-only selection, invalid chromosomes outside the tournament, integration with the real fitness and random.Random, and identical-seed reproduction. Some methods include multiple subtests.

After extraction, all 10 tests passed on Python 3.13. After package renaming, all 10 tests passed again and the Part 2 example ran through its documented module entry point. Its random score is not a benchmark.

Run from the repository root:

```powershell
python -B -m unittest discover -s tests -p "test_*.py" -t . -v
```

## Integration Guidelines for Parts 4 and 5

- Create one random.Random instance per GA run and pass it to operators. Record the seed, configuration, Python version, and code revision. Reproduction assumes compatible software and the same inputs and call sequence.
- Part 1 still uses global random.shuffle. It has not been changed. Passing the shared generator to create_population and create_chromosome remains a proposed change. Seeding operators alone does not reproduce initial population generation.
- Pass the scalar fitness_function callable, not the detailed evaluation dictionary. Larger negative scores are better. Do not assume fitness zero is reachable.
- Supply an explicit smaller tournament size when population size is below 3.
- Correct invalid inputs rather than silently swallowing ValueError. Catch exceptions at an application boundary only when a defined recovery or user-message policy exists.
- Part 4 owns generations, replacement, elitism, and history. Part 5 should compare multiple seeds and examine fitness, deadline penalties, diversity, and convergence.

## Limitations and Future Improvements

No full GA experiments, optimality claim, or selection-method comparison has been completed. Within-day permutations may have equal fitness. Crossover and mutation still need their own brainstorm and TDD cycles. The report will be updated as development continues.
