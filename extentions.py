from config import DADATA_TOKEN, DADATA_SECRET
import requests
from dadata import Dadata
import json

keys = {}

class GetCurrency:
    @staticmethod
    def update_currency():
        r = requests.get(f'https://api.exchangeratesapi.io/latest?')
        currency_codes = json.loads(r.content)['rates']
        for record in currency_codes:
            with Dadata(DADATA_TOKEN, DADATA_SECRET) as dadata:
                result = dadata.find_by_id("currency", record)
                if result != []:
                    _ =  result[0]['value'].lower()
            keys[_] = record


class APIException(Exception):
    pass

class Price:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        
        if base == quote:
            raise APIException(f'Невозможно преобразовать валюту {base}')

        try:
            base = keys[base]
        except KeyError:
            raise APIException(f'Не удалось преобразовать валюту {base}')

        try:
            quote = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось преобразовать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={quote}&base={base}')
        return json.loads(r.content)['rates'][quote] * amount
