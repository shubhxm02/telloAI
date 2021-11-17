from FaceTrackerModule import *
from djitellopy import tello
from time import sleep, time
import cv2

pErrorYV, pErrorUD = 0, 0
HEIGHT, WIDTH = 360, 480

drone = tello.Tello()
keepRecording = True

testing = 0

def init():
    drone.connect()
    drone.streamon()
    if drone.get_battery() < 20:
        return False

    print(drone.get_battery())

    if not testing:
        drone.takeoff()
        drone.move_up(80)

    return True


def get_image():
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (WIDTH, HEIGHT))
    return img


def main():
    if not init():
        return

    global pErrorYV, pErrorUD

    video1 = cv2.VideoWriter(os.path.join('images', '{}raw.avi'.format(time())), cv2.VideoWriter_fourcc(*'XVID'), 30, (WIDTH, HEIGHT))
    video2 = cv2.VideoWriter(os.path.join('images', '{}.avi'.format(time())), cv2.VideoWriter_fourcc(*'XVID'), 30, (WIDTH, HEIGHT))
    
    run = True
    while run:

        img = get_image()
        if img is None:
            continue

        raw = img.copy()

        img, face_info, hand_info = processFrame(img)
        commands, pErrorYV, pErrorUD = follow_face(face_info, pErrorYV, pErrorUD)
        displayText(img, commands, face_info, hand_info)    
        cv2.imshow('img', raw)
        cv2.imshow('processed', img)
        video1.write(raw)
        video2.write(img)

        lr, fb, ud, yv = commands
        if not testing:
            drone.send_rc_control(lr, fb, ud, yv)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            run = False

        if drone.get_battery() < 20:
            run = False

    video1.release()
    video2.release()

    cv2.destroyAllWindows()
    if not testing:
        drone.land()
    drone.end()


if __name__ == '__main__':
    main()