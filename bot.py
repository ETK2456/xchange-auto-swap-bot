import requests, os, json, time
BASE = "https://xchange.me/api/v1"

def create_order():
    from_cur = os.getenv("FROM_CURRENCY", "btc")
    to_cur = os.getenv("TO_CURRENCY", "usdt")
    amount = os.getenv("FROM_AMOUNT", "0.001")
    to_addr = os.getenv("TO_ADDRESS")
    refund_addr = os.getenv("REFUND_ADDRESS")

    print(f"=== CREATING REAL ORDER ===")
    print(f"{amount} {from_cur} -> {to_cur} to {to_addr}")

    payload = {
        "from_currency": from_cur,
        "to_currency": to_cur,
        "from_amount": amount,
        "to_address": to_addr,
        "refund_address": refund_addr
    }

    try:
        r = requests.post(f"{BASE}/exchange", json=payload, timeout=20)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")

        data = r.json()
        if r.status_code == 200 and "payin_address" in str(data).lower():
            print("\n*** SUCCESS! SEND YOUR BTC TO: ***")
            print(json.dumps(data, indent=2))
            # Save order info
            with open("last_order.json", "w") as f:
                json.dump(data, f, indent=2)
        else:
            print("\nCheck response above for payin address")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_order()
