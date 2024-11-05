from typing import List, Optional, Union
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user import utils as ut

from .schemes import TestCreate, TestWithoutResult, TestResultCreate, TestResultInDB
from . import queries as qr

router = APIRouter(prefix="/tests")


@router.post("/", response_model=TestWithoutResult, status_code=status.HTTP_201_CREATED)
async def create_test(
    test_data: TestCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    created_test = await qr.create_test(session, test_data)
    return created_test


@router.post(
    "/results/", response_model=TestResultInDB, status_code=status.HTTP_201_CREATED
)
async def create_test_result(
    test_result_data: TestResultCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    created_test_result = await qr.create_test_result(
        session, current_user.id, test_result_data
    )
    return created_test_result
