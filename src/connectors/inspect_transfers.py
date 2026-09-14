import json
from pathlib import Path

RAW_DATA_PATH = Path("data/raw/alchemy_token_transfers.json")


def main() -> None:
    data = json.loads(RAW_DATA_PATH.read_text(encoding="utf-8"))

    transfers = data["response"]["transfers"]

    print(f"Total transfers: {len(transfers)}")
    print()

    for index, transfer in enumerate(transfers[:5], start=1):
        print(f"Transfer {index}")
        print("Transaction hash:", transfer.get("hash"))
        print("Block number:", transfer.get("blockNum"))
        print("From:", transfer.get("from"))
        print("To:", transfer.get("to"))
        print("Asset:", transfer.get("asset"))
        print("Value:", transfer.get("value"))
        print("Category:", transfer.get("category"))
        print("Metadata:", transfer.get("metadata"))
        print("-" * 60)


if __name__ == "__main__":
    main()