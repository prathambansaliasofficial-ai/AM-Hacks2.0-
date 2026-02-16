import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import holidays

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "attendance.csv")


class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Section")
        self.root.geometry("950x800")
        self.root.config(bg="white")

        tk.Label(root, text="Enter Your Name",
                 font=("Arial", 14), bg="white").pack(pady=10)

        self.name_entry = tk.Entry(root, font=("Arial", 14))
        self.name_entry.pack(pady=10)

        tk.Button(root, text="View Attendance",
                  command=self.load_student_data).pack(pady=10)

        self.calendar = None
        self.chart_canvas = None
        self.percent_label = None

    # ===============================
    # LOAD DATA
    # ===============================
    def load_student_data(self):

        student_name = self.name_entry.get().strip().lower()

        if student_name == "":
            messagebox.showerror("Error", "Please enter your name")
            return

        if not os.path.exists(CSV_FILE):
            messagebox.showerror("Error", "Attendance file not found")
            return

        try:
            df = pd.read_csv(
                CSV_FILE,
                engine="python",
                on_bad_lines="skip"
            )

            # Keep only first 2 columns
            df = df.iloc[:, :2]

            # Rename columns manually
            df.columns = ["Name", "Date"]

        except Exception as e:
            messagebox.showerror("Error", f"CSV Error:\n{e}")
            return

        # -------------------------------a
        # KEEP ONLY Name and Date columns
        # (Ignore Time, Screenshot etc.)
        # -------------------------------
        if "Name" not in df.columns or "Date" not in df.columns:
            messagebox.showerror("Error", "CSV must contain Name and Date columns")
            return

        df = df[["Name", "Date"]].copy()

        df["Name"] = df["Name"].astype(str).str.strip().str.lower()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

        df = df.dropna()

        student_df = df[df["Name"] == student_name]

        if student_df.empty:
            messagebox.showinfo("Info", "No attendance record found.")
            return

        start_date = datetime.date(2025, 4, 1)
        end_date = datetime.date(2027, 3, 31)

        gov_holidays = holidays.India(years=[2025, 2026, 2027])

        # Remove old calendar
        if self.calendar:
            self.calendar.destroy()

        self.calendar = Calendar(
            self.root,
            selectmode='none',
            year=start_date.year,
            month=start_date.month,
            day=start_date.day,
            showothermonthdays=False
        )
        self.calendar.pack(pady=20)

        self.calendar.calevent_remove('all')

        # -------------------------------
        # TAG COLORS (VERY IMPORTANT)
        # -------------------------------
        self.calendar.tag_config('present', background='green', foreground='white')
        self.calendar.tag_config('absent', background='red', foreground='white')
        self.calendar.tag_config('holiday', background='yellow', foreground='black')

        present_dates = set(
            d for d in student_df["Date"]
            if start_date <= d <= end_date
        )

        total_working_days = 0
        present_days = 0
        absent_days = 0
        holiday_days = 0

        current = start_date

        while current <= end_date:

            # Holiday (Weekend OR Govt Holiday)
            if current.weekday() >= 5 or current in gov_holidays:
                self.calendar.calevent_create(current, 'Holiday', 'holiday')
                holiday_days += 1

            else:
                total_working_days += 1

                if current in present_dates:
                    self.calendar.calevent_create(current, 'Present', 'present')
                    present_days += 1
                else:
                    self.calendar.calevent_create(current, 'Absent', 'absent')
                    absent_days += 1

            current += datetime.timedelta(days=1)

        self.calendar.update_idletasks()

        self.show_pie_chart(present_days, absent_days, holiday_days)


    def show_pie_chart(self, present, absent, holiday):

        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            [present, absent, holiday],
            labels=['Present', 'Absent', 'Holidays'],
            colors=['green', 'red', 'yellow'],
            autopct='%1.1f%%'
        )
        ax.set_title("Attendance Summary")

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(pady=20)

        if (present + absent) > 0:
            percentage = (present * 100) / (present + absent)
        else:
            percentage = 0

        if self.percent_label:
            self.percent_label.destroy()

        self.percent_label = tk.Label(
            self.root,
            text=f"Attendance Percentage: {percentage:.2f}%",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        self.percent_label.pack(pady=10)



root = tk.Tk()
app = StudentApp(root)
root.mainloop()
