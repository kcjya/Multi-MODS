
from uicode.start import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json


class Start(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Start, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        with open("./variable/configs/config.json", "r", encoding="utf-8") as fp:
            settings = json.load(fp)
            if not settings["STARTFACE"]:
                self.close()

        self.resize(1000, 600)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)  # 去边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        self.ui.label.setText("Muti-MODS")
        # points
        self.points=""
        # user configs
        self.index = 0
        self.configs_str = [
            "加载 用户配置成功.\n",
            "加载 软件界面成功.\n",
            "初始化YOLOv8引擎.\n",
            "初始化训练环境.\n",
            "初始化电脑设备.\n"
            "正在启动.\n"
        ]

        # timer
        self.timer = QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.updateInfo)
        self.timer.start()

        # 加载图片
        self.ui.start_image.setPixmap(QPixmap("./variable/icons/start_image.png"))
        self.ui.logo.setPixmap(QPixmap("./variable/icons/logo.png"))
        self.ui.start_image.setScaledContents(True)
        self.ui.logo.setScaledContents(True)
        # 窗口圆角
        self.roundedRect(16)
        self.show()


    def updateInfo(self):
        self.points += "."
        self.ui.running.setText(f"加载中{self.points}")
        if len(self.points)>2:
            self.points=""
        if self.index<self.configs_str.__len__():
            self.ui.info.setText(self.configs_str[self.index])
        self.index += 1
        if self.index>12:
            self.timer.stop()
            self.close()
    def roundedRect(self, size):
        bitmap = QBitmap(self.ui.widget.size())
        bitmap.fill()
        painter = QPainter(bitmap)
        painter.begin(self.ui.widget)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRoundedRect(bitmap.rect(), size, size)
        painter.end()
        self.ui.widget.setMask(bitmap)
