from turtle import title
from typing import List, Optional, Union
from unittest import result
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..user.models import User, Role
from ..user.utils import user_exists_by_id

from .models import Category, CategoryQuestion
from .schemes import (
    CategoryCreate,
    CategoryInDB,
    CategoryWithoutQuestions,
    CategoryQuestionCreate,
    CategoryQuestionInDB,
)
from .utils import (
    category_exists_by_title,
    category_exists_by_id,
    category_question_exists,
    category_question_exists_by_id,
)


async def create_category(
    session: AsyncSession, category_data: CategoryCreate
) -> Category:
    await category_exists_by_title(session, category_data.title)

    new_category = Category(
        title=category_data.title, description=category_data.description
    )

    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)

    return new_category


async def get_categories(
    session: AsyncSession, user_role: str
) -> Union[List[CategoryWithoutQuestions], List[CategoryInDB]]:
    if user_role == Role.ADMIN:
        query = select(Category).options(selectinload(Category.questions))
    else:
        query = select(Category)

    result = await session.execute(query)  # noqa: F811
    return result.scalars().all()


async def get_category(
    session: AsyncSession, user_role: str, category_id: int
) -> Union[CategoryWithoutQuestions, CategoryInDB]:
    await category_exists_by_id(session, category_id)

    if user_role == Role.ADMIN:
        query = select(Category).options(selectinload(Category.questions))
    else:
        query = select(Category)

    query = query.where(Category.id == category_id)

    result = await session.execute(query)  # noqa: F811
    return result.scalar()


async def create_category_question(
    session: AsyncSession, category_question_data: CategoryQuestionCreate
) -> CategoryQuestionCreate:
    await category_question_exists(session, category_question_data.content)

    new_category_question = CategoryQuestion(
        category_id=category_question_data.category_id,
        content=category_question_data.content,
        answer=category_question_data.answer,
    )

    session.add(new_category_question)
    await session.commit()
    await session.refresh(new_category_question)

    return new_category_question


async def get_category_questions(
    session: AsyncSession, category_id: Optional[int] = None
) -> List[CategoryQuestionInDB]:
    query = select(CategoryQuestion).options(selectinload(CategoryQuestion.category))

    if category_id:
        await category_exists_by_id(session, category_id)
        query = query.where(CategoryQuestion.category_id == category_id)

    result = await session.execute(query)  # noqa: F811
    questions = result.scalars().all()

    if not questions:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return questions


async def get_category_question(
    session: AsyncSession, question_id
) -> CategoryQuestionInDB:
    await category_question_exists_by_id(session, question_id)
    result = await session.execute(  # noqa: F811
        select(CategoryQuestion)
        .options(selectinload(CategoryQuestion.category))
        .where(CategoryQuestion.id == question_id)
    )

    question = result.scalars().first()
    return question
