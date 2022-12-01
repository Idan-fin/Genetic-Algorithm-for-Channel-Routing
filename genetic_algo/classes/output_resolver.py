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
        outfile = open(self.output_path, "w")
        output = dict()
        output["input_params"] = self.output.best_solution.input_params.__dict__
        output["solution"] = self.output.best_solution.genotype.__dict__
        json.dump(output, outfile, indent=2)
        outfile.close()
