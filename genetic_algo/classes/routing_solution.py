import random
from random import randrange
from typing import List, Optional
from copy import deepcopy

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.genotype import Genotype
from genetic_algo.classes.project_types import Pin, Point2D, Point3D, Direction


NUM_OF_RANDOM_ROUTING_RETRIES = 10  # article param.


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
        """
        Iterate over the grid and look for the same net num at the same (x,y) position in both layers.
        :return: num of via in this solution.
        """
        via_counter: int = 0

        for row_index, row in enumerate(self.genotype.grid[0]):
            for column_index, val in enumerate(row):
                if abs(self.genotype.grid[0][row_index][column_index]) == abs(
                        self.genotype.grid[1][row_index][column_index]) != 0:
                    via_counter += 1

        return via_counter

    def calc_fitness_func1(self) -> float:
        return 1.0/len(self.genotype.grid[0])
        pass

    def calc_fitness_func2(self) -> float:
        return 1.0/(self._calc_net_length_acc()+self.input_params.net_length_factor*self._calc_net_length_opp() +
                    self._calc_via_numbers()*self.input_params.via_numbers_factor)
        pass

    def calc_fitness(self) -> float:
        pass

    @staticmethod
    def _choose_layer() -> int:
        """
        Acording to section 4.3 in the article about choosing a layer .
        :return: layer num.
        """
        # TODO: check about the preferred routing direction of each layer.

        r = random.uniform(0, 1)
        return 0 if r < 2 / 3 else 1

    def _horizontal_line(self,
                         starting_point: Point2D,
                         net_number: int,
                         genotype: Genotype) -> Point2D:
        """
        Draw horizontal line from a given point.
        :param starting_point: will draw from this point to the left and right.
        :param net_number: the new line will contain this net num.
        :param genotype: genotype to work on.
        :return: random point on the new line.
        """
        left_x, right_x = starting_point.x - 1, starting_point.x + 1
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
        """
        Draw vertical line from a given point.
        :param starting_point: will draw from this point up and down.
        :param net_number: the new line will contain this net num.
        :param genotype: genotype to work on.
        :param initial_line: if True, will continue to draw if encountered the same net num.
        :return: random point on the new line.
        """
        top_y, bottom_y = starting_point.y + 1, starting_point.y - 1
        layer = self._choose_layer()

        # draw line from starting point down
        while bottom_y >= 0:
            current_node_val = genotype.grid[layer][bottom_y][starting_point.x]

            # see example for this condition in the article section 4.3, image (a).
            # initial line don't stop on nodes with the same net number
            if abs(current_node_val) > 0 and (abs(current_node_val) != net_number or not initial_line):
                break
            genotype.grid[layer][bottom_y][starting_point.x] = net_number
            bottom_y -= 1
        bottom_y = 0 if bottom_y < 0 else bottom_y

        # draw line from starting point up
        while top_y < genotype.num_of_rows:
            current_node_val = genotype.grid[layer][top_y][starting_point.x]

            # see example for this condition in the article section 4.3, image (a).
            # initial line don't stop on nodes with the same net number
            if abs(current_node_val) > 0 and (abs(current_node_val) != net_number or not initial_line):
                break
            genotype.grid[layer][top_y][starting_point.x] = net_number
            top_y += 1
        top_y = genotype.num_of_rows if top_y >= genotype.num_of_rows else top_y + 1

        return Point2D(x=starting_point.x, y=randrange(bottom_y, top_y))

    def copy_path_to_genotype(self, path: List[Point3D], net_num: int):

        for i, point in enumerate(path):
            # assign negative value to pins (start/end of the path).
            value = -net_num if i == 0 or i == len(path) - 1 else net_num
            self.genotype.grid[point.z][point.y][point.x] = value

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

    @staticmethod
    def _get_pin_to_connect(pool: List[Pin], net_num: Optional[int] = None) -> Pin:
        """
        chose random pin with a specific net_num from given list.
        if didn't get net_num, chose randomly from the entire given list.
        """
        chosen_pin_index = randrange(0, len(pool))

        if net_num:
            same_net_pool = []
            for i, pin in enumerate(pool):
                if abs(pin.value) == net_num:
                    same_net_pool.append(i)
            chosen_pin_index = same_net_pool[randrange(0, len(same_net_pool))]

        return pool.pop(chosen_pin_index)

    def _get_initial_not_connected_pins(self) -> List[Pin]:
        """
        create initial pins pool for the given input params.
        :return: initial not_connected_pins list.
        """
        # TODO: check the pins representation in input_params.pins_position
        bottom_pins = self.input_params.pins_position[0]
        top_pins = self.input_params.pins_position[1]

        pins_pool = []
        max_row_index = self.genotype.num_of_rows - 1
        for i in range(len(bottom_pins)):
            pins_pool.append(Pin(x=i, y=0, z=0, value=(-bottom_pins[i])))
            pins_pool.append(Pin(x=i, y=max_row_index, z=0, value=(-top_pins[i])))
        return pins_pool

    def extend_genotype_num_of_rows_by_one(self):
        """
        When random routing failed for given pins, according to the algorithm we should
        increase the num of rows by 1 and try again.
        """
        # TODO: verify that we can avoid rows 0/max_row
        row_num = randrange(1, self.genotype.num_of_rows-1)  # avoiding 0/max_row rows

        # insert new empty row for each layer
        self.genotype.grid[0].insert(row_num, [0]*self.genotype.num_of_columns)
        self.genotype.grid[1].insert(row_num, [0]*self.genotype.num_of_columns)

        # fill the new rows
        # if we have the same net_num above and beneath the new cell it means that we need
        # to fill the new cell with the same val.
        for i in range(self.genotype.grid):
            for k in range(self.genotype.num_of_columns):
                above_val = abs(self.genotype.grid[i][row_num+1][k])
                beneath_val = abs(self.genotype.grid[i][row_num-1][k])
                if beneath_val == above_val:
                    self.genotype.grid[i][row_num][k] = above_val

        self.genotype.num_of_rows += 1

    def connect_all_pins(self) -> bool:
        """
        This function will activate the random routing on every pin until all pins are connected.
        - It will choose randomly 2 pins to connect on every iteration.
        - Upon random routing failure of 2 pins, this function will increase the num of rows of this
          individual and will try again.
        - As described in the article, after 10 unsuccessful extensions, this function will fail.
        :return: bool for success/failure.
        """
        already_connected_pins = []
        not_connected_pins = self._get_initial_not_connected_pins()

        existing_nets_in_connected_pins = set()

        while not_connected_pins:
            pin_a = self._get_pin_to_connect(pool=not_connected_pins)

            net_num = abs(pin_a.value)
            pool_for_pin_b = already_connected_pins if net_num in existing_nets_in_connected_pins \
                else not_connected_pins
            pin_b = self._get_pin_to_connect(pool=pool_for_pin_b, net_num=net_num)

            random_routing_success = False
            for i in range(NUM_OF_RANDOM_ROUTING_RETRIES):
                if self.random_routing(pin_a=pin_a, pin_b=pin_b):
                    random_routing_success = True
                    break
                else:
                    self.extend_genotype_num_of_rows_by_one()

            if not random_routing_success:
                return False

            already_connected_pins.append(pin_a)
            already_connected_pins.append(pin_b)
            existing_nets_in_connected_pins.add(net_num)

        return True

    def mutate(self):
        pass

    def optimize(self):
        pass