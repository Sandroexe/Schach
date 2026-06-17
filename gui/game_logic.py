# Farben weiss und schwarz importieren
from gui.config import WHITE, BLACK

# Klasse fuer das Spiel
class Game:

    # Startwerte festlegen
    def __init__(self):
        # Speicher fuer alle Figuren auf dem Brett
        self.pieces = {}  
        # Weiss faengt immer an
        self.current_turn = WHITE 
        # Figuren aufstellen
        self.reset_board()

    # Brett leeren und neu aufbauen
    def reset_board(self):
        # Alle alten Figuren loeschen
        self.pieces.clear()
        # Startspieler ist wieder Weiss
        self.current_turn = WHITE

        # Reihenfolge der grossen Figuren von links nach rechts
        back_row = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

        # Schwarze Hauptfiguren in Reihe 0 setzen
        for col, p_type in enumerate(back_row):
            self.pieces[(col, 0)] = {"type": p_type, "color": BLACK}
        # Schwarze Bauern in Reihe 1 setzen
        for col in range(8):
            self.pieces[(col, 1)] = {"type": "pawn", "color": BLACK}

        # Weisse Bauern in Reihe 6 setzen
        for col in range(8):
            self.pieces[(col, 6)] = {"type": "pawn", "color": WHITE}
        # Weisse Hauptfiguren in Reihe 7 setzen
        for col, p_type in enumerate(back_row):
            self.pieces[(col, 7)] = {"type": p_type, "color": WHITE}

    # Figur an einer bestimmten Position suchen
    def get_piece_at(self, col, row):
        return self.pieces.get((col, row))

    # Eine Figur bewegen und Regeln pruefen
    def move_piece(self, from_col, from_row, to_col, to_row):
        # Figur vom alten Feld herunternehmen
        piece = self.pieces.pop((from_col, from_row), None)
        # Am Anfang gibt es noch keinen Gewinner
        game_over_winner = None

        # Wenn eine Figur gefunden wurde
        if piece:
            # Schauen was auf dem Zielfeld steht
            target = self.pieces.get((to_col, to_row))
            # Wenn dort ein Koenig steht ist das Spiel vorbei
            if target and target["type"] == "king":
                # Der aktuelle Spieler hat gewonnen
                game_over_winner = self.current_turn

            # Figur auf das neue Feld stellen
            self.pieces[(to_col, to_row)] = piece

            # Sonderregel fuer Bauern am Ende des Bretts
            if piece["type"] == "pawn":
                # Weisser Bauer erreicht Reihe 0 und wird zur Dame
                if piece["color"] == WHITE and to_row == 0:
                    piece["type"] = "queen"
                # Schwarzer Bauer erreicht Reihe 7 und wird zur Dame
                elif piece["color"] == BLACK and to_row == 7:
                    piece["type"] = "queen"
            
            # Der andere Spieler ist jetzt dran
            self.current_turn = BLACK if self.current_turn == WHITE else WHITE

        # Gewinner zurueckgeben oder None wenn das Spiel weitergeht
        return game_over_winner


#================ CONTROLLER =================#

# Klasse fuer die Steuerung und die Zuege
class Controller:

    # Verbindung zu Spiel und Brett herstellen
    def __init__(self, game, board, pieces):
        self.game = game
        self.board = board
        self.pieces = pieces

    # Alle erlaubten Felder fuer eine Figur berechnen
    def get_valid_moves(self, col, row):
        # Figur auf dem Feld holen
        piece = self.game.get_piece_at(col, row)
        # Wenn das Feld leer ist gibt es keine Zuege
        if not piece:
            return []

        # Typ und Farbe der Figur merken
        p_type = piece["type"]
        color = piece["color"]
        # Liste fuer die gueltigen Zuege erstellen
        valid_moves = []

        # Richtungen fuer gerade Schritte oben unten rechts links
        directions_orthogonal = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
        # Richtungen fuer schraege Schritte in alle vier Ecken
        directions_diagonal = [(1, 1), (1, -1), (-1, 1), (-1, -1)] 

        # Regeln fuer den Bauern
        if p_type == "pawn":
            # Weisse Bauern laufen hoch schwarze Bauern laufen runter
            direction = -1 if color == WHITE else 1
            start_row = 6 if color == WHITE else 1

            # 1 Schritt vorwaerts wenn das Feld frei ist
            if not self.game.get_piece_at(col, row + direction):
                valid_moves.append((col, row + direction))
                # 2 Schritte vom Startfeld wenn der Weg frei ist
                if row == start_row and not self.game.get_piece_at(col, row + 2 * direction):
                    valid_moves.append((col, row + 2 * direction))
            
            # Schraeg schlagen nach links und rechts pruefen
            for dc in [-1, 1]:
                target = self.game.get_piece_at(col + dc, row + direction)
                # Nur erlaubt wenn dort eine gegnerische Figur steht
                if target and target["color"] != color:
                    valid_moves.append((col + dc, row + direction))

        # Regeln fuer den Springer oder das Pferd
        elif p_type == "knight":
            # Alle acht moeglichen Sprünge in L Form aufschreiben
            knight_moves = [
                (col+2, row+1), (col+2, row-1), (col-2, row+1), (col-2, row-1),
                (col+1, row+2), (col+1, row-2), (col-1, row+2), (col-1, row-2)
            ]
            # Jeden Sprung einzeln pruefen
            for c, r in knight_moves:
                # Das Feld muss auf dem Brett liegen
                if 0 <= c < 8 and 0 <= r < 8:
                    target = self.game.get_piece_at(c, r)
                    # Erlaubt wenn das Feld leer ist oder ein Gegner dort steht
                    if not target or target["color"] != color:
                        valid_moves.append((c, r))

        # Regeln fuer Laeufer Turm und Dame
        elif p_type in ["bishop", "rook", "queen"]:
            dirs = []
            # Laeufer und Dame bewegen sich schraeg
            if p_type in ["bishop", "queen"]: dirs += directions_diagonal
            # Turm und Dame bewegen sich gerade
            if p_type in ["rook", "queen"]: dirs += directions_orthogonal

            # Jede Richtung einzeln ablaufen
            for dc, dr in dirs:
                c, r = col + dc, row + dr
                # Solange man nicht vom Brett kaeuft
                while 0 <= c < 8 and 0 <= r < 8:
                    target = self.game.get_piece_at(c, r)
                    # Wenn das Feld leer ist darf man dorthin ziehen
                    if not target:
                        valid_moves.append((c, r))
                    # Wenn eine Figur im Weg steht
                    else:
                        # Wenn es ein Gegner ist darf man ihn schlagen
                        if target["color"] != color:
                            valid_moves.append((c, r)) 
                        # Der Weg ist danach auf jeden Fall blockiert
                        break 
                    # Einen Schritt weiter in die Richtung gehen
                    c += dc
                    r += dr

        # Regeln fuer den Koenig
        elif p_type == "king":
            # Alle acht Richtungen kombinieren
            all_dirs = directions_orthogonal + directions_diagonal
            # Jedes Nachbarfeld pruefen
            for dc, dr in all_dirs:
                c, r = col + dc, row + dr
                # Feld muss auf dem Brett sein
                if 0 <= c < 8 and 0 <= r < 8:
                    target = self.game.get_piece_at(c, r)
                    # Erlaubt wenn frei oder ein Gegner dort steht
                    if not target or target["color"] != color:
                        valid_moves.append((c, r))

        # Liste mit allen erlaubten Feldern zurueckgeben
        return valid_moves

    # Erlaubte Zuege auf dem Bildschirm anzeigen
    def show_moves(self, col, row):
        # Alle alten Punkte loeschen
        self.board.clear_marker()
        # Erlaubte Felder berechnen
        moves = self.get_valid_moves(col, row)
        
        # Jedes erlaubte Zielfeld markieren
        for c, r in moves:
            target = self.game.get_piece_at(c, r)
            # Roter Punkt bei einem Gegner und blauer Punkt bei einem leeren Feld
            color = "red" if target else "blue"
            # Punkt auf das Brett zeichnen
            self.board.draw_marker(c, r, color)