from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
import operator
from src.api import crud
from src.system.CheckerInterface import CheckerInterface
from src.api.schemas import Document
from src.system.Rule import Rule
from src.system.errors.parameter_value_error import ParameterValueError
import fitz,os
import PyPDF2

class Checker(CheckerInterface):
    document: Document
    gost: int
    path: str
    rules: list[Rule]
    connection: Session
    input_file_name: str
    output_file_name: str
    directory: str
    pages_list: List

    def __init__(self, document: Document, gost, path, db):
        self.document = self.load_document(document)
        self.gost = gost
        self.path =path
        self.db = db
        self.rules = self.load_rules(db, gost)

        file_path = self.path.split('/')
        self.input_file_name = file_path[len(file_path) - 1]
        # Output PDF file
        self.output_file_name = self.input_file_name[0:(len(self.input_file_name) - 1) - 3] + '_commented.pdf'
        self.directory = self.path[0:(len(self.path) - (len(self.input_file_name) +
                                                        len(file_path[len(file_path) - 2]) + 2))]

        os.chdir(self.directory)
        total_pages = 0
        with open(os.path.join('./in', self.input_file_name), 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(pdf_reader.pages)

        # Selected pages
        pages = f'1-{total_pages}'
        self.pages_list = self.build_range(pages) if pages else None

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
    def check_parameters(self, element, rule, operator_label):
        try:
            if operator_label(element.dict()[rule.parameter], rule.value):
                element.result[rule.parameter + ' ' + str(rule.value)] = "OK!"
            else:
                if rule.is_recommend:
                    element.result[rule.parameter + ' ' + str(rule.value)] = "Warning!"
                else:
                    self.comment_pdf(input_file=os.path.join('./in', self.input_file_name)
                                     , search_text=element.text
                                     , comment_title='Ошибка!'
                                     , comment_info=rule.parameter + ' ' + str(rule.value)
                                     , output_file=os.path.join('./out', self.output_file_name)
                                     , pages=self.pages_list
                                     )
                    raise ParameterValueError(rule.structural_element, rule.parameter,
                                              element.dict()[rule.parameter], rule.value)
        except ParameterValueError as e:
            element.result[rule.parameter] = e

    def load_document(self, document):
        return document

    def create_report(self):
        doc_type = self.path.split('/')
        if 'pdf' in doc_type[len(doc_type) - 1]:
            self.create_pdf_report()
        elif 'odt' in doc_type[len(doc_type) - 1]:
            self.create_odt_report()
        else:
            raise HTTPException(status_code=404, detail="Document type not found!")

    def create_pdf_report(self):
        pass

    def comment_pdf(self, input_file: str, search_text: str, comment_title: str, comment_info: str, output_file: str,
                    pages: list = None):
        """
        Search for a particular string value in a PDF file and add comments to it.
        """
        pdf_in = fitz.open(input_file)
        found_matches = 0
        red_color = (1, 0, 0)

        # Iterate throughout the document pages
        for pg, page in enumerate(pdf_in):
            page_id = pg + 1
            # If required for specific pages
            if pages:
                if page_id not in pages:
                    continue

            # Use the search for function to find the text
            matched_values = page.search_for(search_text, hit_max=20)
            found_matches += len(matched_values) if matched_values else 0

            # Loop through the matches values
            # item will contain the coordinates of the found text
            for item in matched_values:
                # Enclose the found text with a bounding box
                annot = page.add_rect_annot(item)
                annot.set_border({"dashes": [0], "width": 0.9})
                annot.set_colors({"stroke": red_color})

                # Add comment to the found match
                info = annot.info
                info["title"] = comment_title
                info["content"] = comment_info
                annot.set_info(info)
                annot.update()

        pdf_in.save(output_file, garbage=3, deflate=True)
        pdf_in.close()

    def build_range(self, rangeval: str):
        """
        Build the range of pages based on the parameter inputted rangeval
        """
        result = set()
        for part in rangeval.split(','):
            x = part.split('-')
            result.update(range(int(x[0]), int(x[-1]) + 1))
        return list(sorted(result))

    def create_odt_report(self):
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
