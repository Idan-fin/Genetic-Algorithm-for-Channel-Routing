import unittest
from genetic_algo.classes.genotype import Genotype
from genetic_algo.classes.project_types import Point3D


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_calculate_edge_index(self):
        g = Genotype(num_of_row=150, pins_position=[[1, 2, 3], [1, 2, 3]])
        for i in range(0, 150):
            for j in range(0, 3):
                for k in range(0, 2):
                    self.assertEqual(g.calculate_genotype_index(g._calculate_edge_index(x=i, y=j, z=k)), Point3D(i, j, k))

        pass

    def test_init(self):
        pins_position = [[1, 2, 3], [1, 2, 3]]
        with self.assertRaises(ValueError):
            Genotype(num_of_row=1, pins_position=pins_position)
        with self.assertRaises(ValueError):
            Genotype(num_of_row=1, pins_position=[[1, 2, 3], [1, 2, 2]])
        with self.assertRaises(ValueError):
            Genotype(num_of_row=1, pins_position=[[1, 2, 3], [1, 2]])
        g = Genotype(num_of_row=150, pins_position=pins_position)
        self.assertEqual(len(g.grid), 150)
        self.assertEqual(len(g.grid[0]), 3)
        self.assertEqual(len(g.grid[0][0]), 2)
        for j, l in enumerate(g.grid[0]):
            self.assertEqual(l[0], -pins_position[0][j])
        for j, l in enumerate(g.grid[len(g.grid)-1]):
            self.assertEqual(l[0], -pins_position[1][j])
        pass

    def test_find_shortest_path(self):
        pins_position = [[1, 2, 3], [1, 2, 3]]
        genotype = Genotype(num_of_row=2, pins_position=pins_position)
        for i in range(0, 3):
            point1 = Point3D(0, i, 0)
            point2 = Point3D(1, i, 0)
            res = genotype.find_shortest_path(point1, point2)
            self.assertEqual(res, [point1, point2])
        point1 = Point3D(0, 0, 0)
        point2 = Point3D(1, 1, 0)
        self.assertIsNone(genotype.find_shortest_path(point1, point2))
        pins_position = [[1, 2, 3], [2, 1, 3]]
        point1 = Point3D(0, 0, 0)
        point2 = Point3D(3, 1, 0)
        genotype = Genotype(num_of_row=4, pins_position=pins_position)
        self.assertIsNone(genotype.find_shortest_path(point1, point2))
        genotype.grid[1][0][0] = 1
        genotype.grid[1][1][0] = 1
        genotype.grid[2][1][0] = 1
        self.assertIsNotNone(genotype.find_shortest_path(point1, point2))
        genotype.grid[1][0][0] = 1
        genotype.grid[1][0][1] = 1
        genotype.grid[1][1][0] = 0
        genotype.grid[2][0][1] = 1
        genotype.grid[2][1][1] = 1
        genotype.grid[2][1][0] = 1
        self.assertIsNotNone(genotype.find_shortest_path(point1, point2))
        point2 = Point3D(3, 2, 0)
        self.assertIsNone(genotype.find_shortest_path(point1, point2))



if __name__ == '__main__':
    unittest.main()
