import cv2
import numpy
from PySide6 import QtWidgets, QtCore, QtGui
import qimage2ndarray

from frame_generator import FrameGenerator


class VideoPlayer(QtWidgets.QWidget):
    pause: bool = True

    def __init__(self):
        super().__init__()
        self.video_size = QtCore.QSize(1280, 720)
        self.frame_generator = FrameGenerator()
        self.frame_timer = QtCore.QTimer()
        self.fps = 5
        self.setup_video(self.fps)
        self.frame_label = QtWidgets.QLabel()
        self.quit_button = QtWidgets.QPushButton('Quit')
        self.play_pause_bottom = QtWidgets.QPushButton('Play')
        self.play_speed_bottom = QtWidgets.QPushButton('0.2x')
        self.play_speed_1_bottom = QtWidgets.QPushButton('1x')
        self.play_speed_10_bottom = QtWidgets.QPushButton('10x')
        self.main_layout = QtWidgets.QGridLayout()
        self.setup_ui()
        QtCore.QObject.connect(self.play_pause_bottom, QtCore.SIGNAL('clicked()'), self.play_pause)
        QtCore.QObject.connect(self.play_speed_bottom, QtCore.SIGNAL('clicked()'), self.play_speed)
        QtCore.QObject.connect(self.play_speed_1_bottom, QtCore.SIGNAL('clicked()'), self.play_speed_1)
        QtCore.QObject.connect(self.play_speed_10_bottom, QtCore.SIGNAL('clicked()'), self.play_speed_10)

    def setup_ui(self):
        self.frame_label.setFixedSize(self.video_size)
        self.quit_button.clicked.connect(self.close_win)
        self.main_layout.addWidget(self.frame_label, 0, 0, 3, 5)
        self.main_layout.addWidget(self.play_pause_bottom, 5, 2, 1, 1)
        self.main_layout.addWidget(self.play_speed_bottom, 4, 1, 1, 1)
        self.main_layout.addWidget(self.play_speed_1_bottom, 4, 2, 1, 1)
        self.main_layout.addWidget(self.play_speed_10_bottom, 4, 3, 1, 1)
        self.main_layout.addWidget(self.quit_button, 7, 2, 1, 1)
        self.setLayout(self.main_layout)

    def play_pause(self):
        if not self.pause:
            self.frame_timer.stop()
            self.play_pause_bottom.setText('Play')
        else:
            self.frame_timer.start(int(1000 // self.fps))
            self.play_pause_bottom.setText('Pause')
        self.pause = not self.pause

    def play_speed(self, speed: int = 1):
        self.fps = speed
        self.frame_timer.stop()
        self.frame_timer.start(int(1000 // self.fps))
        self.play_pause_bottom.setText('Pause')
        self.pause = False

    def play_speed_1(self):
        self.play_speed(5)

    def play_speed_10(self):
        self.play_speed(50)

    def setup_video(self, fps: int):
        self.frame_timer.timeout.connect(self.display_video)

    def display_video(self):
        try:
            frame_list: list = next(self.frame_generator)
        except StopIteration:
            return False
        frame = numpy.concatenate(
            (numpy.concatenate((frame_list[2], frame_list[3]), axis=1),
             numpy.concatenate((frame_list[1], frame_list[0]), axis=1)), axis=0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.video_size.width(), self.video_size.height()), interpolation=cv2.INTER_AREA)
        image = qimage2ndarray.array2qimage(frame)

        self.frame_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def close_win(self):
        cv2.destroyAllWindows()
        self.close()
