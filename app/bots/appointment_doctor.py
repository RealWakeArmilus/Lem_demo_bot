from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import logging

import app.Classes_States.SG as SG
from app.Classes_States.SG import update_state
from app.decorators.callback_utils import parse_callback_data

from app.decorators.message import MessageManager
from app.keyboards.appointment_doctor import appointment_doctor_kb, back_menu_appointment_doctor_kb

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == 'AppointmentDoctorBot')
async def start_appointment_doctor_bot(callback: CallbackQuery, state: FSMContext, remove_previous: bool = True):
    """О враче. Начала бота по записи к врачу"""
    text = (
        "<b>👨‍⚕️ **О враче**</b>\n\n"
        "<b>Имя:</b> [Имя врача]\n" 
        "<b>Специализация:</b> [Специализация врача]\n"
        "<b>Опыт работы:</b> [Количество лет] лет\n"  
        "<b>Образование:</b> [Учебное заведение и год окончания]\n\n"
        
        "<b>Профессиональные достижения:</b>\n"
        "- [Достижение 1]\n"
        "- [Достижение 2]\n"
        "- [Достижение 3]\n\n"
        
        "<b>Контактная информация:</b> \n"
        "<b>📞 Телефон:</b> [Контактный телефон]\n"
        "<b>📧 Email:</b> [Email врача]\n\n"
        
        "<b>Описание может быть другим, на ваше усмотрение</b>"
    )
    keyboard = await appointment_doctor_kb()
    message_manager = MessageManager(bot=callback.bot, state=state)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        keyboard=keyboard,
        remove_previous=remove_previous,
        clear_state_all_exception_photo_message_id=True
    )


@router.callback_query(F.data == 'about_the_service')
async def about_the_service(callback: CallbackQuery, state: FSMContext):
    """Об услуге"""
    text = (
        "<b>🩺 **О услуге**</b>\n"
        "<b>Название услуги:</b> [Название услуги]\n"
        "<b>Описание:</b> [Краткое описание услуги]\n\n"
        
        "<b>Преимущества:</b>\n"
        "- [Преимущество 1]\n"
        "- [Преимущество 2]\n"
        "- [Преимущество 3]\n\n"
        
        "<b>Стоимость:</b> [Стоимость услуги]\n"
        "<b>Время проведения:</b> [Продолжительность услуги]\n\n"
        
        "<b>Дополнительная информация или подготовка:</b> [Краткая информация о подготовке или особенностях]\n\n"

        "<b>Описание может быть другим, на ваше усмотрение</b>"
    )
    keyboard = await back_menu_appointment_doctor_kb()
    message_manager = MessageManager(bot=callback.bot, state=state)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        keyboard=keyboard,
        remove_previous=True
    )


# 🔹 Шаблоны текстов шагов
STEP_TEXTS = {
    0: "<b>Всё верно записано?</b>",
    1: "<b>Введите ваше ФИО:</b>\n",
    2: "<b>Введите ваш Номер телефона:</b>\n",
    3: "<b>Выберите Дата и Время:</b>\n"
}


async def step(callback, state, step: int, remove_previous: bool = True, **kwargs):
    """Отправка сообщения для каждого шага создания матча."""
    message_manager = MessageManager(bot=callback.bot, state=state)
    data_form = await state.get_data()

    # Обновляем параметры
    for key, value in kwargs.items():
        if value is not None:
            data_form[key] = value

    # Формируем общий текст этапов с выделением текущего этапа жирным шрифтом
    view_step = f"{step}/3 ЭТАП\n" if step != 0 else ''
    steps_text = (
        f"{view_step}"
        f"{'<b>1 Этап - Ваше ФИО:</b>' if step == 1 else '1 Этап - Ваше ФИО:'} {data_form.get('full_name', '')}\n"
        f"{'<b>2 Этап - Номер телефона:</b>' if step == 2 else '2 Этап - Номер телефона:'} {data_form.get('number_phone', '')}\n"
        f"{'<b>3 Этап - Дата и Время:</b>' if step == 3 else '3 Этап - Дата и Время:'} {data_form.get('choice_date', '')}\n\n"
    )

    # Собираем сообщение
    text = f"{steps_text}{STEP_TEXTS.get(step, '!Неизвестно! на каком вы этапе?').format(data_form=data_form)}"
    keyboard = await back_menu_appointment_doctor_kb(step=step)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        keyboard=keyboard,
        remove_previous=remove_previous
    )


@router.callback_query(F.data == 'sign_up_on_doctor')
async def one_step_sign_up_on_doctor(callback: CallbackQuery, state: FSMContext, remove_previous: bool = True,):
    """Запись к врачу 1/3"""
    await state.set_state(SG.FormSignUpOnDoctor.full_name)
    await step(callback, state, 1, remove_previous)


@router.message(SG.FormSignUpOnDoctor.full_name)
async def two_step_sign_up_on_doctor(message: Message, state: FSMContext):
    """Запись к врачу 2/3"""
    full_name = message.text.strip()
    await update_state(state, full_name=full_name)
    await state.set_state(SG.FormSignUpOnDoctor.number_phone)
    await step(message, state, 2)


@router.message(SG.FormSignUpOnDoctor.number_phone)
async def three_step_sign_up_on_doctor(message: Message, state: FSMContext):
    """Запись к врачу 3/3"""
    input_number_phone = message.text.strip()

    try:
        if not input_number_phone.isdigit() or not input_number_phone.startswith('8'):
            raise Exception('Номер должен начинаться с 8, и состоять только из чисел')
        if len(input_number_phone) != 11:
            raise Exception('Номер должен содержать 11 цифр, включая сначала число 8.')

        input_number_phone = int(input_number_phone)

        await update_state(state, number_phone=input_number_phone)
        await state.set_state(SG.FormSignUpOnDoctor.choice_date)
        await step(message, state, 3)
    except Exception as error:
        text_error = (f'<b>Ошибка:</b> {error}\n\n'
                      f'<b>Повторите попытку</b>')
        message_manager = MessageManager(bot=message.bot, state=state)
        await message_manager.send_photo(
            obj=message,
            text=text_error
        )


@router.callback_query(lambda c: c.data and c.data.startswith('date_'))
async def end_sign_up_on_doctor(callback: CallbackQuery, state: FSMContext):
    """Конец записи к врачу"""
    search_date = parse_callback_data(callback.data, 'date_')[1]
    await update_state(state, choice_date=search_date)
    data_form = await state.get_data()

    print(f'{data_form}')

    await step(callback, state, 0)


@router.callback_query(F.data == 'confirm_appointment_doctor')
async def confirm_sign_up_on_doctor(callback: CallbackQuery, state: FSMContext):
    """Приняли подтверждение данных записи"""
    text = (
        '✅ Ваша запись успешно создана!'
    )
    message_manager = MessageManager(bot=callback.bto, state=state)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        remove_previous=True,
        clear_state_all_exception_photo_message_id=True
    )

    latitude, longitude = 55.756404757933765, 37.615527927133925
    await callback.message.answer_location(latitude=latitude, longitude=longitude)

    text = (
        '<b>Найти нас можете по данному адресу:</b> Манежная пл., 1, стр. 2, Москва, Россия, 125009'
    )
    message_manager = MessageManager(bot=callback.bto, state=state)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        remove_previous=True,
        clear_state_all_exception_photo_message_id=True
    )

    await start_appointment_doctor_bot(callback=callback, state=state, remove_previous=False)


@router.callback_query(F.data == 'restart_appointment_doctor')
async def restart_sign_up_on_doctor(callback: CallbackQuery, state: FSMContext):
    """Отклонили подтверждение данных записи"""
    text = (
        'Вы решили перезаписать данные'
    )
    message_manager = MessageManager(bot=callback.bot, state=state)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        remove_previous=True,
        clear_state_all_exception_photo_message_id=True
    )

    await one_step_sign_up_on_doctor(callback=callback, state=state, remove_previous=False)
