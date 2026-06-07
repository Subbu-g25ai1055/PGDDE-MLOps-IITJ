import socket
import json
import time

LEADER_HOST = "node1"
LEADER_PORT = 5001


def send_transaction(transaction):

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((LEADER_HOST, LEADER_PORT))

        message = {
            "type": "TRANSACTION",
            "data": transaction
        }

        client.send(json.dumps(message).encode())

        client.close()

        print(f"[CLIENT] Sent transaction: {transaction}")

    except Exception as e:
        print(f"[CLIENT] Error sending transaction: {e}")


def run_client():

    counter = 1

    while True:

        transaction = {
            "id": counter,
            "amount": counter * 100
        }

        send_transaction(transaction)

        counter += 1

        time.sleep(10)


if __name__ == "__main__":
    run_client()
