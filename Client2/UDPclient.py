import socket
import sys
import base64
import os

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
    # Send download request
    request = f"DOWNLOAD {filename}"
    response = send_and_receive(socket, server_address, request)

    if not response:
        print(f"Failed to get response for {filename}")
        return

    # Parse server response
    parts = response.split(' ')
    if parts[0] == "ERR":
        print(f"Error: {response}")
        return

    # Parse OK response
    file_size = int(parts[3])
    data_port = int(parts[5])

    # Create local file
    try:
        with open(filename, 'wb') as f:
            print(f"Downloading {filename} ({file_size} bytes): ", end='', flush=True)

            # Download file blocks
            downloaded = 0
            block_size = 1000  # Block size (matches server)
            data_address = (server_address[0], data_port)

            while downloaded < file_size:
                # Calculate current block range
                start = downloaded
                end = min(downloaded + block_size - 1, file_size - 1)

                # Request data block
                request = f"FILE {filename} GET START {start} END {end}"
                response = send_and_receive(socket, data_address, request)

                if not response:
                    print("\nFailed to receive data block")
                    return

                # Process data response
                resp_parts = response.split(' DATA ')
                if len(resp_parts) != 2:
                    print("\nInvalid data response")
                    return

                # Decode and write to file
                data_part = resp_parts[1]
                binary_data = base64.b64decode(data_part)
                f.seek(start)
                f.write(binary_data)

                downloaded += len(binary_data)
                print("*", end='', flush=True)

            # Send close request
            request = f"FILE {filename} CLOSE"
            response = send_and_receive(socket, data_address, request)

            # Verify close confirmation
            if response and response.startswith(f"FILE {filename} CLOSE_OK"):
                print(f"\nSuccessfully downloaded {filename}")
            else:
                print(f"\nWarning: Close confirmation not received for {filename}")

    except IOError as e:
        print(f"\nError writing file {filename}: {e}")

if __name__ == "__main__":
    main()