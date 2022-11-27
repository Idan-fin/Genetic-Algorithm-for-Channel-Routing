# __future__ require python >= 3.7!!
# for type annotation in copy_routing_from_parent.
from __future__ import annotations

import random
from random import randrange
from typing import List, Optional, Dict
from copy import deepcopy

from genetic_algo.classes.input_params import InputParams
from genetic_algo.classes.genotype import Genotype
from genetic_algo.classes.project_types import Pin, Point3D, Direction

NUM_OF_RANDOM_ROUTING_RETRIES = 10  # article param.
NUM_OF_LAYERS = 2


class CellNotEmptyError(Exception):
    pass


class WrongPreferredDirections(Exception):
    pass


class RoutingSolution:

    def __init__(self, input_params: InputParams, num_of_rows: Optional[int] = None):
        self.fitness = self.calc_fitness()
        self.input_params = input_params

        rand_num_of_rows = randrange(2 * self.input_params.expected_final_row_num,
                                     4 * self.input_params.expected_final_row_num)
        num_of_row = num_of_rows or rand_num_of_rows
        self.genotype = Genotype(num_of_row=num_of_row, pins_position=self.input_params.pins_position)

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
                if i < len(self.genotype.grid[0])-1 and abs(self.genotype.grid[layer_index][i+1][j]) == abs(
                        self.genotype.grid[layer_index][i][j]):
                    counter += 1
        return counter

    def _calc_horizontal_net_length(self, layer_index: int) -> int:
        counter: int = 0
        for i, y in enumerate(self.genotype.grid[0]):
            for j, z in enumerate(y):
                if j <= len(y) - 2 and i > 0 and abs(self.genotype.grid[layer_index][i][j + 1]) == abs(
                        self.genotype.grid[layer_index][i][j]) != 0:
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
        return 1.0 / len(self.genotype.grid[0])
        pass

    def calc_fitness_func2(self) -> float:
        return 1.0 / (self._calc_net_length_acc() + self.input_params.net_length_factor * self._calc_net_length_opp() +
                      self._calc_via_numbers() * self.input_params.via_numbers_factor)
        pass

    def calc_fitness(self) -> float:
        pass

    def _choose_layer(self, is_vertical: bool) -> int:
        """
        According to section 4.3 in the article about choosing a layer .
        First calculate the chosen direction according to random number.
        Finally, chose the layer accordingly.
        :return: layer num.
        """
        r = random.uniform(0, 1)
        direction = Direction.vertical.value

        if is_vertical and r < 2 / 3:
            direction = Direction.vertical.value
        elif is_vertical and r >= 2 / 3:
            direction = Direction.horizontal.value
        elif (not is_vertical) and r < 2 / 3:
            direction = Direction.horizontal.value
        elif (not is_vertical) and r >= 2 / 3:
            direction = Direction.vertical.value

        preferred_directions = self.input_params.preferred_direction_layer
        if direction == preferred_directions[0]:
            return 0
        elif direction == preferred_directions[1]:
            return 1
        else:
            raise WrongPreferredDirections()

    def _horizontal_line(self,
                         starting_point: Point3D,
                         net_number: int,
                         genotype: Genotype) -> Point3D:
        """
        Draw horizontal line from a given point.
        :param starting_point: will draw from this point to the left and right.
        :param net_number: the new line will contain this net num.
        :param genotype: genotype to work on.
        :return: random point on the new line.
        """

        # can't draw horizontal line on pins row
        if starting_point.y in {0, genotype.num_of_rows - 1}:
            return starting_point

        left_x, right_x = starting_point.x - 1, starting_point.x + 1
        layer = self._choose_layer(is_vertical=False)

        # TODO: verify this case.
        # create via or abort if not empty
        if layer != starting_point.z:
            if genotype.grid[layer][starting_point.y][starting_point.x] not in {0, net_number}:
                return starting_point
            genotype.grid[layer][starting_point.y][starting_point.x] = net_number

        # draw line from starting point left
        while left_x >= 0:
            current_node_val = genotype.grid[layer][starting_point.y][left_x]

            if abs(current_node_val) > 0 and abs(current_node_val) != net_number:
                break
            genotype.grid[layer][starting_point.y][left_x] = net_number
            left_x -= 1
        left_x += 1

        # draw line from starting point right
        while right_x < genotype.num_of_columns:
            current_node_val = genotype.grid[layer][starting_point.y][right_x]

            if abs(current_node_val) > 0 and abs(current_node_val) != net_number:
                break
            genotype.grid[layer][starting_point.y][right_x] = net_number
            right_x += 1
        right_x -= 1

        x = left_x if left_x == right_x else randrange(left_x, right_x)
        return Point3D(x=x, y=starting_point.y, z=layer)

    def _vertical_line(self,
                       starting_point: Point3D,
                       net_number: int,
                       genotype: Genotype) -> Point3D:
        """
        Draw vertical line from a given point.
        :param starting_point: will draw from this point up and down.
        :param net_number: the new line will contain this net num.
        :param genotype: genotype to work on.
        :return: random point on the new line.
        """
        top_y, bottom_y = starting_point.y + 1, starting_point.y - 1
        layer = self._choose_layer(is_vertical=True)

        if layer != starting_point.z:
            if genotype.grid[layer][starting_point.y][starting_point.x] not in {0, net_number}:
                # TODO: check what to do in that case
                return starting_point
            genotype.grid[layer][starting_point.y][starting_point.x] = net_number

        # draw line from starting point down
        while bottom_y >= 0:
            current_node_val = genotype.grid[layer][bottom_y][starting_point.x]

            # see example for this condition in the article section 4.3, image (a).
            # initial line don't stop on nodes with the same net number
            if abs(current_node_val) > 0 and abs(current_node_val) != net_number:
                break
            genotype.grid[layer][bottom_y][starting_point.x] = net_number
            bottom_y -= 1
        bottom_y += 1

        # draw line from starting point up
        while top_y < genotype.num_of_rows:
            current_node_val = genotype.grid[layer][top_y][starting_point.x]

            # see example for this condition in the article section 4.3, image (a).
            # initial line don't stop on nodes with the same net number
            if abs(current_node_val) > 0 and abs(current_node_val) != net_number:
                break
            genotype.grid[layer][top_y][starting_point.x] = net_number
            top_y += 1
        # TODO: verify theos increments/decrements
        top_y -= 1

        y = bottom_y if bottom_y == top_y else randrange(bottom_y, top_y)
        return Point3D(x=starting_point.x, y=y, z=layer)

    def copy_path_to_genotype(self, path: List[Point3D], net_num: int):

        net_num = abs(net_num)
        path = path
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
        pin_a_random_point = Point3D(x=pin_a.x, y=pin_a.y, z=0)
        pin_b_random_point = Point3D(x=pin_b.x, y=pin_b.y, z=0)
        for i in range(max_num_of_iter):
            # vertical line from random point
            pin_a_random_point = self._vertical_line(genotype=genotype_copy, starting_point=pin_a_random_point,
                                                     net_number=net_number)
            pin_b_random_point = self._vertical_line(genotype=genotype_copy, starting_point=pin_b_random_point,
                                                     net_number=net_number)
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

    def _get_all_pins(self) -> List[Pin]:
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
        row_num = randrange(1, self.genotype.num_of_rows - 1)  # avoiding 0/max_row rows

        # insert new empty row for each layer
        self.genotype.grid[0].insert(row_num, [0] * self.genotype.num_of_columns)
        self.genotype.grid[1].insert(row_num, [0] * self.genotype.num_of_columns)

        # fill the new rows
        # if we have the same net_num above and beneath the new cell it means that we need
        # to fill the new cell with the same val.
        for i in range(NUM_OF_LAYERS):
            for k in range(self.genotype.num_of_columns):
                above_val = abs(self.genotype.grid[i][row_num + 1][k])
                beneath_val = abs(self.genotype.grid[i][row_num - 1][k])
                if beneath_val == above_val:
                    self.genotype.grid[i][row_num][k] = above_val

        self.genotype.num_of_rows += 1

    def fix_all_pins_row_index(self,
                               pin_a: Pin,
                               pin_b: Pin,
                               not_connected_pins: List[Pin],
                               already_connected_pins: List[Pin]) -> (Pin, Pin):
        new_row = self.genotype.num_of_rows - 1
        for pin in not_connected_pins:
            if pin.y > 0:
                pin.y = new_row

        for pin in already_connected_pins:
            if pin.y > 0:
                pin.y = new_row

        pin_a.y = pin_a.y if pin_a.y == 0 else new_row
        pin_b.y = pin_b.y if pin_b.y == 0 else new_row

        return pin_a, pin_b

    # def _get_connected_and_not_connected_pins(self, is_partially_connected: bool) -> (List[Pin], List[Pin]):
    #     """
    #     Check if we have:
    #         - for pin in row 0: cell with the same net num in the layer above or row above.
    #         - for pin in row max_row: cell with the same net num in the layer above or row beneath.
    #     If one of those cases is True the pin is connected.
    #     :param is_partially_connected: if False return all pins as not_connected, else check.
    #     :return: connected and not connected pins lists.
    #     """
    #     connected = []
    #     not_connected = self._get_all_pins()
    #
    #     # TODO - fix BUG should be "if not is_partially_connected"
    #     if not is_partially_connected:
    #         return connected, not_connected
    #
    #     new_not_connected = []
    #     for pin in not_connected:
    #         y_addition = 1 if pin.y == 0 else -1
    #         if abs(self.genotype.grid[pin.z][pin.y + y_addition][pin.x]) == abs(pin.value):
    #             connected.append(pin)
    #         elif abs(self.genotype.grid[pin.z + 1][pin.y][pin.x]) == abs(pin.value):
    #             connected.append(pin)
    #         else:
    #             new_not_connected.append(pin)
    #
    #     return connected, new_not_connected

    def connect_all_pins(self,
                         num_of_retries: Optional[int] = None,
                         is_partially_connected: bool = False) -> bool:
        """
        This function will activate the random routing on every pin until all pins are connected.
        - It will choose randomly 2 pins to connect on every iteration.
        - Upon random routing failure of 2 pins, this function will increase the num of rows of this
          individual and will try again.
        - As described in the article, after 10 unsuccessful extensions, this function will fail.
        :return: bool for success/failure.
        """
        num_of_random_routing_retries = num_of_retries or NUM_OF_RANDOM_ROUTING_RETRIES

        already_connected_pins, not_connected_pins = [], self._get_all_pins()

        existing_nets_in_connected_pins = set()

        while not_connected_pins:
            pin_a = self._get_pin_to_connect(pool=not_connected_pins)

            net_num = abs(pin_a.value)
            pool_for_pin_b = already_connected_pins if net_num in existing_nets_in_connected_pins \
                else not_connected_pins
            pin_b = self._get_pin_to_connect(pool=pool_for_pin_b, net_num=net_num)

            path = self.genotype.find_shortest_path(point1=Point3D(x=pin_a.x, y=pin_a.y, z=pin_a.z),
                                                    point2=Point3D(x=pin_b.x, y=pin_b.y, z=pin_b.z))
            if path:
                # already have path for those pins
                already_connected_pins.append(pin_a)
                already_connected_pins.append(pin_b)
                existing_nets_in_connected_pins.add(net_num)
            else:
                random_routing_success = False
                for i in range(num_of_random_routing_retries):
                    if self.random_routing(pin_a=pin_a, pin_b=pin_b):
                        random_routing_success = True
                        break
                    else:
                        self.extend_genotype_num_of_rows_by_one()
                        pin_a, pin_b = self.fix_all_pins_row_index(
                            pin_a=pin_a, pin_b=pin_b,
                            not_connected_pins=not_connected_pins,
                            already_connected_pins=already_connected_pins)

                if not random_routing_success:
                    return False

                already_connected_pins.append(pin_a)
                already_connected_pins.append(pin_b)
                existing_nets_in_connected_pins.add(net_num)

        return True

    @staticmethod
    def _get_clean_parent(parent: RoutingSolution,
                          cutting_line: int,
                          left_to_line: bool) -> RoutingSolution:

        for layer in range(NUM_OF_LAYERS):
            for row in range(parent.genotype.num_of_rows):
                for column in range(parent.genotype.num_of_columns):

                    clean_current_cell = True
                    if layer == 0 and (row == 0 or row == parent.genotype.num_of_rows - 1):
                        # don't delete pins rows
                        clean_current_cell = False
                    elif column <= cutting_line and left_to_line:
                        clean_current_cell = False
                    elif column > cutting_line and not left_to_line:
                        clean_current_cell = False

                    current_val = parent.genotype.grid[layer][row][column]
                    new_val = 0 if clean_current_cell else current_val
                    parent.genotype.grid[layer][row][column] = new_val

        return parent

    @staticmethod
    def _get_pins_by_net_num(all_pins: List[Pin]) -> Dict[int, List[Pin]]:
        pins_dict = {}

        for pin in all_pins:
            if pin.value in pins_dict:
                pins_dict[pin.value].append(pin)
            else:
                pins_dict[pin.value] = [pin]

        return pins_dict

    def copy_routing_from_parent(self,
                                 parent: RoutingSolution,
                                 cutting_line: int,
                                 left_to_line: bool):

        parent = self._get_clean_parent(parent=parent, cutting_line=cutting_line, left_to_line=left_to_line)

        # necessary info
        all_pins = self._get_all_pins()
        pins_by_net_num = self._get_pins_by_net_num(all_pins=all_pins)
        checked = set()

        # go one by one and copy path between pins if exists in parent.
        for pin in all_pins:

            # add the current pin in this stage to avoid same pin checking.
            checked.add(pin)

            # check path only for pins with same net_num.
            same_net_pins = pins_by_net_num[pin.value]
            for pin_b in same_net_pins:

                # check for path only for pins we didn't checked before.
                if pin_b not in checked:
                    path = parent.genotype.find_shortest_path(
                        point1=Point3D(z=pin.z, y=pin.y, x=pin.x),
                        point2=Point3D(z=pin_b.z, y=pin_b.y, x=pin_b.x)
                    )
                    if path:
                        self.copy_path_to_genotype(path=path, net_num=abs(pin.value))

    def _remove_entire_net(self, net_num: int):
        net_num = abs(net_num)
        for i in range(NUM_OF_LAYERS):
            for j in range(self.genotype.num_of_rows):
                for k in range(self.genotype.num_of_columns):
                    current_val = self.genotype.grid[i][j][k]
                    self.genotype.grid[i][j][k] = current_val if current_val != net_num else 0

    def _remove_random_rectangle(self):

        rand_x = randrange(self.genotype.num_of_columns)
        rand_y = randrange(self.genotype.num_of_rows)
        rand_z = randrange(NUM_OF_LAYERS)

        # TODO: check about the rand size
        size_x, size_y = randrange(self.genotype.num_of_columns), randrange(self.genotype.num_of_rows)

        left = max(0, rand_x - size_x)
        right = min(self.genotype.num_of_columns, rand_x + size_x)
        top = min(self.genotype.num_of_rows, rand_y + size_y)
        bottom = max(0, rand_y - size_y)

        for i in range(bottom, top):
            for j in range(left, right):
                curr_val = self.genotype.grid[rand_z][i][j]

                # keep pins value
                self.genotype.grid[rand_z][i][j] = 0 if curr_val >= 0 else curr_val

    def _mutation_1(self, retries: int):
        """
        mutation 1 will remove and reconnect routs from random rectangle.
        """
        self._remove_random_rectangle()

        return self.connect_all_pins(num_of_retries=retries, is_partially_connected=True)

    def _mutation_2(self, retries: int):
        """
        mutation 2 will delete and reroute nets randomly.
        """
        all_nets = {abs(val) for val in self.genotype.pins_position[0] + self.genotype.pins_position[1]}

        num_of_nets_to_remove = randrange(0, len(all_nets))

        for _ in range(num_of_nets_to_remove):
            net_num = all_nets.pop()
            self._remove_entire_net(net_num=net_num)

        return self.connect_all_pins(num_of_retries=retries, is_partially_connected=True)

    def _mutation_3(self, retries: int):
        """
        mutation 3 will add row in a random index.
        """
        self.extend_genotype_num_of_rows_by_one()

        return True

    def _mutation_4(self, retries: int):
        """
        mutation 4 will remove row in a random index.
        """
        row_num = randrange(1, self.genotype.num_of_rows - 1)  # avoiding 0/max_row rows

        # remove row from both layers
        self.genotype.grid[0].pop(row_num)
        self.genotype.grid[1].pop(row_num)
        self.genotype.num_of_rows -= 1

        return self.connect_all_pins(num_of_retries=retries, is_partially_connected=True)

    def mutate(self, retries: int) -> bool:

        rand_num = random.uniform(0, 1)

        if 0 <= rand_num <= 0.001:
            return self._mutation_1(retries=retries)
        elif 0.001 < rand_num <= 0.003:
            return self._mutation_2(retries=retries)
        elif 0.003 < rand_num <= 0.013:
            return self._mutation_3(retries=retries)
        elif 0.013 < rand_num <= 0.023:
            return self._mutation_4(retries=retries)
        else:
            return True

    def optimize(self):
        pass
