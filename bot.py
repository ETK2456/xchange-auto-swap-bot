import requests, os, json, subprocess

TO_ADDR = "TJ4BveBmTkbozPk5wR7GXcQwfL8FHszQAe"  # <-- YOUR BINANCE TRC20

def main():
    FROM = os.getenv("FROM_CURRENCY", "btc").lower()
    TO = os.getenv("TO_CURRENCY", "usdt").lower()
    AMOUNT = os.getenv("FROM_AMOUNT", "0.001")
    REFUND = os.getenv("REFUND_ADDRESS", "").strip()

    # Use secret if set, else use pasted address
    final_to = os.getenv("TO_ADDRESS", TO_ADDR).strip() or TO_ADDR

    print(f"=== LIVE SWAP ===")
    print(f"{AMOUNT} {FROM} -> {TO} (TRC20-TRX chain)")
    print(f"TO: {final_to}")
    print(f"REFUND: {REFUND}")

    try:
        print("\nDownloading xm-cli.py...")
        r = requests.get("https://xchange.me/xm-cli.py", timeout=15)
        open("xm-cli.py","w").write(r.text)
        
        cmd = f'python3 xm-cli.py create-exchange {FROM} {TO} {final_to} --amount {AMOUNT} --withdraw-to trx --refund-address {REFUND}'
        print(f"Running: {cmd}\n")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=40)
        print(result.stdout)
        print(result.stderr)
        
        if "payin" in result.stdout.lower() or "please pay" in result.stdout.lower():
            print("\n✅ ORDER CREATED - SEND BTC TO ADDRESS ABOVE!")
        else:
            print("\nCheck output above")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
