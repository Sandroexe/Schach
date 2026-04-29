# schach.py

from connection.server import start_server
from connection.client import connect_to_server


def waehle_modus():
    """Zeigt ein einfaches Menü zur Auswahl zwischen Server und Client."""
    print("\n" + "="*40)
    print("SCHACH - Modus Auswahl")
    print("="*40)
    print("1 = Server starten")
    print("2 = Mit Server verbinden (Client)")
    print("3 = Beenden")
    print("="*40)
    
    wahl = input("Wähle eine Option (1/2/3): ").strip()
    return wahl


def starte_modus(wahl):
    """Startet den ausgewählten Modus."""
    if wahl == "1":
        print("\n→ Starte SERVER...")
        start_server()
    elif wahl == "2":
        print("\n→ Starte CLIENT...")
        connect_to_server()
    elif wahl == "3":
        print("Auf Wiedersehen!")
        return False
    else:
        print("⚠ Ungültige Eingabe! Bitte 1, 2 oder 3 eingeben.")
        return None
    return True


if __name__ == "__main__":
    print("starting Schach...")
    
    while True:
        wahl = waehle_modus()
        ergebnis = starte_modus(wahl)
        
        if ergebnis is False:
            break
        elif ergebnis is None:
            continue

