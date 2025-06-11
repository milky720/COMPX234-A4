import socket
import sys


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 UDPclient.py <hostname> <port> <filelist>")
        return

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    filelist = sys.argv[3]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"Client connecting to {hostname}:{port} with file list {filelist}")


if __name__ == "__main__":
    main()