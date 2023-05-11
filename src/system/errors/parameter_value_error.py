from typing import Any

class ParameterValueError(Exception):
    def __init__(self, element: str, parameter: str, value: Any, expected_value: Any):
        self.element = element
        self.parameter = parameter
        self.value = value
        self.expected_value = expected_value

    def __str__(self):
        return f"Error in element {self.element}! " \
               f"Parameter {self.parameter} contains value {self.value}. " \
               f"Excpected - {self.expected_value}! "