from src.system.CheckerInterface import CheckerInterface
from src.api.schemas import Document
from src.system.Rule import Rule

class Checker(CheckerInterface):
    document: Document
    gost: int
    rules: list[Rule]
    connection: None

    def __init__(self, document, gost, connection):
        self.document = self.load_document(document)
        self.gost = gost
        self.connection = connection
        self.rules = self.load_rules(connection)

    def check(self):
        pass

    def load_document(self, document):
        pass

    def create_report(self):
        pass

    def load_rules(self, connection):
        pass