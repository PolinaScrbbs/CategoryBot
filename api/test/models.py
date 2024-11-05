from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, CHAR, DateTime, func
from sqlalchemy.orm import relationship

from ..category.models import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)
    description = Column(String(64), nullable=False)

    results = relationship(
        "TestResult", back_populates="test", cascade="all, delete-orphan"
    )


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True)
    content = Column(String(64), unique=True, nullable=False)
    result = Column(CHAR(9), nullable=False)


class TestResult(Base):
    __tablename__ = "test_result"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    result = Column(CHAR(9), default="0 0 0 0 0", nullable=False)
    created_at = Column(
        DateTime, server_default=func.now(), default=datetime.utcnow, nullable=False
    )
    end_at = Column(DateTime, default=None)

    user = relationship("User", back_populates="test_results")
    test = relationship("Test", back_populates="results")
