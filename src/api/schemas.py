from pydantic import BaseModel

class Paragraph(BaseModel):
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

class Gost_params(BaseModel):
    id: int
    id_gost: int
    id_element: int
    id_param: int
    is_recommented: bool
    operator: str
    value: str
    class Config:
        orm_model = True

class Gosts(BaseModel):
    id: int
    gost: str
    gosts: list[Gost_params] = []

    class Config:
        orm_model = True

class Params(BaseModel):
    id: int
    param: str
    params: list[Gost_params] = []
    class Config:
        orm_model = True

class Elements(BaseModel):
    id: int
    element: str
    description: str
    elements: list[Gost_params] = []
    class Config:
        orm_model = True
