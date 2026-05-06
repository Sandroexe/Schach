# main.py

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
        # Menü anzeigen und Auswahl abfragen
        mode = show_menu()

        if mode == "server":
            print("→ Opening Server window...")
            show_server_window()
        elif mode == "client":
            print("→ Opening Client window...")
            show_client_window()
        elif mode is None:
            print("No selection made!")
        else:
            print(f"Unknown mode selected: {mode}")

    except Exception as e:
        # Fängt unerwartete Fehler während der Laufzeit ab
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    start_app()