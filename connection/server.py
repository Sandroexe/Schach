import socket


def get_ip_address():
    """Gibt die eigene lokale IP-Adresse zurück.

    Die UDP-Verbindung zu einer externen Adresse dient nur dazu, die lokale
    Netzwerk-Schnittstelle zu ermitteln. Zielserver und -port müssen nicht
    erreichbar sein.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Ziel-IP kann beliebig sein, Hauptsache es erlaubt dem System, eine
        # Route zu bestimmen und die eigene Adresse zurückzugeben.
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        # Wenn die Abfrage fehlschlägt, wird die Loopback-Adresse verwendet.
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def start_server():
    """Startet den Schach-Server und wartet auf einen Client."""
    host = '0.0.0.0'  # Empfängt Verbindungen von allen Netzwerkschnittstellen.
    port = 65432

    mein_ip = get_ip_address()

    # Öffnet einen TCP-Socket und sorgt dafür, dass er automatisch geschlossen wird.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()  # Wartet auf eingehende Verbindungen.
        print(f"--- SCHACH SERVER ---")
        print(f"Deine lokale IP-Adresse: {mein_ip}")
        print(f"Warte auf Verbindung auf Port {port}...")

        # Akzeptiert eine ankommende Verbindung und blockiert, bis ein Client kommt.
        conn, addr = s.accept()
        with conn:
            # addr enthält die Adresse des Clients in der Form (ip, port).
            print(f"Verbunden mit Client-IP: {addr[0]}")
            # Sendet dem Client eine Bestätigungsmeldung.
            conn.sendall(b"Verbindung zum Schach-Server erfolgreich!")


if __name__ == "__main__":
    # Führt den Server nur aus, wenn das Skript direkt gestartet wird.
    start_server()
