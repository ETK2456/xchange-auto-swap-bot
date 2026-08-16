import requests, os, json

BASE = "https://xchange.me/api/v1"

def main():
    from_cur = os.getenv("FROM_CURRENCY", "btc").lower()
    to_cur = os.getenv("TO_CURRENCY", "usdt").lower()
    amount = os.getenv("FROM_AMOUNT", "0.001")
    to_addr = os.getenv("TO_ADDRESS", "TJ4BveBmTkbozPk5wR7GXcQwfL8FHszQAe")
    refund_addr = os.getenv("REFUND_ADDRESS", "")

    print(f"=== BOT START ===")
    print(f"FROM: {from_cur} AMOUNT: {amount}")
    print(f"TO: {to_cur} ADDRESS: {to_addr}")
    print(f"REFUND: {refund_addr[:10]}...")

    # 1. Check currencies
    try:
        r = requests.get(f"{BASE}/currencies/to", timeout=10)
        print(f"\nTO currencies available: {r.text[:500]}")
    except Exception as e:
        print(f"Currency check failed: {e}")

    # 2. Estimate
    try:
        params = {
            "from_currency": from_cur,
            "to_currency": to_cur,
            "from_amount": amount
        }
        r = requests.get(f"{BASE}/exchange/estimate", params=params, timeout=15)
        print(f"\nESTIMATE status: {r.status_code}")
        print(f"ESTIMATE body: {r.text}")
        data = r.json() if r.ok else {}
        if r.ok:
            print(f"\n*** RATE: 1 {from_cur} = {data.get('to_amount', '?')} {to_cur} ***")
            print("Estimate OK! Your TO_CURRENCY name is correct.")
        else:
            print(f"\nIf error says 'invalid currency', try changing TO_CURRENCY secret to: usdt_tron or usdttrc20 or usdt_trc20")
    except Exception as e:
        print(f"Estimate failed: {e}")

    print("\n=== TEST DONE - NO REAL ORDER CREATED ===")

if __name__ == "__main__":
    main()
