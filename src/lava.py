import hashlib
import hmac
import json
import uuid

import requests

from src.config import load_config


class LavaFacade:
    def __init__(self, config):
        self.__secret = config["lava"]["privatekey"]
        self.__shopid = config["lava"]["shopid"]

    def create_invoice(self, invoice_sum: int, orderid: int):
        data = {
            "shopId": self.__shopid,
            "sum": 1,
            "orderId": str(uuid.uuid4()),
            "hookUrl": "https://lava.ru",
            "successUrl": "https://lava.ru",
            "failUrl": "https://lava.ru",
            "expire": 300,
            "customFields": "test",
            "comment": "test",
            "includeService": [
                "card",
                "sbp",
                "qiwi"
            ]
        }

        data = dict(sorted(data.items()))
        json_str = json.dumps(data).encode()

        print(json_str)

        sign = hmac.new(bytes(self.__secret, 'UTF-8'), json_str, hashlib.sha256).hexdigest()
        print(json_str)
        print(sign)

        headers = {
            'Signature': sign,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            url='https://api.lava.ru/business/invoice/create',
            data=json_str,
            headers=headers
        )
        print(response.json())

        if response.status_code == 200:
            return True
        else:
            return False


lava = LavaFacade(config=load_config())
lava.create_invoice(10, 123456)
