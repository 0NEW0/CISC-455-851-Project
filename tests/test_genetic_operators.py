"""Unit tests for genetic operators."""

import random
import unittest
from unittest.mock import Mock


class SelectParentTests(unittest.TestCase):
    def setUp(self):
        self.valid_chromosome = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5

    def test_selects_highest_fitness_when_all_scores_are_negative(self):
        from step3_genetic_operators.genetic_operators import select_parent

        base_chromosome = self.valid_chromosome.copy()
        population = [
            base_chromosome,
            base_chromosome[1:] + base_chromosome[:1],
            base_chromosome[2:] + base_chromosome[:2],
        ]
        scores = {
            tuple(population[0]): -120,
            tuple(population[1]): -65,
            tuple(population[2]): -90,
        }

        def fitness_function(chromosome):
            return scores[tuple(chromosome)]

        random_number_generator = Mock()
        random_number_generator.sample.return_value = population

        selected_parent = select_parent(
            population,
            fitness_function,
            random_number_generator,
            tournament_size=3,
        )

        self.assertEqual(selected_parent, population[1])

    def test_returned_parent_can_change_without_modifying_population(self):
        from step3_genetic_operators.genetic_operators import select_parent

        chromosome = self.valid_chromosome.copy()
        population = [chromosome]
        original_population = [individual.copy() for individual in population]
        random_number_generator = Mock()
        random_number_generator.sample.return_value = population

        selected_parent = select_parent(
            population,
            fitness_function=lambda individual: -65,
            random_number_generator=random_number_generator,
            tournament_size=1,
        )

        self.assertEqual(selected_parent, chromosome)
        self.assertIsNot(selected_parent, chromosome)
        selected_parent[0], selected_parent[-1] = selected_parent[-1], selected_parent[0]
        self.assertEqual(population, original_population)

    def test_breaks_ties_randomly_only_among_highest_fitness_participants(self):
        from step3_genetic_operators.genetic_operators import select_parent

        base_chromosome = self.valid_chromosome.copy()
        population = [
            base_chromosome,
            base_chromosome[1:] + base_chromosome[:1],
            base_chromosome[2:] + base_chromosome[:2],
        ]
        scores = {
            tuple(population[0]): -65,
            tuple(population[1]): -120,
            tuple(population[2]): -65,
        }
        random_number_generator = Mock()
        random_number_generator.sample.return_value = population
        random_number_generator.choice.side_effect = lambda candidates: candidates[-1]

        selected_parent = select_parent(
            population,
            fitness_function=lambda chromosome: scores[tuple(chromosome)],
            random_number_generator=random_number_generator,
            tournament_size=3,
        )

        self.assertEqual(selected_parent, population[2])
        random_number_generator.choice.assert_called_once_with(
            [population[0], population[2]]
        )

    def test_rejects_empty_population_before_sampling_or_evaluation(self):
        from step3_genetic_operators.genetic_operators import select_parent

        random_number_generator = Mock()
        random_number_generator.sample.return_value = []
        fitness_function = Mock()

        with self.assertRaisesRegex(ValueError, "Population must not be empty"):
            select_parent(
                [],
                fitness_function,
                random_number_generator,
            )

        random_number_generator.sample.assert_not_called()
        fitness_function.assert_not_called()

    def test_rejects_non_integer_tournament_size(self):
        from step3_genetic_operators.genetic_operators import select_parent

        chromosome = self.valid_chromosome.copy()
        population = [chromosome]
        for invalid_size in (1.0, "1", None, True, False):
            with self.subTest(tournament_size=invalid_size):
                random_number_generator = Mock()
                random_number_generator.sample.return_value = population
                fitness_function = Mock(return_value=-65)

                with self.assertRaisesRegex(ValueError, "Tournament size must be an integer"):
                    select_parent(
                        population,
                        fitness_function,
                        random_number_generator,
                        tournament_size=invalid_size,
                    )

                random_number_generator.sample.assert_not_called()
                fitness_function.assert_not_called()

    def test_rejects_tournament_size_outside_population_bounds(self):
        from step3_genetic_operators.genetic_operators import select_parent

        chromosome = self.valid_chromosome.copy()
        population = [chromosome]
        for invalid_size in (0, -1, 2):
            with self.subTest(tournament_size=invalid_size):
                random_number_generator = Mock()
                random_number_generator.sample.return_value = population
                fitness_function = Mock(return_value=-65)

                with self.assertRaisesRegex(
                    ValueError, "Tournament size must be between 1 and population size"
                ):
                    select_parent(
                        population,
                        fitness_function,
                        random_number_generator,
                        tournament_size=invalid_size,
                    )

                random_number_generator.sample.assert_not_called()
                fitness_function.assert_not_called()

    def test_selects_only_from_sampled_tournament_participants(self):
        from step3_genetic_operators.genetic_operators import select_parent

        base_chromosome = self.valid_chromosome.copy()
        population = [
            base_chromosome,
            base_chromosome[1:] + base_chromosome[:1],
            base_chromosome[2:] + base_chromosome[:2],
        ]
        scores = {
            tuple(population[0]): -10,
            tuple(population[1]): -90,
            tuple(population[2]): -65,
        }
        evaluated_individuals = []

        def fitness_function(chromosome):
            evaluated_individuals.append(chromosome)
            return scores[tuple(chromosome)]

        random_number_generator = Mock()
        participants = [population[1], population[2]]
        random_number_generator.sample.return_value = participants

        selected_parent = select_parent(
            population,
            fitness_function,
            random_number_generator,
            tournament_size=2,
        )

        self.assertEqual(selected_parent, population[2])
        random_number_generator.sample.assert_called_once_with(population, 2)
        self.assertCountEqual(evaluated_individuals, participants)

    def test_rejects_invalid_chromosomes_even_outside_tournament(self):
        from step3_genetic_operators.genetic_operators import select_parent

        valid = self.valid_chromosome.copy()
        invalid_chromosomes = {
            "wrong_length": valid[:-1],
            "unknown_gene": ["Unknown"] + valid[1:],
            "wrong_counts": ["B"] + valid[1:],
        }
        for case, invalid in invalid_chromosomes.items():
            with self.subTest(case=case):
                generator = Mock()
                generator.sample.return_value = [valid]
                fitness_function = Mock(return_value=-65)

                with self.assertRaises(ValueError):
                    select_parent([valid, invalid], fitness_function, generator, 1)

                generator.sample.assert_not_called()
                fitness_function.assert_not_called()

    def test_integrates_with_real_fitness_and_seeded_generator(self):
        from step3_genetic_operators.genetic_operators import select_parent

        import step2_fitness_function.fitness_function as fitness_module

        base = self.valid_chromosome.copy()
        population = [base[offset:] + base[:offset] for offset in range(6)]
        original_population = [individual.copy() for individual in population]
        expected_score = max(map(fitness_module.fitness_function, population))

        selected = select_parent(
            population, fitness_module.fitness_function, random.Random(42),
            tournament_size=len(population),
        )

        self.assertEqual(fitness_module.fitness_function(selected), expected_score)
        fitness_module.validate_chromosome(selected)
        self.assertTrue(all(selected is not individual for individual in population))
        self.assertEqual(population, original_population)

    def test_same_seed_reproduces_selection_sequence(self):
        from step3_genetic_operators.genetic_operators import select_parent

        base = self.valid_chromosome.copy()
        population = [base[offset:] + base[:offset] for offset in range(6)]
        first_generator = random.Random(42)
        second_generator = random.Random(42)

        def fitness_function(chromosome):
            return -65

        first_sequence = [
            select_parent(population, fitness_function, first_generator)
            for _ in range(10)
        ]
        second_sequence = [
            select_parent(population, fitness_function, second_generator)
            for _ in range(10)
        ]

        self.assertEqual(first_sequence, second_sequence)


class CrossoverTests(unittest.TestCase):
    def test_zero_rate_returns_independent_parent_copies_for_both_strategies(self):
        from step3_genetic_operators.genetic_operators import crossover

        base = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        for strategy in ("count_preserving_crossfill", "two_point_repair"):
            with self.subTest(strategy=strategy):
                parent1 = base.copy()
                parent2 = base[2:] + base[:2]
                original_parent1 = parent1.copy()
                original_parent2 = parent2.copy()
                generator = Mock()

                child1, child2 = crossover(
                    parent1, parent2, crossover_rate=0,
                    random_number_generator=generator, strategy=strategy,
                )

                self.assertEqual(child1, parent1)
                self.assertEqual(child2, parent2)
                self.assertIsNot(child1, parent1)
                self.assertIsNot(child2, parent2)
                self.assertIsNot(child1, child2)
                child1[0], child1[-1] = child1[-1], child1[0]
                child2[0], child2[-1] = child2[-1], child2[0]
                self.assertEqual(parent1, original_parent1)
                self.assertEqual(parent2, original_parent2)
                generator.sample.assert_not_called()


    def test_rejects_invalid_crossover_rates_before_randomness(self):
        from step3_genetic_operators.genetic_operators import crossover

        parent = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        invalid_rates = (-0.1, 1.1, "0.5", None, True, False,
                         float("nan"), float("inf"), -float("inf"))
        for strategy in ("count_preserving_crossfill", "two_point_repair"):
            for rate in invalid_rates:
                with self.subTest(strategy=strategy, rate=rate):
                    generator = Mock()
                    with self.assertRaisesRegex(ValueError, "Crossover rate"):
                        crossover(parent, parent.copy(), rate, generator, strategy)
                    self.assertEqual(generator.mock_calls, [])

    def test_rejects_unknown_strategy_even_at_zero_rate(self):
        from step3_genetic_operators.genetic_operators import crossover

        parent = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        for strategy in ("unknown", "", None, [], {}):
            with self.subTest(strategy=strategy):
                generator = Mock()
                with self.assertRaisesRegex(ValueError, "Unknown crossover strategy"):
                    crossover(parent, parent.copy(), 0, generator, strategy)
                self.assertEqual(generator.mock_calls, [])

    def test_rejects_invalid_parent_in_either_position_even_at_zero_rate(self):
        from step3_genetic_operators.genetic_operators import crossover

        valid = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        invalid_parents = (valid[:-1], ["Unknown"] + valid[1:], ["B"] + valid[1:])
        for strategy in ("count_preserving_crossfill", "two_point_repair"):
            for invalid in invalid_parents:
                for invalid_position in (0, 1):
                    with self.subTest(strategy=strategy, invalid=invalid,
                                      position=invalid_position):
                        parents = [valid.copy(), valid.copy()]
                        parents[invalid_position] = invalid
                        originals = [parent.copy() for parent in parents]
                        generator = Mock()
                        with self.assertRaises(ValueError):
                            crossover(*parents, 0, generator, strategy)
                        self.assertEqual(generator.mock_calls, [])
                        self.assertEqual(parents, originals)


    def test_count_preserving_crossfill_matches_fixed_cut_example(self):
        from Shared.chromosome_validation import validate_chromosome
        from step3_genetic_operators.genetic_operators import crossover

        parent1 = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        parent2 = list(reversed(parent1))
        originals = [parent1.copy(), parent2.copy()]
        generator = Mock()
        generator.sample.return_value = [9, 4]
        # Cuts [4:9] preserve five B genes in child 1 and Free,D,D,D,C in child 2.
        # Circular donor traversal starts at index 9; saturated counts are skipped.
        expected_child1 = (
            ["D", "D", "D", "C"] + ["B"] * 5
            + ["C", "C"] + ["A"] * 4 + ["Free"] * 5
        )
        expected_child2 = (
            ["B"] * 4 + ["Free", "D", "D", "D", "C"]
            + ["C", "C"] + ["Free"] * 4 + ["A"] * 4 + ["B"]
        )

        child1, child2 = crossover(
            parent1, parent2, crossover_rate=1,
            random_number_generator=generator,
            strategy="count_preserving_crossfill",
        )

        self.assertEqual(child1, expected_child1)
        self.assertEqual(child2, expected_child2)
        self.assertEqual(child1[4:9], parent1[4:9])
        self.assertEqual(child2[4:9], parent2[4:9])
        validate_chromosome(child1)
        validate_chromosome(child2)
        self.assertEqual([parent1, parent2], originals)
        generator.sample.assert_called_once_with(range(21), 2)
        self.assertIsNot(child1, child2)
        for child in (child1, child2):
            for parent in (parent1, parent2):
                self.assertIsNot(child, parent)


    def test_crossfill_handles_boundary_and_single_gene_segments(self):
        from Shared.chromosome_validation import validate_chromosome
        from step3_genetic_operators.genetic_operators import crossover

        parent1 = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        parent2 = list(reversed(parent1))
        originals = [parent1.copy(), parent2.copy()]
        for start, end in ((0, 4), (15, 20), (0, 20), (0, 1), (19, 20)):
            with self.subTest(start=start, end=end):
                generator = Mock()
                generator.sample.return_value = [start, end]

                children = crossover(parent1, parent2, 1, generator)

                self.assertIsNot(children[0], children[1])
                for child, segment_parent in zip(children, (parent1, parent2)):
                    validate_chromosome(child)
                    self.assertEqual(child[start:end], segment_parent[start:end])
                    for parent in (parent1, parent2):
                        self.assertIsNot(child, parent)
                    if start == 0 and end == 20:
                        self.assertEqual(child, segment_parent)
                self.assertEqual([parent1, parent2], originals)
                generator.sample.assert_called_once_with(range(21), 2)
                generator.random.assert_not_called()

    def test_intermediate_rate_skips_at_or_above_threshold(self):
        from step3_genetic_operators.genetic_operators import crossover

        parent1 = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        parent2 = list(reversed(parent1))
        for strategy in ("count_preserving_crossfill", "two_point_repair"):
            for draw in (0.5, 0.9):
                with self.subTest(strategy=strategy, draw=draw):
                    generator = Mock()
                    generator.random.return_value = draw

                    child1, child2 = crossover(parent1, parent2, 0.5, generator, strategy)

                    self.assertEqual(child1, parent1)
                    self.assertEqual(child2, parent2)
                    self.assertIsNot(child1, parent1)
                    self.assertIsNot(child2, parent2)
                    self.assertIsNot(child1, child2)
                    generator.random.assert_called_once_with()
                    generator.sample.assert_not_called()

    def test_intermediate_rate_activates_crossfill_below_threshold(self):
        from step3_genetic_operators.genetic_operators import crossover

        parent1 = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        parent2 = list(reversed(parent1))
        generator = Mock()
        generator.random.return_value = 0.49
        generator.sample.return_value = [0, 20]

        child1, child2 = crossover(parent1, parent2, 0.5, generator)

        self.assertEqual(child1, parent1)
        self.assertEqual(child2, parent2)
        self.assertIsNot(child1, parent1)
        self.assertIsNot(child2, parent2)
        generator.random.assert_called_once_with()
        generator.sample.assert_called_once_with(range(21), 2)


    def test_two_point_repair_corrects_counts_without_changing_copied_segments(self):
        from Shared.chromosome_validation import validate_chromosome
        from step3_genetic_operators.genetic_operators import crossover

        parent1 = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        parent2 = parent1.copy()
        parent2[0], parent2[4] = parent2[4], parent2[0]
        originals = [parent1.copy(), parent2.copy()]
        # Copy [0:1]. Raw child 1 has an extra A; raw child 2 has an extra B.
        raw_child1 = parent2.copy()
        raw_child1[0] = parent1[0]
        raw_child2 = parent1.copy()
        raw_child2[0] = parent2[0]
        for raw_child in (raw_child1, raw_child2):
            with self.assertRaises(ValueError):
                validate_chromosome(raw_child)
        generator = Mock()
        # Cut boundaries, selected excess-A position, selected excess-B position.
        generator.sample.side_effect = [[0, 1], [4], [8]]
        generator.shuffle.side_effect = lambda genes: genes.reverse()
        expected_child2 = parent1.copy()
        expected_child2[0] = "B"
        expected_child2[8] = "A"

        child1, child2 = crossover(
            parent1, parent2, 1, generator, strategy="two_point_repair",
        )

        self.assertEqual(child1, parent1)
        self.assertEqual(child2, expected_child2)
        for child, segment_parent in zip((child1, child2), (parent1, parent2)):
            validate_chromosome(child)
            self.assertEqual(child[0:1], segment_parent[0:1])
            for parent in (parent1, parent2):
                self.assertIsNot(child, parent)
        self.assertEqual([parent1, parent2], originals)
        self.assertIsNot(child1, child2)
        self.assertEqual(
            [i for i in range(20) if child1[i] != raw_child1[i]], [4]
        )
        self.assertEqual(
            [i for i in range(20) if child2[i] != raw_child2[i]], [8]
        )


    def test_two_point_repair_handles_multiple_missing_gene_types(self):
        from Shared.chromosome_validation import validate_chromosome
        from step3_genetic_operators.genetic_operators import crossover

        parent1 = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        parent2 = list(reversed(parent1))
        originals = [parent1.copy(), parent2.copy()]
        generator = Mock()
        generator.sample.side_effect = [
            [4, 9], [15, 14, 13, 12, 11], [11], [14, 13, 12], [19],
        ]
        shuffled_inputs = []

        def reverse_missing_genes(genes):
            shuffled_inputs.append(genes.copy())
            genes.reverse()

        generator.shuffle.side_effect = reverse_missing_genes
        expected_child1 = (
            ["Free"] * 4 + ["B"] * 5 + ["C"] * 3
            + ["D"] * 3 + ["Free"] + ["A"] * 4
        )
        expected_child2 = (
            ["A"] * 4 + ["Free"] + ["D"] * 3 + ["C"] * 3
            + ["B"] * 4 + ["Free"] * 4 + ["B"]
        )

        children = crossover(parent1, parent2, 1, generator, "two_point_repair")

        self.assertEqual(children, (expected_child1, expected_child2))
        self.assertEqual(shuffled_inputs, [["C", "D", "D", "D", "Free"], ["B"] * 5])
        for child, segment_parent, outside_parent in zip(
            children, (parent1, parent2), (parent2, parent1)
        ):
            validate_chromosome(child)
            self.assertEqual(child[4:9], segment_parent[4:9])
            raw = outside_parent.copy()
            raw[4:9] = segment_parent[4:9]
            self.assertEqual(sum(a != b for a, b in zip(child, raw)), 5)
        self.assertEqual([parent1, parent2], originals)

    def test_two_point_repair_leaves_already_valid_offspring_unchanged(self):
        from step3_genetic_operators.genetic_operators import crossover

        parent1 = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        parent2 = parent1.copy()
        parent2[0], parent2[4] = parent2[4], parent2[0]
        generator = Mock()
        generator.sample.return_value = [0, 5]
        # Both segments have the same counts, so exchanging them needs no repair.
        children = crossover(parent1, parent2, 1, generator, "two_point_repair")

        self.assertEqual(children, (parent1, parent2))
        generator.sample.assert_called_once_with(range(21), 2)
        generator.shuffle.assert_not_called()
        for child in children:
            for parent in (parent1, parent2):
                self.assertIsNot(child, parent)

    def test_two_point_repair_handles_boundary_and_single_gene_segments(self):
        from Shared.chromosome_validation import validate_chromosome
        from step3_genetic_operators.genetic_operators import crossover

        parent1 = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        parent2 = list(reversed(parent1))
        originals = [parent1.copy(), parent2.copy()]
        for start, end in ((0, 4), (15, 20), (0, 20), (0, 1), (19, 20)):
            with self.subTest(start=start, end=end):
                def sample(population, size):
                    if isinstance(population, range):
                        return [start, end]
                    return population[:size]

                generator = Mock()
                generator.sample.side_effect = sample
                generator.shuffle.side_effect = lambda genes: genes.reverse()
                children = crossover(parent1, parent2, 1, generator, "two_point_repair")

                self.assertIsNot(children[0], children[1])
                for child, parent in zip(children, (parent1, parent2)):
                    validate_chromosome(child)
                    self.assertEqual(child[start:end], parent[start:end])
                    for original in (parent1, parent2):
                        self.assertIsNot(child, original)
                    if start == 0 and end == 20:
                        self.assertEqual(child, parent)
                if start == 0 and end == 20:
                    generator.shuffle.assert_not_called()
                    generator.sample.assert_called_once_with(range(21), 2)
                self.assertEqual([parent1, parent2], originals)

    def test_both_strategies_integrate_with_seeded_randomness_and_real_fitness(self):
        from Shared.chromosome_validation import validate_chromosome
        from step2_fitness_function.fitness_function import fitness_function
        from step3_genetic_operators.genetic_operators import crossover

        base = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        for strategy in ("count_preserving_crossfill", "two_point_repair"):
            for seed in (7, 42, 851):
                with self.subTest(strategy=strategy, seed=seed):
                    setup_generator = random.Random(seed)
                    parent1, parent2 = base.copy(), base.copy()
                    setup_generator.shuffle(parent1)
                    setup_generator.shuffle(parent2)
                    originals = [parent1.copy(), parent2.copy()]
                    first_generator = random.Random(seed)
                    second_generator = random.Random(seed)
                    for _ in range(20):
                        first = crossover(parent1, parent2, 0.8, first_generator, strategy)
                        second = crossover(parent1, parent2, 0.8, second_generator, strategy)
                        self.assertEqual(first, second)
                        self.assertIsNot(first[0], first[1])
                        for child in first:
                            validate_chromosome(child)
                            self.assertIsInstance(fitness_function(child), (int, float))
                            for parent in (parent1, parent2):
                                self.assertIsNot(child, parent)
                        self.assertEqual([parent1, parent2], originals)


class MutationTests(unittest.TestCase):
    def test_zero_rate_returns_independent_copy_without_randomness(self):
        from step3_genetic_operators.genetic_operators import mutate

        chromosome = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        original = chromosome.copy()
        generator = Mock()

        mutated = mutate(chromosome, 0, generator)

        self.assertEqual(mutated, chromosome)
        self.assertIsNot(mutated, chromosome)
        mutated[0], mutated[-1] = mutated[-1], mutated[0]
        self.assertEqual(chromosome, original)
        self.assertEqual(generator.mock_calls, [])


    def test_rejects_invalid_mutation_rates_before_randomness(self):
        from step3_genetic_operators.genetic_operators import mutate

        chromosome = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        for rate in (-0.1, 1.1, "0.5", None, True, False,
                     float("nan"), float("inf"), -float("inf")):
            with self.subTest(rate=rate):
                generator = Mock()
                with self.assertRaisesRegex(ValueError, "Mutation rate"):
                    mutate(chromosome, rate, generator)
                self.assertEqual(generator.mock_calls, [])

    def test_rejects_invalid_chromosomes_even_at_zero_rate(self):
        from step3_genetic_operators.genetic_operators import mutate

        valid = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        for chromosome in (valid[:-1], ["Unknown"] + valid[1:], ["B"] + valid[1:]):
            with self.subTest(chromosome=chromosome):
                original = chromosome.copy()
                generator = Mock()
                with self.assertRaises(ValueError):
                    mutate(chromosome, 0, generator)
                self.assertEqual(chromosome, original)
                self.assertEqual(generator.mock_calls, [])

    def test_rate_one_swaps_exactly_the_two_sampled_positions(self):
        from Shared.chromosome_validation import validate_chromosome
        from step3_genetic_operators.genetic_operators import mutate

        chromosome = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        original = chromosome.copy()
        expected = ["Free"] + chromosome[1:19] + ["A"]
        generator = Mock()
        generator.sample.return_value = [0, 19]

        mutated = mutate(chromosome, 1, generator)

        self.assertEqual(mutated, expected)
        validate_chromosome(mutated)
        self.assertIsNot(mutated, chromosome)
        self.assertEqual(chromosome, original)
        generator.sample.assert_called_once_with(range(20), 2)
        generator.random.assert_not_called()

    def test_allows_equal_gene_and_same_day_neutral_swaps(self):
        from step2_fitness_function.fitness_function import fitness_function
        from step3_genetic_operators.genetic_operators import mutate

        chromosome = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        chromosome[1], chromosome[4] = chromosome[4], chromosome[1]
        original = chromosome.copy()
        for positions in ([0, 2], [0, 1]):
            with self.subTest(positions=positions):
                generator = Mock()
                generator.sample.return_value = positions
                expected = chromosome.copy()
                first, second = positions
                expected[first], expected[second] = expected[second], expected[first]

                mutated = mutate(chromosome, 1, generator)

                self.assertEqual(mutated, expected)
                self.assertIsNot(mutated, chromosome)
                self.assertEqual(fitness_function(mutated), fitness_function(chromosome))
                self.assertEqual(chromosome, original)
                generator.sample.assert_called_once_with(range(20), 2)

    def test_intermediate_rate_uses_one_probability_draw(self):
        from step3_genetic_operators.genetic_operators import mutate

        chromosome = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        for draw, should_swap in ((0.49, True), (0.5, False), (0.9, False)):
            with self.subTest(draw=draw):
                generator = Mock()
                generator.random.return_value = draw
                generator.sample.return_value = [0, 19]
                expected = chromosome.copy()
                if should_swap:
                    expected[0], expected[19] = expected[19], expected[0]

                mutated = mutate(chromosome, 0.5, generator)

                self.assertEqual(mutated, expected)
                self.assertIsNot(mutated, chromosome)
                generator.random.assert_called_once_with()
                if should_swap:
                    generator.sample.assert_called_once_with(range(20), 2)
                else:
                    generator.sample.assert_not_called()

    def test_seeded_mutation_preserves_validity_and_reproduces_sequence(self):
        from Shared.chromosome_validation import validate_chromosome
        from step3_genetic_operators.genetic_operators import mutate

        original = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        first, second = original.copy(), original.copy()
        first_generator, second_generator = random.Random(851), random.Random(851)
        for _ in range(30):
            previous = first
            previous_snapshot = previous.copy()
            first = mutate(first, 0.7, first_generator)
            second = mutate(second, 0.7, second_generator)
            validate_chromosome(first)
            self.assertEqual(first, second)
            self.assertIsNot(first, previous)
            self.assertEqual(previous, previous_snapshot)


class GeneticOperatorsIntegrationTests(unittest.TestCase):
    def test_selection_crossover_mutation_pipeline_for_both_strategies(self):
        from Shared.chromosome_validation import validate_chromosome
        from step2_fitness_function.fitness_function import fitness_function
        from step3_genetic_operators.genetic_operators import select_parent, crossover, mutate

        base = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        for strategy in ("count_preserving_crossfill", "two_point_repair"):
            for seed in (7, 42, 851):
                with self.subTest(strategy=strategy, seed=seed):
                    def run_pipeline():
                        generator = random.Random(seed)
                        population = [base.copy() for _ in range(6)]
                        for chromosome in population:
                            generator.shuffle(chromosome)
                        original_population = [chromosome.copy() for chromosome in population]
                        results = []
                        for _ in range(10):
                            parent1 = select_parent(population, fitness_function, generator)
                            parent2 = select_parent(population, fitness_function, generator)
                            parent_snapshots = [parent1.copy(), parent2.copy()]
                            children = crossover(parent1, parent2, 0.8, generator, strategy)
                            for child in children:
                                child_snapshot = child.copy()
                                mutated = mutate(child, 0.5, generator)
                                validate_chromosome(mutated)
                                self.assertIsInstance(fitness_function(mutated), (int, float))
                                self.assertIsNot(mutated, child)
                                self.assertEqual(child, child_snapshot)
                                for original in population + [parent1, parent2]:
                                    self.assertIsNot(mutated, original)
                                results.append(mutated)
                            self.assertEqual([parent1, parent2], parent_snapshots)
                        self.assertEqual(population, original_population)
                        return results

                    self.assertEqual(run_pipeline(), run_pipeline())


if __name__ == "__main__":
    unittest.main()
