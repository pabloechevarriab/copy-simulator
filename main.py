import json
from collections import defaultdict
from pathlib import Path

RAW_DATA_PATH = Path("data/raw/alchemy_token_transfers.json")


def main() -> None:
    data = json.loads(
        RAW_DATA_PATH.read_text(encoding="utf-8")
    )

    transfers = data["response"]["transfers"]

    transfers_by_hash = defaultdict(list)

    for transfer in transfers:
        transaction_hash = transfer.get("hash")

        if transaction_hash:
            transfers_by_hash[transaction_hash].append(transfer)

    print(f"Total transfer events: {len(transfers)}")
    print(f"Unique transactions: {len(transfers_by_hash)}")
    print()

    wallet = "0xce7263b5af8331c3baa620db93b44522d5982e35".lower()

    incoming = 0
    outgoing = 0

    for transfer in transfers:
        from_address = (transfer.get("from") or "").lower()
        to_address = (transfer.get("to") or "").lower()

        if to_address == wallet:
            incoming += 1

        if from_address == wallet:
            outgoing += 1

    print(f"Incoming transfers: {incoming}")
    print(f"Outgoing transfers: {outgoing}")
    print()
    
    incoming_by_contract = defaultdict(int)
    outgoing_by_contract = defaultdict(int)
    token_label_by_contract = {}

    for transfer in transfers:
        from_address = (transfer.get("from") or "").lower()
        to_address = (transfer.get("to") or "").lower()

        raw_contract = transfer.get("rawContract") or {}
        token_contract = (raw_contract.get("address") or "").lower()

        if not token_contract:
            continue

        token_symbol = transfer.get("asset") or "UNKNOWN"
        token_label_by_contract[token_contract] = token_symbol

        if to_address == wallet:
            incoming_by_contract[token_contract] += 1

        if from_address == wallet:
            outgoing_by_contract[token_contract] += 1

    two_way_contracts = set(incoming_by_contract) & set(outgoing_by_contract)

    print("Tokens appearing in both incoming and outgoing transfers:")

    for token_contract in sorted(
        two_way_contracts,
        key=lambda contract: (
            incoming_by_contract[contract] + outgoing_by_contract[contract]
        ),
        reverse=True,
    )[:20]:
        symbol = token_label_by_contract[token_contract]

        print(
            f"  {symbol} | {token_contract} | "
            f"in: {incoming_by_contract[token_contract]} | "
            f"out: {outgoing_by_contract[token_contract]}"
        )

    print()
    
    target_contract = "0xab093def657f15df31b33922a95e047add645b29"

    print("Note: This timeline includes only transfers directly involving the wallet.")
    
    print("SHROOM transfer timeline:")
    
    shroom_transfers = []

    for transfer in transfers:
        raw_contract = transfer.get("rawContract") or {}
        token_contract = (raw_contract.get("address") or "").lower()

        if token_contract != target_contract:
            continue

        from_address = (transfer.get("from") or "").lower()
        to_address = (transfer.get("to") or "").lower()

        if to_address != wallet and from_address != wallet:
            continue

        shroom_transfers.append(transfer)

    shroom_transfers.sort(
        key=lambda transfer: (
            (transfer.get("metadata") or {}).get("blockTimestamp") or ""
        )
    )

    for transfer in shroom_transfers:
        from_address = (transfer.get("from") or "").lower()
        to_address = (transfer.get("to") or "").lower()
        timestamp = (transfer.get("metadata") or {}).get("blockTimestamp")
        amount = transfer.get("value")

        if to_address == wallet:
            direction = "IN "
        else:
            direction = "OUT"

        print(
            f"{timestamp} | {direction} | "
            f"{amount} SHROOM | tx: {transfer.get('hash')}"
        )

    print()
    
    transactions_with_multiple_transfers = 0

    for transaction_hash, transaction_transfers in transfers_by_hash.items():
        if len(transaction_transfers) <= 1:
            continue

        transactions_with_multiple_transfers += 1

        first_transfer = transaction_transfers[0]
        timestamp = (
            first_transfer.get("metadata", {})
            .get("blockTimestamp")
        )

        print("Transaction hash:", transaction_hash)
        print("Timestamp:", timestamp)
        print("Number of transfer events:", len(transaction_transfers))

        for transfer in transaction_transfers:
            print(
                "  ",
                transfer.get("from"),
                "→",
                transfer.get("to"),
                "|",
                transfer.get("asset"),
                "|",
                transfer.get("value"),
            )

        print("-" * 70)

        if transactions_with_multiple_transfers >= 10:
            break

    print()
    print(
        "Transactions with multiple transfer events:",
        transactions_with_multiple_transfers,
    )


if __name__ == "__main__":
    main()