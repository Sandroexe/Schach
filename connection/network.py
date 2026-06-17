import socket
import threading
import json


class NetworkManager:

    def __init__(self):
        self.conn = None
        self.board_callback = None
        self.connected = False
        self.connected_callback = None
        self.disconnected_callback = None
        self.role = None
        self.ip = None
        self.port = None
        self.reconnecting = False

    def set_board_callback(self, cb):
        self.board_callback = cb

    def set_connected_callback(self, cb):
        self.connected_callback = cb

    def set_disconnected_callback(self, cb):
        self.disconnected_callback = cb

    def start_server(self, port=65432):
        # 1. Rolle als Server speichern (wichtig fuer spaetere Logik)
        self.role = 'server'
        self.port = port
        
        # 2. Einen TCP-Socket erstellen (AF_INET = IPv4, SOCK_STREAM = TCP)
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 3. Socket-Option setzen: Erlaubt das sofortige Wiederverwenden des Ports nach einem Neustart
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 4. Den Socket an alle verfuegbaren Netzwerkkarten ('0.0.0.0') und den Port binden
        srv.bind(('0.0.0.0', port))
        # 5. Auf Verbindung warten (max. 1 Client in der Warteschlange)
        srv.listen(1)
        print(f"[Server] Waiting for connection on port {port}...")

        try:
            # 6. Verbindung annehmen (blockiert das Programm, bis der Client beitreten will)
            # conn ist die Verbindung zum Client, addr enthaelt die IP-Adresse des Clients
            self.conn, addr = srv.accept()
            # 7. Den lauschenden Server-Socket schliessen, da wir nur einen Client wollten
            srv.close()
            # 8. Status auf Verbunden setzen
            self.connected = True
            print(f"[Server] Client connected: {addr[0]}")
            # 9. Wenn die GUI eine Funktion hinterlegt hat, diese jetzt ausfuehren (z.B. Label updaten)
            if self.connected_callback:
                self.connected_callback()
            # 10. Hintergrund-Thread starten, der permanent auf eintreffende Daten lauscht (verhindert GUI-Einfrieren)
            threading.Thread(target=self._recv_loop, daemon=True).start()
        except Exception as e:
            print(f"[Server] Error accepting connection: {e}")

    def connect_to_server(self, ip, port=65432):
        # 1. Rolle als Client speichern
        self.role = 'client'
        self.ip = ip
        self.port = port
        
        try:
            # 2. TCP-Socket erstellen (IPv4, TCP-Strom)
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"[Client] Connecting to {ip}:{port}...")
            # 3. Verbindung zum Server mit dessen IP-Adresse und Port aufbauen
            self.conn.connect((ip, port))
            # 4. Status auf Verbunden setzen
            self.connected = True
            print(f"[Client] Connected to {ip}")
            # 5. GUI benachrichtigen, dass die Verbindung steht
            if self.connected_callback:
                self.connected_callback()
            # 6. Hintergrund-Thread starten, um Zuege des Servers ohne GUI-Blockieren zu empfangen
            threading.Thread(target=self._recv_loop, daemon=True).start()
        except Exception as e:
            print(f"[Client] Connection failed: {e}")
            raise

    def send_board_state(self, board_matrix):
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
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        msg = json.loads(line)
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
        if not self.connected and not self.reconnecting:
            self.reconnecting = True
            
            if self.conn:
                try:
                    self.conn.close()
                except Exception:
                    pass
                self.conn = None
            
            print("[Network] Verbindung verloren! Versuche Wiederverbindung...")
            
            if self.disconnected_callback:
                self.disconnected_callback()
                
            threading.Thread(target=self._reconnect_loop, daemon=True).start()

    def _reconnect_loop(self):
        import time
        while not self.connected:
            time.sleep(2)
            print(f"[Network] Wiederverbindungsversuch als {self.role}...")
            
            if self.role == 'server':
                try:
                    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    srv.bind(('0.0.0.0', self.port))
                    srv.listen(1)
                    
                    self.conn, addr = srv.accept()
                    srv.close()
                    
                    self.connected = True
                    self.reconnecting = False
                    print(f"[Server] Wiederverbindung erfolgreich! Client verbunden: {addr[0]}")
                    
                    if self.connected_callback:
                        self.connected_callback()
                        
                    threading.Thread(target=self._recv_loop, daemon=True).start()
                    break
                except Exception as e:
                    print(f"[Server] Wiederverbindung fehlgeschlagen: {e}")
                    
            elif self.role == 'client':
                try:
                    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.conn.connect((self.ip, self.port))
                    
                    self.connected = True
                    self.reconnecting = False
                    print(f"[Client] Wiederverbindung erfolgreich! Verbunden mit {self.ip}")
                    
                    if self.connected_callback:
                        self.connected_callback()
                        
                    threading.Thread(target=self._recv_loop, daemon=True).start()
                    break
                except Exception as e:
                    print(f"[Client] Wiederverbindung fehlgeschlagen: {e}")
                    if self.conn:
                        try:
                            self.conn.close()
                        except Exception:
                            pass
                        self.conn = None