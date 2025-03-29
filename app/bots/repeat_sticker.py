from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import logging
import asyncio

from app.decorators.message import MessageManager
from app.main.cmd_menu_handler import cmd_menu

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == 'RepeatStickerBot')
async def start_repeat_sticker_bot(callback: CallbackQuery, state: FSMContext):
    """Запуск бота повторяющего стикер"""
    text = "<b>Отправь мне любой стикер. Я его повторю</b>"
    message_manager = MessageManager(bot=callback.bot, state=state)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        remove_previous=True
    )


@router.message(F.sticker)
async def check_sticker(message: Message, state: FSMContext):
    """Прием стикера и его немедленная отправка. Затем открытие главного меню"""
    await message.bot.send_sticker(chat_id=message.chat.id, sticker=message.sticker.file_id)

    text = "<b>Вау! Круто получилось, не правда ли?)</b>"
    message_manager = MessageManager(bot=message.bot, state=state)
    await message_manager.send_photo(
        obj=message,
        text=text
    )

    await asyncio.sleep(2)
    await cmd_menu(message, state)


# @router.message()
# async def check_sticker(message: Message):
#     """Показывает id стикера"""
#     await message.answer(message.sticker.file_id)
