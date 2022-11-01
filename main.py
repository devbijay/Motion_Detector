import cv2
import threading
import imutils
import winsound

SENSITIVITY = 300
RELATIVE_SENSITIVITY = 30

# Press S to Start & Q To Quit Alarm

alarm_status = False
alarm_mode = False
alarm_counter = 0


def alarm_function():
    global alarm_status
    for _ in range(10):
        if not alarm_mode:
            break
        print("Movement Detected")
        winsound.Beep(2500, 1000)
    alarm_status = False


cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cam.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

while True:
    _, frame = cam.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        bw_frames = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bw_frames = cv2.GaussianBlur(bw_frames, (5, 5), 0)
        diff = cv2.absdiff(bw_frames, start_frame)
        threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = bw_frames

        if threshold.sum() > SENSITIVITY:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
    else:
        cv2.imshow("Camera", frame)

    if alarm_counter > RELATIVE_SENSITIVITY:
        if not alarm_status:
            alarm_status = True
            threading.Thread(target=alarm_function).start()
    key_press = cv2.waitKey(30)
    if key_press == ord("S") or key_press == ord("s"):
        alarm_mode = not alarm_status
        alarm_counter = 0

    if key_press == ord("Q") or key_press == ord("q"):
        alarm_mode = False
        break
cam.release()
cv2.destroyAllWindows()
