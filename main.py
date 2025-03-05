import cv2
import os


def create_capture():
    pass


def search_video():
    video: tuple
    for file in os.listdir(r'data'):
        if file.endswith('.avi'):
            video


def save_frame(capture):
    index = 0
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        cv2.imwrite(f"frame{index}.jpg", frame)
        index += 1


create_capture()
capture = cv2.VideoCapture(r'data/1.avi')
capture.release()
