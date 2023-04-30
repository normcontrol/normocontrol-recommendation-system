from pydantic import BaseModel

class Paragraph(BaseModel):
    # indent: str
    page_breake_before: str
    keep_lines_together: str
    keep_with_next: str
    outline_level: str
    text: str
    count_of_sp_sbl: str
    count_sbl: str
    lowercase: str
    uppercase: str
    last_sbl: str
    first_key: str
    bold: str
    italics: str


class Document(BaseModel):
    owner: str
    time: str
    content: dict[str, Paragraph]

