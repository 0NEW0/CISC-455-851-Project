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


if __name__ == "__main__":
    unittest.main()
