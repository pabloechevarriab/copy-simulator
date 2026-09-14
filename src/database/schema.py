from src.database.connection import get_connection


def create_tables() -> None:
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS token_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chain TEXT NOT NULL,
            wallet_address TEXT NOT NULL,
            token_contract TEXT NOT NULL,
            raw_balance TEXT NOT NULL,
            decimals INTEGER NOT NULL,
            human_balance TEXT NOT NULL,
            observed_at_utc TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")