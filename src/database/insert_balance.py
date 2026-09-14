import csv
from pathlib import Path

from src.database.connection import get_connection

CSV_PATH = Path("data/processed/current_token_balances.csv")


def insert_balances() -> None:
    connection = get_connection()

    with CSV_PATH.open(
        mode="r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            connection.execute(
                """
                INSERT INTO token_balances (
                    chain,
                    wallet_address,
                    token_contract,
                    raw_balance,
                    decimals,
                    human_balance,
                    observed_at_utc
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["chain"],
                    row["wallet_address"],
                    row["token_contract"],
                    row["raw_balance"],
                    int(row["decimals"]),
                    row["human_balance"],
                    row["observed_at_utc"],
                ),
            )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    insert_balances()
    print("Balance inserted successfully.")