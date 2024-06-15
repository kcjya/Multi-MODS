import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建视频播放器和视频视口
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)

        # 设置视频视口为中心部件
        self.setCentralWidget(self.video_widget)

        # 创建按钮和布局
        self.button = QPushButton('Play', self)
        self.button.clicked.connect(self.handle_button)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.sliderMoved.connect(self.set_position)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.slider)

        # 创建一个QWidget作为中心部件的容器
        container = QWidget(self)
        container.setLayout(layout)

        # 将容器放置在视频视口下方
        self.setCentralWidget(container)

        # 设置视频播放器的输出到视频视口
        self.media_player.setVideoOutput(self.video_widget)

        # 加载视频文件
        video_url = QUrl.fromLocalFile('C:\AllFile\Project\Pyqt\plant\samples\Camera_xhs_1692028278315.mp4')
        self.media_player.setMedia(QMediaContent(video_url))

    def handle_button(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.button.setText('Play')
        else:
            self.media_player.play()
            self.button.setText('Pause')

    def set_position(self, position):
        self.media_player.setPosition(position)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
