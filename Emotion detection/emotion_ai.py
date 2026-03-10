import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("emotion_model.h5")

emotions = ['angry','disgust','fear','happy','neutral','sad','surprise']

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cap = cv2.VideoCapture(0)


def detect_emotion():

    ret, frame = cap.read()

    if not ret:
        return "neutral"

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.3,5)

    detected_emotion = "neutral"

    for (x,y,w,h) in faces:

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi,(48,48))
        roi = roi / 255.0
        roi = np.reshape(roi,(1,48,48,1))

        prediction = model.predict(roi, verbose=0)

        detected_emotion = emotions[np.argmax(prediction)]

    cv2.imshow("Face Detection", frame)
    cv2.waitKey(1)

    return detected_emotion