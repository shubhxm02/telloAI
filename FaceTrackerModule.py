import os
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(
    os.path.join("haarcascades", "haarcascade_fullbody.xml")
)
hand_cascade = cv2.CascadeClassifier(os.path.join("haarcascades", "hand.xml"))

fbRange = [10000, 14000]
pid = [0.4, 0.4, 0]
pErrorYV, pErrorUD = 0, 0

cap = 0

HEIGHT, WIDTH = 360, 480


def findFaces(img, imgGray):

    faces = face_cascade.detectMultiScale(imgGray, 1.3, 10)

    faceListCenter = []
    faceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
        centerx = x + w // 2
        centery = y + h // 2
        area = w * h
        faceListArea.append(area)
        faceListCenter.append([centerx, centery])

    if len(faceListCenter) != 0:
        index = faceListArea.index(max(faceListArea))
        return img, [faceListCenter[index], faceListArea[index]]
    else:
        return img, [[0, 0], 0]


def findHands(img, imgGray):
    return img, 0


def processFrame(img):
    # face_cascade = cv2.CascadeClassifier(os.path.join('haarcascades', 'haarcascade_frontalface_default.xml'))
    # hand_cascade = cv2.CascadeClassifier(os.path.join('haarcascades', 'haarcascade_frontalface_default.xml'))

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img, face_info = findFaces(img, imgGray)
    img, hand_info = findHands(img, imgGray)

    return img, face_info, hand_info


def displayText(img, commands, face_info, hand_info):
    (cx, cy), area = face_info

    if area == 0:
        cv2.putText(
            img,
            "searching for face...",
            (30, 30),
            cv2.FONT_HERSHEY_COMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )
        return

    global HEIGHT, WIDTH
    cv2.arrowedLine(
        img,
        (WIDTH // 2, HEIGHT // 2),
        (face_info[0][0], face_info[0][1]),
        (200, 0, 100),
        3,
    )
    cv2.putText(
        img,
        "commands : {}".format(commands),
        (30, 30),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        img,
        "x : {} y : {}".format(cx, cy),
        (30, 60),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        img,
        "area : {}".format(area),
        (30, 90),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )

    print_data = []

    [lr, fb, ud, yv] = commands

    if lr > 0:
        lr = "left"
    elif lr < 0:
        lr = "right"
    if fb > 0:
        fb = "forward"
    elif fb < 0:
        fb = "backward"
    if ud > 0:
        ud = "up"
    elif ud < 0:
        ud = "down"
    if yv > 0:
        yv = "cw"
    elif yv < 0:
        yv = "ccw"

    cv2.putText(
        img,
        "drone moves : {}".format(lr),
        (30, 200),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        img,
        "drone moves : {}".format(fb),
        (30, 230),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        img,
        "drone moves : {}".format(ud),
        (30, 260),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        img,
        "drone rotates : {}".format(yv),
        (30, 290),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )


def follow_face(info, pErrorYV, pErrorUD, vel=20):
    lr, fb, ud, yv = 0, 0, 0, 0

    area, x, y = info[1], info[0][0], info[0][1]
    global HEIGHT, WIDTH

    if area == 0:
        commands = [0, 0, 0, 20]
        errorUD, errorYV = 0, 0
        return commands, errorYV, errorUD

    errorYV = x - WIDTH // 2
    yv = pid[0] * errorYV + pid[1] * (errorYV - pErrorYV)
    yv = int(np.clip(yv, -100, 100))

    errorUD = HEIGHT // 2 - y
    ud = pid[0] * errorUD + pid[1] * (errorUD - pErrorUD)
    ud = int(np.clip(ud, -100, 100))

    if area > fbRange[1]:
        fb = -vel
    elif area < fbRange[0] and area > 0:
        fb = vel

    commands = [lr, fb, ud, yv]

    return commands, errorYV, errorUD


def main():

    pErrorYV, pErrorUD = 0, 0

    global cap
    cap = cv2.VideoCapture(1)
    _, img = cap.read()
    global HEIGHT, WIDTH
    HEIGHT, WIDTH, _ = img.shape

    while True:
        _, img = cap.read()

        img, face_info, hand_info = processFrame(img)

        commands, pErrorYV, pErrorUD = follow_face(face_info, pErrorYV, pErrorUD)

        displayText(img, commands, face_info, hand_info)

        cv2.imshow("img", img)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break

    cap.release()


if __name__ == "__main__":
    main()
