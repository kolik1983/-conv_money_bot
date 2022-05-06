import requests
import json
from libr import money_keys


class APIException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Нельзя конвертировать одинаковую валюту {base}.')

        try:
            quote_ticer = money_keys[quote]
        except KeyError:
            raise APIException(f'Нет такой валюты{quote}!')

        try:
            base_ticer = money_keys[base]
        except KeyError:
            raise APIException(f'Нет такой валюты{base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверно введено число {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticer}&tsyms={base_ticer}')
        all_base = (json.loads(r.content)[money_keys[base]]) * amount

        return all_base


