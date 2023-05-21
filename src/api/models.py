from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from src.api.database import Base

class Gosts(Base):
    __tablename__ = "gosts"
    id = Column(Integer, primary_key=True, index=True)
    gost = Column(String)
    gosts = relationship("Gost_params", back_populates="id_gosts")
    goststatistics = relationship("DocumentStatistics", back_populates="id_gosts")

class Params(Base):
    __tablename__ = "params"
    id = Column(Integer, primary_key=True, index=True)
    param = Column(String)
    pdf = Column(Boolean)
    params = relationship("Gost_params", back_populates="id_params")
    paramstatistics = relationship("DocumentStatistics", back_populates="id_params")

class Elements(Base):
    __tablename__ = "elements"
    id = Column(Integer, primary_key=True, index=True)
    element = Column(String)
    description = Column(String)
    elements = relationship("Gost_params", back_populates="id_elements")
    elementstatistics = relationship("DocumentStatistics", back_populates="id_elements")

class Gost_params(Base):
    __tablename__ = "gost_params"
    id = Column(Integer, primary_key=True, index=True)
    id_gost = Column(Integer, ForeignKey("gosts.id"))
    id_element = Column(Integer, ForeignKey("elements.id"))
    id_param = Column(Integer, ForeignKey("params.id"))
    is_recommented = Column(Boolean)
    operator = Column(String)
    value = Column(String)
    id_gosts = relationship("Gosts", back_populates="gosts")
    id_elements = relationship("Elements", back_populates="elements")
    id_params = relationship("Params", back_populates="params")


class Documents(Base):
    __tablename__ = "Documents"
    id_document = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer)
    title = Column(String)
    input_document = Column(String)
    output_document = Column(String)
    date_created = Column(Date)
    # id_status = Column(Integer, ForeignKey("DocumentStatistics.id"))
    id_status = relationship("DocumentStatistics", back_populates="id_documents")

class DocumentStatistics(Base):
    __tablename__ = "DocumentStatistics"
    id = Column(Integer, primary_key=True, index=True)

    id_document = Column(Integer, ForeignKey("Documents.id_document"))
    id_gost = Column(Integer, ForeignKey("gosts.id"))
    id_element = Column(Integer, ForeignKey("elements.id"))
    id_param = Column(Integer, ForeignKey("params.id"))

    id_documents = relationship("Documents", back_populates="id_status")
    id_gosts = relationship("Gosts", back_populates="goststatistics")
    id_elements = relationship("Elements", back_populates="elementstatistics")
    id_params = relationship("Params", back_populates="paramstatistics")
    value = Column(String)
