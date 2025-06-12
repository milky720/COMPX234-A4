import socket
import sys

def send_and_receive(socket, address, message, max_attempts=5):
    current_timeout = 1000  # The initial timeout is 1 second
    attempts = 0

    while attempts < max_attempts:
        try:
            socket.sendto(message.encode(), address)
            socket.settimeout(current_timeout / 1000)

            response, _ = socket.recvfrom(4096)
            return response.decode()

        except socket.timeout:
            attempts += 1
            current_timeout *= 2
            print(f"Timeout, attempt {attempts} of {max_attempts}, new timeout: {current_timeout}ms")

    return None

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 UDPclient.py <hostname> <port> <filelist>")
        return

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    filelist = sys.argv[3]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"Client connecting to {hostname}:{port} with file list {filelist}")

    try:
        with open(filelist, 'r') as f:
            files_to_download = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File list {filelist} not found")
        return

    server_address = (hostname, port)

    for filename in files_to_download:
        print(f"Requesting file: {filename}")
        download_file(client_socket, server_address, filename)


def download_file(socket, server_address, filename):
    request = f"DOWNLOAD {filename}"
    response = send_and_receive(socket, server_address, request)

    if not response:
        print(f"Failed to get response for {filename}")
        return

    print(f"Server response: {response}")

if __name__ == "__main__":
    main()