from abc import ABC, abstractmethod


class CheckerInterface(ABC):

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def load_document(self, document):
        pass

    @abstractmethod
    def create_report(self):
        pass

    @abstractmethod
    def load_rules(self, db, gost):
        pass