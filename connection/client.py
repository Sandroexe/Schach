import socket


def connect_to_server():
    host = input("Enter the server IP address: ")
    port = 65432

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print(f"Attempting to connect to {host}...")
            sock.connect((host, port))

            data = sock.recv(1024)
            print(f"Response: {data.decode('utf-8')}")
    except Exception as e:
        print(f"Error: Connection could not be established.\n{e}")


if __name__ == "__main__":
    connect_to_server()
