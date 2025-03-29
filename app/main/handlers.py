from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import logging

from app.decorators.message import MessageManager
from app.keyboards.handlers import handlers_kb

logger = logging.getLogger(__name__)
router = Router()

from app.bots.repeat_sticker import router as repeat_sticker_bot_router
from app.bots.profile import router as profile_router
from app.bots.library_greek_gods import router as library_greek_gods_router
from app.bots.checking_channel_subscription import router as checking_channel_subscription_router
from app.bots.appointment_doctor import router as appointment_doctor_router
from app.bots.checking_crypto_wallet import router as checking_crypto_wallet_router

router.include_router(repeat_sticker_bot_router)
router.include_router(profile_router)
router.include_router(library_greek_gods_router)
router.include_router(checking_channel_subscription_router)
router.include_router(appointment_doctor_router)
router.include_router(checking_crypto_wallet_router)


@router.message(Command('start'))
async def handle_start(message: Message, state: FSMContext):
    if message.chat.type != 'private' or message.from_user.is_bot:
        return

    sticker_id = 'CAACAgIAAxkBAAMCZ-EcQ6nS0oQY76_S0hQafV0gj0YAAgUAA8A2TxP5al-agmtNdTYE'
    await message.bot.send_sticker(chat_id=message.chat.id, sticker=sticker_id)

    text = (
        "Приветствую!\n"
        "Я покажу вам примеры своих работ\n"
        "<b>Просто нажми на кнопку из списка меню</b>"
    )
    keyboard = await handlers_kb()
    message_manager = MessageManager(bot=message.bot, state=state)
    await message_manager.send_photo(
        obj=message,
        text=text,
        keyboard=keyboard
    )



