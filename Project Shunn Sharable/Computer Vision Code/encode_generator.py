import os
import cv2
import face_recognition
import pickle
folderPath = "D:\\programs\\Project Data\\face recognition"

pathList = os.listdir(folderPath)
imgList = []
imgNames = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    imgNames.append(os.path.splitext(path)[0])


def findEncodings(imagelist):
    encodeList = []
    for img in imagelist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding started ......")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithNames = [encodeListKnown, imgNames]
print("Encoding Complete")

file = open('EncodeFile.p', 'wb')
pickle.dump(encodeListKnownWithNames, file)
file.close()
print("File Saved")