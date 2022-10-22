from typing import List, Optional
from random import randrange

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

    def _copy_routing_from_parent(self,
                                  child: RoutingSolution,
                                  parent: RoutingSolution,
                                  cutting_line: int,
                                  left_to_line: bool):
        # TODO: implement
        pass

    def _create_initial_descendant(self, parents: List[RoutingSolution]) -> RoutingSolution:

        # TODO: make both parents copies and extend the "shorter" parent
        #       a.k.a make both parents with the same num of rows
        cutting_column_index = randrange(0, parents[0].genotype.num_of_columns)
        child = RoutingSolution(input_params=self.input_params)
        self._copy_routing_from_parent(child=child, parent=parents[0], cutting_line=cutting_column_index,
                                       left_to_line=True)
        self._copy_routing_from_parent(child=child, parent=parents[1], cutting_line=cutting_column_index,
                                       left_to_line=False)

        return child

    def _crossover(self, parents: List[RoutingSolution]) -> RoutingSolution:
        """
        Make parents crossover by calling create initial descendant.
        Connect free pins with the new solution's connect all pins.
        Try until all pins are connected.
        :param parents: 2 solutions to crossover
        :return: new "child" solution
        """
        new_sol = self._create_initial_descendant(parents=parents)
        num_of_connect_all_pin_retries = new_sol.genotype.num_of_rows  # see section 4.6
        # TODO: fix connect_all_pins to get initial connected pins
        is_connected = new_sol.connect_all_pins(num_of_retries=num_of_connect_all_pin_retries)

        while not is_connected:
            new_sol = self._create_initial_descendant(parents=parents)
            num_of_connect_all_pin_retries = new_sol.genotype.num_of_rows  # see section 4.6
            is_connected = new_sol.connect_all_pins(num_of_retries=num_of_connect_all_pin_retries)

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
