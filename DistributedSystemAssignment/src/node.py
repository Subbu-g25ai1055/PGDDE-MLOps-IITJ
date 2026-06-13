import socket
import threading
import json
import os
import time

# Current node ID from Docker environment
NODE_ID = os.environ.get("NODE_ID", "node1")

# Node port mapping
PORTS = {
    "node1": 5001,
    "node2": 5002,
    "node3": 5003,
    "node4": 5004,
    "node5": 5005
}

HOST = "0.0.0.0"
PORT = PORTS[NODE_ID]

# Other cluster nodes
PEERS = [node for node in PORTS if node != NODE_ID]

# Distributed ledger
ledger = []

# Failed nodes tracker
failed_nodes = set()

# Initial leader
leader = "node5"

# Heartbeat tracking
last_heartbeat = time.time()

# Timeout duration
HEARTBEAT_TIMEOUT = 10


def log(message):
    print(f"[{NODE_ID}] {message}", flush=True)


def elect_new_leader():

    global leader

    # Deterministic failover order
    failover_order = [
        "node5",
        "node4",
        "node3",
        "node2",
        "node1"
    ]

    # Select highest available node
    for node in failover_order:

        if node not in failed_nodes:

            leader = node

            break

    log(f"Leader election completed -> New leader: {leader}")


def handle_connection(conn, addr):

    global last_heartbeat
    global leader

    try:

        data = conn.recv(4096).decode()

        if not data:
            return

        message = json.loads(data)

        msg_type = message.get("type")

        # HEARTBEAT MESSAGE
        if msg_type == "HEARTBEAT":

            sender = message.get("leader")

            leader = sender

            last_heartbeat = time.time()

            log(f"Heartbeat received from {sender}")

        # TRANSACTION MESSAGE
        elif msg_type == "TRANSACTION":

            transaction = message.get("data")

            log(
                f"Transaction received -> "
                f"ID: {transaction['id']}, "
                f"Amount: {transaction['amount']}"
            )

            ledger.append(transaction)

            log(
                f"Ledger synchronized -> "
                f"{len(ledger)} transactions committed"
            )

        # BYZANTINE MESSAGE
        elif msg_type == "FAKE_PREPARE":

            log("WARNING: Byzantine fake prepare message detected")

        else:

            log(f"Unknown message type: {msg_type}")

    except Exception as e:

        log(f"Error handling connection: {e}")

    finally:

        conn.close()


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen()

    log(f"Listening on port {PORT}")

    while True:

        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_connection,
            args=(conn, addr)
        )

        thread.start()


def send_message(target_node, message):

    try:

        peer_port = PORTS[target_node]

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((target_node, peer_port))

        client.send(json.dumps(message).encode())

        client.close()

    except Exception as e:

        log(f"Failed to send message to {target_node}: {e}")


def heartbeat_loop():

    while True:

        # Only leader sends heartbeats
        if NODE_ID == leader:

            for peer in PEERS:

                # Skip failed nodes
                if peer in failed_nodes:
                    continue

                heartbeat_message = {
                    "type": "HEARTBEAT",
                    "leader": NODE_ID
                }

                send_message(peer, heartbeat_message)

        time.sleep(3)


def leader_monitor():

    global last_heartbeat

    while True:

        # Followers monitor leader heartbeat
        if NODE_ID != leader:

            elapsed = time.time() - last_heartbeat

            if elapsed > HEARTBEAT_TIMEOUT:

                failed_nodes.add(leader)

                log("Leader timeout detected")

                log("Starting leader election")

                elect_new_leader()

                last_heartbeat = time.time()

        time.sleep(2)


if __name__ == "__main__":

    log("Node starting...")

    # Start TCP server
    threading.Thread(target=start_server).start()

    # Start heartbeat sender
    threading.Thread(target=heartbeat_loop).start()

    # Start leader monitoring
    threading.Thread(target=leader_monitor).start()

    while True:
        time.sleep(1)