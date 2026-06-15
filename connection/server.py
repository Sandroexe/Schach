import socket


def get_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('8.8.8.8', 1))
        ip = sock.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        sock.close()
    return ip


def start_server():
    host = '0.0.0.0'
    port = 65432

    local_ip = get_ip_address()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        print(f"--- CHESS SERVER ---")
        print(f"Your local IP address: {local_ip}")
        print(f"Waiting for connection on port {port}...")

        conn, addr = sock.accept()
        with conn:
            print(f"Connected with client IP: {addr[0]}")
            conn.sendall(b"Successfully connected to Chess server!")


if __name__ == "__main__":
    start_server()
