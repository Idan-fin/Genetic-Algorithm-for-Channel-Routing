import unittest

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.population import Population
from genetic_algo.classes.routing_solution import RoutingSolution


class PopulationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.input_params = InputParams(input_file_path='test1.json')

    def _print_solution(self, sol: RoutingSolution):
        print(sol.genotype.grid)

    def test_initial_population_sanity_check(self):
        population = Population(input_params=self.input_params)
        for sol in population.routing_solutions:
            self._print_solution(sol=sol)

