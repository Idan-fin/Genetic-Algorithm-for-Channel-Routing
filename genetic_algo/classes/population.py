from typing import List
import collections
from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.routing_solution import RoutingSolution


class Population:

    def __init__(self, input_params: InputParams):
        self.input_params: InputParams = input_params
        self.routing_solutions = self._generate_initial_population()
        self.best_solution = self.get_best()

    def _generate_initial_population(self) -> List[RoutingSolution]:
        """
        Create num of routing solutions according to the given input.
        For each iteration, try to create new solution and connect all pins.
        If RoutingSolution.connect_all_pins failed, create new RoutingSolution and try again until succeed.
        :return: initial population.
        """
        initial_population = []

        for i in range(self.input_params.population_size):

            solution_created_successfully = False
            while not solution_created_successfully:
                next_solution = RoutingSolution(input_params=self.input_params)
                solution_created_successfully = next_solution.connect_all_pins()

                if solution_created_successfully:
                    initial_population.append(next_solution)

        return initial_population

    def _create_fitness_dictionary(self):
        dictionary = dict()
        for individual in self.routing_solutions:
            if dictionary[individual.calc_fitness_func1()]:
                dictionary[individual.calc_fitness_func1()].append(individual)
            else:
                dictionary[individual.calc_fitness_func1()] = [individual]

        

    def _select_parents(self) -> List[RoutingSolution]:
        pass

    def _crossover(self, parents: List[RoutingSolution]) -> List[RoutingSolution]:
        pass

    def generate_next_generation(self) -> None:
        pass

    def reduction(self) -> None:
        pass

    def get_best(self) -> RoutingSolution:
        pass
