import math
import cv2
import os

from datetime import datetime


class FrameGenerator:
    """Generates synchronized frames from 4 videos"""

    def __init__(self):
        self.video_name, self.annotations_name = self.search_file()
        if len(self.video_name) != len(self.annotations_name) or len(self.video_name) != 4:
            raise FileNotFoundError('Файл аннотации или видео отсутствует')
        self.capture = self.create_capture()
        self.time_frame: list[list[float]] = self.get_time_frame()
        self.min_time_frame, self.max_time_frame = self.get_min_max_time()

        self.time_iter: list = [iter(self.time_frame[i]) for i in range(len(self.time_frame))]
        self.time: list = [next(self.time_iter[i]) for i in range(len(self.time_iter))]

        self.frame: list = [cv2.imread(f'data/1.jpg') for _ in range(len(self.time_iter))]
        self.current_time: float = self.min_time_frame - 0.2
        self.long: int = math.ceil((self.max_time_frame - self.min_time_frame) / 0.2)

    def __iter__(self):
        return self

    def __next__(self):
        if self.long > 0:
            self.current_time += 0.2
            for i in range(len(self.frame)):
                if self.time[i] <= self.current_time:
                    self.frame[i], self.time[i] = self.get_current_frame(i)
            self.long -= 1
            return self.frame
        for i in range(len(self.frame)):
            self.capture[i].release()
        raise StopIteration

    @staticmethod
    def search_file() -> tuple[list, list]:
        """search file .avi and .txt in directory data"""
        video: list = []
        annotations: list = []
        for file in os.listdir(r'data'):
            if file.endswith('.avi'):
                video.append(file)
            elif file.endswith('.txt'):
                annotations.append(file)
        return video, annotations

    def create_capture(self) -> list:
        cap: list = [cv2.VideoCapture(f'data/{i}') for i in self.video_name]
        return cap

    def get_time_frame(self) -> list[list[float]] | None:
        time_fr: list = []
        for i, ann in enumerate(self.annotations_name):
            time_fr.append([])
            with open(f'data/{ann}', 'r') as file:
                for j in file.readlines():
                    try:
                        time = float(j[0:-3])
                    except ValueError('В файле указано не время'):
                        return None
                    else:
                        time_fr[i].append(time)
        return time_fr

    def get_min_max_time(self) -> tuple[float, float]:
        min_time: float = min(i[0] for i in self.time_frame)
        max_time: float = max(i[-1] for i in self.time_frame)
        return min_time, max_time

    def get_current_frame(self, number: int):
        frame = self.frame[number]
        time = self.time[number]
        try:
            time = next(self.time_iter[number])
        except StopIteration:
            pass
        else:
            frame = self.capture[number].read()[1]
            self.add_data_to_frame(frame, number)
        return frame, time

    def add_data_to_frame(self, frame, number: int):
        time = str(datetime.fromtimestamp(self.time[number]).strftime('%Y-%m-%d %H:%M:%S'))
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(frame, time, (700, 50), font, 3, (0, 0, 255), 2, cv2.LINE_AA)
