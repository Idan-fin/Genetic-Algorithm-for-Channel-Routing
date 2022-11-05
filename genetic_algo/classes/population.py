from typing import List
from random import randrange
from copy import deepcopy

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

    def _select_parents(self) -> List[RoutingSolution]:
        pass

    @staticmethod
    def _make_parents_same_length(parents: List[RoutingSolution]) -> List[RoutingSolution]:

        parent_a, parent_b = parents[0], parents[1]

        num_of_rows_diff = parent_a.genotype.num_of_rows - parent_b.genotype.num_of_rows

        if num_of_rows_diff == 0:
            return parents

        longer, shorter = (parent_a, parent_b) if num_of_rows_diff > 0 else (parent_b, parent_a)

        while shorter.genotype.num_of_rows < longer.genotype.num_of_rows:
            shorter.extend_genotype_num_of_rows_by_one()

        return [longer, shorter]

    def _create_initial_descendant(self, parents: List[RoutingSolution]) -> RoutingSolution:

        parents = [deepcopy(parents[0]), deepcopy(parents[1])]  # don't change the original parents.
        parents = self._make_parents_same_length(parents=parents)

        # TODO: check if we can include column 0 and max_column
        cutting_column_index = randrange(0, parents[0].genotype.num_of_columns)

        child = RoutingSolution(input_params=self.input_params,
                                num_of_rows=parents[0].genotype.num_of_rows)

        child.copy_routing_from_parent(parent=parents[0], cutting_line=cutting_column_index, left_to_line=True)
        child.copy_routing_from_parent(parent=parents[1], cutting_line=cutting_column_index, left_to_line=False)

        return child

    def _crossover(self, parents: List[RoutingSolution]) -> RoutingSolution:
        """
        Make parents crossover by calling create initial descendant.
        Connect free pins with the new solution's connect all pins.
        Try until all pins are connected.
        :param parents: 2 solutions to crossover
        :return: new "child" solution
        """
        new_sol = None
        is_connected = False

        while not is_connected:
            new_sol = self._create_initial_descendant(parents=parents)
            num_of_connect_all_pin_retries = new_sol.genotype.num_of_rows  # see section 4.6
            is_connected = new_sol.connect_all_pins(num_of_retries=num_of_connect_all_pin_retries,
                                                    is_partially_connected=True)

        return new_sol

    def generate_next_generation(self) -> None:
        """
        Create new solutions for "next generation".
        Use the _select_parents and pass them to the _crossover.
        Num of descendants = input_params.max_descendants
        """
        # TODO: verify
        for i in range(self.input_params.max_descendants):
            parents = self._select_parents()
            new_sol = self._crossover(parents=parents)
            self.routing_solutions.append(new_sol)

    def reduction(self) -> None:
        pass

    def get_best(self) -> RoutingSolution:
        pass
