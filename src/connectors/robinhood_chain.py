import json
from datetime import datetime, timezone
from pathlib import Path

import requests

ROBINHOOD_API_URL = (
    "https://robinhoodchain.blockscout.com/api/v2/addresses"
)

WALLET_ADDRESS = "0xce7263b5af8331c3baa620db93b44522d5982e35"

RAW_DATA_PATH = Path("data/raw/robinhood_token_transfers.json")


def fetch_token_transfers(wallet_address: str) -> dict:
    url = f"{ROBINHOOD_API_URL}/{wallet_address}/token-transfers"

    response = requests.get(
        url,
        params={"limit": 50},
        timeout=20,
    )

    response.raise_for_status()

    return response.json()


def save_raw_response(data: dict) -> None:
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    output = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "wallet_address": WALLET_ADDRESS,
        "response": data,
    }

    RAW_DATA_PATH.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    data = fetch_token_transfers(WALLET_ADDRESS)
    save_raw_response(data)

    items = data.get("items", [])

    print(f"Downloaded {len(items)} token transfers.")
    print(f"Saved raw response to: {RAW_DATA_PATH}")