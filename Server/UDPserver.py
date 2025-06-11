import socket
import sys
import threading
import random

def handle_file_transmission(client_socket, filename, client_address):
    # Implemented later
    pass

def handle_download_request(welcome_socket, data, client_address):
    request = data.decode().strip()
    parts = request.split(' ')

    if len(parts) != 2 or parts[0] != "DOWNLOAD":
        return  # Ignore invalid requests

    filename = parts[1]
    try:
        with open(filename, 'rb') as f:
            f.seek(0, 2)
            file_size = f.tell()

        # Randomly select port between 50000-51000
        new_port = random.randint(50000, 51000)

        # Create new socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.bind(('', new_port))

        # Send OK response
        response = f"OK {filename} SIZE {file_size} PORT {new_port}"
        welcome_socket.sendto(response.encode(), client_address)

        # Start new thread to handle file transmission
        threading.Thread(target=handle_file_transmission,
                         args=(client_socket, filename, client_address)).start()

    except FileNotFoundError:
        response = f"ERR {filename} NOT_FOUND"
        welcome_socket.sendto(response.encode(), client_address)

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
        handle_download_request(welcome_socket, data, client_address)


if __name__ == "__main__":
    main()