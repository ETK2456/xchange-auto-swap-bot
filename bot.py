import requests, os, json

# Xchange.me real API - using their web endpoint that xm-cli.py uses
BASE = "https://xchange.me/api"

def main():
    FROM = os.getenv("FROM_CURRENCY", "btc").lower()
    TO = os.getenv("TO_CURRENCY", "usdt").lower()  # must be usdt for your case
    AMOUNT = os.getenv("FROM_AMOUNT", "0.001")
    TO_ADDR = os.getenv("TO_ADDRESS", "").strip()  # Your TJ4B... TRC20
    REFUND = os.getenv("REFUND_ADDRESS", "").strip()

    print(f"=== LIVE: {AMOUNT} {FROM} -> {TO} (TRC20) ===")
    print(f"TO_ADDR: {TO_ADDR}")
    print(f"REFUND: {REFUND}")

    if not TO_ADDR:
        print("ERROR: TO_ADDRESS missing!")
        return

    # The correct way: use xchange.me exchange creation endpoint
    # According to CLI docs: --withdraw-to trx for USDT-TRC20
    # Endpoint found in xm-cli.py is /api/exchange
    
    url = "https://xchange.me/api/exchange"
    
    # Try the actual API format from CLI
    payload = {
        "from_currency": FROM,
        "to_currency": TO,
        "to_address": TO_ADDR,
        "refund_address": REFUND,
        "from_amount": AMOUNT,
        "withdraw_to": "trx",  # <-- THIS IS KEY FOR TRC20!
        "dest_chain": "trx"
    }
    
    # Try 1: POST to /api/exchange
    try:
        print(f"\n[TRY 1] POST {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        r = requests.post(url, json=payload, headers={"Content-Type": "application/json", "Accept": "application/json"}, timeout=30)
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text[:2000]}")
        if "payin_address" in r.text.lower() or "address" in r.text.lower() and r.status_code in [200,201]:
            print("\n✅ SUCCESS!")
            return
    except Exception as e:
        print(f"Try1 error: {e}")

    # Try 2: POST to /api/v1/exchange/create
    try:
        url2 = "https://xchange.me/api/v1/exchange"
        print(f"\n[TRY 2] POST {url2}")
        r = requests.post(url2, json=payload, timeout=30)
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text[:2000]}")
    except Exception as e:
        print(f"Try2 error: {e}")

    # Try 3: Using xm-cli.py directly - download and run like official CLI
    print("\n[TRY 3] Downloading official xm-cli.py and using it")
    try:
        cli_url = "https://xchange.me/xm-cli.py"
        cli_code = requests.get(cli_url, timeout=15).text
        open("xm-cli.py", "w").write(cli_code)
        print("Downloaded xm-cli.py")
        print("Run it with: python3 xm-cli.py create-exchange btc usdt YOUR_ADDR --amount 0.001 --withdraw-to trx")
        # We can't run torsocks in Actions, but run without --onion
        import subprocess
        cmd = f'python3 xm-cli.py create-exchange {FROM} {TO} {TO_ADDR} --amount {AMOUNT} --withdraw-to trx --refund-address {REFUND}'
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except Exception as e:
        print(f"Try3 error: {e}")

if __name__ == "__main__":
    main()
