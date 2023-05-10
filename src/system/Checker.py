from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
import operator
from src.api import crud
from src.system.CheckerInterface import CheckerInterface
from src.api.schemas import Document, Paragraph
from src.system.Rule import Rule
from src.system.errors.parameter_value_error import ParameterValueError
import fitz, os


class Checker(CheckerInterface):
    document: Document
    gost: int
    path: str
    rules: list[Rule]
    connection: Session
    input_file_name: str
    output_file_name: str

    def __init__(self, document: Document, gost, path, db):
        self.document = self.load_document(document)
        self.gost = gost
        self.path = path
        self.db = db
        self.rules = self.load_rules(db, gost)

        file_path = self.path.split('\\')
        self.input_file_name = file_path[len(file_path) - 1]
        # Output PDF file
        self.output_file_name = self.input_file_name[0:(len(self.input_file_name) - len(
            file_path[len(file_path) - 1])) - 4] + '_commented.pdf'

    def check(self):
        def check_parameters(element, rule, operator_label):
            try:
                try:
                    value = float(rule.value)
                except:
                    value = rule.value
                if rule.parameter in ['font_name', 'text_size']:
                    if len(element.dict()[rule.parameter]) > 1:
                        element.result['Error'][rule.parameter] = 'Используется несколько разных видов ' + \
                                                                  rule.parameter
                    else:
                        for list_value in element.dict()[rule.parameter]:
                            if operator_label(list_value, value):
                                element.result['Success'][rule.parameter + ' ' + str(rule.value)] = "OK!"
                            else:
                                if rule.is_recommend:
                                    element.result['Warning'][rule.parameter + ' ' + str(list_value)] = "Warning!"
                                else:
                                    raise ParameterValueError(rule.structural_element, rule.parameter,
                                                              list_value, rule.value)
                else:
                    if operator_label(element.dict()[rule.parameter], value):
                        element.result['Success'][rule.parameter + ' ' + str(rule.value)] = "OK!"
                    else:
                        if rule.is_recommend:
                            element.result['Warning'][rule.parameter + ' ' + str(rule.value)] = "Warning!"
                        else:
                            raise ParameterValueError(rule.structural_element, rule.parameter,
                                                      element.dict()[rule.parameter], rule.value)
            except ParameterValueError as e:
                element.result['Error'][rule.parameter] = str(e)

        for element in self.document.content.values():
            if isinstance(element, Paragraph):
                doc_type = self.path.split('/')
                if 'pdf' in doc_type[len(doc_type) - 1]:
                    document_type = 'pdf'
                elif 'odt' in doc_type[len(doc_type) - 1]:
                    document_type = 'odt'
                else:
                    raise HTTPException(status_code=404, detail="Document type not found!")
                element.result = {
                    'Success': {},
                    'Warning': {},
                    'Error': {}
                }

                list_of_rule = []
                for rule in self.rules:
                    if document_type == 'pdf':
                        if rule.pdf is True:
                            list_of_rule.append(rule)
                    else:
                        list_of_rule.append(rule)

                for rule in list_of_rule:
                    if rule.structural_element == element.current_element_mark:
                        match rule.operator:
                            case '=':
                                check_parameters(element, rule, operator.eq)
                            case '>=':
                                rule.value = float(rule.value)
                                check_parameters(element, rule, operator.ge)
                            case '<=':
                                rule.value = float(rule.value)
                                check_parameters(element, rule, operator.le)
        return self.document

    def load_document(self, document):
        return document

    def create_report(self):
        file_path = self.path.split('\\')
        directory = self.path[0:(len(self.path) - (len(file_path[len(file_path) - 1]) + 4))]
        os.chdir(directory)
        pdf_in = fitz.open(os.path.join('.\\in', self.input_file_name))
        for element in self.document.content.values():
            if isinstance(element, Paragraph):
                comment = ''
                for param, err in element.result['Error'].items():
                    comment += param + ' - ' + err + '\n\n'
                if comment != '':
                    pdf_in = self.comment_pdf(pdf_in=pdf_in,
                                              element=element,
                                              comment_title='Error',
                                              comment_info=comment
                                              )
        pdf_in.save(os.path.join('.\\out', self.output_file_name), garbage=3, deflate=True)
        pdf_in.close()

    def comment_pdf(self, pdf_in, element, comment_title: str, comment_info: str):
        """
        Search for a particular string value in a PDF file and add comments to it.
        """
        red_color = (1, 0, 0)
        for pg, page in enumerate(pdf_in):
            page_id = pg + 1
            if self.document.page_count:
                if page_id not in range(self.document.page_count):
                    continue

            for key, rect in element.bbox.items():
                if key == page_id:
                    annot = page.add_rect_annot(fitz.Rect(round(rect[0]), round(page.rect.y1 - rect[1]),
                                                          round(rect[2]), round(page.rect.y1 - rect[3]))
                                                .round())
                    annot.set_border({"dashes": [0], "width": 0.9})
                    annot.set_colors({"colors": red_color, "stroke": red_color, "fill": red_color}),
                    annot.set_opacity(0.3)
                    # Add comment to the found match
                    info = annot.info
                    info["title"] = comment_title
                    info["content"] = comment_info
                    annot.set_info(info)
                    annot.update()
        return pdf_in

    def load_rules(self, db, gost):
        all_gost_params = crud.get_gost_params(db, gost_id=gost)
        if all_gost_params is None:
            raise HTTPException(status_code=404, detail="Gost params not found!")
        rules_list = []
        for param in all_gost_params:
            rules_list.append(Rule(param.id_elements.description, param.id_elements.element,
                                   param.id_params.param, param.is_recommented, param.operator, param.value,
                                   param.id_params.pdf))
        self.rules = rules_list
        return rules_list
