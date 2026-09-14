from src.config import TRACKED_WALLET
from src.connectors.alchemy_rpc import rpc_request


TOKEN_CONTRACT = "0x8b3e3ba1a55b939f93f0a205f94520b9468e17f8"

BALANCE_OF_SELECTOR = "0x70a08231"
DECIMALS_SELECTOR = "0x313ce567"


def encode_address(address: str) -> str:
    clean_address = address.removeprefix("0x")

    return clean_address.lower().rjust(64, "0")


def call_token_function(
    function_selector: str,
    address: str,
) -> str:
    data = function_selector + encode_address(address)

    return rpc_request(
        "eth_call",
        [
            {
                "to": TOKEN_CONTRACT,
                "data": data,
            },
            "latest",
        ],
    )


def main() -> None:
    raw_balance_hex = call_token_function(
        BALANCE_OF_SELECTOR,
        TRACKED_WALLET,
    )

    raw_decimals_hex = rpc_request(
        "eth_call",
        [
            {
                "to": TOKEN_CONTRACT,
                "data": DECIMALS_SELECTOR,
            },
            "latest",
        ],
    )

    raw_balance = int(raw_balance_hex, 16)
    decimals = int(raw_decimals_hex, 16)
    token_balance = raw_balance / (10**decimals)

    print("Wallet:", TRACKED_WALLET)
    print("Raw token balance:", raw_balance)
    print("Token decimals:", decimals)
    print("Human-readable balance:", token_balance)


if __name__ == "__main__":
    main()