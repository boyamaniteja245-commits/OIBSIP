import socket
import threading
from datetime import datetime

HOST = "localhost"
PORT = 5555

clients = {}
lock = threading.Lock()


def timestamp():
    return datetime.now().strftime("%H:%M")


def broadcast(message, exclude=None):
    with lock:
        disconnected = []

        for client in clients:
            if client != exclude:
                try:
                    client.send(message.encode("utf-8"))
                except:
                    disconnected.append(client)

        for client in disconnected:
            clients.pop(client, None)


def handle_client(client_socket, address):
    try:
        username = client_socket.recv(1024).decode("utf-8").strip()

        if not username:
            username = f"User-{address[1]}"

        with lock:
            clients[client_socket] = username

        join_message = f"[{timestamp()}] Server: {username} joined the chat."
        print(join_message)
        broadcast(join_message, exclude=client_socket)

        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            message = data.decode("utf-8").strip()

            if message.lower() == "/quit":
                break

            formatted_message = f"[{timestamp()}] {username}: {message}"

            print(formatted_message)
            broadcast(formatted_message)

    except ConnectionResetError:
        pass

    finally:
        with lock:
            username = clients.pop(client_socket, "Unknown")

        disconnect_message = (
            f"[{timestamp()}] Server: {username} disconnected."
        )

        print(disconnect_message)
        broadcast(disconnect_message)

        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started on {HOST}:{PORT}")
    print("Waiting for clients...")
    print("Press Ctrl+C to stop the server.")

    try:
        while True:
            client_socket, address = server.accept()

            print(f"New connection from {address}")

            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address),
                daemon=True
            )

            thread.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()