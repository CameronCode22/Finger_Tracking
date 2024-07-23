import cv2
import mediapipe as mp
import hand_tracking_moduleV2 as htm
import time
import serial

ser = serial.Serial('COM6', 9600)
time.sleep(2)

# Constants for colors and camera size
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
wCam, hCam = 640, 480

# Camera configuration
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

# Initializing the hand detector
detector = htm.handDetector(detectionCon=0.7)
numberOfFingers = 0

# Function for summing the values in a dictionary
def sum_dict(dict):
    result = 0
    for key in dict:
        result += dict[key]
    return result

last_sent = time.time()
while True:
    fingers = {"4": 0, "8": 0, "12": 0, "16": 0, "20": 0}

    success, img = cap.read()
    img = detector.findHands(img)
    landmarks = detector.findPosition(img, draw=False)

    # Finger recognition
    if len(landmarks) != 0:
        # Landmark [id][x=1, y=2]
        # Thumb
        if landmarks[4][1] > landmarks[3][1]:
            fingers["4"] = 1

        # Index finger
        if landmarks[8][2] < landmarks[6][2]:
            fingers["8"] = 1

        # Middle finger
        if landmarks[12][2] < landmarks[10][2]:
            fingers["12"] = 1

        # Ring finger
        if landmarks[16][2] < landmarks[14][2]:
            fingers["16"] = 1

        # Little finger
        if landmarks[20][2] < landmarks[18][2]:
            fingers["20"] = 1

    # Total the number of fingers detected
    numberOfFingers = sum_dict(fingers)

    # Display the number of fingers on the screen
    cv2.rectangle(img, (25, 150), (100, 400), GREEN, cv2.FILLED)
    #cv2.putText(img, f'{numberOfFingers}', (35, 300), cv2.FONT_HERSHEY_PLAIN, 6, BLUE, 2)
    print("number count",numberOfFingers)

    current_time = time.time()
    if current_time - last_sent > 0.5:
        command = ''.join(str(fingers[key]) for key in ["4", "8", "12", "16", "20"]) + '\n'
        ser.write(command.encode())
        print(f"Sending command: {command}")
        last_sent = current_time
    # FPS display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, BLUE, 2)

    # Display the image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
