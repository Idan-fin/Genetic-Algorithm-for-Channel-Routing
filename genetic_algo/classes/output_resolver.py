from dataclasses import dataclass

import genetic_algo.classes.routing_solution


@dataclass
class OutputType:
    best_solution: genetic_algo.classes.routing_solution.RoutingSolution


class OutputResolver:

    def resolve_output(self):
        pass
