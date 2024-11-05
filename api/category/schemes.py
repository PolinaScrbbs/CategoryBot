from typing import List, Optional
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    title: str
    description: str

class CategoryQuestionCreate(BaseModel):
    category_id: int
    content: str
    answer: str

class CategoryWithoutQuestions(BaseModel):
    id: int
    title: str
    description: str

class CategoryQuestionWithoutCategory(BaseModel):
    id: int
    content: str
    answer: str

class CategoryInDB(CategoryWithoutQuestions):
    questions: Optional[List[CategoryQuestionWithoutCategory]]

class CategoryQuestionInDB(BaseModel):
    id: int
    content: str
    answer: str
    category: CategoryWithoutQuestions




