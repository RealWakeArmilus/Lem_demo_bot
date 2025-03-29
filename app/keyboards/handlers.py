from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def handlers_kb() -> InlineKeyboardMarkup:
    """
    :return: меню для команды старт
    """
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text=str('Бот №1: Повторяет ваш стикер'), callback_data=f'RepeatStickerBot'))
    builder.add(InlineKeyboardButton(text=str('Бот №2: Личная анкета'), callback_data=f'ProfileBot'))
    builder.add(InlineKeyboardButton(text=str('Бот №3: Библиотека греч. богов'), callback_data=f'LibraryGreekGodsBot'))
    builder.add(InlineKeyboardButton(text=str('Бот №4: Проверка подписки на канал'), callback_data=f'CheckingChannelSubscriptionBot'))
    builder.add(InlineKeyboardButton(text=str('Бот №5: Проверка счета на криптокошельке'), callback_data=f'CheckingCryptoWalletBot'))
    builder.add(InlineKeyboardButton(text=str('Бот №6: Запись к врачу'), callback_data=f'AppointmentDoctorBot'))

    builder.adjust(1)

    return builder.as_markup()
