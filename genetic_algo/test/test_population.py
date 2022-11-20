import unittest

from random import seed

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.population import Population
from genetic_algo.classes.routing_solution import RoutingSolution


class PopulationTest(unittest.TestCase):

    def setUp(self) -> None:
        seed(13)
        self.input_params = InputParams(input_file_path='test3.json')

    @staticmethod
    def _print_solution(sol: RoutingSolution):
        print('************************************')
        for layer in sol.genotype.grid:
            for row in layer:
                print(row)
            print('************************************')

    @staticmethod
    def _print_fitness(dictionary_by_fitness):
        print('************************************')
        for fitness, individual_list in dictionary_by_fitness.items():
            print("fitness: " + str(fitness))
        print('************************************')



    def test_initial_population_sanity_check(self):
        population = Population(input_params=self.input_params)
        self._print_solution(sol=population.routing_solutions[0])
        self._print_fitness(population.dictionary_by_fitness)

    def test_crossover_sanity_check(self):
        population = Population(input_params=self.input_params)
        parents = population.routing_solutions[:2]
        child = population._crossover(parents=parents)
        self._print_solution(sol=child)

    def test_select_parents_sanity_check(self):
        population = Population(input_params=self.input_params)
        parents = population._select_parents()
        self._print_solution(parents[0])
        self._print_solution(parents[1])

