from typing import Any
from pydantic import BaseModel

class Paragraph(BaseModel):
    page_breake_before: Any | None = None
    keep_lines_together: Any | None = None
    keep_with_next: Any | None = None
    outline_level: Any | None = None
    text: str | None = None
    count_of_sp_sbl: float | None = None
    count_sbl: float | None = None
    lowercase: bool | None = None
    uppercase: bool | None = None
    last_sbl: str | None = None
    first_key: str | None = None
    bold: Any | None = None
    italics: Any | None = None
    indent: float | None = None
    line_spacing: float | None = None
    alignment: Any | None = None
    mrgrg: Any | None = None
    mrglf: Any | None = None
    mrgtop: Any | None = None
    mrgbtm: Any | None = None
    font_name: str | None = None
    text_size: float | None = None
    underlining: Any | None = None
    sub_text: Any | None = None
    super_text: Any | None = None
    color_text: str | None = None
    no_change_fontname: bool | None = None
    no_change_text_size: bool | None = None
    current_element_mark: str | None = None
    result: None = None
    class Config:
        orm_model = True

class Document(BaseModel):
    owner: str
    time: str
    content: dict[str, Paragraph]
    class Config:
        orm_model = True

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
