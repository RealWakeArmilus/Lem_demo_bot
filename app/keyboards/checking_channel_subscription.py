from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.main.config import CHANNEL_USERNAME


async def checking_channel_subscription_kb() -> InlineKeyboardMarkup:
    """
    :return: меню для команды старт
    """
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text=str("Подписаться"), url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
    builder.add(InlineKeyboardButton(text=str('Проверить подписку'), callback_data=f'check_sub'))
    builder.add(InlineKeyboardButton(text=str('Вернуться в главное меню'), callback_data=f'MainMenu'))

    builder.adjust(1)

    return builder.as_markup()
