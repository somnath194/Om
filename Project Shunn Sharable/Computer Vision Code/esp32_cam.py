import cv2
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# # Warm up camera
# for _ in range(10):
#     cap.read()

while True:
    ret, frame = cap.read()
    cv2.imshow("Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
