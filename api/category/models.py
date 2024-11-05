from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from ..user.models import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(20), unique=True, nullable=False)
    description = Column(String(256), nullable=False)

    questions = relationship(
        "CategoryQuestion", back_populates="category", cascade="all, delete-orphan"
    )


class CategoryQuestion(Base):
    __tablename__ = "category_questions"

    id = Column(Integer, primary_key=True)
    category_id = Column(ForeignKey("categories.id"), nullable=False)
    content = Column(String(64), unique=True, nullable=False)
    answer = Column(String(128), nullable=False)

    category = relationship("Category", back_populates="questions")
