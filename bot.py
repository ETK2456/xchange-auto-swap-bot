import requests, os, json

BASE_URL = "https://xchange.me/api/v1"

def main():
    # Get from GitHub Secrets
    FROM = os.getenv("FROM_CURRENCY", "btc").lower().strip()
    TO = os.getenv("TO_CURRENCY", "usdt").lower().strip()
    AMOUNT = os.getenv("FROM_AMOUNT", "0.001").strip()
    TO_ADDR = os.getenv("TO_ADDRESS", "").strip() # TJ4B... Binance TRC20
    REFUND = os.getenv("REFUND_ADDRESS", "").strip() # BTC refund

    print("="*50)
    print(f"XCHANGE BOT - LIVE MODE")
    print(f"Swap: {AMOUNT} {FROM.upper()} -> {TO.upper()}")
    print(f"Receive at: {TO_ADDR}")
    print(f"Refund to: {REFUND}")
    print("="*50)

    if not TO_ADDR or not REFUND:
        print("ERROR: TO_ADDRESS or REFUND_ADDRESS secret missing!")
        return

    # Step 1: Create exchange
    url = f"{BASE_URL}/exchange"
    payload = {
        "from_currency": FROM,
        "to_currency": TO,
        "from_amount": str(AMOUNT),
        "to_address": TO_ADDR,
        "refund_address": REFUND
    }

    print(f"\n[1] Creating order... {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        r = requests.post(url, json=payload, timeout=30)
        print(f"\nStatus Code: {r.status_code}")
        print(f"Raw Response: {r.text}\n")

        data = r.json()

        # Check success
        if r.status_code == 200 or r.status_code == 201:
            print("✅ ORDER CREATED SUCCESSFULLY!")
            print(json.dumps(data, indent=2))

            payin = data.get("payin_address") or data.get("from", {}).get("address") or data.get("payinAddress")
            payin_amount = data.get("payin_amount") or data.get("from", {}).get("amount") or AMOUNT
            order_id = data.get("id") or data.get("order_id") or "N/A"

            print("\n" + "="*50)
            print(f"👉 SEND {payin_amount} BTC TO:")
            print(f" {payin}")
            print(f"Order ID: {order_id}")
            print(f"USDT will arrive at: {TO_ADDR} (TRC20)")
            print("="*50)

        else:
            print("❌ FAILED TO CREATE ORDER")
            print(f"Error: {data}")

    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    main()
