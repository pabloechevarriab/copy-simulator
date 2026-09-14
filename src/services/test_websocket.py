import json

import websocket

from src.config import ALCHEMY_WS_URL


def main() -> None:
    connection = websocket.create_connection(
        ALCHEMY_WS_URL,
        timeout=30,
    )

    subscription_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_subscribe",
        "params": ["newHeads"],
    }

    connection.send(json.dumps(subscription_request))

    subscription_response = json.loads(connection.recv())

    print("Subscription response:")
    print(subscription_response)

    print("Waiting for the next block...")

    block_notification = json.loads(connection.recv())

    print("New block notification:")
    print(block_notification)

    connection.close()


if __name__ == "__main__":
    main()