from typing import List, Optional, Union
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.category.models import Category

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user import utils as ut

from .schemes import (
    CategoryCreate,
    CategoryWithoutQuestions,
    CategoryInDB,
    CategoryQuestionCreate,
    CategoryQuestionInDB,
)
from . import queries as qr

router = APIRouter(prefix="/categories")


@router.post("/", response_model=CategoryCreate, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    created_category = await qr.create_category(session, category_data)
    return created_category


@router.get(
    "/", response_model=Union[List[CategoryWithoutQuestions], List[CategoryInDB]]
)
async def get_categories(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    categories = await qr.get_categories(session, current_user.role)
    return categories


@router.get(
    "/{category_id}", response_model=Union[CategoryWithoutQuestions, CategoryInDB]
)
async def get_category(
    category_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    category = await qr.get_category(session, current_user.role, category_id)
    return category


@router.post(
    "/questions/",
    response_model=CategoryQuestionCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_category_question(
    category_question_data: CategoryQuestionCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    created_question = await qr.create_category_question(
        session, category_question_data
    )
    return created_question


@router.get("/questions/", response_model=List[CategoryQuestionInDB])
async def get_category_questions(
    category_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    category_questions = await qr.get_category_questions(session, category_id)

    return category_questions


@router.get("/questions/{question_id}", response_model=CategoryQuestionInDB)
async def get_category_question(
    question_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    category_question = await qr.get_category_question(session, question_id)
    return category_question
