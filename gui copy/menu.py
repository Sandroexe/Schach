import tkinter as tk


def show_menu():
    """Display selection GUI and return 'server' or 'client'."""
    selection = None
    
    def choose_server():
        nonlocal selection
        selection = "server"
        window.destroy()
    
    def choose_client():
        nonlocal selection
        selection = "client"
        window.destroy()
    
    # Create window
    window = tk.Tk()
    window.title("CHESS")
    window.geometry("400x300")
    window.resizable(False, False)
    window.configure(bg="#f0f0f0")
    
    # Title
    title = tk.Label(
        window,
        text="CHESS",
        font=("Arial", 32, "bold"),
        bg="#f0f0f0",
        fg="#333333"
    )
    title.pack(pady=20)
    
    # Subtitle/Label
    subtitle = tk.Label(
        window,
        text="Select Game Mode",
        font=("Arial", 14),
        bg="#f0f0f0",
        fg="#666666"
    )
    subtitle.pack(pady=10)
    
    # Button container
    button_frame = tk.Frame(window, bg="#f0f0f0")
    button_frame.pack(pady=30, padx=20, fill=tk.BOTH, expand=True)
    
    # Host button (Server)
    button_host = tk.Button(
        button_frame,
        text="Host Game\n(Server)",
        command=choose_server,
        font=("Arial", 14, "bold"),
        bg="#4CAF50",
        fg="white",
        height=4,
        border=0,
        cursor="hand2",
        activebackground="#45a049"
    )
    button_host.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
    
    # Join button (Client)
    button_join = tk.Button(
        button_frame,
        text="Join Game\n(Client)",
        command=choose_client,
        font=("Arial", 14, "bold"),
        bg="#2196F3",
        fg="white",
        height=4,
        border=0,
        cursor="hand2",
        activebackground="#0b7dda"
    )
    button_join.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
    
    # Display window
    window.mainloop()
    
    return selection


if __name__ == "__main__":
    # Test the menu window directly
    result = show_menu()
    print(f"Selected mode: {result}")

