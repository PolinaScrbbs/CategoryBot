from fastapi import HTTPException, status
from sqlalchemy.sql import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Category, CategoryQuestion


async def category_exists_by_title(session: AsyncSession, title: str) -> None:
    result = await session.execute(select(exists().where(Category.title == title)))
    category_exists = result.scalar()

    if category_exists:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Категория уже существует")


async def category_exists_by_id(session: AsyncSession, id: int) -> None:
    result = await session.execute(select(exists().where(Category.id == id)))
    category_exists = result.scalar()

    if not category_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Категория не найдена")


async def category_question_exists(session: AsyncSession, content: str) -> None:
    result = await session.execute(
        select(exists().where(CategoryQuestion.content == content))
    )
    category_question_exists = result.scalar()

    if category_question_exists:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Вопрос уже существует")


async def category_question_exists_by_id(session: AsyncSession, id: int) -> None:
    result = await session.execute(select(exists().where(CategoryQuestion.id == id)))
    category_exists = result.scalar()

    if not category_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Вопрос не найдена")
