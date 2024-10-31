from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)

    questions = relationship("Questions", back_populates="module", cascade="all, delete-orphan")

class Questions(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    module_id  = Column(Integer, ForeignKey("modules.id"), nullable=False)
    title = Column(String(70), unique=True, nullable=False)
    answer = Column(String(100), nullable=False)

    module = relationship("Module", back_populates="questions")
