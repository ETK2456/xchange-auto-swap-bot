import hmac, hashlib, json, requests, os, time

BINANCE_TRC20 = "TJ4BveBmTkbozPk5wR7GXcQwfL8FHszQAe"

def sign(data_str, secret):
    return hmac.new(secret.encode(), data_str.encode(), hashlib.sha256).hexdigest()

def api_request(method, params, api_key, api_secret):
    url = f"https://ff.io/api/v2/{method}"
    data_json = json.dumps(params) if params else "{}"
    sig = sign(data_json, api_secret) if params else sign("", api_secret)
    headers = {
        "X-API-KEY": api_key,
        "X-API-SIGN": sig,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if method == "ccies":
        r = requests.post(url, data="{}", headers=headers, timeout=20)
    else:
        r = requests.post(url, data=data_json, headers=headers, timeout=20)
    return r.json()

def get_order_status(order_id, api_key, api_secret):
    # For get order, method is /api/v2/order/{id} but via POST with empty? Actually API uses POST order
    # According to docs: POST https://ff.io/api/v2/order/{id}
    url = f"https://ff.io/api/v2/order/{order_id}"
    data_json = json.dumps({})
    sig = sign(data_json, api_secret)
    headers = {
        "X-API-KEY": api_key,
        "X-API-SIGN": sig,
        "Content-Type": "application/json",
    }
    r = requests.post(url, data=data_json, headers=headers, timeout=20)
    return r.text

def main():
    API_KEY = os.getenv("FF_API_KEY", "").strip()
    API_SECRET = os.getenv("FF_API_SECRET", "").strip()
    FROM_AMOUNT = os.getenv("FROM_AMOUNT", "0.001").strip()
    FROM_CCY = os.getenv("FROM_CURRENCY", "BTC").strip().upper() or "BTC"
    TO_ADDR = os.getenv("TO_ADDRESS", BINANCE_TRC20).strip() or BINANCE_TRC20
    
    # For TRX test, set FROM_CURRENCY = TRX in secrets and FROM_AMOUNT = 15
    if FROM_CCY == "TRX":
        test_amount = float(FROM_AMOUNT) if float(FROM_AMOUNT) > 1 else 15.0
    else:
        test_amount = float(FROM_AMOUNT)

    print(f"=== FIXEDFLOAT AUTO BOT + CHECKER ===")
    print(f"From: {test_amount} {FROM_CCY} -> USDTTRC")
    print(f"To: {TO_ADDR}")
    print(f"Order ID to check: FZ7M47 (last BTC order)")

    if not API_KEY or not API_SECRET:
        print("ERROR: Missing API keys")
        return

    # 1. Check previous order FZ7M47 status
    print("\n--- CHECKING PREVIOUS ORDER FZ7M47 ---")
    try:
        status_text = get_order_status("FZ7M47", API_KEY, API_SECRET)
        print(f"Status Raw: {status_text[:2000]}")
        try:
            j = json.loads(status_text)
            if j.get("code") == 0:
                d = j.get("data", {})
                print(f"Order FZ7M47 Status: {d.get('status')} | {d.get('type')}")
                print(f"From: {d.get('from',{}).get('amount')} {d.get('from',{}).get('code')} -> To: {d.get('to',{}).get('amount')} {d.get('to',{}).get('code')}")
        except:
            pass
    except Exception as e:
        print(f"Check failed: {e}")

    # 2. If FROM_CCY is TRX, create new test order (or if you want new BTC order, keep BTC)
    # Skip create if you only want checker - set env SKIP_CREATE=true
    if os.getenv("SKIP_CREATE","").lower() == "true":
        print("\nSKIP_CREATE=true, not creating new order")
        return

    print(f"\n--- CREATING NEW ORDER {FROM_CCY} -> USDTTRC ---")
    create_params = {
        "fromCcy": FROM_CCY,
        "toCcy": "USDTTRC",
        "amount": test_amount,
        "direction": "from",
        "type": "float",
        "toAddress": TO_ADDR
    }
    result = api_request("create", create_params, API_KEY, API_SECRET)
    print(f"Create Response: {json.dumps(result)[:3000]}")

    if result.get("code") == 0:
        data = result.get("data", {})
        print("\n" + "="*60)
        print("✅ NEW ORDER CREATED")
        print(f"ID: {data.get('id')}")
        print(f"SEND {data.get('from',{}).get('amount')} {data.get('from',{}).get('code')} TO:")
        print(f"{data.get('from',{}).get('address')}")
        print(f"RECEIVE {data.get('to',{}).get('amount')} USDTTRC AT {TO_ADDR}")
        print("="*60)

        # 3. Auto poll status every 30s for 10 mins
        order_id = data.get('id')
        if order_id:
            print(f"\n--- AUTO CHECKING {order_id} every 30s (10 times) ---")
            for i in range(10):
                time.sleep(30)
                try:
                    s = get_order_status(order_id, API_KEY, API_SECRET)
                    j = json.loads(s)
                    if j.get("code")==0:
                        st = j.get("data",{}).get("status")
                        print(f"[{i+1}/10] Status: {st}")
                        if st in ["DONE","EXPIRED","EMERGENCY","CLOSED"]:
                            print(f"Final status: {st}, full: {s[:1000]}")
                            break
                    else:
                        print(f"[{i+1}] Check msg: {j.get('msg')}")
                except Exception as e:
                    print(f"[{i+1}] Check error {e}")
    else:
        print(f"Create failed: {result.get('msg')}")

if __name__ == "__main__":
    main()
