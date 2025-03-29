from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import logging
import asyncio

from app.decorators.message import MessageManager
from app.keyboards.profile import profile_kb
from app.main.cmd_menu_handler import cmd_menu

logger = logging.getLogger(__name__)
router = Router()

from app.main.cmd_menu_handler import router as cmd_menu_handler_router

router.include_router(cmd_menu_handler_router)


@router.callback_query(F.data == 'ProfileBot')
async def start_profile_bot(callback: CallbackQuery, state: FSMContext):
    """Показ профиля сотрудника"""
    text = (
        "<b>🧑‍💻 Профиль сотрудника</b>\n\n"
        "👋 Привет! Меня зовут <i>Эмиль</i> — я разработчик Телеграм-ботов\n\n"
        "🔧 <b>Навыки:</b>\n"
        "• <b>Backend:</b> Python (Aiogram, asyncio, flask)\n"
        "• <b>Fronted:</b> HTML, CSS, JS\n"
        "• <b>Data base:</b> SQLite, PostgreSQL, MySQL\n"
        "• <b>Git System:</b> Git, GitHub, GitLab\n\n"
        "📂 <b>Проекты:</b>\n"
        "• Все текущие боты в этом боте, ввиде портфолио\n"
        "• @Supremacy1914_IMF_Bot\n"
        "📬 <b>Связь:</b>\n"
        "<i>Готов обсудить проект или сотрудничество. Просто выбери пункт в меню ниже 🙂</i>"
    )
    keyboard = await profile_kb()
    message_manager = MessageManager(bot=callback.bot, state=state)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        keyboard=keyboard,
        remove_previous=True
    )


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


@router.callback_query(F.data == "SendContact")
async def request_contact_keyboard(callback: CallbackQuery):
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📲 Отправить мой номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await callback.message.answer(
        "Пожалуйста, нажмите кнопку ниже, чтобы отправить ваш контакт 👇",
        reply_markup=contact_keyboard
    )
    await callback.answer()


# Убираем reply-кнопку
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Contact


@router.message(F.contact)
async def handle_contact(message: Message, state: FSMContext):
    contact: Contact = message.contact
    full_name = f"{contact.first_name} {contact.last_name or ''}".strip()
    username = f'{message.from_user.username}'
    phone = contact.phone_number

    text = (
        f"Спасибо, {full_name}!\n"
        f"Получил ваш номер: {phone} 📲\n"
        f"<b>Обязательно с вами свяжусь!</b>"
    )
    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='html'
    )

    send_text = (
        f"<b>Вам отправили свой номер от Бота №2, пользователь:</b> {full_name}!\n"
        f"<b>Получил номер:</b> {phone} 📲\n"
        f"<b>Напиши ему:</b> {username}"
    )
    await message.bot.send_message(
        chat_id=5311154389,
        text=send_text,
        parse_mode = 'html'
    )

    await asyncio.sleep(2)
    await cmd_menu(message, state)


