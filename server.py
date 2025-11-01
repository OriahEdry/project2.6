"""
author: Oriah Edry
Program name: project 2.6
Description:
Date: 01/11/2025
"""
import socket
import datetime
import random
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler('log.txt', mode='a', encoding='utf-8')  # רק לקובץ
    ]
)

def create_server_socket(host='127.0.0.1', port=6741):
    """Create and bind the server socket."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[SERVER] Listening on {host}:{port}")
    logging.info("[SERVER] Listening on {host}:{port}")
    return server_socket


def process_command(command, server_name="OriahProServer"):
    """Return response string based on the received command."""
    assert isinstance(command, str), "Command must be a string"
    command = command.strip().upper()

    if command == "TIME":
        return datetime.datetime.now().strftime("%H:%M:%S")
    elif command == "NAME":
        return server_name
    elif command == "RAND":
        random1 = (random.randint(1, 10))

        assert random1 < 11, "invalid random number"
        assert random1 > 0, "invalid random number"
        return str(random1)


    elif command == "EXIT":
        return "Goodbye!"
    else:
        return "Unknown command"


def handle_client(client_socket, server_name="OriahProServer"):
    """Handle communication with a single connected client."""
    with client_socket:
        while True:
            # Receive exactly 4 bytes for the command
            data = client_socket.recv(4)
            if not data:
                print("[SERVER] Client disconnected.")
                logging.info("[SERVER] Client disconnected.")
                break

            command = data.decode('utf-8').strip().upper()
            assert len(command) > 0, "Received empty command"
            print(f"[SERVER] Received command: {command}")
            logging.info("[SERVER] Received command: {command}")

            # Process and prepare response
            response = process_command(command, server_name)
            assert isinstance(response, str), "Response must be a string"

            response_bytes = response.encode('utf-8')
            length_prefix = f"{len(response_bytes):04}"  # e.g., "0008"
            assert len(length_prefix) == 4, "Length prefix must be exactly 4 bytes"

            # Send length prefix + message
            client_socket.sendall(length_prefix.encode('utf-8') + response_bytes)
            print(f"[SERVER] Sent: '{response}' ({len(response_bytes)} bytes)")
            logging.info("[SERVER] Sent: '{response}' ({len(response_bytes)} bytes)")

            # Exit condition
            if command == "EXIT":
                print("[SERVER] Client requested to disconnect.")
                logging.info("[SERVER] Client disconnected.")
                break


def start_server(host='127.0.0.1', port=6741):
    """Main function to start the server and handle incoming clients."""
    server_socket = create_server_socket(host, port)

    while True:
        print("[SERVER] Waiting for a new client...")
        logging.info("Waiting for a new client...")
        client_socket, client_address = server_socket.accept()
        print(f"[SERVER] Connected to {client_address}")
        logging.info("Connected to %s", client_address)
        handle_client(client_socket)
        print("[SERVER] Ready for the next client.\n")
        logging.info("Ready for next client.")


if __name__ == "__main__":
    start_server()
