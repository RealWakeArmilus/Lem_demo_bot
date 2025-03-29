import logging
from aiogram.fsm.context import FSMContext

# import StatesGroup
from aiogram.fsm.state import StatesGroup, State


logger = logging.getLogger(__name__)


# State updater utility
async def update_state(state: FSMContext, **kwargs):
    await state.update_data(**kwargs)
    logger.info(f"FSMContext updated with: {kwargs}")


class FormSignUpOnDoctor(StatesGroup):
    full_name = State()
    number_phone = State()
    choice_date = State()

