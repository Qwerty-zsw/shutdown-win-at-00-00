import os
import time
import threading
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from win10toast import ToastNotifier

# Initialize toast notifier
toaster = ToastNotifier()

def show_warning():
    toaster.show_toast(
        "⚠️ Shutdown Warning",
        "Your system will automatically shut down in 45 seconds!",
        duration=10,
        threaded=True
    )

def shutdown_system():
    # Normal shutdown (no force)
    os.system("shutdown /s /t 0")

def update_timer(label):
    while True:
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        remaining = next_midnight - now
        total_seconds = int(remaining.total_seconds())

        if total_seconds <= 45:
            label.config(text="⚠️ 45 seconds remaining! System will shut down soon!", foreground="red")
            show_warning()
            time.sleep(45)
            shutdown_system()
            break

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        label.config(text=f"⏳ Time left until local midnight:\n{hours:02d}:{minutes:02d}:{seconds:02d}")
        time.sleep(1)

def start_gui():
    root = tk.Tk()
    root.title("Midnight Shutdown Timer")
    root.geometry("400x200")
    root.resizable(False, False)
    root.configure(bg="#1e1e1e")

    style = ttk.Style()
    style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 14))

    label = ttk.Label(root, text="Calculating time until midnight...", anchor="center")
    label.pack(expand=True)

    # Run timer in a background thread so GUI stays responsive
    thread = threading.Thread(target=update_timer, args=(label,), daemon=True)
    thread.start()

    root.mainloop()

if __name__ == "__main__":
    start_gui()
