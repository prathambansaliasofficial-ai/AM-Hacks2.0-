import cv2
import numpy as np 
import os

import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    print("No name provided.")
    exit()


cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
)


skip = 0
face_data = []
dataset_path = "./face_dataset/"



while True:
	ret,frame = cap.read()

	gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	if ret == False:
		continue

	faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
	if len(faces) == 0:
		continue

	k = 1

	faces = sorted(faces, key = lambda x : x[2]*x[3] , reverse = True)

	skip += 1

	for face in faces[:1]:
		x,y,w,h = face

		offset = 5
		face_offset = frame[y-offset:y+h+offset,x-offset:x+w+offset]
		face_selection = cv2.resize(face_offset,(100,100))

		if skip % 10 == 0:
			face_data.append(face_selection)
			print (len(face_data))


		cv2.imshow(str(k), face_selection)
		k += 1
		
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

	cv2.imshow("faces",frame)

	key_pressed = cv2.waitKey(1) & 0xFF
	if key_pressed == ord('q'):
		break

face_data = np.array(face_data)
face_data = face_data.reshape((face_data.shape[0], -1))
print(face_data.shape)


# Get absolute path of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create dataset folder path relative to script
dataset_path = os.path.join(BASE_DIR, "face_dataset")

# Create folder if it doesn’t exist
os.makedirs(dataset_path, exist_ok=True)

# Full file path
file_path = os.path.join(dataset_path, file_name + ".npy")

# Save file
np.save(file_path, face_data)

print("Dataset saved at:", file_path)

cap.release()
cv2.destroyAllWindows()
