from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def appointment_doctor_kb() -> InlineKeyboardMarkup:
    """
    :return: меню для команды старт
    """
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text=str('Узнать о услуге'), callback_data=f'about_the_service'))
    builder.add(InlineKeyboardButton(text=str('Записаться к врачу'), callback_data=f'sign_up_on_doctor'))
    builder.add(InlineKeyboardButton(text=str('Вернуться в главное меню'), callback_data=f'MainMenu'))

    builder.adjust(1)

    return builder.as_markup()


async def back_menu_appointment_doctor_kb(step: int | None = None) -> InlineKeyboardMarkup:
    """
    :return: меню для команды старт
    """
    builder = InlineKeyboardBuilder()

    if step == 0:
        builder.add(InlineKeyboardButton(text=str('Да, подтверждаю запись'), callback_data=f'confirm_appointment_doctor'))
        builder.add(InlineKeyboardButton(text=str('Нет, хочу перезаписать'), callback_data=f'restart_appointment_doctor'))
    elif step == 3:
        builder.add(InlineKeyboardButton(text=str('25.05 в 10:30'), callback_data=f'date_25.05 в 10:30'))
        builder.add(InlineKeyboardButton(text=str('26.05 в 15:30'), callback_data=f'date_26.05 в 15:30'))
        builder.add(InlineKeyboardButton(text=str('27.05 в 17:30'), callback_data=f'date_27.05 в 17:30'))

    builder.add(InlineKeyboardButton(text=str('Назад'), callback_data=f'AppointmentDoctorBot'))

    builder.adjust(1)

    return builder.as_markup()
