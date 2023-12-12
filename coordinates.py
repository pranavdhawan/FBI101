import cv2
import dlib
import numpy as np
from imutils import face_utils
import pyautogui
import time
import os
import pygetwindow as gw  # Import the pygetwindow library

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

print_interval = 2
log_file_path = "console.txt"

def common_coordinates(left, right):
    x = (left[0] + right[0]) // 2
    y = (left[1] + right[1]) // 2
    return x, y


# Check if the file exists, if not, create it
if not os.path.exists(log_file_path):
    with open(log_file_path, "w") as new_file:
        pass

last_print_time = time.time() - print_interval

with open(log_file_path, "a") as log_file:
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)
            left_eye = shape[42:48]
            right_eye = shape[36:42]
            left_eye_center = np.mean(left_eye, axis=0, dtype=int)
            right_eye_center = np.mean(right_eye, axis=0, dtype=int)
            
            normalized_left_eye_x = int((left_eye_center[0] / frame.shape[1]) * screen_width)
            normalized_left_eye_y = int((left_eye_center[1] / frame.shape[0]) * screen_height)
            normalized_right_eye_x = int((right_eye_center[0] / frame.shape[1]) * screen_width)
            normalized_right_eye_y = int((right_eye_center[1] / frame.shape[0]) * screen_height)
            
            final_coordinates = common_coordinates([normalized_left_eye_x, normalized_left_eye_y], [normalized_right_eye_x, normalized_right_eye_y])


            current_time = time.time()
            if current_time - last_print_time >= print_interval:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))

                # Get the active window title
                active_window_title = gw.getActiveWindow().title()

                log_file.write(f"{timestamp} _ Application: {active_window_title}, Common Coordinates: {final_coordinates}\n")
                last_print_time = current_time

            cv2.circle(frame, tuple(left_eye_center), 5, (0, 255, 0), -1)
            cv2.circle(frame, tuple(right_eye_center), 5, (0, 255, 0), -1)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
