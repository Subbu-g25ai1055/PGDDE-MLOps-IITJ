import socket
import json
import time

TARGET_NODE = "node2"
TARGET_PORT = 5002


def send_fake_message():

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((TARGET_NODE, TARGET_PORT))

        fake_message = {
            "type": "FAKE_PREPARE",
            "data": "CORRUPTED_TRANSACTION"
        }

        client.send(json.dumps(fake_message).encode())

        client.close()

        print("[ADVERSARY] Sent fake prepare message")

    except Exception as e:
        print(f"[ADVERSARY] Error: {e}")


def run_adversary():

    while True:

        send_fake_message()

        time.sleep(20)


if __name__ == "__main__":
    run_adversary()