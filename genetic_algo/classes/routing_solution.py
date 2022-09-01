import random
from random import randrange
from typing import List
from copy import deepcopy

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.genotype import Genotype
from genetic_algo.classes.project_types import Pin, Point2D, Point3D


class RoutingSolution:

    def __init__(self, input_params: InputParams):
        self.fitness = self.calc_fitness()
        self.input_params = input_params
        self.genotype = Genotype(
            num_of_row=randrange(2 * self.input_params.expected_final_row_num,
                                 4 * self.input_params.expected_final_row_num),
            pins_position=self.input_params.pins_position)

    def _calc_net_length_opp(self) -> int:
        pass

    def _calc_net_length_acc(self) -> int:
        pass

    def _calc_via_numbers(self) -> int:

        via_counter: int = 0

        for i in range(self.genotype.grid):
            for j in range(self.genotype.grid[i]):
                if abs(self.genotype.grid[i][j][0]) == abs(
                        self.genotype.grid[i][j][1]):
                    via_counter += 1

        return via_counter

    def calc_fitness(self) -> float:
        pass

    def _choose_layer(self) -> int:

        # TODO: check about the preferred routing direction of each layer.
        # see section 4.3 in the article abot choosing a layer

        r = random.uniform(0, 1)
        return 0 if r < 2 / 3 else 1

    def _horizontal_line(self,
                         starting_point: Point2D,
                         net_number: int,
                         grid: List[list[List[int]]]) -> Point2D:

        number_of_columns = len(grid[0][0])
        left_x, right_x = starting_point.x, starting_point.x
        layer = self._choose_layer()

        # rout from starting point left
        while left_x >= 0:
            current_node_val = grid[layer][starting_point.y][left_x]

            if abs(current_node_val) > 0:
                break
            grid[layer][starting_point.y][left_x] = net_number
            left_x -= 1

        # rout from starting point right
        while right_x < number_of_columns:
            current_node_val = grid[layer][starting_point.y][right_x]

            if abs(current_node_val) > 0:
                break
            grid[layer][starting_point.y][right_x] = net_number
            right_x += 1

        return Point2D(randrange(left_x + 1, right_x - 1), y=starting_point.y)

    def _vertical_line(self,
                       starting_point: Point2D,
                       net_number: int,
                       grid: List[list[List[int]]],
                       initial_line: bool = False) -> Point2D:

        number_of_rows = len(grid[0])
        top_y, bottom_y = starting_point.y, starting_point.y
        layer = self._choose_layer()

        # rout from starting point down
        while bottom_y >= 0:
            current_node_val = grid[layer][bottom_y][starting_point.x]

            # see example for this condition in the article section 4.3, image (a).
            if abs(current_node_val) > 0 and (abs(current_node_val) != net_number or not initial_line):
                break
            grid[layer][bottom_y][starting_point.x] = net_number
            bottom_y -= 1

        # rout from starting point up
        while top_y < number_of_rows:
            current_node_val = grid[layer][top_y][starting_point.x]

            # see example for this condition in the article section 4.3, image (a).
            if abs(current_node_val) > 0 and (abs(current_node_val) != net_number or not initial_line):
                break
            grid[layer][bottom_y][starting_point.x] = net_number
            top_y += 1

        return Point2D(x=starting_point.x, y=randrange(bottom_y + 1, top_y - 1))

    def random_routing(self, pin_a: Pin, pin_b: Pin) -> bool:
        """
        see section 4.3 in the article 3rd paragraph about random routing.
        :param pin_a: first pin to connect
        :param pin_b: second pin to connect
        :return: return True if succeed else False.
        """

        # work on a copy instead of the original grid
        grid_copy = deepcopy(self.genotype.grid)

        # see formula 1 in the article, section 4.3 .
        curr_number_of_rows = len(self.genotype.grid[0])
        max_num_of_iter = 3 * abs(pin_a.x - pin_b.x) + curr_number_of_rows + 10

        net_number = abs(pin_a.value)
        # create initial vertical lines. see image (a) in the article section 4.3
        pin_a_random_point = self._vertical_line(grid=grid_copy,
                                                 starting_point=Point2D(x=pin_a.x, y=pin_a.y),
                                                 initial_line=True,
                                                 net_number=net_number)
        pin_b_random_point = self._vertical_line(grid=grid_copy,
                                                 starting_point=Point2D(x=pin_b.x, y=pin_b.y),
                                                 initial_line=True,
                                                 net_number=net_number)
        i = 0
        while i < max_num_of_iter:

            # horizontal line from random point
            pin_a_random_point = self._horizontal_line(grid=grid_copy, starting_point=pin_a_random_point,
                                                       net_number=net_number)
            pin_b_random_point = self._horizontal_line(grid=grid_copy, starting_point=pin_b_random_point,
                                                       net_number=net_number)

            # vertical lines from random point
            pin_a_random_point = self._vertical_line(grid=grid_copy, starting_point=pin_a_random_point,
                                                     net_number=net_number)
            pin_b_random_point = self._vertical_line(grid=grid_copy, starting_point=pin_b_random_point,
                                                     net_number=net_number)

            i += 1

        if i >= max_num_of_iter:
            return False

        self.genotype.grid = grid_copy
        return True

    def mutate(self):
        pass

    def optimize(self):
        pass
