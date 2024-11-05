from fastapi import HTTPException, status
from sqlalchemy.sql import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Test, TestResult

async def test_exists_by_title(session: AsyncSession, title: str) -> None:
    result = await session.execute(select(exists().where(Test.title == title)))
    category_exists = result.scalar()

    if category_exists:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Тест уже существует")
    
async def test_result_exists(session: AsyncSession, id: int) -> None:
    result = await session.execute(select(exists().where(TestResult.id == id)))
    category_exists = result.scalar()

    if not category_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Результат не найден")