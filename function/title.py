
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Titlebar(QWidget):
    def __init__(self, parent=None):
        super(Titlebar, self).__init__(parent)
        self.parent = parent
        self.setFixedHeight(45)

        self.showmaxed = False

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.icon = QPushButton(self)
        self.icon.setStyleSheet(self.qss("icon"))
        self.icon.setFixedSize(45, 45)

        # self.title = QLabel(parent=self, text="Muti-MODS beta 2.23.2")
        self.title = QLabel(parent=self, text="基于机器视觉的多模型对象检测系统(Muti-MODS V1.0.1)")
        self.title.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.title.setFont(QFont("微软雅黑", 9))
        self.title.setStyleSheet("color:#FFFFFF;with:400px;")

        self.btn_close = QPushButton(self)
        self.btn_close.setIcon(QIcon("./variable/icons/closew.png"))
        self.btn_close.setStyleSheet(self.qss("title_close"))
        self.btn_close.setFixedSize(45, 45)
        self.btn_min = QPushButton(self)
        self.btn_min.setIcon(QIcon("./variable/icons/minw.png"))
        self.btn_min.setStyleSheet(self.qss("title_other"))
        self.btn_min.setFixedSize(48, 45)

        self.btn_max = QPushButton(self)
        self.btn_max.setIcon(QIcon("./variable/icons/maxw.png"))
        self.btn_max.setStyleSheet(self.qss("title_other"))
        self.btn_max.setFixedSize(48, 45)

        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_max.clicked.connect(self.btn_max_clicked)

        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def qss(self, qss_name, typ="style"):
        with open(f"./variable/{typ}/{qss_name}.qss", "r", encoding="utf-8") as fp:
            return fp.read()

    def resizeEvent(self, QResizeEvent):
        super(Titlebar, self).resizeEvent(QResizeEvent)
        self.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing and not self.showmaxed:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())

            self.start = self.end

    def mouseDoubleClickEvent(self, QMouseEvent):
        if self.showmaxed:
            self.parent.showNormal()
            self.showmaxed = False
            self.btn_max.setIcon(QIcon("variable/icons/maxw.png"))
        else:
            self.showmaxed = True
            self.parent.showMaximized()
            self.btn_max.setIcon(QIcon("variable/icons/resetw.png"))

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        if not self.showmaxed:
            self.showmaxed = True
            self.parent.showMaximized()
            self.btn_max.setIcon(QIcon("variable/icons/resetw.png"))
        else:
            self.showmaxed = False
            self.parent.showNormal()
            self.btn_max.setIcon(QIcon("variable/icons/maxw.png"))

    def btn_min_clicked(self):
        self.parent.showMinimized()

