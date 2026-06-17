# Alle Einstellungen importieren
from gui.config import *

# Klasse fuer das Schachbrett
class Board:

    # Startwerte fuer das Brett festlegen
    def __init__(self, canvas):
        # Das Zeichenfeld merken
        self.canvas = canvas
        # Eine leere Liste fuer die Zugpunkte erstellen
        self.marker = []

    # Das Schachbrett mit seinen Quadraten zeichnen
    def draw_board(self):

        # Alle Reihen durchgehen
        for r in range(BOARD_SIZE):
            # Alle Spalten durchgehen
            for c in range(BOARD_SIZE):

                # Farbe abwechseln je nachdem ob die Summe gerade oder ungerade ist
                color = COLOR1 if (r + c) % 2 == 0 else COLOR2

                # Ein Viereck fuer das Feld auf die Grafik zeichnen
                self.canvas.create_rectangle(
                    c * FELD,
                    r * FELD,
                    (c + 1) * FELD,
                    (r + 1) * FELD,
                    fill=color
                )

    # Alle bunten Punkte vom Brett wieder loeschen
    def clear_marker(self):

        # Jeden gemerkten Punkt einzeln aus der Grafik entfernen
        for m in self.marker:
            self.canvas.delete(m)

        # Die Liste der Punkte wieder komplett leeren
        self.marker.clear()

    # Einen bunten Kreismarker fuer einen erlaubten Zug zeichnen
    def draw_marker(self, col, row, color):

        # Einen kleinen Kreis genau in die Mitte des Feldes zeichnen
        m = self.canvas.create_oval(
            col * FELD + FELD//2 - 5,
            row * FELD + FELD//2 - 5,
            col * FELD + FELD//2 + 5,
            row * FELD + FELD//2 + 5,
            fill=color
        )

        # Den neuen Kreis in der Liste merken damit man ihn spaeter loeschen kann
        self.marker.append(m)