""" Load .yaml config file and apply transformations available in "transformations" module."""
import logging
import os
import random
import yaml

from vision.aug.transformations import *
from vision.aug.transformations.transformation import Transformation


class TransformationManager(object):
    def __init__(self, filename="", dirname=None, distribution_config=None):
        self.filename = filename
        self.parameters = {}
        if filename:
            self.parameters = self.load_parameters(filename, dirname)
        self.params_config = []
        self.tools = self.load_tools()
        self.distribution = self.process_distribution(distribution_config) if distribution_config else None

    @staticmethod
    def process_distribution(distribution_config):
        distribution_dict = {}
        for distribution, value in distribution_config.items():
            for func in value["functions"]:
                distribution_dict[func] = (distribution, value["params"])

        return distribution_dict

    def apply_transformations(self, image, layer, json_data):
        operations = self.parameters.get(layer, [])
        for operation in operations:
            for img_id, loaded_parameters in operation.items():
                if isinstance(loaded_parameters, list) and "choice" in img_id:
                    loaded_parameters = random.choice(loaded_parameters)
                    img_id = list(loaded_parameters.keys())[0]
                    loaded_parameters = loaded_parameters[img_id]

                if not isinstance(loaded_parameters, list):
                    loaded_parameters = [loaded_parameters]

                for parameters in loaded_parameters:
                    if parameters != {} and None not in parameters.values():
                        image = self.try_to_call_method(img_id, image, parameters.copy(), json_data)

        return image

    def try_to_call_method(self, method_id, image, parameters, json_data):
        class_name = method_id.split(".")[0]
        method_name = method_id.split(".")[1]
        not_found_flag = True
        for tool in self.tools:
            if tool.__name__ == class_name:
                not_found_flag = False
                try:
                    if random.random() < parameters["probability"]:
                        params = self.create_param_config(parameters, method_id)
                        parameters.pop("probability", None)
                        
                        # fill unusual params
                        if 'json_data' in params.keys():
                            params['json_data'] = json_data
                            
                        if isinstance(image, list):
                            image = [getattr(tool(), method_name)(i, **params) for i in image]
                        else:
                            image = getattr(tool(), method_name)(image, **params)

                        self.params_config.append({method_id: params})

                except AttributeError:
                    logging.warning("Class '{}' doesn\"t contain matching method ('{}')".format(
                        class_name, method_name))

        if not_found_flag:
            logging.warning("'{}' not found.".format(method_id))

        return image

    def create_param_config(self, parameters, method_id):
        config_params = {}
        for key, value in parameters.items():
            if key != "probability":
                if not isinstance(value, list):
                    config_params[key] = parameters[key]
                else:
                    config_params[key] = self.get_random_value_in_range(value, method_id)

        return config_params

    def get_random_value_in_range(self, extrema, method_id):
        def get_probability():
            if self.distribution is not None:
                if method_id in self.distribution:
                    func, params = self.distribution[method_id]
                    prob = func(*params)
                    return (extrema[1] - extrema[0]) * prob + extrema[0]

            return random.uniform(extrema[0], extrema[1])

        if isinstance(extrema[0], int) and isinstance(extrema[1], int):
            return int(get_probability())

        elif isinstance(extrema[0], float) or isinstance(extrema[1], float):
            return get_probability()

        elif isinstance(extrema[0], list) and isinstance(extrema[1], list):
            return [
                self.get_random_value_in_range([extrema[0][i], extrema[1][i]], method_id)
                for i in range(0, len(extrema[0]))
            ]

    @staticmethod
    def load_parameters(filename, dirname=None):
        if not dirname:
            dirname = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dirname, "configs", filename)
        if os.path.exists(path):
            with open(path) as f:
                return yaml.load(f)
        else:
            logging.error("Generator config file '{}' not found.".format(path))
        return None

    def load_tools(self):
        return Transformation.__subclasses__()

    @staticmethod
    def merge_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z
