import cv2
import glob
import time
import os
from threading import Thread
from emailing import send_emai

video = cv2.VideoCapture(0)
time.sleep(1)

# initializing variable
first_frame = None
status_list = []
count = 1


def clear_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.read(image)


# video.read() captures a frame from the webcam. check is a boolean indicating success, and frame is the captured image.
while True:
    status = 0
    check, frame = video.read()

    # Converting to Grayscale and Blurring
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # setting the first frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # calculating the difference
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Thresholding and dilating
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Finding contours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Drawing rectangle motion around
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if rectangle.any():
            status = 1
            cv2.imwrite(f'images/{count}.png', frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images)) / 2
            image_with_object = index

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_emai, args=(image_with_object, ))
        email_thread.daemon = True
        clear_thread = Thread(target=clear_folder)
        clear_thread.daemon = True

        email_thread.start()

        print(status_list)

    # Displacing the video
    cv2.imshow("video", frame)
    key = cv2.waitKey(1)

    # here if the user enters q it will stop te camera
    if key == ord("q"):
        break


video.release()
clear_thread.start()