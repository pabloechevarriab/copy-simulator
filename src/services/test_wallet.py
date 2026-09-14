from src.config import TRACKED_WALLET
from src.connectors.alchemy_rpc import rpc_request


def main() -> None:
    balance_hex = rpc_request(
        "eth_getBalance",
        [TRACKED_WALLET, "latest"],
    )

    balance_wei = int(balance_hex, 16)
    balance_eth = balance_wei / 10**18

    print("Tracked wallet:", TRACKED_WALLET)
    print("Balance in wei:", balance_wei)
    print("Balance in ETH:", balance_eth)


if __name__ == "__main__":
    main()