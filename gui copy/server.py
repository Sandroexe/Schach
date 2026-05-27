import tkinter as tk
import threading
from connection.server import get_ip_address
from connection.network import NetworkManager
from gui.game import show_game_window


def show_server_window():
    """Display the server setup window and launch the game once a client connects."""
    window = tk.Tk()
    window.title("CHESS - Host Game")
    window.geometry("400x280")
    window.resizable(False, False)
    window.configure(bg="#f0f0f0")

    # Title
    tk.Label(
        window, text="Host Game",
        font=("Arial", 28, "bold"), bg="#f0f0f0", fg="#333333"
    ).pack(pady=20)

    tk.Label(
        window, text="Your IP Address:",
        font=("Arial", 12), bg="#f0f0f0", fg="#666666"
    ).pack(pady=5)

    # Show local IP so the opponent knows where to connect
    ip_address = get_ip_address()
    tk.Label(
        window, text=ip_address,
        font=("Arial", 20, "bold"), bg="#e8f5e9", fg="#2e7d32", pady=10
    ).pack(fill=tk.X, padx=20, pady=10)

    status_label = tk.Label(
        window, text="",
        font=("Arial", 11), bg="#f0f0f0", fg="#FFC107"
    )
    status_label.pack(pady=5)

    def start_game():
        """Create NetworkManager, start server in background, open game window."""
        button_start.config(state=tk.DISABLED, text="Waiting for client...")
        status_label.config(text="Listening on port 65432…")

        net = NetworkManager()

        def run_server():
            net.start_server()
            # Once connected, open the game window on the main thread
            window.after(0, lambda: launch_game(net))

        threading.Thread(target=run_server, daemon=True).start()

    def launch_game(net):
        window.destroy()
        show_game_window("server", net, "white")

    button_start = tk.Button(
        window,
        text="Start Server",
        command=start_game,
        font=("Arial", 14, "bold"),
        bg="#4CAF50", fg="white",
        height=2, border=0, cursor="hand2",
        activebackground="#45a049"
    )
    button_start.pack(fill=tk.X, padx=20, pady=20)

    window.mainloop()


if __name__ == "__main__":
    show_server_window()
