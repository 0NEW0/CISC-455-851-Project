# Genetic Operators: Design Decisions

## Scope and Representation

Part 3 implements tournament selection, two crossover strategies, and swap mutation. Chromosomes contain 20 slots with fixed counts: A=4, B=5, C=3, D=3, Free=5. Task-to-day assignments affect fitness; within-day order does not. A late schedule can still be structurally valid.

## Operator Choices

| Component | Decision | Reason and tradeoff |
|---|---|---|
| Selection | Tournament, default size 3; no replacement within a tournament | Controls pressure without depending on the magnitude of fitness gaps. Size 3 is not experimentally optimal. |
| Ties | Random choice among the best participants | Avoids consistently favoring the first equal-score individual. |
| Crossfill | Preserve a segment and fill circularly using remaining counts | Valid by construction, but donor genes may move to different days. |
| Two-point repair | Exchange positional information, then repair excess counts outside the protected segment | Preserves the segment and minimizes count-correction changes, but repair can alter useful assignments. |
| Mutation | One swap between distinct sampled positions | Preserves counts with a localized change. Equal-label and same-day neutral swaps are allowed. |

Crossfill adapts Lecture 4's cut and crossfill: our version uses two cuts, a protected internal segment, circular filling, and repeated labels. It is not the exact one-cut prefix operator shown in class. Repair samples excess occurrences outside the segment and shuffles missing labels; it uses no fitness heuristic. Neither crossover has been established as superior.

Both crossovers share two distinct boundaries from 0 through chromosome length and use [start:end]. A full-length segment is allowed. The second child reverses parent roles.

## Common Guarantees

All outputs are independent lists; inputs remain unchanged even when operations are skipped. Rates are finite real values in [0, 1], excluding booleans. Invalid rates, unknown crossover strategies, and invalid chromosomes raise ValueError before randomness, even at rate zero.

Selection validates the entire population, scores only sampled participants, and maximizes fitness. Tournament size must be an integer between 1 and population size. Full-population validation on each call adds overhead but explicitly rejects invalid individuals outside the tournament.

Crossover owns one probability decision per pair; mutation owns one per chromosome. Zero skips the operation and one always activates it. Intermediate rates activate when random() < rate. No operation is required to improve fitness.

## Shared Structure

Validation was extracted from Part 2 into Shared/chromosome_validation.py without changing its rules. Parts 2 and 3 share it; Part 2 still exposes the imported function. Step folders were renamed to lowercase package names with underscores, enabling standard imports.

Each package has __init__.py, which marks a regular Python package; tests also uses it for discovery compatibility. It does not add paths to Python's search path. No importlib loaders or sys.path modifications remain. Execution instructions are in [NEXT_STEPS.md](NEXT_STEPS.md).

## TDD and Verification

Missing behavior was tested before implementation, followed by implementation and refactoring. Tests for existing behavior passed immediately rather than forcing an artificial failure.

| Area | Test methods |
|---|---:|
| Selection | 10 |
| Crossover | 13 |
| Mutation | 7 |
| Integrated operator pipeline | 1 |
| Total | 31 |

All 31 methods passed on Python 3.13, including exact offspring examples, invalid inputs, independent copies, neutral swaps, cut boundaries, probability thresholds, real fitness, and seeded reproduction. Some methods contain multiple subtests. Integration covers both strategies with seeds 7, 42, and 851. These results verify covered behavior, not full-GA performance or optimality.

## Course References

- Lecture 4, Eight Queens (4-EightQueens.pdf), slide 8: cut and crossfill.
- Lecture 6, Genetic Algorithm (6-GA.pdf), slides 2 and 18-21: representation, crossover bias, and problem-dependent choice.
- Lecture 8, Permutation Representation (8-PermutationRep.pdf), slides 2-7 and 8-13: distinct-element assumptions, mutation, PMX, and edge crossover. Our repeated labels need adaptations.
- Lecture 9, Selection and Population Management (9-SelPop.pdf), slides 15-16: tournament size and sampling.
- Lecture 12, Parameter Setting (12-ParameterSetting.pdf), slides 6-7 and 13: symbolic versus numeric parameters and repeated-run evaluation.
