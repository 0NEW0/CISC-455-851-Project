from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from step5_experiments_visualization import visualize


class TrialAggregationTests(unittest.TestCase):
    def test_means_use_each_distinct_seed_and_keep_the_best_schedule(self):
        base = ["A"] * 4 + ["B"] * 5 + ["C"] * 3 + ["D"] * 3 + ["Free"] * 5
        histories = {1: [-90, -81, -78], 2: [-120, -87, -66], 3: [-90, -87, -75]}
        schedules = {1: base, 2: base[1:] + base[:1], 3: base[2:] + base[:2]}

        def run_trial(*, seed, **settings):
            return {
                "best_history": histories[seed],
                "best_fitness": histories[seed][-1],
                "best_chromosome": schedules[seed],
            }

        for experiment in (visualize.population_test, visualize.mutation_test,
                           visualize.crossover_test, visualize.elite_test):
            with (
                self.subTest(experiment=experiment.__name__),
                patch.object(visualize.ga, "run_ga", side_effect=run_trial) as run_ga,
                patch.object(visualize, "plot_data") as plot,
                patch.object(visualize, "display_schedule") as display,
                redirect_stdout(StringIO()),
            ):
                experiment(generations=2, trials=3)

                self.assertEqual([c.kwargs["seed"] for c in run_ga.call_args_list], [1, 2, 3] * 5)
                self.assertEqual([c.args[1] for c in plot.call_args_list], [[-100, -85, -73]] * 5)
                self.assertEqual([c.args[0] for c in display.call_args_list], [schedules[2]] * 5)
                self.assertEqual(histories[1], [-90, -81, -78])


if __name__ == "__main__":
    unittest.main()
