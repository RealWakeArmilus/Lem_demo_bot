from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import logging

from app.decorators.message import MessageManager
from app.keyboards.library_greek_gods import library_greek_gods_kb, back_library_greek_gods_kb
from app.decorators.callback_utils import parse_callback_data

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == 'LibraryGreekGodsBot')
async def start_library_greek_gods_bot(callback: CallbackQuery, state: FSMContext):
    """Показ списка греческих богов"""
    text = (
        "Данный бот является библиотекой древнегреческих богов\n"
        "<b>Выберите интересующего вас бога</b>"
    )
    keyboard = await library_greek_gods_kb()
    message_manager = MessageManager(bot=callback.bot, state=state)
    await message_manager.send_photo(
        obj=callback,
        text=text,
        keyboard=keyboard,
        remove_previous=True
    )


@router.callback_query(lambda c: c.data and c.data.startswith('God_'))
async def show_greek_god_details(callback: CallbackQuery, state: FSMContext):
    """Показ информации о выбранном греческом боге"""
    search_god = parse_callback_data(callback.data, 'God_')[1]

    gods_data = {
        'Morpheus': {
            'name': 'Morpheus',
            'info': (
                'Морфе́й (др.-греч. Μορφεύς — «формирователь», «тот, кто формирует [сновидения]») — бог добрых (пророческих или лживых) снов в греческой мифологии.\n\n'
                'Его отцом является Гипнос — бог сна и сновидений.\n'
                'По одной из версий, его матерью была Аглая, дочь Зевса и Эвриномы, одна из трёх граций, спутниц Афродиты, имя которой в дословном переводе означает «Ясная». По другой версий — Нюкта, богиня ночи...'
            ),
            'photo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Guerin_Morpheus%26Iris1811.jpg/411px-Guerin_Morpheus%26Iris1811.jpg'
        },
        'Adonis': {
            'name': 'Adonis',
            'info': (
                'Адо́нис (др.-греч. Ἄδωνις, от финик. ʾadōnī «мой господин»; также связывался с ἁδονά «удовольствие», «чувственное наслаждение») — в древнегреческой мифологии — по наиболее популярной версии — сын Кинира от его собственной дочери Смирны.\n\n'
                'Адонис славился своей красотой: в него влюбляется богиня любви Афродита. Его также называют возлюбленным Диониса.\n'
            ),
            'photo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Adonis_Mazarin_Louvre_MR239.jpg/330px-Adonis_Mazarin_Louvre_MR239.jpg'
        },
        'Talos': {
            'name': 'Talos',
            'info': (
                'Талос (др.-греч. Τάλως), согласно спартанскому мифографу Кинефону — отец Гефеста.\n\n'
                'По распространённому преданию (например, у Гомера), Гефест был сыном Зевса и Геры. Это разногласие, вероятно, объясняется недоразумением Кинефона: Зевс носит прозвище Ταλλαϊος, вероятно, как олицетворение Солнца'
            ),
            'photo': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Didrachm_Phaistos_obverse_CdM.jpg'
        },
        'Alastor': {
            'name': 'Alastor',
            'info': (
                'Ала́стор, греч. Ἀλάστωρ – «Губитель». В греческой мифологии — дух мщения. Представление об Аласторе, возникшее в народном веровании, особенно развито трагиками.\n\n'
                'Как отмечает Н. В. Брагинская: «слово „аластор“ имеет активно-пассивный смысл: с одной стороны … это демон-мститель … и вообще злой дух, с другой стороны, Эдип — тоже аластор, то есть „проклятье“ Фив»'
            ),
            'photo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Alastor_%28Dictionnaire_Infernal%29.png/411px-Alastor_%28Dictionnaire_Infernal%29.png'
        }
    }

    god = gods_data.get(search_god)

    if god:
        name_god = god['name']
        info_god = god['info']
        photo = god['photo']
    else:
        name_god = 'Неизвестно'
        info_god = 'Бог с таким именем не найден.'
        photo = 'https://habrastorage.org/webt/ay/dp/mt/aydpmtdaqx8ueuo3kitujhva7mm.gif'
        print(f"Неизвестный бог: {search_god}")

    text = (
        f"<b>Древнегреческий бог:</b> {name_god}\n\n"
        f"<b>Информация:</b> {info_god}"
    )

    keyboard = await back_library_greek_gods_kb()
    message_manager = MessageManager(bot=callback.bot, state=state)
    await message_manager.send_photo(
        obj=callback,
        photo_path=photo,
        text=text,
        keyboard=keyboard,
        remove_previous=True
    )