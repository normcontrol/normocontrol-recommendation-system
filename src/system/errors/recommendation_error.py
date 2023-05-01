from typing import Any

class RecommendationError(Exception):
    def __init__(self, element: str, parameter: str, value: Any, expected_value: Any):
        self.element = element
        self.parameter = parameter
        self.value = value
        self.expected_value = expected_value

    def __str__(self):
        return f"Рекомендация в элементе {self.element}!" \
               f"Параметр {self.parameter} содержит значение {self.value}." \
               f"Рекомендуемое значение - {self.expected_value}!"