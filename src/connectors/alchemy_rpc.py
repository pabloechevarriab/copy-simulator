import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

WALLET_ADDRESS = "0xce7263b5af8331c3baa620db93b44522d5982e35"

RAW_DATA_PATH = Path("data/raw/alchemy_token_transfers.json")


def get_rpc_url() -> str:
    api_key = os.getenv("ALCHEMY_API_KEY")

    if not api_key:
        raise RuntimeError(
            "ALCHEMY_API_KEY is missing from the .env file."
        )

    return f"https://robinhood-mainnet.g.alchemy.com/v2/{api_key}"


def fetch_asset_transfers() -> dict:
    all_transfers = []
    page_key = None

    while True:
        request_params = {
            "fromAddress": WALLET_ADDRESS,
            "category": ["erc20"],
            "withMetadata": True,
            "excludeZeroValue": True,
            "maxCount": "0x64",
        }

        if page_key:
            request_params["pageKey"] = page_key

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "alchemy_getAssetTransfers",
            "params": [request_params],
        }

        response = requests.post(
            get_rpc_url(),
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:
            raise RuntimeError(data["error"])

        result = data["result"]
        all_transfers.extend(result.get("transfers", []))

        page_key = result.get("pageKey")

        if not page_key:
            break

    page_key = None

    while True:
        request_params = {
            "toAddress": WALLET_ADDRESS,
            "category": ["erc20"],
            "withMetadata": True,
            "excludeZeroValue": True,
            "maxCount": "0x64",
        }

        if page_key:
            request_params["pageKey"] = page_key

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "alchemy_getAssetTransfers",
            "params": [request_params],
        }

        response = requests.post(
            get_rpc_url(),
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:
            raise RuntimeError(data["error"])

        result = data["result"]
        all_transfers.extend(result.get("transfers", []))

        page_key = result.get("pageKey")

        if not page_key:
            break

    unique_transfers = {
        transfer["uniqueId"]: transfer
        for transfer in all_transfers
        if transfer.get("uniqueId")
    }

    return {
        "transfers": list(unique_transfers.values()),
        "total_count": len(unique_transfers),
    }


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
    transfers = fetch_asset_transfers()
    save_raw_response(transfers)

    transfer_items = transfers.get("transfers", [])

    print(f"Downloaded {len(transfer_items)} transfers.")
    print(f"Saved raw response to: {RAW_DATA_PATH}")