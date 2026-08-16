import os, hmac, hashlib, requests, json

API_KEY = os.getenv("FF_API_KEY")
API_SECRET = os.getenv("FF_API_SECRET")
FROM_CUR = os.getenv("FROM_CURRENCY", "BTC")
FROM_AMT = os.getenv("FROM_AMOUNT", "0.001")
TO_CUR = "USDTTRC20"
TO_ADDR = "TJ4BveBmTkbozPk5wR7GXcQwfL8FHszQAe"

def sign(msg):
    if not API_SECRET:
        return ""
    return hmac.new(API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()

def check_order(order_id):
    try:
        if not API_KEY or not API_SECRET:
            print("No API keys - skip check")
            return None
        sig = sign(order_id)
        r = requests.get(f"https://ff.io/api/v2/order/{order_id}",
            headers={"X-API-KEY": API_KEY, "X-API-SIGN": sig}, timeout=20)
        print(f"[{order_id}] Status {r.status_code}")
        print(r.text[:800])
        return r.json() if r.ok else None
    except Exception as e:
        print(f"Error checking {order_id}: {e}")

def create_order():
    try:
        if not API_KEY or not API_SECRET:
            print("No API keys - cannot create order")
            return
        payload = {"fromCurrency": FROM_CUR, "toCurrency": TO_CUR, "fromQty": float(FROM_AMT), "toAddress": TO_ADDR, "type": "fixed"}
        body = json.dumps(payload, separators=(',', ':'))
        sig = sign(body)
        r = requests.post("https://ff.io/api/v2/order",
            headers={"X-API-KEY": API_KEY, "X-API-SIGN": sig, "Content-Type": "application/json"},
            data=body, timeout=20)
        print(f"CREATE {FROM_CUR} {FROM_AMT}: {r.status_code}")
        print(r.text[:1000])
    except Exception as e:
        print(f"Create error: {e}")

if __name__ == "__main__":
    print(f"=== Bot Start ===")
    print(f"From: {FROM_CUR} {FROM_AMT} -> {TO_CUR} to {TO_ADDR}")
    print(f"API Key set: {bool(API_KEY)}")
    
    # Check your existing order
    check_order("FZ7M47")
    
    # If TRX mode, create new order
    if FROM_CUR == "TRX":
        print("TRX mode - creating test order...")
        create_order()
    
    print("=== Bot Finished - Success ===")
