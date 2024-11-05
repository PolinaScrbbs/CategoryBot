from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from ..user.schemes import BaseUser


class TestCreate(BaseModel):
    title: str
    description: str


class TestWithoutResult(BaseModel):
    id: int
    title: str
    description: str


class TestInDB(TestWithoutResult):
    pass


class TestResultCreate(BaseModel):
    test_id: int = 1
    result: str = "0 0 0 0 0"


class TestResultInDB(BaseModel):
    id: int
    user: BaseUser
    test: TestWithoutResult
    result: str
    created_at: datetime
    end_at: Optional[datetime]

    class Config:
        from_attributes = True
