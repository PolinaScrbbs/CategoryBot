from turtle import title
from typing import List, Union
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..user.models import User, Role
from ..user.utils import user_exists_by_id

from .models import Category, CategoryQuestion
from .schemes import CategoryCreate, CategoryInDB, CategoryWithoutQuestions
from .utils import category_exists


async def create_category(
    session: AsyncSession, category_data: CategoryCreate
) -> Category:
    await category_exists(session, category_data.title)

    new_category = Category(
        title=category_data.title,
        description=category_data.description
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

    result = await session.execute(query)
    return result.scalars().all()
    

