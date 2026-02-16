import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.title("Admin Section")
root.geometry("400x450")
root.config(bg="white")

# ===== TITLE =====
title = tk.Label(root, text="Admin Section",
                 font=("Arial", 20, "bold"),
                 bg="white")
title.pack(pady=30)

# ================= FUNCTIONS =================

def take_attendance():
    subprocess.Popen([sys.executable,
                      os.path.join(BASE_DIR, "face_recognition.py")])

def open_attendance_photos():
    folder_path = os.path.join(BASE_DIR, "screenshots")
    os.makedirs(folder_path, exist_ok=True)

    if sys.platform == "darwin":
        subprocess.Popen(["open", folder_path])
    elif sys.platform == "win32":
        os.startfile(folder_path)
    else:
        subprocess.Popen(["xdg-open", folder_path])

# 🔥 POPUP FOR NAME ENTRY
def open_database_popup():
    popup = tk.Toplevel(root)
    popup.title("Create Student Profile")
    popup.geometry("300x200")
    popup.config(bg="white")

    label = tk.Label(popup, text="Enter Student Name:",
                     font=("Arial", 12),
                     bg="white")
    label.pack(pady=15)

    name_entry = tk.Entry(popup, font=("Arial", 12), width=25)
    name_entry.pack(pady=10)

    def submit_name():
        student_name = name_entry.get().strip()

        if student_name == "":
            messagebox.showerror("Error", "Name cannot be empty!")
            return

        subprocess.Popen([sys.executable,
                          os.path.join(BASE_DIR, "face_data.py"),
                          student_name])

        popup.destroy()

    submit_btn = tk.Button(popup,
                           text="Start Capture",
                           bg="#f5c6f7",
                           command=submit_name)
    submit_btn.pack(pady=15)

# ================= BUTTONS =================

btn1 = tk.Button(root,
                 text="Take Attendance",
                 width=25,
                 height=2,
                 bg="#b2f0e6",
                 command=take_attendance)
btn1.pack(pady=15)

btn2 = tk.Button(root,
                 text="Create New Student Profile",
                 width=25,
                 height=2,
                 bg="#f5c6f7",
                 command=open_database_popup)
btn2.pack(pady=15)

btn3 = tk.Button(root,
                 text="Attendance Photos",
                 width=25,
                 height=2,
                 bg="#d0c6f7",
                 command=open_attendance_photos)
btn3.pack(pady=15)

root.mainloop()
