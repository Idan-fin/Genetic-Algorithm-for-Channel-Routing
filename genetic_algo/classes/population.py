from typing import List

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.routing_solution import RoutingSolution


class Population:

    def __init__(self, input_params: InputParams):
        self.input_params: InputParams = input_params
        self.routing_solutions = self.generate_initial_population()
        self.best_solution = self.get_best()

    def generate_initial_population(self) -> List[RoutingSolution]:
        pass

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
