from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import FSInputFile
import aiohttp
import tempfile
import os
import logging

logger = logging.getLogger(__name__)


class MessageManager:
    def __init__(self, bot, state: FSMContext):
        self.bot = bot
        self.state = state

    async def send_photo(
            self,
            obj: Message | CallbackQuery,  # Это может быть как Message, так и CallbackQuery
            photo_path: str | None = None,
            keyboard: InlineKeyboardMarkup | None = None,
            text: str | None = None,
            remove_previous: bool = False,
            clear_state_photo_message_id: bool = False,
            clear_state_all_exception_photo_message_id: bool = False
    ):
        """
        Отправка сообщения с фотографией с возможностью:
        - удаления предыдущего сообщения,
        - добавления текста,
        - добавления кнопок,
        - очистки состояния (FSMContext).

        :param obj: Сообщение (Message) или запрос callback (CallbackQuery).
        :param photo_path: Путь к фото, которое будет отправлено (по умолчанию None).
        :param keyboard: Кнопки, которые будут прикреплены к сообщению (по умолчанию None).
        :param text: Текст, который будет отправлен с фото (по умолчанию None).
        :param remove_previous: Нужно ли удалять предыдущее сообщение с фото (по умолчанию False).
        :param clear_state_photo_message_id: Нужно ли очищать параметр photo_message_id из состояния (по умолчанию False).
        :param clear_state_all_exception_photo_message_id: Нужно ли очистить все данные в состоянии, кроме photo_message_id (по умолчанию False)
        """
        # Проверка, с каким объектом работаем (Message или CallbackQuery)
        if isinstance(obj, CallbackQuery):
            message = obj.message
        elif isinstance(obj, Message):
            message = obj
        else:
            raise TypeError("Неправильный тип объекта, ожидался Message или CallbackQuery")

        # Если нужно удалить предыдущее сообщение, удаляем его
        if remove_previous:
            data = await self.state.get_data()
            photo_message_id = data.get('photo_message_id')

            if photo_message_id:
                try:
                    await message.chat.delete_message(photo_message_id)
                except Exception as error:
                    print(f"Ошибка при удалении сообщения: {error}")
                # Обновляем состояние, удаляя ID старого сообщения
                await self.state.update_data(photo_message_id=None)

        # Если photo_path передан, отправляем фото, иначе только текст
        caption_text = text or None

        # Определяем, URL это или локальный путь
        if photo_path:
            photo = None
            temp_path = None

            try:
                # Если это ссылка — скачиваем во временный файл
                if photo_path.startswith("http://") or photo_path.startswith("https://"):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(photo_path) as resp:
                            if resp.status != 200:
                                raise Exception(f"Не удалось скачать изображение: {photo_path}")
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                                tmp.write(await resp.read())
                                temp_path = tmp.name
                                photo = FSInputFile(temp_path)

                # Если это локальный путь — проверяем, существует ли файл
                elif os.path.isfile(photo_path):
                    photo = FSInputFile(photo_path)
                else:
                    raise FileNotFoundError(f"Файл не найден: {photo_path}")

                # Отправляем фото
                sent_message = await message.answer_photo(
                    photo=photo,
                    caption=caption_text,
                    reply_markup=keyboard if isinstance(keyboard, InlineKeyboardMarkup) else None,
                    parse_mode='html'
                )

            except Exception as e:
                logger.error(f"Ошибка при отправке фото ({photo_path}): {e}")
                return

            finally:
                # Удаляем временный файл, если использовался
                if temp_path and os.path.isfile(temp_path):
                    try:
                        os.unlink(temp_path)
                    except Exception as e:
                        logger.warning(f"Не удалось удалить временный файл {temp_path}: {e}")

        else:
            # Если нет фото — просто отправляем текст
            try:
                sent_message = await message.answer(
                    text=caption_text,
                    reply_markup=keyboard if isinstance(keyboard, InlineKeyboardMarkup) else None,
                    parse_mode='html'
                )
            except Exception as e:
                logger.error(f"Ошибка при отправке текста: {e}")
                return

        # Сохраняем ID сообщения в state
        await self.state.update_data(photo_message_id=sent_message.message_id)

        # Очистка состояния, если требуется
        if clear_state_photo_message_id:
            await self.state.update_data(photo_message_id=None)

        if clear_state_all_exception_photo_message_id:
            await self.clear_state_all_exception_photo_message_id()

        await self.del_object()


    async def clear_state_all_exception_photo_message_id(self):
        # Получаем данные из state
        state_data = await self.state.get_data()

        # Сохраняем photo_message_id, если он есть
        photo_message_id = state_data.get("photo_message_id")

        # Очищаем state
        await self.state.clear()

        # Восстанавливаем только photo_message_id
        if photo_message_id is not None:
            await self.state.update_data(photo_message_id=photo_message_id)


    async def del_object(self):
        """Очищает данные из экземпляра"""
        self.bot = None
        self.state = None
        del self

