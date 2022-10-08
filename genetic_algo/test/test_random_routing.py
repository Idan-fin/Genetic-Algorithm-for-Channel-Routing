import unittest
from unittest.mock import patch
from typing import List
from copy import deepcopy

from genetic_algo.classes.project_types import Point3D, Point2D
from genetic_algo.classes.routing_solution import RoutingSolution
from genetic_algo.test.mock_classes.mock_input_params import MockInputParams
from genetic_algo.test.data.random_routing_test_data import MOCK_INPUT_DATA


class RandomRoutingTest(unittest.TestCase):

    def setUp(self) -> None:
        self.input_params = MockInputParams(input_file_path='mock_path')
        self.input_params._parse_parameters_from_kwargs(**MOCK_INPUT_DATA)
        self.routing_solution = RoutingSolution(input_params=self.input_params)

    def test_choose_layer(self):
        """
        test case:
        - when random number is > 2/3 return value is layer 1.
        - when random number is < 2/3 return value is layer 0.
        """
        with patch('random.uniform', return_value=0.5) as mock_uniform:
            self.assertEqual(self.routing_solution._choose_layer(), 0)

        with patch('random.uniform', return_value=0.7) as mock_uniform:
            self.assertEqual(self.routing_solution._choose_layer(), 1)

    @patch('genetic_algo.classes.routing_solution.RoutingSolution._choose_layer', return_value=0)
    def test_vertical_line_no_obstacle_initial_line(self, mock_choose_layer):
        """
        test case:
        - vertical line from (x=1, y=0, z=0).
        - point (x=1, y=1, z=0) has the same net num, since this is initial line, we don't stop.
        - result - column 1 in layer 0 become 1
        """
        # expected grid and grid before horizontal routing
        old_grid = [[[0, -1, 0, -2], [0, 1, 0, 0], [0, 0, 0, 0], [-1, 0, 0, -2]],
                    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
        expected_grid = [[[0, -1, 0, -2], [0, 1, 0, 0], [0, 1, 0, 0], [-1, 1, 0, -2]],
                         [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]

        # set current genotype grid and params
        self.routing_solution.genotype.grid = old_grid
        self.routing_solution.genotype.num_of_rows = len(old_grid[0])
        self.routing_solution.genotype.num_of_columns = len(old_grid[0][0])

        # get params for horizontal routing
        genotype_copy = deepcopy(self.routing_solution.genotype)
        net_num = 1
        starting_point = Point2D(x=1, y=0)

        ret = self.routing_solution._vertical_line(starting_point=starting_point, net_number=net_num,
                                                   genotype=genotype_copy, initial_line=True)

        # validate grid after routing and ret random point
        self.assertEqual(expected_grid, genotype_copy.grid)
        self.assertEqual(starting_point.x, ret.x)
        self.assertGreaterEqual(ret.y, 0)
        self.assertLess(ret.y, len(old_grid[0]))

    @patch('genetic_algo.classes.routing_solution.RoutingSolution._choose_layer', return_value=0)
    def test_vertical_line_same_net_num_not_initial(self, mock_choose_layer):
        """
        test case:
        - vertical line from (x=1, y=0, z=0).
        - point (x=1, y=1, z=0) has the same net num, since this is NOT initial line, we stop.
        - result - same grid as old grid.
        """
        # expected grid and grid before horizontal routing
        old_grid = [[[0, -1, 0, -2], [0, 1, 0, 0], [0, 0, 0, 0], [-1, 0, 0, -2]],
                    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
        expected_grid = old_grid

        # set current genotype grid and params
        self.routing_solution.genotype.grid = old_grid
        self.routing_solution.genotype.num_of_rows = len(old_grid[0])
        self.routing_solution.genotype.num_of_columns = len(old_grid[0][0])

        # get params for horizontal routing
        genotype_copy = deepcopy(self.routing_solution.genotype)
        net_num = 1
        starting_point = Point2D(x=1, y=0)

        ret = self.routing_solution._vertical_line(starting_point=starting_point, net_number=net_num,
                                                   genotype=genotype_copy)

        # validate grid after routing and ret random point
        self.assertEqual(expected_grid, genotype_copy.grid)
        self.assertEqual(starting_point.x, ret.x)
        self.assertGreaterEqual(ret.y, 0)
        self.assertLess(ret.y, len(old_grid[0]))

    @patch('genetic_algo.classes.routing_solution.RoutingSolution._choose_layer', return_value=0)
    def test_vertical_line_not_initial_with_obstacle(self, mock_choose_layer):
        """
        test case:
        - vertical line from (x=1, y=1, z=0).
        - line 3 is all 2.
        - result - 1 in column 1 rows - 0, 1, 2
        """
        # expected grid and grid before horizontal routing
        old_grid = [[[-1, 0, 0, -2, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [2, 2, 2, 2, 2], [-1, 0, 0, -2, 0]],
                    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]
        expected_grid = [[[-1, 1, 0, -2, 0], [1, 1, 1, 1, 1], [0, 1, 0, 0, 0], [2, 2, 2, 2, 2], [-1, 0, 0, -2, 0]],
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]

        # set current genotype grid and params
        self.routing_solution.genotype.grid = old_grid
        self.routing_solution.genotype.num_of_rows = len(old_grid[0])
        self.routing_solution.genotype.num_of_columns = len(old_grid[0][0])

        # get params for horizontal routing
        genotype_copy = deepcopy(self.routing_solution.genotype)
        net_num = 1
        starting_point = Point2D(x=1, y=1)

        ret = self.routing_solution._vertical_line(starting_point=starting_point, net_number=net_num,
                                                   genotype=genotype_copy)

        # validate grid after routing and ret random point
        self.assertEqual(expected_grid, genotype_copy.grid)
        self.assertEqual(starting_point.x, ret.x)
        self.assertGreaterEqual(ret.y, 0)
        self.assertLess(ret.y, len(old_grid[0]))

    @patch('genetic_algo.classes.routing_solution.RoutingSolution._choose_layer', return_value=0)
    def test_horizontal_line_no_obstacle(self, mock_choose_layer):
        """
        test case:
        - horizontal line from (x=1, y=1, z=0), no obstacle in the way.
        - result - line 1 in layer 0 become 1
        """
        # expected grid and grid before horizontal routing
        old_grid = [[[0, -1, 0, -2], [0, 1, 0, 0], [0, 1, 0, 0], [-1, 1, 0, -2]],
                    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
        expected_grid = [[[0, -1, 0, -2], [1, 1, 1, 1], [0, 1, 0, 0], [-1, 1, 0, -2]],
                         [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]

        # set current genotype grid and params
        self.routing_solution.genotype.grid = old_grid
        self.routing_solution.genotype.num_of_rows = len(old_grid[0])
        self.routing_solution.genotype.num_of_columns = len(old_grid[0][0])

        # get params for horizontal routing
        genotype_copy = deepcopy(self.routing_solution.genotype)
        net_num = 1
        starting_point = Point2D(x=1, y=1)

        ret = self.routing_solution._horizontal_line(starting_point=starting_point, net_number=net_num,
                                                     genotype=genotype_copy)

        # validate grid after routing and ret random point
        self.assertEqual(expected_grid, genotype_copy.grid)
        self.assertEqual(starting_point.y, ret.y)
        self.assertGreaterEqual(ret.x, 0)
        self.assertLess(ret.x, len(old_grid[0][0]))

    @patch('genetic_algo.classes.routing_solution.RoutingSolution._choose_layer', return_value=0)
    def test_horizontal_line_with_obstacle(self, mock_choose_layer):
        """
        test case:
        - horizontal line from (x=1, y=1, z=0), with obstacle in the way (vertical line in column 3 layer 0).
        - result - line 1 in layer 0 become 1 in positions - 0, 1 ,2.
        """
        # expected grid and grid before horizontal routing
        old_grid = [[[0, -1, 0, 2, 0], [0, 1, 0, 2, 0], [0, 1, 0, 2, 0], [-1, 1, 0, -2, 0]],
                    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]
        expected_grid = [[[0, -1, 0, 2, 0], [1, 1, 1, 2, 0], [0, 1, 0, 2, 0], [-1, 1, 0, -2, 0]],
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]

        # set current genotype grid and params
        self.routing_solution.genotype.grid = old_grid
        self.routing_solution.genotype.num_of_rows = len(old_grid[0])
        self.routing_solution.genotype.num_of_columns = len(old_grid[0][0])

        # get params for horizontal routing
        genotype_copy = deepcopy(self.routing_solution.genotype)
        net_num = 1
        starting_point = Point2D(x=1, y=1)

        ret = self.routing_solution._horizontal_line(starting_point=starting_point, net_number=net_num,
                                                     genotype=genotype_copy)

        # validate grid after routing and ret random point
        self.assertEqual(expected_grid, genotype_copy.grid)
        self.assertEqual(starting_point.y, ret.y)
        self.assertGreaterEqual(ret.x, 0)
        self.assertLess(ret.x, len(old_grid[0][0]))

    def test_copy_path_to_genotype(self):
        """
        test case:
        - get path and copy to existing genotype grid
        - validate grid contains net number in every point in the path
        - validate every other point remains the same
        """
        old_grid = [[[-1, 0, -2], [0, 0, 2], [-1, 0, -2]],
                    [[0, 0, 0], [0, 0, 2], [0, 0, 2]]]
        self.routing_solution.genotype.grid = old_grid

        path: List[Point3D] = [Point3D(z=0, y=0, x=0), Point3D(z=0, y=1, x=0), Point3D(z=0, y=2, x=0)]
        net_num = 1

        self.routing_solution.copy_path_to_genotype(path=path, net_num=net_num)

        for i, point in enumerate(path):
            # first and last point are pins, value of pins is negative.

            grid_val = self.routing_solution.genotype.grid[point.z][point.y][point.x]
            if 0 < i < len(path) - 1:
                self.assertEqual(net_num, grid_val)
            else:
                self.assertEqual(-net_num, grid_val)

        # check every other node beside the path, remains the same
        points_set = set((p.z, p.y, p.z) for p in path)
        grid = self.routing_solution.genotype.grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                for k in range(len(grid[0][0])):
                    # if this is not part of new path
                    if (i, j, k) not in points_set:
                        self.assertEqual(old_grid[i][j][k], grid[i][j][k])

    def test_random_routing(self):
        """
        test case:
        -
        """
        pass
