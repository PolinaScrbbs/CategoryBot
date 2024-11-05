from typing import List, Union
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user import utils as ut

from .schemes import CategoryCreate, CategoryWithoutQuestions, CategoryInDB
from . import queries as qr

router = APIRouter(prefix="/categories")


@router.post("/", response_model=CategoryCreate, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    await ut.admin_check(current_user)
    created_reservation = await qr.create_category(
        session, category_data
    )
    return created_reservation

@router.get("/", response_model=Union[List[CategoryWithoutQuestions], List[CategoryInDB]])
async def get_categories(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    categories = await qr.get_categories(session, current_user.role)
    return categories
