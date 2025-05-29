import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


import absl.logging
absl.logging.set_verbosity('error')
import cv2
import mediapipe as mp
import time
import hand_tracking_module as htm
import autopy
import numpy as np
import urllib.request

# Configurations
wCam, hCam = 640, 480
wScr, hScr = autopy.screen.size()
frameRx, frameRy = 100, 50
alpha = 0.25  # smoothing factor for exponential moving average
clickCooldown = 0.3
clickThreshold = 35

# ip = "http://192.168.1.4:8080/video"
phone_url = 'http://192.168.1.4:8080/shot.jpg'


# Initialize detector and capture
detector = htm.handDetector(maxHands=1)
running = False

def hand_mouse_mode():
    global running
    running = True

    plocx, plocy = 0, 0
    clocx, clocy = 0, 0
    lastClickTime = 0
    pTime = 0

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("[ERROR] Camera not accessible.")
        return
    
    while running:
        # img_resp = urllib.request.urlopen(phone_url)
        # imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        # frame = cv2.imdecode(imgnp, -1)
        ret, frame = cap.read()
        if not ret or frame is None:
            print("[WARN] Frame not captured.")
            continue

        img = cv2.resize(frame, (wCam, hCam))
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]  # Index finger tip
            x2, y2 = lmList[12][1:]  # Middle finger tip

            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameRx, frameRy), (wCam - frameRx, hCam - frameRx - frameRy), (255, 0, 255), 2)

            # Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameRx, wCam - frameRx), (0, wScr))
                y3 = np.interp(y1, (frameRy, hCam - frameRx - frameRy), (0, hScr))

                clocx = (1 - alpha) * plocx + alpha * x3
                clocy = (1 - alpha) * plocy + alpha * y3

                clocx = max(0, min(clocx, wScr - 1))
                clocy = max(0, min(clocy, hScr - 1))

                autopy.mouse.move(wScr - clocx, clocy)
                cv2.circle(img, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
                plocx, plocy = clocx, clocy

            # Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img, draw=False)
                if length < clickThreshold and (time.time() - lastClickTime) > clickCooldown:
                    lastClickTime = time.time()
                    autopy.mouse.click()
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 0), cv2.FILLED)

        # FPS Calculation
        cTime = time.time()
        fps = 1 / (cTime - pTime) if cTime != pTime else 0
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)

        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
    
    cv2.destroyAllWindows()
    cap.release()
    return
    
def stop_hand_mouse():
    global running
    running = False

# # # Call this function from anywhere
# if __name__ == "__main__":
#     hand_mouse_mode()
