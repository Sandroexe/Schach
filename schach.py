# schach.py

print("Starting Chess application...")

try:
    # Versuche, die notwendigen Module zu importieren
    from gui.menu import show_menu
    from gui.server import show_server_window
    from gui.client import show_client_window
except ImportError as e:
    print(f"Fehler beim Laden der GUI-Komponenten: {e}")
    exit(1)



def start_app():
    try:
        # Menü zur mode Auswahl anzeigen bzw. starten
        mode = show_menu()

        if mode == "server":
            print("Starting Server...")
            show_server_window()

        elif mode == "client":
            print("Starting Client...")
            show_client_window()

        elif mode is None:
            print("Starting nothing.")

        else:
            print(f"Unknown mode selected: {mode}")

    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")



if __name__ == "__main__":
    start_app()