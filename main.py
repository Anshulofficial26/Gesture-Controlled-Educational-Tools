import cv2
import os
import numpy as np
from cvzone.HandTrackingModule import HandDetector


width, height = 1280, 720
gestureThreshold = 450
folderPath = "Slides"

# this opens the camera for video capture using openCV
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# this detects hands with detection confidence of 80 per cent and with max hands in frame 1...
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# used variables
imgList = []
delay = 20
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(250 * 1), int(400 * 1)

# this gets the list of slides to be presented as images...
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)  # flips the image in horizontal direction as the hand movements were opp. of actual
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # this finds the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # this detects hand from the img and returns the img...

    # gesture threshold
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (150, 150, 150), 5)

    if hands and buttonPressed is False:

        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # marks list of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # fingers up algo

        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 8, (255, 0, 0), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, 8, (255, 0, 0), cv2.FILLED)

        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

    else:
        annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
