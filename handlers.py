from aiogram import types
from aiogram.types import ParseMode
from main import dp, redis_client
from requests import get_all_values, get_course


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        course = await get_course(True)
        items_list = ''
        for item in course:
            for key, value in item.items():
                items_list += f'[{key}: {value}]\n'

        await message.answer('🤖 Вас приветствует бот EXZ(ЭКЗИ) \n💱Доступные команыд\n'
                             '💵 /exchange ОТ К количество - конвертация\n💵 /rates - получение актуального курса'
                             '\n💱 Доступные курсы валют: \n' + items_list)

    except Exception as e:
        await message.answer(f'Возникла ошибка: {e}')


@dp.message_handler(commands=['exchange'])
async def exchange(message: types.Message):
    try:
        _, from_currency, to_currency, amount = message.text.split()
        amount = float(amount)

        from_rate = redis_client.get(from_currency)
        to_rate = redis_client.get(to_currency)
        str_rate = ''
        all_rate = await get_all_values()
        for string in all_rate.keys():
            str_rate += f' [{string}]   '
        if from_rate and to_rate:
            from_rate = float(from_rate)
            to_rate = float(to_rate)

            result = (amount * from_rate) / to_rate

            response = f"{amount} {from_currency} = {result:.2f} {to_currency}"

            await message.reply(response, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.reply(f"Ошибка: Один из указанных тикеров не найден.\nДоступные: {str_rate}")

    except Exception as e:
        await message.answer(f'Возникла ошибка: {e}')


@dp.message_handler(commands=['rates'])
async def exchange(message: types.Message):
    try:
        all_items = await get_course(trun='all')
        await message.reply(all_items)

    except Exception as e:
        await message.answer(f'Возникла ошибка: {e}')