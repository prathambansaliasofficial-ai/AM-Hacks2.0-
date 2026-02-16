import cv2
import pytesseract
import pandas as pd
import os
from datetime import datetime

# If using Windows, uncomment and set path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cap = cv2.VideoCapture(0)

csv_file = "names.csv"

# Create CSV if not exists
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Name", "Timestamp"])
    df.to_csv(csv_file, index=False)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press 's' to take screenshot and detect text
    if key == ord('s'):
        print("📸 Screenshot Taken")

        # Create unique filename using timestamp
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"screenshot_{timestamp_str}.png"

        # Save screenshot in same folder
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")


        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Optional: improve OCR accuracy
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Extract text
        text = pytesseract.image_to_string(gray)

        print("Detected Text:")
        print(text)

        # Clean text into lines
        lines = text.split('\n')
        names = [line.strip() for line in lines if line.strip() != ""]

        # Save each detected line as name
        for name in names:
            new_row = pd.DataFrame(
                [[name, datetime.now()]],
                columns=["Name", "Timestamp"]
            )
            new_row.to_csv(csv_file, mode='a', header=False, index=False)

        print("Saved to CSV!")

    # Press q to quit
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
