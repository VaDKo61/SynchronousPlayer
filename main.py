import sys

from PySide6 import QtWidgets

from video_player import VideoPlayer

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())