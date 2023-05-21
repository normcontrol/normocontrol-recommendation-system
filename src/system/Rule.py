from typing import Any

class Rule:
    structural_element_description: str
    structural_element: str
    structural_element_id: int
    parameter_id: int
    parameter: str
    is_recommend: bool
    operator: str
    parameter: bool
    value: Any

    def __init__(self, structural_element_description: str, structural_element: str,
                 parameter: str, is_recommend: bool, operator: str, value: Any, pdf: bool, structural_element_id: int,
                 parameter_id: int):
        self.structural_element_description = structural_element_description
        self.structural_element = structural_element
        self.parameter = parameter
        self.pdf = pdf
        self.is_recommend = is_recommend
        self.operator = operator
        self.value = value
        self.structural_element_id = structural_element_id
        self.parameter_id = parameter_id
