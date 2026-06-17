from PIL import Image, ImageTk
import os
from gui.config import WHITE

class Pieces:

    def __init__(self, canvas):
        self.canvas = canvas
        base = os.path.dirname(os.path.abspath(__file__))
        self.images = {}
        self.canvas_ids = {} # Merkt sich die ID der Bilder auf dem Canvas

        # Alle Figurentypen definieren
        piece_types = ["pawn", "knight", "bishop", "rook", "queen", "king"]
        
        # Schleife lädt w_pawn.png, b_pawn.png, w_knight.png usw.
        for color_prefix, color_name in [("w_", WHITE), ("b_", "black")]:
            for p_type in piece_types:
                filename = f"{color_prefix}{p_type}.png"
                img_path = os.path.join(base, "images", filename)

                try:
                    img = Image.open(img_path).resize((40, 40))
                    self.images[f"{color_name}_{p_type}"] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Fehler beim Laden von {filename}: {e}. Stelle sicher, dass das Bild im 'images'-Ordner existiert!")

    def draw_all_pieces(self, game_pieces, feld):
        # Zuerst alle alten Figuren vom Canvas löschen
        for cid in self.canvas_ids.values():
            self.canvas.delete(cid)
        self.canvas_ids.clear()

        # Alle Figuren aus dem Dictionary neu aufs Board zeichnen
        for (col, row), piece in game_pieces.items():
            key = f"{piece['color']}_{piece['type']}"
            if key in self.images:
                cid = self.canvas.create_image(
                    col * feld + feld // 2,
                    row * feld + feld // 2,
                    image=self.images[key]
                )
                self.canvas_ids[(col, row)] = cid