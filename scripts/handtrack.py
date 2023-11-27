import cv2 as cv
import time
import mediapipe as mp

class handDetcetor():
    def __init__(self, mode = False, maxHands = 2, complexity = 1, detectionCon = 0.75, trackCon = 0.75 ):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw= True):
        imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #self.results = self.hands.process(frame)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks: 
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame     

    def findPosition(self, frame, handNo = 0, draw = True):
            
            lmList = []
            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    #print(id, lm)
                    h, w, c= frame.shape
                    cx, cy= int(lm.x*w), int(lm.y*h)
                    #print(id, cx, cy)
                    lmList.append([id, cx, cy])
                    if draw :
                        cv.circle(frame, (cx, cy), 3, (255,0,255), cv.FILLED)

                if len(self.results.multi_hand_landmarks) == 2:
                    myHand2 = self.results.multi_hand_landmarks[handNo+1]
                    for id, lm in enumerate(myHand2.landmark):
                        #print(id, lm)
                        h, w, c= frame.shape
                        cx, cy= int(lm.x*w), int(lm.y*h)
                        #print(id, cx, cy)
                        lmList.append([id, cx, cy])
                        if draw :
                            cv.circle(frame, (cx, cy), 3, (255,0,255), cv.FILLED)

            return lmList

def pointing_up(lmList, action):
    if((lmList[12][2] > lmList[8][2] and lmList[16][2] > lmList[8][2] and lmList[12][2] > lmList[8][2]) and lmList[0][2] > lmList[8][2] and lmList[8][2] < lmList[6][2] and lmList[8][2] < lmList[7][2]  and lmList[4][2] > lmList[8][2]):
        if((lmList[8][1] > lmList[20][1]) and (lmList[6][1] > lmList[4][1])):
            action.append("pointing up")
        if((lmList[8][1] < lmList[20][1]) and (lmList[6][1] < lmList[4][1])):
            action.append("pointing up")
    
    elif len(lmList) > 21:
        if((lmList[12+21][2] > lmList[8+21][2] and lmList[16+21][2] > lmList[8+21][2] and lmList[12+21][2] > lmList[8+21][2]) and lmList[0+21][2] > lmList[8+21][2] and lmList[8+21][2] < lmList[6+21][2] and lmList[8+21][2] < lmList[7+21][2]  and lmList[4+21][2] > lmList[8+21][2]):
            if((lmList[8+21][1] > lmList[20+21][1]) and (lmList[6+21][1] > lmList[4+21][1])):
                action.append("pointing up")
            if((lmList[8+21][1] < lmList[20+21][1]) and (lmList[6+21][1] < lmList[4+21][1])):
                action.append("pointing up")
        
def pointing_down(lmList, action):
    if((lmList[12][2] < lmList[8][2] and lmList[16][2] < lmList[8][2] and lmList[12][2] < lmList[8][2]) and lmList[0][2] < lmList[8][2] and lmList[8][2] > lmList[6][2] and lmList[8][2] > lmList[7][2] and lmList[4][2] < lmList[8][2]):
        if((lmList[8][1] > lmList[20][1]) and (lmList[6][1] > lmList[4][1])):
            action.append("pointing down")
        if((lmList[8][1] < lmList[20][1]) and (lmList[6][1] < lmList[4][1])):
            action.append("pointing down")    

    elif len(lmList) > 21:
        if((lmList[12+21][2] < lmList[8+21][2] and lmList[16+21][2] < lmList[8+21][2] and lmList[12+21][2] < lmList[8+21][2]) and lmList[0+21][2] < lmList[8+21][2] and lmList[8+21][2] > lmList[6+21][2] and lmList[8+21][2] > lmList[7+21][2] and lmList[4+21][2] < lmList[8+21][2]):
            if((lmList[8+21][1] > lmList[20+21][1]) and (lmList[6+21][1] > lmList[4+21][1])):
                action.append("pointing down")
            if((lmList[8+21][1] < lmList[20+21][1]) and (lmList[6+21][1] < lmList[4+21][1])):
                action.append("pointing down")

def main():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    pTime = 0
    cTime = 0
    detector = handDetcetor()
    while True:
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)
        action = []
        if len(lmList) != 0:
            # Gesto 1
            pointing_up(lmList, action)
            # Gesto 2
            pointing_down(lmList, action)    

        if len(action) != 0:
            cv.putText(frame, action[0], (100,170), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
            if len(action) > 1:
                cv.putText(frame, action[1], (400,170), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
            
        #FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv.imshow('Imagem', frame)
        if cv.waitKey(1) == 27:
            break


if __name__ == "__main__":
    main()