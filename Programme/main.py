import tkinter as tk
from tkinter import messagebox # 👈 Neu für das Pop-up-Fenster
from config import *
from board import Board
from game import Game, Controller
from pieces import Pieces

selected_pos = None

root = tk.Tk()
root.title(WINDOW_TITLE)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Linke Seite: Das Spielfeld
canvas = tk.Canvas(frame, width=400, height=400)
canvas.grid(row=0, column=0)

# Rechte Seite: Die Info-Anzeige
right_frame = tk.Frame(frame, padx=20)
right_frame.grid(row=0, column=1, sticky="n")

title_label = tk.Label(right_frame, text="STATUS", font=("Helvetica", 14, "bold"))
title_label.pack(pady=(0, 10))

turn_label = tk.Label(
    right_frame, 
    text="Christoph ist dran", 
    font=("Helvetica", 12), 
    bg="white", 
    fg="black", 
    width=14, 
    height=2,
    relief="groove"
)
turn_label.pack()

# Initialisierung
board = Board(canvas)
game = Game()
pieces = Pieces(canvas)
controller = Controller(game, board, pieces)

board.draw_board()
pieces.draw_all_pieces(game.pieces, FELD)

def update_turn_label():
    if game.current_turn == WHITE:
        turn_label.config(text="Christoph ist dran", bg="white", fg="black")
    else:
        turn_label.config(text="Sandro ist dran", bg="black", fg="white")

def click(event):
    global selected_pos

    col = event.x // FELD
    row = event.y // FELD

    # 1. ZUG-LOGIK
    if selected_pos:
        valid_moves = controller.get_valid_moves(selected_pos[0], selected_pos[1])
        
        if (col, row) in valid_moves:
            # Zug ausführen und prüfen, ob ein König geschlagen wurde
            winner = game.move_piece(selected_pos[0], selected_pos[1], col, row)
            
            board.clear_marker()
            pieces.draw_all_pieces(game.pieces, FELD)
            selected_pos = None
            update_turn_label()

            # Wenn ein König geschlagen wurde -> Game Over Pop-up!
            if winner:
                winner_name = "Christoph" if winner == WHITE else "Sandro"
                messagebox.showinfo("Schachmatt!", f"König is down {winner_name} hat gwonnen")
                
                # Spiel zurücksetzen
                game.reset_board()
                pieces.draw_all_pieces(game.pieces, FELD)
                update_turn_label()
            return
        
    # 2. AUSWAHL-LOGIK
    piece = game.get_piece_at(col, row)
    if piece and piece["color"] == game.current_turn:
        selected_pos = (col, row)
        controller.show_moves(col, row)
    else:
        board.clear_marker()
        selected_pos = None

canvas.bind("<Button-1>", click)
root.mainloop()