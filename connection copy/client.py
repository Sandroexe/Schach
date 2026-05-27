import socket


def connect_to_server():
    """Connect to the Chess server and receive a response."""
    # User must enter the server IP address.
    host = input("Enter the server IP address: ")
    port = 65432

    try:
        # Open TCP socket and ensure it is closed at the end.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print(f"Attempting to connect to {host}...")
            sock.connect((host, port))

            # Receive up to 1024 bytes from server.
            data = sock.recv(1024)
            print(f"Response: {data.decode('utf-8')}")
    except Exception as e:
        # Print error message for any connection failure.
        print(f"Error: Connection could not be established.\n{e}")


if __name__ == "__main__":
    # Führt die Verbindungsfunktion nur aus, wenn das Skript direkt gestartet wird.
    connect_to_server()
