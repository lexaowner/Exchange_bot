import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from main import redis_client


async def get_course(trun=None):
    url = 'https://cbr.ru/scripts/XML_daily.asp'
    try:
        async with aiohttp.ClientSession() as aiohttp_session:
            async with aiohttp_session.get(url) as data:
                response = await data.text()

                root = ET.fromstring(response)
                request = []
                list_request = ''
                for valute in root.findall('Valute'):
                    name = valute.find('Name').text
                    char_code = valute.find('CharCode').text
                    value = valute.find('Value').text.replace(',', '.')
                    request.append({name: char_code})
                    list_request += f'{name} [{char_code}] = {value}\n'
                    redis_client.set(char_code, value)

                if trun is None:
                    return

                elif trun is not None and trun != 'all':
                    return request

                elif trun == 'all':
                    return list_request
    except Exception as e:
        print(f'Возникла ошибка в функции get_course: {e}')


async def get_all_values():
    try:
        keys = redis_client.keys('*')
        all_values = {key: redis_client.get(key) for key in keys}
        return all_values

    except Exception as e:
        print(f'Возникла ошибка в функции get_all_values: {e}')


async def get_value_by_ticker(ticker):
    try:
        print(redis_client.get(ticker))
        return redis_client.get(ticker)

    except Exception as e:
        print(f'Возникла ошибка в функции get_value_by_ticker: {e}')
