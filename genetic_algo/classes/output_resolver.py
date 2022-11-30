from dataclasses import dataclass
import json
import genetic_algo.classes.routing_solution


@dataclass
class OutputType:
    best_solution: genetic_algo.classes.routing_solution.RoutingSolution


class OutputResolver:
    output: OutputType
    output_path: str

    def __init__(self, output_type: OutputType, output_path: str):
        self.output = output_type
        self.output_path = output_path

    def resolve_output(self):
        f = open(self.output_path, "w")
        json_type = json.dumps(self.output.best_solution)
        f.write(json_type)
        f.close()

