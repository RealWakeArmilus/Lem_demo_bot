from app.main.config import CHANNEL_USERNAME
import logging

logger = logging.getLogger(__name__)


async def identify_subscription(bot, user_id: int) -> bool:
    """--- Проверка подписки ---"""
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        return False
