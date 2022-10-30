import unittest

from random import seed

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.population import Population
from genetic_algo.classes.routing_solution import RoutingSolution


class PopulationTest(unittest.TestCase):

    def setUp(self) -> None:
        seed(13)
        self.input_params = InputParams(input_file_path='test3.json')

    def _print_solution(self, sol: RoutingSolution):
        print('************************************')
        for layer in sol.genotype.grid:
            for row in layer:
                print(row)
            print('************************************')
    def test_initial_population_sanity_check(self):
        population = Population(input_params=self.input_params)
        self._print_solution(sol=population.routing_solutions[0])

