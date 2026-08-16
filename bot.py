import requests, time, os, sys
from dotenv import load_dotenv
load_dotenv()
BASE = "https://xchange.me/api/v1"

class XChangeBot:
    def __init__(self):
        self.from_cur = os.getenv("FROM_CURRENCY","btc").lower()
        self.to_cur = os.getenv("TO_CURRENCY","xmr").lower()
        self.amount = float(os.getenv("FROM_AMOUNT","0.01"))
        self.to_address = os.getenv("TO_ADDRESS")
        self.refund_address = os.getenv("REFUND_ADDRESS")
        if not self.to_address:
            print("ERROR: Set TO_ADDRESS")
            sys.exit(1)

    def estimate(self):
        r = requests.get(f"{BASE}/exchange/estimate", params={
            "from_currency": self.from_cur,
            "to_currency": self.to_cur,
            "from_amount": self.amount
        }).json()
        print(f"ESTIMATE: {self.amount} {self.from_cur} => {r.get('to_amount')} {self.to_cur} | Rate: {r.get('rate')}")
        return r

    def create_order(self):
        payload = {
            "from_currency": self.from_cur,
            "to_currency": self.to_cur,
            "from_amount": self.amount,
            "to_address": self.to_address,
            "refund_address": self.refund_address
        }
        r = requests.post(f"{BASE}/exchange", json=payload).json()
        print("\n=== ORDER CREATED ===")
        print(r)
        return r

if __name__ == "__main__":
    bot = XChangeBot()
    bot.estimate()
    if input("Create REAL order? (y/n): ").lower() == 'y':
        bot.create_order()
