import socket
import threading
import json


class NetworkManager:
    """Manages a persistent TCP connection between two chess clients.

    Protocol: newline-delimited JSON messages.
    Example message: {"board": [["TW", "SW", "LW", "DW", "KW", "LW", "SW", "TW"], ...]}
    """

    def __init__(self):
        self.conn = None
        
        # anderer Variable name weil es ja ned moves back callt sondern as Ganze Board
        self.board_callback = None
        
        self.connected = False
        self.connected_callback = None  # called (with no args) once connection is established
        self.disconnected_callback = None  # Wird aufgerufen, wenn die Verbindung abbricht
        
        # Verbindungsdetails für die automatische Wiederverbindung
        self.role = None  # Entweder 'server' oder 'client'
        self.ip = None    # IP-Adresse des Servers (nur für Client)
        self.port = None  # Port-Nummer
        self.reconnecting = False  # Verhindert parallele Reconnect-Threads

    # Komplettes Speil Brett neu "Besetzen" also ned nur den move sondern alles nochmal aufzeichnen
    
    def set_board_callback(self, cb):
        """Register a function to call when a new board state is received: cb(board_matrix)."""
        self.board_callback = cb

    def set_connected_callback(self, cb):
        """Register a function to call once the connection is established."""
        self.connected_callback = cb

    def set_disconnected_callback(self, cb):
        """Register a function to call when the connection is lost."""
        self.disconnected_callback = cb

    def start_server(self, port=65432):
        """Bind, listen, and block until one client connects.
        
        Call this in a background thread so it does not block the GUI.
        """
        # Speichere die Rolle und den Port für spätere Wiederverbindungen
        self.role = 'server'
        self.port = port
        
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('0.0.0.0', port))
        srv.listen(1)
        print(f"[Server] Waiting for connection on port {port}...")

        try:
            self.conn, addr = srv.accept()
            srv.close()
            self.connected = True
            print(f"[Server] Client connected: {addr[0]}")
            if self.connected_callback:
                self.connected_callback()
            threading.Thread(target=self._recv_loop, daemon=True).start()
        except Exception as e:
            print(f"[Server] Error accepting connection: {e}")

    def connect_to_server(self, ip, port=65432):
        """Connect to the server at the given IP.
        
        Call this in a background thread so it does not block the GUI.
        """
        # Speichere die Rolle, IP und den Port für spätere Wiederverbindungen
        self.role = 'client'
        self.ip = ip
        self.port = port
        
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"[Client] Connecting to {ip}:{port}...")
            self.conn.connect((ip, port))
            self.connected = True
            print(f"[Client] Connected to {ip}")
            if self.connected_callback:
                self.connected_callback()
            threading.Thread(target=self._recv_loop, daemon=True).start()
        except Exception as e:
            print(f"[Client] Connection failed: {e}")
            raise

    # Board Matrix komplett übertragen, nicht nur de Einzelnen Züge
    
    def send_board_state(self, board_matrix):
        """Send the complete board state to the opponent.

        Args:
            board_matrix: Ein 2D Array (Liste in Listen) deines Schachbretts.
        """
        if not self.conn:
            print("[Network] Cannot send board: not connected.")
            return
        try:
            msg = json.dumps({"board": board_matrix}) + "\n"
            self.conn.sendall(msg.encode('utf-8'))
        except Exception as e:
            print(f"[Network] Send error: {e}")
            self.connected = False
            self._handle_disconnect()

    def _recv_loop(self):
        """Background thread: continuously reads incoming moves."""
        buf = ""
        while True:
            try:
                data = self.conn.recv(4096).decode('utf-8')
                if not data:
                    print("[Network] Connection closed by peer.")
                    self.connected = False
                    self._handle_disconnect()
                    break
                buf += data
                # Process all complete newline-delimited messages in the buffer.
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        msg = json.loads(line)
                        
                        # Hier Reaktion auf das Komplette Board, ned nur die einzelnen Züge.
                        
                        if self.board_callback and "board" in msg:
                            self.board_callback(msg["board"])
                            
                    except json.JSONDecodeError as e:
                        print(f"[Network] Bad message: {line!r} — {e}")
            except Exception as e:
                print(f"[Network] Receive error: {e}")
                self.connected = False
                self._handle_disconnect()
                break

    def _handle_disconnect(self):
        """Interne Methode: Wird aufgerufen, wenn die Verbindung verloren geht."""
        # Nur ausführen, wenn wir tatsächlich als getrennt markiert sind und nicht bereits versuchen uns wiederzuverbinden
        if not self.connected and not self.reconnecting:
            self.reconnecting = True
            
            # Schließe alte Socket-Verbindungen sauber
            if self.conn:
                try:
                    self.conn.close()
                except Exception:
                    pass
                self.conn = None
            
            print("[Network] Verbindung verloren! Versuche Wiederverbindung...")
            
            # Benachrichtige die GUI über den Verbindungsabbruch
            if self.disconnected_callback:
                self.disconnected_callback()
                
            # Starte den Wiederverbindungsprozess in einem separaten Hintergrund-Thread
            threading.Thread(target=self._reconnect_loop, daemon=True).start()

    def _reconnect_loop(self):
        """Hintergrund-Thread: Versucht alle 2 Sekunden, die Verbindung wiederherzustellen."""
        import time
        while not self.connected:
            time.sleep(2)  # Wartezeit zwischen den Versuchen
            print(f"[Network] Wiederverbindungsversuch als {self.role}...")
            
            if self.role == 'server':
                try:
                    # Als Server: Erneut einen Socket binden und auf den Client warten
                    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    srv.bind(('0.0.0.0', self.port))
                    srv.listen(1)
                    
                    self.conn, addr = srv.accept()
                    srv.close()
                    
                    self.connected = True
                    self.reconnecting = False
                    print(f"[Server] Wiederverbindung erfolgreich! Client verbunden: {addr[0]}")
                    
                    # GUI benachrichtigen
                    if self.connected_callback:
                        self.connected_callback()
                        
                    # Empfangsthread neu starten
                    threading.Thread(target=self._recv_loop, daemon=True).start()
                    break
                except Exception as e:
                    print(f"[Server] Wiederverbindung fehlgeschlagen: {e}")
                    
            elif self.role == 'client':
                try:
                    # Als Client: Versuche die Verbindung zum Server IP/Port wieder aufzubauen
                    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.conn.connect((self.ip, self.port))
                    
                    self.connected = True
                    self.reconnecting = False
                    print(f"[Client] Wiederverbindung erfolgreich! Verbunden mit {self.ip}")
                    
                    # GUI benachrichtigen
                    if self.connected_callback:
                        self.connected_callback()
                        
                    # Empfangsthread neu starten
                    threading.Thread(target=self._recv_loop, daemon=True).start()
                    break
                except Exception as e:
                    print(f"[Client] Wiederverbindung fehlgeschlagen: {e}")
                    # Socket aufräumen, damit wir im nächsten Durchlauf frisch beginnen können
                    if self.conn:
                        try:
                            self.conn.close()
                        except Exception:
                            pass
                        self.conn = None