import cv2 as cv
import time
import mediapipe as mp
from cvzone import HandTrackingModule

cap = cv.VideoCapture(0)

detector = HandTrackingModule.HandDetector()

pTime = 0
cTime = 0

while True:
        ret, frame = cap.read()
        hands, frame = detector.findHands(frame)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv.imshow('Imagem', frame)
        if cv.waitKey(1) == 27:
            break