import hmac
import hashlib
import json
import requests
import os

# Your Binance TRC20
BINANCE_TRC20 = "TJ4BveBmTkbozPk5wR7GXcQwfL8FHszQAe"

def sign(data_str, secret):
    return hmac.new(secret.encode(), data_str.encode(), hashlib.sha256).hexdigest()

def main():
    API_KEY = os.getenv("FF_API_KEY", "").strip()
    API_SECRET = os.getenv("FF_API_SECRET", "").strip()
    FROM_AMOUNT = os.getenv("FROM_AMOUNT", "0.001").strip()
    TO_ADDR = os.getenv("TO_ADDRESS", BINANCE_TRC20).strip() or BINANCE_TRC20

    print("=== FIXEDFLOAT BTC -> USDT TRC20 ===")
    print(f"Amount: {FROM_AMOUNT} BTC")
    print(f"To: {TO_ADDR}")

    if not API_KEY or not API_SECRET:
        print("ERROR: FF_API_KEY or FF_API_SECRET missing in GitHub Secrets!")
        return

    url = "https://ff.io/api/v2/create"
    params = {
        "fromCcy": "BTC",
        "toCcy": "USDTTRC",
        "amount": float(FROM_AMOUNT),
        "direction": "from",
        "type": "float",
        "toAddress": TO_ADDR
    }

    data_json = json.dumps(params)
    signature = sign(data_json, API_SECRET)

    headers = {
        "X-API-KEY": API_KEY,
        "X-API-SIGN": signature,
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json"
    }

    print("\nCreating order on ff.io...")
    r = requests.post(url, data=data_json, headers=headers, timeout=30)
    
    print(f"HTTP: {r.status_code}")
    print(f"Body: {r.text}\n")

    try:
        j = r.json()
        if j.get("code") == 0:
            data = j.get("data", {})
            order_id = data.get("id") or data.get("orderId") or "N/A"
            from_info = data.get("from", {})
            to_info = data.get("to", {})

            print("="*50)
            print("✅ SUCCESS! ORDER CREATED")
            print(f"Order ID: {order_id}")
            print(f"")
            print(f"👉 SEND {from_info.get('amount')} {from_info.get('code')} TO:")
            print(f"   {from_info.get('address')}")
            print(f"")
            print(f"YOU WILL RECEIVE {to_info.get('amount')} USDT TRC20")
            print(f"AT: {TO_ADDR}")
            print("="*50)
        else:
            print(f"❌ Failed: {j.get('msg')} Code: {j.get('code')}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()
