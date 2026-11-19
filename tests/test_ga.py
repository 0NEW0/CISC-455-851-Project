import unittest
from unittest.mock import patch

from Shared.chromosome_validation import validate_chromosome
from step1_problem_representation.schedule_data import DAYS, SLOTS_PER_DAY
from step2_fitness_function.fitness_function import evaluate_fitness
from step4_ga_implementation.genetic_algorithm import run_ga


class TestGeneticAlgorithm(unittest.TestCase):
    def test_history_lengths(self):
        result = run_ga(population_size=20, generations=15, seed=1)
        self.assertEqual(len(result["best_history"]), 16)
        self.assertEqual(len(result["average_history"]), 16)

    def test_best_fitness_never_decreases_with_elitism(self):
        history = run_ga(population_size=20, generations=30, seed=2)["best_history"]
        self.assertTrue(all(b >= a for a, b in zip(history, history[1:])))

    def test_best_chromosome_is_valid(self):
        result = run_ga(population_size=20, generations=20, seed=3)
        validate_chromosome(result["best_chromosome"])

    def test_same_seed_same_result(self):
        first = run_ga(population_size=20, generations=20, seed=7)
        second = run_ga(population_size=20, generations=20, seed=7)
        self.assertEqual(first["best_history"], second["best_history"])
        self.assertEqual(first["best_chromosome"], second["best_chromosome"])
        slots = first["parameters"]["unavailable_slots"]
        self.assertEqual(slots, second["parameters"]["unavailable_slots"])
        self.assertEqual(len(slots), 2)
        self.assertNotEqual(slots[0][0], slots[1][0])
        for day, slot in slots:
            self.assertIn(day, range(len(DAYS)))
            self.assertIn(slot, range(SLOTS_PER_DAY))

    def test_ga_scores_slot_conflicts_and_short_project_sessions(self):
        compliant = [
            "B", "B", "D", "Free",
            "A", "Free", "A", "C",
            "A", "A", "C", "Free",
            "B", "B", "B", "C",
            "D", "D", "Free", "Free",
        ]
        conflicting = compliant.copy()
        for first, second in ((1, 2), (4, 5), (17, 18)):
            conflicting[first], conflicting[second] = conflicting[second], conflicting[first]
        slots = ((1, 1), (4, 2))
        original_score = evaluate_fitness(conflicting)["fitness"]
        adjusted = evaluate_fitness(conflicting, unavailable_slots=slots)
        self.assertEqual(adjusted["unavailable_slot_conflicts"], 2)
        self.assertEqual(adjusted["short_sessions"], 2)
        self.assertEqual(adjusted["fitness"], original_score - 2040)

        with (
            patch("step4_ga_implementation.genetic_algorithm.choose_unavailable_slots", return_value=slots),
            patch("step4_ga_implementation.genetic_algorithm.create_population", return_value=[conflicting, compliant]),
        ):
            settings = dict(population_size=2, generations=1, elite_count=1,
                            tournament_size=2, crossover_rate=0, mutation_rate=0, seed=1)
            baseline = run_ga(**settings, use_constraints=False)
            current = run_ga(**settings)

        self.assertEqual(baseline["best_chromosome"], conflicting)
        self.assertEqual(current["best_chromosome"], compliant)
        self.assertEqual(current["best_fitness"], original_score)
        self.assertEqual(current["best_breakdown"]["unavailable_slot_conflicts"], 0)
        self.assertEqual(current["best_breakdown"]["short_sessions"], 0)

    def test_improves_over_initial_population(self):
        result = run_ga(seed=4)
        self.assertGreater(result["best_fitness"], result["best_history"][0])

    def test_both_crossover_strategies_run(self):
        for strategy in ("count_preserving_crossfill", "two_point_repair"):
            result = run_ga(population_size=20, generations=20, seed=5,
                            crossover_strategy=strategy)
            validate_chromosome(result["best_chromosome"])
            self.assertEqual(result["parameters"]["crossover_strategy"], strategy)

    def test_odd_population_size(self):
        result = run_ga(population_size=21, generations=10, seed=6)
        self.assertEqual(len(result["best_history"]), 11)

    def test_parameters_are_recorded(self):
        parameters = run_ga(population_size=10, generations=3, seed=8)["parameters"]
        self.assertEqual(parameters["seed"], 8)
        self.assertIn("python_version", parameters)

    def test_all_survival_schemes_run_and_stay_valid(self):
        from step4_ga_implementation.genetic_algorithm import SURVIVAL_SCHEMES
        for scheme in SURVIVAL_SCHEMES:
            with self.subTest(scheme=scheme):
                result = run_ga(population_size=20, generations=15, seed=9,
                                survival=scheme)
                validate_chromosome(result["best_chromosome"])
                self.assertEqual(len(result["best_history"]), 16)
                self.assertEqual(result["parameters"]["survival"], scheme)

    def test_best_never_decreases_for_schemes_that_keep_the_best(self):
        for scheme in ("elitist", "mu_plus_lambda", "steady_state"):
            with self.subTest(scheme=scheme):
                history = run_ga(population_size=20, generations=30, seed=10,
                                 survival=scheme)["best_history"]
                self.assertTrue(all(b >= a for a, b in zip(history, history[1:])))

    def test_unknown_survival_scheme_is_rejected(self):
        with self.assertRaises(ValueError):
            run_ga(survival="unknown")

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            run_ga(population_size=1)
        with self.assertRaises(ValueError):
            run_ga(generations=0)
        with self.assertRaises(ValueError):
            run_ga(population_size=10, elite_count=10)
        with self.assertRaises(ValueError):
            run_ga(population_size=10, tournament_size=11)


if __name__ == "__main__":
    unittest.main()
