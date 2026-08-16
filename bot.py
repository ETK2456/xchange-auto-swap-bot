import os, time, hmac, hashlib, requests, json

API_KEY = os.getenv("FF_API_KEY")
API_SECRET = os.getenv("FF_API_SECRET")
FROM_CUR = os.getenv("FROM_CURRENCY", "BTC")
FROM_AMT = float(os.getenv("FROM_AMOUNT", "0.001"))
TO_CUR = "USDTTRC20"
TO_ADDR = "TJ4BveBmTkbozPk5wR7GXcQwfL8FHszQAe"

def sign(msg):
    return hmac.new(API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()

def check_order(order_id):
    try:
        sig = sign(order_id)
        r = requests.get(f"https://ff.io/api/v2/order/{order_id}",
            headers={"X-API-KEY": API_KEY, "X-API-SIGN": sig}, timeout=20)
        print(f"[{order_id}] {r.status_code}: {r.text[:400]}")
        return r.json() if r.ok else None
    except Exception as e:
        print(f"Error checking {order_id}: {e}")

def create_order():
    try:
        payload = {"fromCurrency": FROM_CUR, "toCurrency": TO_CUR, "fromQty": FROM_AMT, "toAddress": TO_ADDR, "type": "fixed"}
        body = json.dumps(payload, separators=(',', ':'))
        sig = sign(body)
        r = requests.post("https://ff.io/api/v2/order",
            headers={"X-API-KEY": API_KEY, "X-API-SIGN": sig, "Content-Type": "application/json"},
            data=body, timeout=20)
        print(f"CREATE {FROM_CUR}: {r.status_code} {r.text[:600]}")
    except Exception as e:
        print(f"Create error: {e}")

if __name__ == "__main__":
    print(f"Bot start: {FROM_CUR} {FROM_AMT} -> {TO_CUR}")
    if not API_KEY:
        print("No FF_API_KEY secret set! Add in Settings > Secrets")
    else:
        print("Checking FZ7M47...")
        check_order("FZ7M47")
        if FROM_CUR == "TRX":
            create_order()
    print("Loop start - checking every 60s")
    while True:
        time.sleep(60)
        if API_KEY:
            check_order("FZ7M47")
