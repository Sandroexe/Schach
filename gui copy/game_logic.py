from gui.config import WHITE, BLACK

class Game:

    def __init__(self):
        self.pieces = {}  # Key: (col, row), Value: {"type": "pawn", "color": WHITE}
        self.current_turn = WHITE # Weiß beginnt immer
        self.reset_board()

    def reset_board(self):
        self.pieces.clear()
        self.current_turn = WHITE

        # Figuren-Reihenfolge für die Grundlinie
        back_row = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

        # Schwarz aufstellen (Reihe 0 und 1)
        for col, p_type in enumerate(back_row):
            self.pieces[(col, 0)] = {"type": p_type, "color": BLACK}
        for col in range(8):
            self.pieces[(col, 1)] = {"type": "pawn", "color": BLACK}

        # Weiß aufstellen (Reihe 6 und 7)
        for col in range(8):
            self.pieces[(col, 6)] = {"type": "pawn", "color": WHITE}
        for col, p_type in enumerate(back_row):
            self.pieces[(col, 7)] = {"type": p_type, "color": WHITE}

    def get_piece_at(self, col, row):
        return self.pieces.get((col, row))

    def move_piece(self, from_col, from_row, to_col, to_row):
        # Holt die Figur vom Startfeld weg
        piece = self.pieces.pop((from_col, from_row), None)
        game_over_winner = None

        if piece:
            # Prüfen, ob auf dem Zielfeld ein König steht
            target = self.pieces.get((to_col, to_row))
            if target and target["type"] == "king":
                # Der aktuelle Spieler gewinnt, weil er den gegnerischen König schlägt
                game_over_winner = self.current_turn

            # Setzt die Figur auf das neue Feld
            self.pieces[(to_col, to_row)] = piece

            # ==========================================================
            # BAUERNTRANSFORMATION (PROMOTION)
            # ==========================================================
            if piece["type"] == "pawn":
                # Weiß (Christoph) erreicht die oberste Reihe (0)
                if piece["color"] == WHITE and to_row == 0:
                    piece["type"] = "queen"
                # Schwarz (Sandro) erreicht die unterste Reihe (7)
                elif piece["color"] == BLACK and to_row == 7:
                    piece["type"] = "queen"
            # ==========================================================
            
            # Wechselt den Spieler
            self.current_turn = BLACK if self.current_turn == WHITE else WHITE

        # Gibt zurück, ob jemand gewonnen hat (None, WHITE oder BLACK)
        return game_over_winner


#================ CONTROLLER =================#

class Controller:

    def __init__(self, game, board, pieces):
        self.game = game
        self.board = board
        self.pieces = pieces

    def get_valid_moves(self, col, row):
        """Berechnet alle erlaubten Felder für eine Figur auf (col, row)"""
        piece = self.game.get_piece_at(col, row)
        if not piece:
            return []

        p_type = piece["type"]
        color = piece["color"]
        valid_moves = []

        # Richtungen für Läufer, Turm, Dame
        directions_orthogonal = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        directions_diagonal = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        if p_type == "pawn":
            direction = -1 if color == WHITE else 1
            start_row = 6 if color == WHITE else 1

            # 1 Schritt vorwärts
            if not self.game.get_piece_at(col, row + direction):
                valid_moves.append((col, row + direction))
                # 2 Schritte vom Startfeld
                if row == start_row and not self.game.get_piece_at(col, row + 2 * direction):
                    valid_moves.append((col, row + 2 * direction))
            
            # Schlagen diagonal
            for dc in [-1, 1]:
                target = self.game.get_piece_at(col + dc, row + direction)
                if target and target["color"] != color:
                    valid_moves.append((col + dc, row + direction))

        elif p_type == "knight":
            knight_moves = [
                (col+2, row+1), (col+2, row-1), (col-2, row+1), (col-2, row-1),
                (col+1, row+2), (col+1, row-2), (col-1, row+2), (col-1, row-2)
            ]
            for c, r in knight_moves:
                if 0 <= c < 8 and 0 <= r < 8:
                    target = self.game.get_piece_at(c, r)
                    if not target or target["color"] != color:
                        valid_moves.append((c, r))

        elif p_type in ["bishop", "rook", "queen"]:
            dirs = []
            if p_type in ["bishop", "queen"]: dirs += directions_diagonal
            if p_type in ["rook", "queen"]: dirs += directions_orthogonal

            for dc, dr in dirs:
                c, r = col + dc, row + dr
                while 0 <= c < 8 and 0 <= r < 8:
                    target = self.game.get_piece_at(c, r)
                    if not target:
                        valid_moves.append((c, r))
                    else:
                        if target["color"] != color:
                            valid_moves.append((c, r))
                        break # Blockiert durch Figur
                    c += dc
                    r += dr

        elif p_type == "king":
            all_dirs = directions_orthogonal + directions_diagonal
            for dc, dr in all_dirs:
                c, r = col + dc, row + dr
                if 0 <= c < 8 and 0 <= r < 8:
                    target = self.game.get_piece_at(c, r)
                    if not target or target["color"] != color:
                        valid_moves.append((c, r))

        return valid_moves

    def show_moves(self, col, row):
        self.board.clear_marker()
        moves = self.get_valid_moves(col, row)
        
        for c, r in moves:
            target = self.game.get_piece_at(c, r)
            color = "red" if target else "blue"
            self.board.draw_marker(c, r, color)