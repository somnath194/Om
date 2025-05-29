import pickle
import numpy as np
import urllib.request

# url = 'http://192.168.202.51/cam-hi.jpg'
esp_url = 'http://192.168.1.11/cam-hi.jpg'
phone_url = 'http://192.168.1.4:8080/shot.jpg'


#Load the encoding file
file = open('D:\\programs\\Project Shunn\\Computer Vision Code\\EncodeFile.p', 'rb')
encodeListKnownWithNames = pickle.load(file)
file.close()
encodeListKnown, imgNames = encodeListKnownWithNames

def faceRecognitionMode():
        import face_recognition
        import cv2
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

        if not cap.isOpened():
            print("[ERROR] Camera not accessible.")
            return

        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("[WARN] Frame not captured.")
                continue

            # img_resp = urllib.request.urlopen(phone_url)
            # imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            # frame = cv2.imdecode(imgnp, -1)

            imgS = cv2.resize(frame, (0,0), None, 0.2, 0.2)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(imgS, model='hog')
            encodeCurframe = face_recognition.face_encodings(imgS, faceCurFrame)
            
            for faceEncode, faceLoc in zip(encodeCurframe, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, faceEncode)
                faceDis = face_recognition.face_distance(encodeListKnown, faceEncode)
                
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = imgNames[matchIndex]

                    top, right, bottom, left = faceLoc
                    top, right, bottom, left = top*5, right*5, bottom*5, left*5
                    cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)

                    # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0,0,255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left+6, bottom+25), font, 1.0, (255,255,255), 1)



            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            
        cap.release()

def cctv_camera():
    import cv2
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()

        # img_resp = urllib.request.urlopen(esp_url)
        # imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        # frame = cv2.imdecode(imgnp, -1)

        cv2.imshow("video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

# Call this function from anywhere
# if __name__ == "__main__":
#     cctv_camera()
