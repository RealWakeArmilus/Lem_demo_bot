from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def library_greek_gods_kb() -> InlineKeyboardMarkup:
    """
    :return: меню библиотеки греческих богов
    """
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text=str('Морфей'), callback_data=f'God_Morpheus'))
    builder.add(InlineKeyboardButton(text=str('Адонис'), callback_data=f'God_Adonis'))
    builder.add(InlineKeyboardButton(text=str('Талос'), callback_data=f'God_Talos'))
    builder.add(InlineKeyboardButton(text=str('Аластор'), callback_data=f'God_Alastor'))
    builder.add(InlineKeyboardButton(text=str('Вернуться в главное меню'), callback_data=f'MainMenu'))


    builder.adjust(1)

    return builder.as_markup()


async def back_library_greek_gods_kb() -> InlineKeyboardMarkup:
    """
    :return: клавитура с одной кнопкой вернутся в меню греческих богов
    """
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text=str('Назад в библиотеку'), callback_data=f'LibraryGreekGodsBot'))


    builder.adjust(1)

    return builder.as_markup()