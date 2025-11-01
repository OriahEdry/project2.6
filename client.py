"""
author: Oriah Edry
Program name: project 2.6
Description:
Date: 01/11/2025
"""
import socket


# ----------------------------- CLIENT SETUP -----------------------------
def create_client_socket(host='127.0.0.1', port=6741):
    """Create and connect the client socket."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"[CLIENT] Connected to {host}:{port}")
    return client_socket


# ----------------------------- SEND & RECEIVE -----------------------------
def send_command(client_socket, command):
    """Send a 4-byte command and receive a length-prefixed response."""
    assert isinstance(command, str), "Command must be a string"
    command = command.strip().upper()
    message = command.ljust(4)[:4]  # pad or cut to 4 bytes
    assert len(message) == 4, "Command must be exactly 4 bytes"

    # Send command
    client_socket.sendall(message.encode('utf-8'))

    # Receive 4-byte length prefix
    length_data = client_socket.recv(4)
    if not length_data:
        print("[CLIENT] Server closed the connection.")
        return None

    response_length = int(length_data.decode('utf-8'))
    assert response_length >= 0, "Invalid response length"

    # Receive full message
    response_data = b""
    while len(response_data) < response_length:
        packet = client_socket.recv(response_length - len(response_data))
        if not packet:
            break
        response_data += packet

    assert len(response_data) == response_length, "Incomplete response received"
    return response_data.decode('utf-8')


# ----------------------------- MAIN CLIENT LOOP -----------------------------
def start_client(host='127.0.0.1', port=6741):
    """Main loop to send commands to the server."""
    client_socket = create_client_socket(host, port)

    print("Available commands: TIME, NAME, RAND, EXIT")

    while True:
        command = input("Enter command: ").strip()
        if not command:
            continue

        response = send_command(client_socket, command)
        if response is None:
            break
        print(f"[SERVER RESPONSE] {response}")

        if command.upper() == "EXIT":
            break

    client_socket.close()
    print("[CLIENT] Disconnected from server.")


# ----------------------------- ENTRY POINT -----------------------------
if __name__ == "__main__":
    start_client()