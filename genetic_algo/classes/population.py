from typing import List
import collections
from random import randrange
from copy import deepcopy
from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.routing_solution import RoutingSolution
from genetic_algo.classes.genotype import Genotype
import random
from collections import OrderedDict


class Population:

    def __init__(self, input_params: InputParams):
        self.input_params: InputParams = input_params
        self.routing_solutions = self._generate_initial_population()
        self.dictionary_by_fitness = self._create_fitness_dictionary()
        self.best_solution = self._get_dictionary_best()

    def _generate_initial_population(self) -> List[RoutingSolution]:
        """
        Create num of routing solutions according to the given input.
        For each iteration, try to create new solution and connect all pins.
        If RoutingSolution.connect_all_pins failed, create new RoutingSolution and try again until succeed.
        :return: initial population.
        """
        initial_population = []

        for i in range(self.input_params.population_size):
            print("sol: " + str(i) + "\n")
            solution_created_successfully = False
            while not solution_created_successfully:
                next_solution = RoutingSolution(input_params=self.input_params)
                solution_created_successfully = next_solution.connect_all_pins()

                if solution_created_successfully:
                    initial_population.append(next_solution)

        return initial_population

    @staticmethod
    def _calc_fitness_func2(individual: RoutingSolution):
        return individual.calc_fitness_func2()

    @staticmethod
    def _add_to_dictionary(dictionary, key, val):
        if key in dictionary:
            dictionary[key].append(val)
        else:
            dictionary[key] = [val]

    @staticmethod
    def _calculate_f_p_i(individual_i: RoutingSolution):
        return individual_i.calc_fitness_func1()

    @staticmethod
    def _calculate_f_p_j(individual_j: RoutingSolution,
                         individual_j_plus_1_fitness: RoutingSolution, size_of_list):
        return individual_j.calc_fitness_func1() - \
               ((individual_j_plus_1_fitness - individual_j.calc_fitness_func1()) / size_of_list)

    @staticmethod
    def _calculate_f_p_x(individual_x: RoutingSolution,
                         individual_i: RoutingSolution, individual_j: RoutingSolution, f_p_i, f_p_j, f_2_p_i, f_2_p_j):
        delta_f = f_p_j - f_p_i
        delta_f_2 = f_2_p_i - f_2_p_j
        if delta_f_2 == 0:
            return f_p_j
        return f_p_j - (delta_f * (f_2_p_j - individual_x.calc_fitness_func2())) / delta_f_2

    def _add_fitness_group_to_dictionary(self, dictionary_by_fitness, individual_list, p_j_plus_1_fitness):
        iterator = 0
        for individual in individual_list:
            if iterator == 0:
                p_i = individual
                p_i_fitness = self._calculate_f_p_i(p_i)
                self._add_to_dictionary(dictionary_by_fitness, p_i_fitness,
                                        p_i)
                if len(individual_list) > 1:
                    p_j = individual_list[len(individual_list) - 1]
                    p_j_fitness = self._calculate_f_p_j(p_j, p_j_plus_1_fitness, len(individual_list))
                    self._add_to_dictionary(dictionary_by_fitness, p_j_fitness, p_j)
            else:
                if len(individual_list) > 2:
                    p_x = individual
                    p_x_fitness = self._calculate_f_p_x(p_x, p_i, p_j, p_i_fitness,
                                                        p_j_fitness, p_i.calc_fitness_func2(),
                                                        p_j.calc_fitness_func2())
                    self._add_to_dictionary(dictionary_by_fitness, p_x_fitness,
                                            p_x)
            iterator += 1

    def _create_fitness_dictionary(self):
        dictionary_by_fitness_function1 = OrderedDict()
        for individual in self.routing_solutions:
            self._add_to_dictionary(dictionary_by_fitness_function1, individual.calc_fitness_func1(), individual)
        dictionary_by_fitness = OrderedDict()
        k = 0
        prev_fitness: float
        prev_list: list
        for fitness, individual_list in sorted(dictionary_by_fitness_function1.items()):
            individual_list.sort(key=self._calc_fitness_func2)
            if k == 0:
                prev_fitness = fitness
                prev_list = individual_list
            else:

                p_j: RoutingSolution
                p_j_fitness: float
                p_i: RoutingSolution
                p_i_fitness: float
                self._add_fitness_group_to_dictionary(dictionary_by_fitness, prev_list,
                                                      fitness)
                prev_fitness = fitness
                prev_list = individual_list
            k += 1
        self._add_fitness_group_to_dictionary(dictionary_by_fitness, prev_list, 1 / (1 / prev_fitness) - 1)
        temp = sorted(dictionary_by_fitness.items())
        return dict((x, y) for x, y in temp)

    def _sum_all_fitness(self) -> float:
        fitness_sum = 0
        for fitness, individual_list in self.dictionary_by_fitness.items():
            fitness_sum += fitness * len(individual_list)
        return fitness_sum

    @staticmethod
    def _choose_random_element_from_list(elements_list):
        rand = random.randint(0, len(elements_list) - 1)
        return elements_list[rand]

    def _select_individual(self, sum_all_fitness: float):
        first_fitness = self.dictionary_by_fitness.__iter__().__next__()
        rand = random.uniform(first_fitness, sum_all_fitness)
        iterator = 0
        prev_fitness = 0
        prev_list: list[RoutingSolution]
        selected_list: list[RoutingSolution]
        for fitness, individual_list in self.dictionary_by_fitness.items():
            if iterator == 0:
                last_fitness = fitness
                last_list = individual_list
                selected_list = individual_list
            else:
                if fitness >= rand:
                    if rand - prev_fitness < fitness - rand:
                        selected_list = last_list
                    else:
                        selected_list = individual_list
                    break
        return self._choose_random_element_from_list(selected_list)

    def _select_parents(self) -> List[RoutingSolution]:
        sum_all_fitness = self._sum_all_fitness()
        return [self._select_individual(sum_all_fitness), self._select_individual(sum_all_fitness)]

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
        for i in range(self.input_params.max_descendants-1):
            parents = self._select_parents()
            new_sol = self._crossover(parents=parents)
            self.routing_solutions.append(new_sol)
        self.dictionary_by_fitness = self._create_fitness_dictionary()

    def reduction(self) -> None:
        num_of_solutions_to_remove = self.input_params.max_descendants
        new_routing_solutions = []
        for fitness, individual_list in self.dictionary_by_fitness.items():
            if num_of_solutions_to_remove == 0:
                for individual in individual_list:
                    new_routing_solutions.append(individual)
            else:
                num_of_solutions_to_remove -= len(individual_list)
                for individual in individual_list:
                    if num_of_solutions_to_remove < 0:
                        new_routing_solutions.append(individual)
                        num_of_solutions_to_remove += 1
                    else:
                        break
        self.routing_solutions = new_routing_solutions

    def _get_dictionary_best(self) -> RoutingSolution:

        return list(self.dictionary_by_fitness.items())[-1][1][0]

    def get_best(self) -> RoutingSolution:
        dictionary_best = self._get_dictionary_best()
        dictionary_best_fitness_func1 = self.best_solution.calc_fitness_func1()
        old_best_fitness_func1 = dictionary_best.calc_fitness_func1()

        if dictionary_best_fitness_func1 > old_best_fitness_func1:
            return self.best_solution
        elif dictionary_best_fitness_func1 < old_best_fitness_func1:
            return dictionary_best
        else:
            dictionary_best_fitness_func2 = self.best_solution.calc_fitness_func2()
            old_best_fitness_func2 = dictionary_best.calc_fitness_func2()
            if dictionary_best_fitness_func2 > old_best_fitness_func2:
                return self.best_solution
            else:
                return dictionary_best

        pass

    def mutate_all_solutions_and_calc_new_fitness(self):
        """
        Activate mutate() for every routing solution.
        mutate(), will perform 1 of 4 mutation or not at all,
        according to the odds specified in the article.
        Finally, calc new fitness.
        """
        num_of_retries = 30  # article param

        population_after_mutation = []

        for sol in self.routing_solutions:
            old_sol = deepcopy(sol)
            success = sol.mutate(retries=num_of_retries)

            population_after_mutation.append(sol if success else old_sol)

        self.routing_solutions = population_after_mutation

        self.dictionary_by_fitness = self._create_fitness_dictionary()
