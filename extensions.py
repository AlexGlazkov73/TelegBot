import requests
import json

keys = {
    'евро': 'EUR',
    'рубль': 'RUB',
    'доллар': 'USD'
 }

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote.lower() == base.lower():
            raise APIException(f'Невозмоэжно перевести одинаковые валюты {base}')

        try:
            quote_ticker = key_[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = key_[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неправильное количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[key_[base]]
        total = total_base * amount

        return total

