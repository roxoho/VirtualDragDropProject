import cv2
import handTrackingModule as HTM
import math
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HTM.hand_Detector(detectionCon=0.8)

#cx, cy = 100, 100
#w, h = 200, 200


class DragRect():
    def __init__(self, posCenter, size=[200, 200], colorR = [255,0,255]):
        self.posCenter = posCenter
        self.size = size
        self.colorR = colorR

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        #if finger tip in the rectangle area
        if cx-w//2 < cursor[1] < cx+w//2 and cy-h//2 < cursor[2] < cy+h//2:
            self.posCenter = cursor[1], cursor[2]
            self.colorR = [0,255,0]






def findDistance(img, lmlist, a, b, draw=True):
    length = 0

    if len(lmlist) != 0:
        x1, y1 = lmList[a][1], lmList[a][2]
        x2, y2 = lmList[b][1], lmList[b][2]
        Cx, Cy = (x2+x1)//2, (y2+y1)//2
        if draw:
            cv2.circle(img,(x1, y1), 10, (255,0,255), cv2.FILLED)
            cv2.circle(img,(x2, y2), 10, (255,0,255), cv2.FILLED)
            cv2.circle(img,(Cx, Cy), 10, (255,0,255), cv2.FILLED)
            cv2.line(img,(x1, y1),(x2, y2),(255,0,255),2)

        length = math.hypot(x2-x1,y2-y1)

    return length


rectList = []

for i in range(5):
    rectList.append(DragRect([i*250+150, 150]))

while True:
    ret, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    colorR = (255, 0, 255)

    if lmList:
        length = findDistance(img, lmList, 8, 12)
        print(length)
        if length < 45:
            cursor = lmList[8]
            #call the update here
            for rect in rectList:
                rect.update(cursor)

    #draw
    imgNew = np.zeros_like(img,np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        #colorR = tuple(rect.colorR)
        cv2.rectangle(imgNew, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Webcam", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
