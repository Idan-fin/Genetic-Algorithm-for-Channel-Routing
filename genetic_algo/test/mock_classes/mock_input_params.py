from genetic_algo.classes.input_params import InputParams


class MockInputParams(InputParams):

    def _parse_input_file(self):
        pass

    def _parse_parameters_from_kwargs(self, **kwargs):
        self.pins_position = kwargs['pins_position']
        self.population_size = kwargs['population_size']
        self.net_length_factor = kwargs['net_length_factor']
        self.via_numbers_factor = kwargs['via_numbers_factor']
        self.max_descendants = kwargs['max_descendants']
        self.max_generations = kwargs['max_generations']
        self.mut_1_prob = kwargs['mut_1_prob']
        self.mut_2_prob = kwargs['mut_2_prob']
        self.mut_3_prob = kwargs['mut_3_prob']
        self.mut_4_prob = kwargs['mut_4_prob']
        self.expected_final_row_num = kwargs['expected_final_row_num']
        self.preferred_direction_layer = kwargs["preferred_direction_layer"]
