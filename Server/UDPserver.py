import socket
import sys
import threading


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 UDPserver.py <port>")
        return

    port = int(sys.argv[1])
    welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    welcome_socket.bind(('', port))

    print(f"Server started on port {port}")

    while True:
        data, client_address = welcome_socket.recvfrom(1024)
        print(f"Received connection from {client_address}")


if __name__ == "__main__":
    main()