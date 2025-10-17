import os
import time
import threading
import ctypes
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from win10toast import ToastNotifier

# Initialize toast notifier
toaster = ToastNotifier()

def show_warning():
    """نمایش نوتیفیکیشن ویندوز"""
    toaster.show_toast(
        "⚠️ Shutdown Warning",
        "Your system will automatically shut down in 45 seconds!",
        duration=10,
        threaded=True
    )

def shutdown_system():
    """خاموش کردن سیستم"""
    os.system("shutdown /s /t 0")

def force_foreground_window(hwnd):
    """فورس کردن پنجره برای اومدن روی همه‌چیز (حتی fullscreen)"""
    user32 = ctypes.windll.user32
    SW_SHOW = 5
    HWND_TOPMOST = -1
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_SHOWWINDOW = 0x0040

    # نمایش و topmost کردن
    user32.ShowWindow(hwnd, SW_SHOW)
    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)

    # تلاش برای فوکوس
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    user32.FlashWindow(hwnd, True)

def update_timer(label, root):
    """به‌روزرسانی تایمر تا نیمه‌شب"""
    warning_shown = False

    while True:
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        remaining = next_midnight - now
        total_seconds = int(remaining.total_seconds())

        if total_seconds <= 45 and not warning_shown:
            hwnd = root.winfo_id()
            force_foreground_window(hwnd)

            label.config(
                text="⚠️ 45 seconds remaining!\nSystem will shut down soon!",
                foreground="red",
                font=("Kalameh Black", 18)
            )

            show_warning()
            warning_shown = True

            # منتظر ماندن برای اتمام ۴۵ ثانیه و سپس خاموش شدن
            time.sleep(45)
            shutdown_system()
            break

        # محاسبه زمان باقی‌مانده
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        label.config(text=f"Remaining\n   {hours:02d}:{minutes:02d}:{seconds:02d}")
        time.sleep(1)

def start_gui():
    """شروع رابط کاربری گرافیکی"""
    root = tk.Tk()
    root.title("00:00:00")
    root.geometry("260x130")
    root.resizable(False, False)
    root.configure(bg="#1e1e1e")

    style = ttk.Style()
    style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Kalameh Black", 20))

    label = ttk.Label(root, text="Calculating time until midnight...", anchor="center")
    label.pack(expand=True)

    # اجرای تایمر در ترد جداگانه
    thread = threading.Thread(target=update_timer, args=(label, root), daemon=True)
    thread.start()

    root.mainloop()

if __name__ == "__main__":
    start_gui()
