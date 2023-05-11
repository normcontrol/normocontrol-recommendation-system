from fastapi import HTTPException
from sqlalchemy.orm import Session
import operator
from src.api import crud
from src.system.CheckerInterface import CheckerInterface
from src.api.schemas import Document, Paragraph
from src.system.Rule import Rule
from src.system.errors.parameter_value_error import ParameterValueError
import aspose.words as aw
from datetime import date
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
        file_name = self.input_file_name[0:(len(self.input_file_name) - len(file_path[len(file_path) - 1])) - 4]
        if 'odt' in path:
            self.output_file_name = file_name + '_commented.docx'
        elif 'pdf' in path:
            self.output_file_name = file_name + '_commented.pdf'

    def check(self):
        def check_parameters(element, rule, operator_label):
            try:
                try:
                    value = float(rule.value)
                except:
                    value = rule.value
                if rule.parameter in ['font_name', 'text_size']:
                    if len(element.dict()[rule.parameter]) > 1:
                        str_of_parameters = ''
                        for param in element.dict()[rule.parameter]:
                            str_of_parameters += f'{param}, '
                        element.result['Error'][rule.parameter] = f'Several different types of {rule.parameter} are used:\n' \
                                                                  f'[{str_of_parameters}]'

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

    def create_pdf_report(self):
        file_path = self.path.split('\\')
        directory = self.path[0:(len(self.path) - (len(file_path[len(file_path) - 1]) + 4))]
        os.chdir(directory)
        pdf_in = fitz.open(os.path.join('.\\in', self.input_file_name))
        for element in self.document.content.values():
            if isinstance(element, Paragraph):

                warning_str = ''
                for param, err in element.result['Warning'].items():
                    warning_str += param + ' - ' + err + '\n\n'

                error_str = ''
                for param, err in element.result['Error'].items():
                    error_str += param + ' - ' + err + '\n\n'

                red_color = (1, 0, 0)
                warning_color = (0, 1, 1)
                if warning_str != '' and error_str == '':
                    pdf_in = self.comment_pdf(pdf_in=pdf_in,
                                              element=element,
                                              comment_title='Warning',
                                              comment_info=warning_str,
                                              color=warning_color
                                              )
                elif error_str != '' and warning_str == '':
                    pdf_in = self.comment_pdf(pdf_in=pdf_in,
                                              element=element,
                                              comment_title='Error',
                                              comment_info=error_str,
                                              color=red_color
                                              )
                elif error_str != '' and warning_str != '':
                    pdf_in = self.comment_pdf(pdf_in=pdf_in,
                                              element=element,
                                              comment_title='Error',
                                              comment_info=error_str + '\n [Warning !!!] \n' + warning_str,
                                              color=red_color
                                              )

        pdf_in.save(os.path.join('.\\out', self.output_file_name), garbage=3, deflate=True)
        pdf_in.close()

    def create_docx_report(self):
        file_path = self.path.split('\\')
        directory = self.path[0:(len(self.path) - (len(file_path[len(file_path) - 1]) + 4))]
        os.chdir(directory)

        doc = aw.Document(directory + '\\in\\' + self.input_file_name)
        for element in self.document.content.values():
            if isinstance(element, Paragraph):
                warning_str = ''
                for param, err in element.result['Warning'].items():
                    warning_str += param + ' - ' + err + '\n\n'

                error_str = ''
                for param, err in element.result['Error'].items():
                    error_str += param + ' - ' + err + '\n\n'

                red_color = (1, 0, 0)
                warning_color = (0, 1, 1)
                if warning_str != '' and error_str == '':
                    pdf_in = self.comment_docx(doc=doc,
                                              element=element,
                                              comment_title='Warning',
                                              comment_info=warning_str,
                                              color=warning_color
                                              )
                elif error_str != '' and warning_str == '':
                    pdf_in = self.comment_docx(doc=doc,
                                              element=element,
                                              comment_title='Error',
                                              comment_info=error_str,
                                              color=red_color
                                              )
                elif error_str != '' and warning_str != '':
                    pdf_in = self.comment_docx(doc=doc,
                                              element=element,
                                              comment_title='Error',
                                              comment_info=error_str + '\n [Warning !!!] \n' + warning_str,
                                              color=red_color
                                              )
        doc.save(directory + '\\out\\' + self.output_file_name)

    def comment_pdf(self, pdf_in, element, comment_title: str, comment_info: str, color):
        """
        Search for a particular string value in a PDF file and add comments to it.
        """

        for pg, page in enumerate(pdf_in):
            page_id = pg + 1
            if self.document.page_count:
                if page_id not in range(self.document.page_count+1):
                    continue

            for key, rect in element.bbox.items():
                if key == page_id:
                    annot = page.add_rect_annot(fitz.Rect(round(rect[0]), round(page.rect.y1 - rect[1]),
                                                          round(rect[2]), round(page.rect.y1 - rect[3]))
                                                .round())
                    annot.set_border({"dashes": [0], "width": 0.9})
                    annot.set_colors({"colors": color, "stroke": color, "fill": color}),
                    annot.set_opacity(0.3)
                    # Add comment to the found match
                    info = annot.info
                    info["title"] = comment_title
                    info["content"] = comment_info
                    annot.set_info(info)
                    annot.update()
        return pdf_in

    def comment_docx(self, doc, element, comment_title, comment_info, color):
        word = element.text
        # Use Range.replace method to make each searched word a separate Run node.
        opt = aw.replacing.FindReplaceOptions()
        opt.use_substitutions = True
        doc.range.replace(word, "$0", opt)

        # Get all runs
        runs = doc.get_child_nodes(aw.NodeType.RUN, True)

        for r in runs:
            run = r.as_run()
            # process the runs with text that matches the searched word.
            if run.text == word:
                run.font.highlight_color = color
                comment = aw.Comment(doc, "Нормоконтролер", "Нормоконтролер", date.today())
                comment.paragraphs.add(aw.Paragraph(doc))
                comment.first_paragraph.runs.add(aw.Run(doc, comment_title + '\n' + comment_info))
                # Wrap the Run with CommentRangeStart and CommentRangeEnd
                run.parent_node.insert_before(aw.CommentRangeStart(doc, comment.id), run)
                run.parent_node.insert_after(aw.CommentRangeEnd(doc, comment.id), run)
                # Add a comment.
                run.parent_node.insert_after(comment, run)
        return doc

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

