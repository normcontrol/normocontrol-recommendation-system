from fastapi import HTTPException
from sqlalchemy.orm import Session
import operator
from src.api import crud
from src.system.CheckerInterface import CheckerInterface
from src.api.schemas import Document
from src.system.Rule import Rule
from src.system.errors.parameter_value_error import ParameterValueError


class Checker(CheckerInterface):
    document: Document
    gost: int
    rules: list[Rule]
    connection: Session

    def __init__(self, document: Document, gost, db):
        self.document = self.load_document(document)
        self.gost = gost
        self.db = db
        self.rules = self.load_rules(db, gost)

    def check(self):
        for element in self.document.content.values():
            element.result = {}
            for rule in self.rules:
                if rule.structural_element == element.current_element_mark:
                    match rule.operator:
                        case '=':
                            self.check_parameters(element, rule, operator.eq)
                        case '>=':
                            rule.value = float(rule.value)
                            self.check_parameters(element, rule, operator.ge)
                        case '<=':
                            rule.value = float(rule.value)
                            self.check_parameters(element, rule, operator.le)

        return self.document

    @classmethod
    def check_parameters(cls, element, rule, operator_label):
        try:
            if operator_label(element.dict()[rule.parameter], rule.value):
                element.result[rule.parameter + ' ' + str(rule.value)] = "OK!"
            else:
                if rule.is_recommend:
                    element.result[rule.parameter + ' ' + str(rule.value)] = "Warning!"
                else:
                    raise ParameterValueError(rule.structural_element, rule.parameter,
                                              element.dict()[rule.parameter], rule.value)
        except ParameterValueError as e:
            element.result[rule.parameter] = e

    def load_document(self, document):
        return document

    def create_report(self):
        pass

    def load_rules(self, db, gost):
        all_gost_params = crud.get_gost_params(db, gost_id=gost)
        if all_gost_params is None:
            raise HTTPException(status_code=404, detail="Gost params not found!")
        rules_list = []
        for param in all_gost_params:
            rules_list.append(Rule(param.id_elements.description, param.id_elements.element,
                                   param.id_params.param, param.is_recommented, param.operator, param.value))
        self.rules = rules_list
        return rules_list
