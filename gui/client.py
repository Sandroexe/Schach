import tkinter as tk
import threading
from connection.network import NetworkManager
from gui.game import show_game_window


def show_client_window():
    """Display the client connection window."""
    window = tk.Tk()
    window.title("CHESS - Join Game")
    window.geometry("400x300")
    window.resizable(False, False)
    window.configure(bg="#f0f0f0")

    tk.Label(
        window, text="Join Game",
        font=("Arial", 28, "bold"), bg="#f0f0f0", fg="#333333"
    ).pack(pady=20)

    tk.Label(
        window, text="Enter Server IP Address:",
        font=("Arial", 12), bg="#f0f0f0", fg="#666666"
    ).pack(pady=5)

    ip_input = tk.Entry(window, font=("Arial", 14), width=20, border=2)
    ip_input.pack(pady=10)
    ip_input.focus()

    error_label = tk.Label(
        window, text="",
        font=("Arial", 10), bg="#f0f0f0", fg="#d32f2f"
    )
    error_label.pack(pady=3)

    button_connect = tk.Button(
        window,
        text="Connect",
        font=("Arial", 14, "bold"),
        bg="#2196F3", fg="white",
        height=2, border=0, cursor="hand2",
        activebackground="#0b7dda"
    )
    button_connect.pack(fill=tk.X, padx=20, pady=15)

    def connect():
        ip = ip_input.get().strip()
        if not ip:
            error_label.config(text="Please enter an IP address!")
            return

        button_connect.config(state=tk.DISABLED, text="Connecting…")
        error_label.config(text="")

        net = NetworkManager()

        def run_connect():
            try:
                net.connect_to_server(ip)
                window.after(0, lambda: launch_game(net))
            except Exception as e:
                window.after(0, lambda: show_error(str(e)))

        threading.Thread(target=run_connect, daemon=True).start()

    def launch_game(net):
        window.destroy()
        show_game_window("client", net, "black")

    def show_error(msg):
        button_connect.config(state=tk.NORMAL, text="Connect")
        error_label.config(text=f"Connection failed: {msg}")

    button_connect.config(command=connect)
    ip_input.bind("<Return>", lambda _: connect())

    window.mainloop()


if __name__ == "__main__":
    show_client_window()
