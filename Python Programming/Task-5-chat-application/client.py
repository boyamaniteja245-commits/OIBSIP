import socket
import threading

HOST = "localhost"
PORT = 5555


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:
                print("\nDisconnected from server.")
                break

            print(f"\n{message}")
            print("You: ", end="", flush=True)

        except:
            print("\nConnection to server lost.")
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Could not connect to the server.")
        print("Make sure server.py is running first.")
        return

    username = input("Enter your username: ")

    client_socket.send(username.encode("utf-8"))

    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    )

    receive_thread.start()

    print("\nConnected to the chat!")
    print("Type your messages below.")
    print("Type /quit to leave the chat.\n")

    try:
        while True:
            message = input("You: ")

            if not message:
                continue

            client_socket.send(message.encode("utf-8"))

            if message.lower() == "/quit":
                break

    except KeyboardInterrupt:
        client_socket.send("/quit".encode("utf-8"))

    finally:
        client_socket.close()
        print("Disconnected from chat.")


if __name__ == "__main__":
    start_client()