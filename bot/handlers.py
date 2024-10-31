from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from .database import async_session
from .database.models import Module, Questions

router = Router()

@router.message(Command(commands=['start']))
async def start_handler(message: Message):
    async with async_session() as session:
        result = await session.execute(select(Module))
        modules = result.scalars().all()

    keyboard_builder = InlineKeyboardBuilder()
    for module in modules:
        keyboard_builder.button(text=module.title, callback_data=f"module_{module.id}")
    keyboard_builder.adjust(1)
    
    await message.answer("Выберите модуль:", reply_markup=keyboard_builder.as_markup())

@router.callback_query(lambda c: c.data and c.data.startswith('module_'))
async def module_handler(callback_query: CallbackQuery):
    module_id = int(callback_query.data.split('_')[1])

    async with async_session() as session:
        result = await session.execute(select(Questions).where(Questions.module_id == module_id))
        questions = result.scalars().all()

    if not questions:
        await callback_query.message.edit_text("Вопросов нет для выбранного модуля.")
        return

    keyboard_builder = InlineKeyboardBuilder()
    for question in questions:
        keyboard_builder.button(text=question.title, callback_data=f"question_{question.id}")
    keyboard_builder.adjust(1)
    
    await callback_query.message.edit_text("Выберите вопрос:", reply_markup=keyboard_builder.as_markup())

@router.callback_query(lambda c: c.data and c.data.startswith('question_'))
async def question_handler(callback_query: CallbackQuery):
    question_id = int(callback_query.data.split('_')[1])

    async with async_session() as session:
        result = await session.execute(select(Questions).where(Questions.id == question_id))
        question = result.scalar_one()

    await callback_query.message.edit_text(f"Ответ: {question.answer}")
