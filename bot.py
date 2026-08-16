import os, time, hmac, hashlib, requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("FF_API_KEY")
API_SECRET = os.getenv("FF_API_SECRET")
FROM_CUR = os.getenv("FROM_CURRENCY", "BTC")
FROM_AMT = float(os.getenv("FROM_AMOUNT", "0.001"))
TO_CUR = "USDTTRC20"
TO_ADDR = "TJ4BveBmTkbozPk5wR7GXcQwfL8FHszQAe"

def sign(msg):
    return hmac.new(API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()

def check_order(order_id):
    sig = sign(order_id)
    r = requests.get(f"https://ff.io/api/v2/order/{order_id}",
        headers={"X-API-KEY": API_KEY, "X-API-SIGN": sig}, timeout=20)
    print(f"[{order_id}] {r.status_code}: {r.text[:300]}")
    return r.json() if r.ok else None

def create_order():
    # get price
    payload = {"fromCurrency": FROM_CUR, "toCurrency": TO_CUR, "fromQty": FROM_AMT, "toAddress": TO_ADDR, "type": "fixed"}
    # signing for POST needs json dump
    import json
    body = json.dumps(payload, separators=(',', ':'))
    sig = sign(body)
    r = requests.post("https://ff.io/api/v2/order",
        headers={"X-API-KEY": API_KEY, "X-API-SIGN": sig, "Content-Type": "application/json"},
        data=body, timeout=20)
    print("CREATE:", r.status_code, r.text[:500])
    return r.json()

if __name__ == "__main__":
    print(f"Bot start: {FROM_CUR} {FROM_AMT} -> {TO_CUR} to {TO_ADDR}")
    # 1. Check old order FZ7M47
    if API_KEY:
        print("Checking FZ7M47...")
        check_order("FZ7M47")
        # 2. Create test if TRX
        if FROM_CUR == "TRX":
            print("Creating TRX test order...")
            create_order()
    else:
        print("No API keys set - set FF_API_KEY, FF_API_SECRET in GitHub Secrets")
    # Loop
    while True:
        time.sleep(30)
        if API_KEY:
            check_order("FZ7M47")
