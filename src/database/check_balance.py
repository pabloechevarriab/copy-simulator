from src.database.connection import get_connection


def show_balances() -> None:
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            chain,
            wallet_address,
            token_contract,
            human_balance,
            observed_at_utc
        FROM token_balances
        """
    ).fetchall()

    connection.close()

    for row in rows:
        print(row)


if __name__ == "__main__":
    show_balances()