from fastapi import HTTPException, status
from sqlalchemy.sql import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Category

async def category_exists(session: AsyncSession, title: str) -> None:
    result = await session.execute(
        select(exists().where(Category.title == title))
    )
    category_exists = result.scalar()

    if category_exists:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Билет уже забронирован")
