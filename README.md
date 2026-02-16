# 🎓 Face Recognition Based Attendance Management System

An automated attendance management system built using **Python, OpenCV, Tkinter, and Pandas** that detects faces in real time and records attendance digitally with screenshot proof.

---

## 📌 Project Description

The **Face Recognition Attendance Management System** automates classroom attendance using computer vision.

Instead of manually marking attendance, the system:

- Detects faces using a webcam  
- Recognizes students using the KNN algorithm  
- Saves attendance automatically  
- Stores screenshot proof  
- Displays attendance in a color-coded calendar  
- Generates a pie chart summary  

This system improves efficiency, accuracy, and transparency.

---

## 🚀 Features

### 👨‍🏫 Teacher Module
- Real-time face detection using Haarcascade
- Face recognition using KNN
- Save attendance on key press (`S`)
- Stores:
  - Name
  - Date
  - Time
  - Screenshot
- Allows multiple attendance entries
- Screenshot proof stored locally

---

### 👨‍🎓 Student Module
- Student enters their name
- Displays 2-year academic calendar
- Color-coded attendance:
  - 🟢 Green → Present
  - 🔴 Red → Absent
  - 🟡 Yellow → Weekend / Govt Holiday
- Pie chart visualization
- Attendance percentage calculation

---

## 🛠 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core programming |
| OpenCV | Face detection |
| NumPy | Numerical operations |
| Pandas | CSV handling |
| Tkinter | GUI |
| tkcalendar | Calendar UI |
| Matplotlib | Data visualization |
| Holidays | Govt holiday detection |

---

## 📂 Project Structure

