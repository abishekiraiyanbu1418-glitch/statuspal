import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api-m.sandbox.paypal.com"


def get_access_token():
    response = requests.post(
        BASE_URL + "/v1/oauth2/token",
        auth=(os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_CLIENT_SECRET")),
        data={"grant_type": "client_credentials"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_test_order(amount="25.00"):
    token = get_access_token()
    response = requests.post(
        BASE_URL + "/v2/checkout/orders",
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
        json={
            "intent": "CAPTURE",
            "purchase_units": [
                {"amount": {"currency_code": "USD", "value": amount}}
            ],
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["id"]


def get_order(order_id):
    token = get_access_token()
    response = requests.get(
        BASE_URL + "/v2/checkout/orders/" + order_id,
        headers={"Authorization": "Bearer " + token},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    order_id = create_test_order()
    order = get_order(order_id)
    print("Order ID:", order["id"])
    print("Status:", order["status"])
    print("Amount:", order["purchase_units"][0]["amount"])