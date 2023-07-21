import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie
from menu import return_menu, call_hour, pretty_date, call_ymd, return_nextday


class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()
        self.timer = QtCore.QTimer(self)
        self.img_path = img_path
        self.xy = xy
        self.from_xy = xy
        self.from_xy_diff = [0, 0]
        self.to_xy = xy
        self.to_xy_diff = [0, 0]
        self.speed = 60
        self.direction = [0, 0]  # x: 0(left), 1(right), y: 0(up), 1(down)
        self.size = size
        self.on_top = on_top
        self.localPos = None

        self.setupUI()
        self.show()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.to_xy_diff == [0, 0] and self.from_xy_diff == [0, 0]:
            pass
        else:
            self.walk_diff(self.from_xy_diff, self.to_xy_diff,
                           self.speed, restart=True)

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.localPos = a0.localPos()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        self.timer.stop()
        self.xy = [(a0.globalX() - self.localPos.x()),
                   (a0.globalY() - self.localPos.y())]
        self.move(*self.xy)

    def walk(self, from_xy, to_xy, speed=60):
        self.from_xy = from_xy
        self.to_xy = to_xy
        self.speed = speed

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.__walkHandler)
        self.timer.start(1000 / self.speed)

    def walk_diff(self, from_xy_diff, to_xy_diff, speed=60, restart=False):
        self.from_xy = [self.xy[0] + from_xy_diff[0],
                        self.xy[1] + from_xy_diff[1]]
        self.to_xy = [self.xy[0] + to_xy_diff[0],
                      self.xy[1] + to_xy_diff[1]]
        self.speed = speed
        if restart:
            self.timer.start()
        else:
            self.timer.timeout.connect(self.__walkHandler)
            self.timer.start(1000 / self.speed)

    def __walkHandler(self):
        if self.xy[0] >= self.to_xy[0]:
            self.direction[0] = 0
        elif self.xy[0] < self.from_xy[0]:
            self.direction[0] = 1

        if self.direction[0] == 0:
            self.xy[0] -= 1
        else:
            self.xy[0] += 1

        if self.xy[1] >= self.to_xy[1]:
            self.direction[1] = 0
        elif self.xy[1] < self.from_xy[1]:
            self.direction[1] = 1

        if self.direction[1] == 0:
            self.xy[1] -= 1
        else:
            self.xy[1] += 1

        self.move(*self.xy)

    def setupUI(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint |
                                      QtCore.Qt.WindowStaysOnTopHint
                                      if self.on_top else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        label.setMovie(movie)
        movie.start()
        movie.stop()

        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()

        self.setGeometry(self.xy[0], self.xy[1], w, h)

        threeMeal = [' 아침',' 점심',' 저녁']
        date = call_ymd()
        if call_hour() < 7:
            slot = 1
        elif call_hour() >= 7 and call_hour() < 13:
            slot = 2
        elif call_hour() >= 13 and call_hour() < 19:
            slot = 3
        else:
            slot = 1
            date = return_nextday(call_ymd())
        meal = return_menu(slot,date)
        # meal.insert(0,pretty_date()+threeMeal[slot-1])
             
        meal = '\n'.join(meal)
        
        self.label_title = QtWidgets.QLabel(pretty_date()+threeMeal[slot-1])
        self.label_title.setStyleSheet("color: black;"
                                      "background-color: white;"
                                      "font-weight:600;"
                                      "border-radius: 3px")
        self.label_title.setFont(QtGui.QFont("Nanumbarungothic", 13))
        self.label_menu = QtWidgets.QLabel(meal)
        self.label_menu.setStyleSheet("color: black;"
                                      "background-color: white;"
                                      #  "border-style: solid;"
                                      #  "border-width: 2px;"
                                      #  "border-color: white;"

                                      "border-radius: 3px")
        self.label_menu.setFont(QtGui.QFont("Nanumbarungothic", 13))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.label_title)
        vbox.addWidget(self.label_menu)
        vbox.addWidget(label)
        centralWidget.setLayout(vbox)
        self.label_title.hide()
        self.label_menu.hide()

    def mouseDoubleClickEvent(self, e):
        # QtWidgets.qApp.quit()
        self.label_title.show()
        self.label_menu.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    s = Sticker('bird.gif', xy=[433, 800], size=1, on_top=True)
    # s.walk_diff([0,0],[1000,0],1000)
    # s1 = Sticker('gif/amongus/red_vent.gif', xy=[780, 1020], size=0.3, on_top=True)

    # s2 = Sticker('gif/amongus/orange.gif', xy=[1200, 1020], size=0.3, on_top=True)

    # s3 = Sticker('gif/amongus/blue_green.gif', xy=[400, 920], size=1.0, on_top=True)

    # s4 = Sticker('gif/amongus/mint.gif', xy=[1000, 950], size=0.2, on_top=True)
    # s4.walk_diff(from_xy_diff=[-100, 0], to_xy_diff=[100, 0], speed=120)

    # s5 = Sticker('gif/amongus/brown.gif', xy=[200, 1010], size=0.75, on_top=True)

    # s6 = Sticker('gif/amongus/yellow.gif', xy=[1850, 800], size=0.75, on_top=True)
    # # s6.walk(from_xy=[0, 800], to_xy=[1850, 800], speed=240)

    # s7 = Sticker('gif/amongus/magenta.gif', xy=[1500, 900], size=0.5, on_top=True)
    # s.walk_diff(from_xy_diff=[-100, 0], to_xy_diff=[100, 0], speed=180)

    sys.exit(app.exec_())
