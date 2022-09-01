from typing import List, Optional
from igraph import Graph
from project_types import Point3D
import random


class Genotype:

    def __init__(self, num_of_row: int, pins_position: List[List[int]]):  # Idan
        self.grid = self._generate_initial_genotype(num_of_row=num_of_row, pins_position=pins_position)

    @staticmethod
    def _generate_initial_genotype(self, num_of_row: int, pins_position: List[List[int]]) -> List[List[List[int]]]:
        x = random.randint(num_of_row*2, num_of_row*4)

        genotype = [[[0 for k in range(2)] for j in range(len(pins_position[0]))] for i in range(x)]
        for j, l in enumerate(genotype[0]):
            l[0] = pins_position[0][j]
        for j, l in enumerate(genotype[x-1]):
            l[0] = pins_position[1][j]
        return genotype

        pass

    def _calculate_edge_index(self, x: int, y: int, z: int) -> int:
        return len(self.grid)*len(self.grid[0])*z+len(self.grid)*y+x
        pass

    def _calculate_edge_index(self, p: Point3D) -> int:
        return self._calculate_edge_index(p.x, p.y, p.z)
        pass

    def create_graph(self, net_id: int) -> Graph:
        g = Graph()
        g.add_vertices(len(self.grid)*len(self.grid[0])*len(self.grid[0][0]))
        for i, y in enumerate(self.grid):
            for j, z in enumerate(y):
                for k, val in enumerate(z):
                    if i < len(self.grid)-2 and abs(self.grid[i+1][j][k]) == abs(val) == net_id:
                        g.add_edge(self._calculate_edge_index(i, j, k), (self._calculate_edge_index(i+1, j, k)))
                        pass
                    if j < len(y)-2 and i > 0 and abs(self.grid[i][j+1][k]) == abs(val) == net_id:
                        g.add_edge(self._calculate_edge_index(i, j, k), (self._calculate_edge_index(i, j+1, k)))
                        pass
                    if k == 0 and abs(self.grid[i][j][k+1]) == abs(val) == net_id:
                        g.add_edge(self._calculate_edge_index(i, j, k), (self._calculate_edge_index(i, j, k+1)))
                        pass
        return g
        pass

    def calculate_genotype_index(self, index: int) -> Point3D:
        pass

    def find_shortest_path(self, point1: Point3D, point2: Point3D) -> Optional[list[Point3D]]:
        """

        :param point1:
        :param point2:
        :return: Shortest path, Null if path not exist
        """
        g = self.create_graph(abs(self.grid[point1.x][point1.y][point1.z]))
        g.get_shortest_paths(self._calculate_edge_index(point1), self._calculate_edge_index(point2))
        pass
