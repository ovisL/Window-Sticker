import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie


class Sticker(QtWidgets.QMainWindow):
    def __init__(self, path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()
        self.timer = QtCore.QTimer(self)
        self.path = path
        self.xy = xy

        self.from_xy = xy
        self.to_xy = xy

        self.from_xy_diff = [0, 0]
        self.to_xy_diff = [0, 0]
        self.direction = [0, 0]
        self.localPos = None

        self.speed = 60
        self.size = size
        self.on_top = on_top

        self.initUI()
        self.show()

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.localPos = a0.localPos()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        self.xy = [(a0.globalX() - self.localPos.x()),
                   (a0.globalY() - self.localPos.y())]
        self.move(*self.xy)

    def initUI(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        flags = QtCore.Qt.WindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
            if self.on_top
            else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        img_label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.path)
        img_label.setMovie(movie)
        movie.start()
        movie.stop()

        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()

        self.setGeometry(self.xy[0], self.xy[1], w, h)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    s = Sticker('bird.gif', [600, 800], size=1, on_top=True)
    sys.exit(app.exec_())
