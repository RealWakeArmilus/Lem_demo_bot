from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import logging

from app.decorators.message import MessageManager
from app.keyboards.checking_crypto_wallet import checking_crypto_wallet_kb

logger = logging.getLogger(__name__)
router = Router()

import requests

TON_API_URL = "https://tonapi.io/v2/accounts/"
MY_TOKEN_CRYPTO_WALLET = 'UQDXAVRit4KXoPvG7zbRkkM12z0ab-zfgEQxs_LTRXdG7Odz'


def get_jetton_balance(wallet_address: str):
    """
    Получает баланс конкретного Jetton-токена на TON-кошельке.

    :param wallet_address: Адрес кошелька в сети TON.
    :return: Баланс токена в формате float.
    """

    # Используем публичный API tonapi.io или toncenter.com
    api_url = f"https://tonapi.io/v2/accounts/{wallet_address}/jettons"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        balances = data.get("balances", [])

        if not balances:
            logger.info("Балансов токенов не найдено.")
            return []

        all_balances = []

        for jetton in balances:
            balance = int(jetton["balance"]) / (10 ** jetton["jetton"]["decimals"])
            name = jetton["jetton"]["name"]
            symbol = jetton["jetton"]["symbol"]
            address = jetton["wallet_address"]["address"]
            is_scam = jetton["wallet_address"]["is_scam"]
            image = jetton["jetton"].get("image", "Нет изображения")

            token_data = {
                "name": name,
                "symbol": symbol,
                "balance": balance,
                "wallet_address": address,
                "is_scam": is_scam,
                "image": image
            }

            all_balances.append(token_data)

        balance = {}

        for balance_coin in all_balances:
            if balance_coin['name'] == 'FPIBANK' and balance_coin['symbol'] == 'FPIBANK':
                balance['FPIBANK'] = balance_coin['balance']
            if balance_coin['name'] == 'IF' and balance_coin['symbol'] == 'IF':
                balance['IF'] = balance_coin['balance']

        return balance

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса: {e}")
        return []


@router.callback_query(F.data == 'CheckingCryptoWalletBot')
async def start_checking_crypto_wallet_bot(callback: CallbackQuery, state: FSMContext):
    wallet_token = MY_TOKEN_CRYPTO_WALLET
    # Проверяем баланс кошелька через API
    balances = get_jetton_balance(
        wallet_address=wallet_token
    )
    message_manager = MessageManager(bot=callback.bot, state=state)
    keyboard = await checking_crypto_wallet_kb()
    await message_manager.send_photo(
        obj=callback,
        text=(f'✅ Кошелек найден\n'
              f'💰 Баланс: {round(balances['FPIBANK'], 4)} FPIBANK\n'
              f'💰 Баланс: {round(balances['IF'], 4)} IF'),
        keyboard=keyboard,
        remove_previous=True
    )