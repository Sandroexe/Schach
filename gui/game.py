import tkinter as tk
from chess.board import ChessBoard


SQ = 60  # Square size in pixels


def show_game_window(mode, network, my_color):
    """Display the interactive chess game window.

    Args:
        mode:     'server' or 'client' (used for display only).
        network:  NetworkManager instance (already started).
        my_color: 'white' or 'black' — which side this player controls.
    """
    chess_board = ChessBoard()
    selected = [None]       # [row, col] of currently selected piece, or [None]
    my_turn = [my_color == "white"]   # White always moves first

    # ------------------------------------------------------------------ Window
    window = tk.Tk()
    window.title("CHESS - Game")
    window.geometry("900x700")
    window.resizable(False, False)
    window.configure(bg="#2c2c2c")

    # ------------------------------------------------------------------ Top bar
    status_frame = tk.Frame(window, bg="#1a1a1a", height=50)
    status_frame.pack(fill=tk.X)

    mode_label = tk.Label(
        status_frame,
        text=f"Mode: {mode.upper()}  |  Playing as: {my_color.capitalize()}",
        font=("Arial", 12, "bold"),
        bg="#1a1a1a",
        fg="#4CAF50" if mode == "server" else "#2196F3"
    )
    mode_label.pack(side=tk.LEFT, padx=15, pady=10)

    connection_label = tk.Label(
        status_frame,
        text="● Waiting for opponent...",
        font=("Arial", 11, "bold"),
        bg="#1a1a1a",
        fg="#FFC107"
    )
    connection_label.pack(side=tk.RIGHT, padx=15, pady=10)

    # ------------------------------------------------------------------ Content
    content_frame = tk.Frame(window, bg="#2c2c2c")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ---- Left: Board
    board_outer = tk.Frame(content_frame, bg="#2c2c2c")
    board_outer.pack(side=tk.LEFT, padx=10)

    board_title = tk.Label(
        board_outer, text="Chess Board",
        font=("Arial", 14, "bold"), bg="#2c2c2c", fg="white"
    )
    board_title.pack(pady=10)

    canvas = tk.Canvas(
        board_outer,
        width=8 * SQ, height=8 * SQ,
        bg="#333333",
        highlightthickness=2,
        highlightbackground="#555555"
    )
    canvas.pack()

    # ---- Right: Info panel
    info_frame = tk.Frame(content_frame, bg="#1a1a1a", width=350)
    info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

    # Turn / status text
    status_title = tk.Label(
        info_frame, text="Game Status",
        font=("Arial", 12, "bold"), bg="#1a1a1a", fg="white"
    )
    status_title.pack(pady=(20, 5))

    turn_label = tk.Label(
        info_frame,
        text="Waiting for connection...",
        font=("Arial", 11),
        bg="#1a1a1a",
        fg="#FFC107",
        wraplength=300,
        justify=tk.LEFT
    )
    turn_label.pack(padx=10, pady=5)

    check_label = tk.Label(
        info_frame,
        text="",
        font=("Arial", 12, "bold"),
        bg="#1a1a1a",
        fg="#f44336"
    )
    check_label.pack(padx=10, pady=2)

    # Player labels
    tk.Label(info_frame, text="Players", font=("Arial", 12, "bold"),
             bg="#1a1a1a", fg="white").pack(pady=(20, 5))

    player_frame = tk.Frame(info_frame, bg="#2c2c2c")
    player_frame.pack(fill=tk.X, padx=10, pady=5)

    white_frame = tk.Frame(player_frame, bg="#f0d9b5", height=40)
    white_frame.pack(fill=tk.X, pady=3)
    tk.Label(
        white_frame,
        text="♙ White" + (" (You)" if my_color == "white" else ""),
        font=("Arial", 11, "bold"), bg="#f0d9b5", fg="#333"
    ).pack(pady=6)

    black_frame = tk.Frame(player_frame, bg="#333333", height=40)
    black_frame.pack(fill=tk.X, pady=3)
    tk.Label(
        black_frame,
        text="♟ Black" + (" (You)" if my_color == "black" else ""),
        font=("Arial", 11, "bold"), bg="#333333", fg="#f0d9b5"
    ).pack(pady=6)

    # Move history
    tk.Label(info_frame, text="Move History", font=("Arial", 12, "bold"),
             bg="#1a1a1a", fg="white").pack(pady=(20, 5))

    history_text = tk.Text(
        info_frame,
        font=("Courier", 9), bg="#333333", fg="#ffffff",
        height=10, width=30,
        state=tk.DISABLED, relief=tk.FLAT
    )
    history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Buttons
    btn_frame = tk.Frame(info_frame, bg="#1a1a1a")
    btn_frame.pack(fill=tk.X, padx=10, pady=10)

    def resign():
        turn_label.config(text="You resigned.", fg="#f44336")
        canvas.unbind("<Button-1>")

    tk.Button(
        btn_frame, text="Resign",
        font=("Arial", 10, "bold"), bg="#f44336", fg="white",
        cursor="hand2", command=resign
    ).pack(fill=tk.X, pady=5)

    # ------------------------------------------------------------------ Footer
    footer_frame = tk.Frame(window, bg="#1a1a1a", height=30)
    footer_frame.pack(fill=tk.X)
    tk.Label(
        footer_frame,
        text="Chess Game v1.0  |  Netzwerk-Schach — HTL Anichstraße",
        font=("Arial", 9), bg="#1a1a1a", fg="#999999"
    ).pack(pady=5)

    # ------------------------------------------------------------------ Drawing
    LIGHT = "#f0d9b5"
    DARK  = "#b58863"
    SEL   = "#aad751"   # selected square highlight
    LAST  = "#cdd96e"   # last-move highlight

    last_move = [None]  # stores (from_pos, to_pos) for highlight

    def col_letter(c): return chr(ord('a') + c)

    def draw_board():
        canvas.delete("squares")
        for r in range(8):
            for c in range(8):
                base = LIGHT if (r + c) % 2 == 0 else DARK
                # Highlight last move
                if last_move[0] and ([r, c] in last_move[0]):
                    fill = SEL
                # Highlight selected square
                elif selected[0] and [r, c] == selected[0]:
                    fill = SEL
                else:
                    fill = base
                x1, y1 = c * SQ, r * SQ
                canvas.create_rectangle(x1, y1, x1 + SQ, y1 + SQ,
                                        fill=fill, outline="", tags="squares")
                # Rank / file labels
                if c == 0:
                    canvas.create_text(x1 + 4, y1 + 4, text=str(8 - r),
                                       fill="#666", font=("Arial", 8, "bold"),
                                       anchor="nw", tags="squares")
                if r == 7:
                    canvas.create_text(x1 + SQ - 4, y1 + SQ - 4,
                                       text=col_letter(c),
                                       fill="#666", font=("Arial", 8, "bold"),
                                       anchor="se", tags="squares")

    def draw_pieces():
        canvas.delete("pieces")
        for r in range(8):
            for c in range(8):
                piece = chess_board.get(r, c)
                if piece:
                    sym  = chess_board.symbol(piece)
                    fill = "white" if chess_board.is_white(piece) else "#1a1a1a"
                    canvas.create_text(
                        c * SQ + SQ // 2, r * SQ + SQ // 2,
                        text=sym, font=("Arial", int(SQ * 0.55)),
                        fill=fill, tags="pieces"
                    )

    def redraw():
        draw_board()
        draw_pieces()

    def add_history(from_pos, to_pos, piece):
        move_str = f"{chess_board.symbol(piece)}{col_letter(from_pos[1])}{8 - from_pos[0]}" \
                   f" → {col_letter(to_pos[1])}{8 - to_pos[0]}\n"
        history_text.config(state=tk.NORMAL)
        history_text.insert(tk.END, move_str)
        history_text.see(tk.END)
        history_text.config(state=tk.DISABLED)

    def update_turn_label():
        opponent_color = "black" if my_color == "white" else "white"
        if my_turn[0]:
            turn_label.config(text="Your turn!", fg="#4CAF50")
        else:
            turn_label.config(text="Opponent's turn...", fg="#FFC107")
        # Check detection
        if chess_board.is_in_check(my_color):
            check_label.config(text="⚠ You are in check!")
        elif chess_board.is_in_check(opponent_color):
            check_label.config(text="⚠ Opponent in check!")
        else:
            check_label.config(text="")

    # ------------------------------------------------------------------ Clicks
    def on_click(event):
        if not my_turn[0]:
            return
        col = event.x // SQ
        row = event.y // SQ
        if not (0 <= row < 8 and 0 <= col < 8):
            return

        piece = chess_board.get(row, col)

        if selected[0] is None:
            # Select a piece that belongs to the player
            if chess_board.owns(piece, my_color):
                selected[0] = [row, col]
                redraw()
        else:
            from_pos = selected[0]
            to_pos   = [row, col]

            # Clicking the same square again → deselect
            if from_pos == to_pos:
                selected[0] = None
                redraw()
                return

            # Clicking another own piece → re-select
            if chess_board.owns(piece, my_color):
                selected[0] = [row, col]
                redraw()
                return

            # Execute the move
            moving_piece = chess_board.get(from_pos[0], from_pos[1])
            add_history(from_pos, to_pos, moving_piece)
            chess_board.move(from_pos, to_pos)
            network.send_move(from_pos, to_pos)
            last_move[0] = (from_pos, to_pos)
            selected[0] = None
            my_turn[0]  = False
            redraw()
            update_turn_label()

    canvas.bind("<Button-1>", on_click)

    # ------------------------------------------------------------------ Network
    def on_connected():
        """Called by NetworkManager once connection is established."""
        window.after(0, _handle_connected)

    def _handle_connected():
        connection_label.config(text="● Connected", fg="#4CAF50")
        update_turn_label()

    def on_move_received(from_pos, to_pos):
        """Called from the network recv thread — use window.after for thread safety."""
        window.after(0, lambda: _apply_received(from_pos, to_pos))

    def _apply_received(from_pos, to_pos):
        piece = chess_board.get(from_pos[0], from_pos[1])
        add_history(from_pos, to_pos, piece)
        chess_board.move(from_pos, to_pos)
        last_move[0] = (from_pos, to_pos)
        my_turn[0]   = True
        redraw()
        update_turn_label()

    network.set_move_callback(on_move_received)
    network.set_connected_callback(on_connected)

    # If already connected when window opens (client side), trigger immediately
    if network.connected:
        _handle_connected()

    # ------------------------------------------------------------------ Init
    redraw()
    turn_label.config(text="Waiting for connection...")
    window.mainloop()


if __name__ == "__main__":
    import sys
    from connection.network import NetworkManager
    # Quick local test: python -m gui.game server
    mode = sys.argv[1] if len(sys.argv) > 1 else "server"
    net  = NetworkManager()
    show_game_window(mode, net, "white")
