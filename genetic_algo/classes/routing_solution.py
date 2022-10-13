import random
from random import randrange
from typing import List
from copy import deepcopy

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.genotype import Genotype
from genetic_algo.classes.project_types import Pin, Point2D, Point3D, Direction


class RoutingSolution:

    def __init__(self, input_params: InputParams):
        self.fitness = self.calc_fitness()
        self.input_params = input_params
        self.genotype = Genotype(
            num_of_row=randrange(2 * self.input_params.expected_final_row_num,
                                 4 * self.input_params.expected_final_row_num),
            pins_position=self.input_params.pins_position)

    def _calc_net_length_opp(self) -> int:
        counter: int = 0
        if self.input_params.preferred_direction_layer[0] == Direction.vertical:
            counter += self._calc_horizontal_net_length(layer_index=0)
        if self.input_params.preferred_direction_layer[1] == Direction.vertical:
            counter += self._calc_horizontal_net_length(layer_index=1)
        if self.input_params.preferred_direction_layer[0] == Direction.horizontal:
            counter += self._calc_vertical_net_length(layer_index=0)
        if self.input_params.preferred_direction_layer[1] == Direction.horizontal:
            counter += self._calc_vertical_net_length(layer_index=1)
        return counter

    # todo combine _calc_net_length_acc and _calc_net_length_opp
    def _calc_net_length_acc(self) -> int:
        counter: int = 0
        if self.input_params.preferred_direction_layer[0] == Direction.horizontal:
            counter += self._calc_horizontal_net_length(layer_index=0)
        if self.input_params.preferred_direction_layer[1] == Direction.horizontal:
            counter += self._calc_horizontal_net_length(layer_index=1)
        if self.input_params.preferred_direction_layer[0] == Direction.vertical:
            counter += self._calc_vertical_net_length(layer_index=0)
        if self.input_params.preferred_direction_layer[1] == Direction.vertical:
            counter += self._calc_vertical_net_length(layer_index=1)
        return counter

    def _calc_vertical_net_length(self, layer_index: int) -> int:
        counter: int = 0
        for i, y in enumerate(self.genotype.grid[0]):
            for j, z in enumerate(y):
                if i <= self.genotype.grid[0] and abs(self.genotype.grid[layer_index][i+1][j]) == abs(
                        self.genotype.grid[layer_index][i][j]):
                    counter += 1
        return counter

    def _calc_horizontal_net_length(self, layer_index: int) -> int:
        counter: int = 0
        for i, y in enumerate(self.genotype.grid[0]):
            for j, z in enumerate(y):
                if j <= len(y) - 2 and i > 0 and abs(self.genotype.grid[layer_index][i][j + 1]) == abs(
                        self.genotype.grid[layer_index][i][j]):
                    counter += 1
        return counter

    def _calc_via_numbers(self) -> int:

        via_counter: int = 0

        for row_index, row in enumerate(self.genotype.grid[0]):
            for column_index, val in enumerate(row):
                if abs(self.genotype.grid[0][row_index][column_index]) == abs(
                        self.genotype.grid[1][row_index][column_index]) != 0:
                    via_counter += 1

        return via_counter

    def calc_fitness_func1(self) -> float:
        return 1.0/len(self.genotype.grid[0][0])
        pass

    def calc_fitness_func2(self) -> float:
        return 1.0/(self._calc_net_length_acc()+self.input_params.net_length_factor*self._calc_net_length_opp() +
                    self._calc_via_numbers()*self.input_params.via_numbers_factor)
        pass

    def calc_fitness(self) -> float:
        pass

    @staticmethod
    def _choose_layer() -> int:

        # TODO: check about the preferred routing direction of each layer.
        # see section 4.3 in the article abot choosing a layer

        r = random.uniform(0, 1)
        return 0 if r < 2 / 3 else 1

    def _horizontal_line(self,
                         starting_point: Point2D,
                         net_number: int,
                         genotype: Genotype) -> Point2D:

        left_x, right_x = starting_point.x, starting_point.x
        layer = self._choose_layer()

        # draw line from starting point left
        while left_x >= 0:
            current_node_val = genotype.grid[layer][starting_point.y][left_x]

            if abs(current_node_val) > 0:
                break
            genotype.grid[layer][starting_point.y][left_x] = net_number
            left_x -= 1
        left_x = 0 if left_x < 0 else left_x

        # draw line from starting point right
        while right_x < genotype.num_of_columns:
            current_node_val = genotype.grid[layer][starting_point.y][right_x]

            if abs(current_node_val) > 0:
                break
            genotype.grid[layer][starting_point.y][right_x] = net_number
            right_x += 1
        right_x = genotype.num_of_columns if right_x >= genotype.num_of_columns else right_x + 1

        return Point2D(x=randrange(left_x, right_x), y=starting_point.y)

    def _vertical_line(self,
                       starting_point: Point2D,
                       net_number: int,
                       genotype: Genotype,
                       initial_line: bool = False) -> Point2D:

        top_y, bottom_y = starting_point.y, starting_point.y
        layer = self._choose_layer()

        # draw line from starting point down
        while bottom_y >= 0:
            current_node_val = genotype.grid[layer][bottom_y][starting_point.x]

            # see example for this condition in the article section 4.3, image (a).
            # initial line don't stop on nodes with the same net number
            if abs(current_node_val) > 0 and (abs(current_node_val) != net_number and not initial_line):
                break
            genotype.grid[layer][bottom_y][starting_point.x] = net_number
            bottom_y -= 1
        bottom_y = 0 if bottom_y < 0 else bottom_y

        # draw line from starting point up
        while top_y < genotype.num_of_rows:
            current_node_val = genotype.grid[layer][top_y][starting_point.x]

            # see example for this condition in the article section 4.3, image (a).
            # initial line don't stop on nodes with the same net number
            if abs(current_node_val) > 0 and (abs(current_node_val) != net_number and not initial_line):
                break
            genotype.grid[layer][top_y][starting_point.x] = net_number
            top_y += 1
        top_y = genotype.num_of_rows if top_y >= genotype.num_of_rows else top_y + 1

        return Point2D(x=starting_point.x, y=randrange(bottom_y, top_y))

    def copy_path_to_genotype(self, path: List[Point3D], net_num: int):

        for i, point in enumerate(path):
            # assign negative value to pins (start/end of the path).
            value = -net_num if i == 0 or i == len(path) - 1 else net_num
            self.genotype.grid[point.z][point.y][point.x] = net_num

    def random_routing(self, pin_a: Pin, pin_b: Pin) -> bool:
        """
        see section 4.3 in the article 3rd paragraph about random routing.
        @param pin_a: first pin to connect
        @param pin_b: second pin to connect
        @return: return True if succeed else False.
        """
        # work on a copy instead of the original genotype
        genotype_copy = deepcopy(self.genotype)

        # see formula 1 in the article, section 4.3 .
        max_num_of_iter = 3 * abs(pin_a.x - pin_b.x) + genotype_copy.num_of_rows + 10

        net_number = abs(pin_a.value)
        # initial points for vertical lines
        pin_a_random_point = Point2D(x=pin_a.x, y=pin_a.y)
        pin_b_random_point = Point2D(x=pin_b.x, y=pin_b.y)
        for i in range(max_num_of_iter):
            # vertical line from random point
            pin_a_random_point = self._vertical_line(genotype=genotype_copy, starting_point=pin_a_random_point,
                                                     initial_line=i == 0, net_number=net_number)
            pin_b_random_point = self._vertical_line(genotype=genotype_copy, starting_point=pin_b_random_point,
                                                     initial_line=i == 0, net_number=net_number)
            # horizontal line from random point
            pin_a_random_point = self._horizontal_line(genotype=genotype_copy, starting_point=pin_a_random_point,
                                                       net_number=net_number)
            pin_b_random_point = self._horizontal_line(genotype=genotype_copy, starting_point=pin_b_random_point,
                                                       net_number=net_number)

            path = genotype_copy.find_shortest_path(point1=Point3D(x=pin_a.x, y=pin_a.y, z=pin_a.z),
                                                    point2=Point3D(x=pin_b.x, y=pin_b.y, z=pin_b.z))
            if path:
                self.copy_path_to_genotype(path=path, net_num=net_number)
                return True

        return False

    def mutate(self):
        pass

    def optimize(self):
        pass
