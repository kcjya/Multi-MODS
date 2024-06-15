
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from function.viewer import Imager
import pyqtgraph as pg


class mediaView(QWidget):
    # 初始化信号
    stateChange = pyqtSignal(str)
    posChange = pyqtSignal(QPoint)

    def __init__(self, parent=None):
        super(mediaView, self).__init__(parent)

        layout = QVBoxLayout(self)
        self.setMouseTracking(True)
        self.current = ""
        self.imager = Imager(self)
        self.imager.setStyleSheet("background-color:rgb(0,0,0);")

        self.video_view = QVideoWidget(self)
        self.video_view.addActions([QAction("sss"), QAction("idhd")])
        self.video_player = QMediaPlayer(self)
        self.video_player.setVideoOutput(self.video_view)

        self.imager.hide()
        self.video_view.hide()

        # 训练可视化
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.hide()
        self.plot_widget.showGrid(x=False, y=False)  # 显示网格
        # 修改坐标轴字体
        self.plot_widget.getAxis("bottom").setFont(QFont("微软雅黑", 8))
        self.plot_widget.getAxis("left").setVisible(False)
        # 禁用缩放，只允许左右移动
        self.plot_widget.setMouseEnabled(x=True, y=False)
        # 添加LabelItem来显示当前值
        self.current_value = pg.LabelItem(justify='right')
        self.plot_widget.scene().addItem(self.current_value)
        # 捕获鼠标移动事件
        self.plot_widget.plotItem.vb.scene().sigMouseMoved.connect(self.update_current_value)

        self.curves = []
        self.colors = ['w', 'g', 'r', 'y']
        self.num_curves = 4
        names = ["GPU内存", "box loss", "cls loss", "dfl loss"]
        self.legend = self.plot_widget.addLegend()
        for i in range(self.num_curves):
            curve = pg.PlotCurveItem(pen=self.colors[i % len(self.colors)])
            self.plot_widget.addItem(curve)
            self.curves.append(curve)
            self.legend.addItem(self.curves[i], names[i])

        # 控制部分
        player_process = QHBoxLayout(self)
        self.player_slider = QSlider(self)
        self.player_slider.sliderMoved.connect(self.setVideoPos)
        self.player_slider.setOrientation(1)
        self.player_slider.setStyleSheet(self.qss("qslider"))
        self.next_time = QPushButton(self)
        self.next_time.setFixedSize(QSize(25, 25))
        self.next_time.setIcon(QIcon("./variable/icons/last.png"))
        self.next_time.clicked.connect(lambda: self.video_player.setPosition(self.video_player.position() - 5000))
        self._pause_ = QPushButton(self)
        self._pause_.setFixedSize(QSize(25, 25))
        self._pause_.setIcon(QIcon("./variable/icons/play.png"))
        self._pause_.clicked.connect(lambda: self.video_player.pause())
        self.last_time = QPushButton(self)
        self.last_time.setFixedSize(QSize(25, 25))
        self.last_time.setIcon(QIcon("./variable/icons/next.png"))
        self.last_time.clicked.connect(lambda: self.video_player.setPosition(self.video_player.position() + 5000))
        player_process.addWidget(self.player_slider)
        player_process.addWidget(self.next_time)
        player_process.addWidget(self._pause_)
        player_process.addWidget(self.last_time)
        player_process.setContentsMargins(0, 0, 0, 0)
        self.process_frame = QFrame(self)
        self.process_frame.hide()
        self.process_frame.setFixedHeight(25)
        self.process_frame.setLayout(player_process)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.imager)
        layout.addWidget(self.video_view)
        layout.addWidget(self.plot_widget)
        layout.setMenuBar(self.process_frame)
        self.setLayout(layout)

    def qss(self, qss_name, typ="style"):
        with open(f"./variable/{typ}/{qss_name}.qss", "r", encoding="utf-8") as fp:
            return fp.read()


    # 更新LabelItem的文本
    def update_current_value(self, pos):
        mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
        self.current_value.setText(f"x={mouse_point.x():.2f}, y={mouse_point.y():.2f}")

    def mouseMoveEvent(self, event):
        self.posChange.emit(event.pos())



    def showImage(self, path):
        """
        显示图片到center view
        2023-7-24 无修改
        :param path:
        :return:
        """
        if path == "": return
        pixmap = None
        try:
            pixmap = QPixmap(path)
            self.current = path
        except Exception as e:
            # 这里比较方便的是，可能传进来的是图片数组
            pixmap = path
        self.imager.setImage(pixmap)

        self.imager.show()
        self.video_view.hide()
        self.plot_widget.setVisible(False)
        self.process_frame.hide()

    def setVideoPos(self, curtv):
        self.video_player.setPosition(curtv)

    def showVideo(self, path):
        """
        显示视频到center view
        2023-7-24 无修改
        :param data:
        :return:
        """
        # self.player.setNotifyInterval(1000)  # 信息更新周期, ms
        self.process_frame.show()
        content = QMediaContent(QUrl.fromLocalFile(path))
        self.video_player.setMedia(content)
        self.video_player.setNotifyInterval(1000)  # 信息更新周期
        self.video_player.play()

        self.total_duration = 0
        self.video_info = ""
        self.video_player.positionChanged.connect(self.positionChanged)
        self.video_player.durationChanged.connect(self.durationChanged)
        self.imager.hide()
        self.video_view.show()
        self.plot_widget.setVisible(False)

    def plotTrainDatas(self, x, y):
        for i in range(self.num_curves):
            self.curves[i].setData(x, y[i])
        self.plot_widget.autoRange()
        self.plot_widget.setVisible(True)
        self.imager.hide()
        self.video_view.hide()

    def play(self):
        self.video_player.play()

    def stop(self):
        self.video_player.stop()

    def pause(self):
        self.video_player.pause()

    def durationChanged(self, duration):
        secs = duration / 1000
        mins = secs / 60
        secs = secs % 60
        self.total_duration = f"{int(mins)}:{int(secs)}"
        self.player_slider.setRange(0, duration)

    def positionChanged(self, position):
        secs = position / 1000
        mins = secs / 60
        secs = secs % 60
        self.video_info = f"播放时长:{int(mins)}:{int(secs)}/{self.total_duration}"
        self.stateChange.emit(self.video_info)
        # 设置设置
        self.player_slider.setValue(position)

