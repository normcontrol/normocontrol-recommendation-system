from typing import Any, List, Union, Literal, Annotated
from pydantic import BaseModel, Field


class GostID(BaseModel):
    gost_id: int

class StructuralElement(BaseModel):
    element_class: Literal['StructuralElement']
    page_breake_before: Any | None = None
    keep_lines_together: Any | None = None
    keep_with_next: Any | None = None
    outline_level: Any | None = None
    indent: float | None = None
    line_spacing: float | None = None
    alignment: Any | None = None
    mrgrg: Any | None = None
    mrglf: Any | None = None
    mrgtop: Any | None = None
    mrgbtm: Any | None = None
    result: None = None
    class Config:
        orm_model = True

class Paragraph(StructuralElement):
    element_class: Literal['Paragraph']
    font_name: str | None = None
    text_size: float | None = None
    text: str | None = None
    count_of_sp_sbl: float | None = None
    count_sbl: float | None = None
    lowercase: bool | None = None
    uppercase: bool | None = None
    last_sbl: str | None = None
    first_key: str | None = None
    bold: Any | None = None
    italics: Any | None = None
    underlining: Any | None = None
    sub_text: Any | None = None
    super_text: Any | None = None
    color_text: str | None = None
    no_change_fontname: bool | None = None
    no_change_text_size: bool | None = None
    current_element_mark: str | None = None
    class Config:
        orm_model = True

class TableRow(BaseModel):
    name: str | None = None
    family: str | None = None
    properties_min_height: float | None = None
    class Config:
        orm_model = True

class TableCell(BaseModel):
    name: str | None = None
    family: str | None = None
    border: float | None = None
    writing_mode: str | None = None
    padding_top: float | None = None
    padding_left: float | None = None
    padding_bottom: float | None = None
    padding_right: float | None = None
    text: str | None = None
    class Config:
        orm_model = True

class Table(StructuralElement):
    element_class: Literal['Table']
    inner_text: list | None = None
    master_page_number: int | None = None
    family: str | None = None
    width: float | None = None
    bbox: tuple[int | float, int | float, int | float, int | float] | None = None
    page_bbox: tuple[int | float, int | float, int | float, int | float] | None = None
    cells: List[TableCell] | None = None
    rows: List[TableRow] | None = None
    class Config:
        orm_model = True

class List(Paragraph):
    element_class: Literal['List']
    type: str | None = None
    name: str | None = None
    level: str | None = None
    start_value: str | None = None
    style_char: str | None = None
    style_name: str | None = None
    class Config:
        orm_model = True

class Image(BaseModel):
    href: str | None = None
    type: str | None = None
    show: str | None = None
    actuate: str | None = None
    class Config:
        orm_model = True

class Frame(StructuralElement):
    element_class: Literal['Frame']
    style_name: str | None = None
    anchor_type: str | None = None
    bbox: tuple[int | float, int | float, int | float, int | float] | None = None
    width: float | None = None
    height: float | None = None
    rel_width: str | None = None
    rel_height: str | None = None
    image: Image | None = None
    page_number: int | None = None
    class Config:
        orm_model = True

class Document(BaseModel):
    owner: str
    time: str
    content: dict[str, Annotated[Union[Paragraph, Table, List, Frame], Field(discriminator='element_class')]]
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

class Path(BaseModel):
    path: str
    class Config:
        orm_model = True