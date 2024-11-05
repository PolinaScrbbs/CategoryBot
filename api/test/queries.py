from typing import List, Optional, Union
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Test, TestResult
from .schemes import TestCreate, TestResultCreate, TestResultInDB
from .utils import test_exists_by_title, test_result_exists

async def create_test(
    session: AsyncSession, 
    test_data: TestCreate
) -> TestCreate:
    await test_exists_by_title(session, test_data.title)

    new_test = Test(
        title = test_data.title, description = test_data.description
    )

    session.add(new_test)
    await session.commit()
    await session.refresh(new_test)
    return new_test

async def create_test_result(
    session: AsyncSession,
    current_user_id: int,
    test_result_data: TestResultCreate
) -> TestResultInDB:
    new_test_result = TestResult(
        user_id = current_user_id,
        test_id = test_result_data.test_id,
        result = test_result_data.result,
    )

    session.add(new_test_result)
    await session.commit()
    await session.refresh(new_test_result)

    test_result = await get_test_result_by_id(session, new_test_result.id)
    return test_result

async def get_test_result_by_id(
    session: AsyncSession,
    test_result_id: int
) -> TestResultInDB:
    await test_result_exists(session, test_result_id)

    result = await session.execute(
        select(TestResult)
        .options(
            selectinload(TestResult.user), 
            selectinload(TestResult.test)
        )
        .where(
            TestResult.id == test_result_id
        )
    )

    return result.scalar()
    

