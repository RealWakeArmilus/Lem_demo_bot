from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def profile_kb() -> InlineKeyboardMarkup:
    """
    :return: меню для команды старт
    """
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text=str('Отправить контакты'), callback_data=f'SendContact'))
    builder.add(InlineKeyboardButton(text=str('Вернуться в главное меню'), callback_data=f'MainMenu'))


    builder.adjust(1)

    return builder.as_markup()
