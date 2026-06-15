from gui.config import *

class Board:

    def __init__(self, canvas):
        self.canvas = canvas
        self.marker = []

    def draw_board(self):

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):

                color = COLOR1 if (r + c) % 2 == 0 else COLOR2

                self.canvas.create_rectangle(
                    c * FELD,
                    r * FELD,
                    (c + 1) * FELD,
                    (r + 1) * FELD,
                    fill=color
                )

    def clear_marker(self):

        for m in self.marker:
            self.canvas.delete(m)

        self.marker.clear()

    def draw_marker(self, col, row, color):

        m = self.canvas.create_oval(
            col * FELD + FELD//2 - 5,
            row * FELD + FELD//2 - 5,
            col * FELD + FELD//2 + 5,
            row * FELD + FELD//2 + 5,
            fill=color
        )

        self.marker.append(m)