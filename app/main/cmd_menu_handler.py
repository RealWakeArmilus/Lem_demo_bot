from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.decorators.message import MessageManager
from app.keyboards.handlers import handlers_kb

router = Router()


@router.callback_query(F.data == 'MainMenu')
async def cmd_menu(message: Message, state: FSMContext):
    """Главное меню"""
    text = (
        "Проверь другие мои работы\n"
        "<b>Просто нажми на кнопку из списка меню</b>"
    )

    keyboard = await handlers_kb()
    message_manager = MessageManager(bot=message.bot, state=state)
    await message_manager.send_photo(
        obj=message,
        text=text,
        keyboard=keyboard,
        remove_previous=True
    )
