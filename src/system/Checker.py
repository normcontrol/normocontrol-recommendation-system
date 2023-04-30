from src.system.CheckerInterface import CheckerInterface
from src.api.schemas import Document
from src.system.Rule import Rule


class Checker(CheckerInterface):
    document: Document
    gost: int
    rules: list[Rule]

    def check(self):
        pass

    def load_document(self):
        pass

    def create_report(self):
        pass

    def load_rules(self):
        pass