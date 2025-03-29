from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import logging

import app.verify.checks as checks

from app.decorators.message import MessageManager
from app.keyboards.checking_channel_subscription import checking_channel_subscription_kb

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == 'CheckingChannelSubscriptionBot')
async def start_checking_channel_subscription_bot(callback: CallbackQuery, state: FSMContext):
    """Проверяет подписку на канал"""
    text = (
        "Данный бот проверяет вашу подписку на телеграм канал @Supremacy1914_IMF_Channel\n\n"
        "<b>При разработке бота для вас, можно выбрать любой ваш канал, где нужна проверка пользователей на подписку</b>"
    )
    keyboard = await checking_channel_subscription_kb()
    message_manager = MessageManager(bot=callback.bot, state=state)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        keyboard=keyboard,
        remove_previous=True
    )


@router.callback_query(lambda c: c.data == "check_sub")
async def check_sub_again(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки "Я подписался"""
    user_id = callback.from_user.id
    is_subscribed = await checks.identify_subscription(
        bot=callback.message.bot,
        user_id=user_id
    )

    if is_subscribed:
        await callback.message.answer("✅ Вы успешно подписаны!", show_alert=True)
        await start_checking_channel_subscription_bot(callback, state)
    else:
        await callback.answer("❌ Вы еще не подписались!", show_alert=True)

