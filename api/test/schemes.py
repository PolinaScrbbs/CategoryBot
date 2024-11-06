from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from ..user.schemes import BaseUser


class TestCreate(BaseModel):
    title: str
    description: str


class TestWithoutQuestionsAndResult(BaseModel):
    id: int
    title: str
    description: str

class TestQuestionsWithoutTest(BaseModel):
    id: int
    content: str
    result: str
    
class TestInDB(TestWithoutQuestionsAndResult):
    questions: List[TestQuestionsWithoutTest]

class TestResultCreate(BaseModel):
    test_id: int = 1
    result: str = "0 0 0 0 0"

class TestResultInDB(BaseModel):
    id: int
    user: BaseUser
    test: TestWithoutQuestionsAndResult
    result: str
    created_at: datetime
    end_at: Optional[datetime]

    class Config:
        from_attributes = True


