import requests

from src.config import (
    ALCHEMY_API_KEY,
    ALCHEMY_HTTP_URL,
)


def rpc_request(method: str, params: list) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }

    response = requests.post(
        ALCHEMY_HTTP_URL,
        json=payload,
        timeout=20,
    )

    response.raise_for_status()

    result = response.json()

    if "error" in result:
        raise RuntimeError(result["error"])

    return result["result"]


def main() -> None:
    if not ALCHEMY_API_KEY:
        raise ValueError("ALCHEMY_API_KEY is missing.")

    chain_id_hex = rpc_request("eth_chainId", [])
    latest_block_hex = rpc_request("eth_blockNumber", [])

    chain_id = int(chain_id_hex, 16)
    latest_block = int(latest_block_hex, 16)

    print("Connected chain ID:", chain_id)
    print("Latest block:", latest_block)


if __name__ == "__main__":
    main()