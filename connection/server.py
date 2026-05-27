import socket


def get_ip_address():
    """Get the local IP address.

    The UDP connection to an external address is only used to determine the local
    network interface. The target server and port do not need to be reachable.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Target IP can be any, as long as it allows the system to determine a
        # route and return the local address.
        sock.connect(('8.8.8.8', 1))
        ip = sock.getsockname()[0]
    except Exception:
        # If the query fails, use the loopback address.
        ip = '127.0.0.1'
    finally:
        sock.close()
    return ip


def start_server():
    """Start the Chess server and wait for a client connection."""
    host = '0.0.0.0'  # Accept connections from all network interfaces.
    port = 65432

    local_ip = get_ip_address()

    # Open TCP socket and ensure it is automatically closed.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()  # Wait for incoming connections.
        print(f"--- CHESS SERVER ---")
        print(f"Your local IP address: {local_ip}")
        print(f"Waiting for connection on port {port}...")

        # Accept an incoming connection and block until a client arrives.
        conn, addr = sock.accept()
        with conn:
            # addr contains the client address in the form (ip, port).
            print(f"Connected with client IP: {addr[0]}")
            # Send confirmation message to client.
            conn.sendall(b"Successfully connected to Chess server!")


if __name__ == "__main__":
    # Führt den Server nur aus, wenn das Skript direkt gestartet wird.
    start_server()
