from typing import Any

class Rule:
    structural_element_description: str
    structural_element: str
    parameter: str
    is_recommend: bool
    operator: str
    parameter: bool
    value: Any

    def __init__(self, structural_element_description: str, structural_element: str,
                 parameter: str, is_recommend: bool, operator: str, value: Any, pdf: bool):
        self.structural_element_description = structural_element_description
        self.structural_element = structural_element
        self.parameter = parameter
        self.pdf = pdf
        self.is_recommend = is_recommend
        self.operator = operator
        self.value = value
