import unittest

from random import seed

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.population import Population
from genetic_algo.classes.routing_solution import RoutingSolution
from genetic_algo.classes.genetic_algorithm import GeneticAlgorithm


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        seed(13)
        self.input_params = InputParams(input_file_path='test3.json')

    def test_something(self):
        pass

    @staticmethod
    def _print_solution(sol: RoutingSolution):
        print('************************************')
        for layer in sol.genotype.grid:
            for row in layer:
                print(row)
            print('************************************')

    def test_sanity_check(self):
        genetic_algorithm = GeneticAlgorithm(input_params=self.input_params)
        genetic_algorithm.run()
        self._print_solution(genetic_algorithm.population.best_solution)


if __name__ == '__main__':
    unittest.main()
