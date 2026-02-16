# Face Recognition Based Attendance Management System

An automated attendance management system built using Python, OpenCV, Tkinter, and Pandas that detects faces in real time and records attendance digitally with screenshot proof.

---

## Project Description

The Face Recognition Attendance Management System automates classroom attendance using computer vision.

Instead of manually marking attendance, the system:
- Detects faces using a webcam  
- Recognizes students using the KNN algorithm  
- Saves attendance automatically  
- Stores screenshot proof  
- Displays attendance in a color-coded calendar  
- Generates a pie chart summary  

This system improves efficiency, accuracy, and transparency.

---

## Features

### Teacher Module
- Real-time face detection using Haarcascade
- Face recognition using KNN
- Save attendance on key press (S key)
- Stores name, date, time, and screenshot
- Allows multiple attendance entries
- Screenshot proof stored locally

### Student Module
- Student enters their name
- Displays 2-year academic calendar
- Color-coded attendance (Green: Present, Red: Absent, Yellow: Weekend/Holiday)
- Pie chart visualization
- Attendance percentage calculation

---

## Technologies Used

- **Python** - Core programming
- **OpenCV** - Face detection
- **NumPy** - Numerical operations
- **Pandas** - CSV handling
- **Tkinter** - GUI
- **tkcalendar** - Calendar UI
- **Matplotlib** - Data visualization
- **Holidays** - Government holiday detection

---

## How It Works

### Face Registration
- Capture multiple face images
- Store as NumPy arrays
- Each student has a .npy file

### Face Recognition Process
1. Webcam captures frame  
2. Convert to grayscale  
3. Detect face using Haarcascade  
4. Resize face to 100x100  
5. Flatten image  
6. Compare using KNN  
7. Predict student name  

### Attendance Saving
When S key is pressed, screenshot is saved and data appended to attendance.csv

---

## Calendar Logic (Student Module)

Academic year range with color coding:
- Green indicates present
- Red indicates absent
- Yellow indicates weekend or government holiday

Enter student name to view attendance.

---

## Testing Scenarios

- 100% attendance student
- Partial attendance
- Multiple entries same day
- Full 2-year calculation
- No attendance record

---

## Advantages

- Eliminates proxy attendance
- Automated system
- Screenshot proof
- Easy to use
- Expandable
- Real-time processing

---

## Limitations

- Sensitive to lighting conditions
- Camera quality affects recognition accuracy
- KNN not ideal for large-scale deployment
- CSV not suitable for very large datasets

---

## Future Improvements

- Replace KNN with Deep Learning (FaceNet/CNN)
- Add MySQL/PostgreSQL database
- Web-based dashboard
- Admin login authentication
- Cloud storage integration
- SMS/Email attendance alerts
- Export attendance to PDF
- Monthly attendance reports

---

## Learning Outcomes

- Computer Vision fundamentals
- KNN classification algorithm
- GUI development with Tkinter
- Data handling with Pandas
- Visualization with Matplotlib
- Debugging real-world software issues

---

## License

This project is developed for educational purposes. Free to use and modify for learning and research.
