import hashlib
import hmac
import json

import requests


class LavaFacade:
    def __init__(self, config):
        self.__secret = config["lava"]["privatekey"]
        self.__shopid = config["lava"]["shopid"]

    def create_invoice(self, invoice_sum: int, orderid: int):
        data = {
            'sum': invoice_sum,
            'orderId': orderid,
            'shopId': self.__shopid
        }

        json_str = json.dumps(data).encode()

        sign = hmac.new(bytes(self.__secret, 'UTF-8'), json_str, hashlib.sha256).hexdigest()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Signature": sign
        }

        response = requests.post(
            url='https://api.lava.ru/business/invoice/create',
            data=json_str,
            headers=headers
        )

        if response.status_code == 200:
            return True
        else:
            return False