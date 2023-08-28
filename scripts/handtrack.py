import cv2 as cv
import time
import mediapipe as mp
cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0




if not cap.isOpened():
    print("Cannt open camera")
    exit()

while True:
    ret, frame = cap.read()
    imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            #land marks
            for id, lm in enumerate(handLms.landmark):
                #print(id, lm)
                h, w, c= frame.shape
                cx, cy= int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 0:
                    cv.circle(frame, (cx, cy), 25, (255,0,255), cv.FILLED)

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

        #FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame,str(int(fps)),(10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)

    if not ret:
        print("can` recive frame (stream end?). Exiting ...")
        break
    cv.imshow('Imagem', frame)
    if cv.waitKey(1) == ord('q'):
        break
    
    


cap.realease()
cv.destroyAllWindows()