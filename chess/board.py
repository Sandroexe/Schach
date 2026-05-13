"""Chess board state management.

Pieces are stored as single characters:
  Uppercase = White:  P R N B Q K
  Lowercase = Black:  p r n b q k
"""

SYMBOLS = {
    "P": "♙", "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔",
    "p": "♟", "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚",
}

INITIAL_BOARD = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]


class ChessBoard:
    def __init__(self):
        # Deep copy so INITIAL_BOARD is never mutated.
        self.board = [row[:] for row in INITIAL_BOARD]

    def get(self, row, col):
        """Return the piece at (row, col), or None if empty."""
        return self.board[row][col]

    def move(self, from_pos, to_pos):
        """Move the piece at from_pos to to_pos. No legality check."""
        fr, fc = from_pos
        tr, tc = to_pos
        piece = self.board[fr][fc]
        self.board[tr][tc] = piece
        self.board[fr][fc] = None

    def symbol(self, piece):
        """Return the Unicode chess symbol for a piece character."""
        return SYMBOLS.get(piece, "")

    def is_white(self, piece):
        return piece is not None and piece.isupper()

    def is_black(self, piece):
        return piece is not None and piece.islower()

    def owns(self, piece, color):
        """Return True if piece belongs to the given color ('white' or 'black')."""
        if piece is None:
            return False
        if color == "white":
            return self.is_white(piece)
        return self.is_black(piece)

    def find_king(self, color):
        """Return (row, col) of the king for the given color."""
        target = "K" if color == "white" else "k"
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target:
                    return (r, c)
        return None

    def is_in_check(self, color):
        """Return True if the given color's king is currently in check."""
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        opponent = "black" if color == "white" else "white"
        # Check if any opponent piece can capture the king.
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and self.owns(piece, opponent):
                    if self._can_attack(r, c, king_pos[0], king_pos[1]):
                        return True
        return False

    def _can_attack(self, fr, fc, tr, tc):
        """Return True if the piece at (fr, fc) can attack square (tr, tc).
        
        Basic attack patterns only (no en-passant, no castling).
        """
        piece = self.board[fr][fc]
        if piece is None:
            return False
        p = piece.lower()
        dr = tr - fr
        dc = tc - fc

        if p == "p":
            direction = -1 if self.is_white(piece) else 1
            return dr == direction and abs(dc) == 1

        if p == "n":
            return (abs(dr), abs(dc)) in [(1, 2), (2, 1)]

        if p == "k":
            return abs(dr) <= 1 and abs(dc) <= 1

        if p == "r":
            if not (dr == 0 or dc == 0):
                return False
            return self._clear_path(fr, fc, tr, tc)

        if p == "b":
            if not (abs(dr) == abs(dc)):
                return False
            return self._clear_path(fr, fc, tr, tc)

        if p == "q":
            straight = dr == 0 or dc == 0
            diagonal = abs(dr) == abs(dc)
            if not (straight or diagonal):
                return False
            return self._clear_path(fr, fc, tr, tc)

        return False

    def _clear_path(self, fr, fc, tr, tc):
        """Return True if there are no pieces between (fr,fc) and (tr,tc)."""
        sr = (0 if tr == fr else (1 if tr > fr else -1))
        sc = (0 if tc == fc else (1 if tc > fc else -1))
        r, c = fr + sr, fc + sc
        while (r, c) != (tr, tc):
            if self.board[r][c] is not None:
                return False
            r += sr
            c += sc
        return True
