import tkinter as tk
from tkinter import messagebox
from gui.config import *
from gui.board import Board
from gui.game_logic import Game, Controller
from gui.pieces import Pieces

selected_pos = None

def show_game_window(mode, network, my_color):
    global selected_pos
    selected_pos = None

    root = tk.Tk()
    root.title(f"{WINDOW_TITLE} - {mode.upper()}")
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    canvas = tk.Canvas(frame, width=400, height=400)
    canvas.grid(row=0, column=0)

    right_frame = tk.Frame(frame, padx=20)
    right_frame.grid(row=0, column=1, sticky="n")

    title_label = tk.Label(right_frame, text="STATUS", font=("Helvetica", 14, "bold"))
    title_label.pack(pady=(0, 10))

    turn_label = tk.Label(
        right_frame, 
        text="Server ist dran", 
        font=("Helvetica", 12), 
        bg="white", 
        fg="black", 
        width=16, 
        height=2,
        relief="groove"
    )
    turn_label.pack(pady=(0, 10))

    role_text = "Du spielst als: " + ("Server (Weiß)" if my_color == WHITE else "Client (Schwarz)")
    role_label = tk.Label(right_frame, text=role_text, font=("Helvetica", 10, "italic"))
    role_label.pack(pady=(0, 10))

    connection_label = tk.Label(
        right_frame,
        text="Verbunden" if network.connected else "Warten auf Verbindung...",
        font=("Helvetica", 10, "bold"),
        fg="green" if network.connected else "orange"
    )
    connection_label.pack(pady=(0, 10))

    board = Board(canvas)
    game = Game()
    pieces = Pieces(canvas)
    controller = Controller(game, board, pieces)

    board.draw_board()
    pieces.draw_all_pieces(game.pieces, FELD)

    def update_turn_label():
        if game.current_turn == WHITE:
            turn_label.config(text="Server ist dran", bg="white", fg="black")
        else:
            turn_label.config(text="Client ist dran", bg="black", fg="white")

    def serialize_board_state(winner=None):
        serializable_pieces = {f"{c},{r}": p for (c, r), p in game.pieces.items()}
        return {
            "pieces": serializable_pieces,
            "current_turn": game.current_turn,
            "winner": winner
        }

    def send_game_state(winner=None):
        state = serialize_board_state(winner)
        network.send_board_state(state)

    def show_winner_popup(winner):
        winner_name = "Server" if winner == WHITE else "Client"
        messagebox.showinfo("Schachmatt!", f"König is down. {winner_name} hat gewonnen")
        game.reset_board()
        pieces.draw_all_pieces(game.pieces, FELD)
        update_turn_label()

    def click(event):
        global selected_pos

        if not network.connected:
            return

        if game.current_turn != my_color:
            return

        col = event.x // FELD
        row = event.y // FELD

        if selected_pos:
            valid_moves = controller.get_valid_moves(selected_pos[0], selected_pos[1])
            
            if (col, row) in valid_moves:
                winner = game.move_piece(selected_pos[0], selected_pos[1], col, row)
                
                board.clear_marker()
                pieces.draw_all_pieces(game.pieces, FELD)
                selected_pos = None
                update_turn_label()

                send_game_state(winner)

                if winner:
                    show_winner_popup(winner)
                    send_game_state(None)
                return
            
        piece = game.get_piece_at(col, row)
        if piece and piece["color"] == game.current_turn:
            selected_pos = (col, row)
            controller.show_moves(col, row)
        else:
            board.clear_marker()
            selected_pos = None

    def handle_received_state(state):
        new_pieces = {}
        for k, p in state.get("pieces", {}).items():
            col_str, row_str = k.split(",")
            new_pieces[(int(col_str), int(row_str))] = p
        
        game.pieces = new_pieces
        game.current_turn = state.get("current_turn", WHITE)
        winner = state.get("winner")

        board.clear_marker()
        pieces.draw_all_pieces(game.pieces, FELD)
        update_turn_label()

        if winner:
            show_winner_popup(winner)

    def on_board_received(state):
        root.after(0, lambda: handle_received_state(state))

    def on_connected():
        root.after(0, lambda: connection_label.config(text="Verbunden", fg="green"))
        if game.current_turn == my_color:
            root.after(0, send_game_state)

    def on_disconnected():
        root.after(0, lambda: connection_label.config(text="Verbindung verloren...", fg="red"))

    network.set_board_callback(on_board_received)
    network.set_connected_callback(on_connected)
    network.set_disconnected_callback(on_disconnected)

    canvas.bind("<Button-1>", click)
    update_turn_label()
    
    root.mainloop()
