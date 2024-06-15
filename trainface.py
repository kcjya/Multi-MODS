from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from uicode import train
import sys

class Trainer(QMainWindow, train.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Trainer, self).__init__(parent)
        self.ui = train.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("MODS训练器")
        self.resize(int(self.parent().width()*0.75),int(self.parent().height()*0.75))
        self.ui.train_manager.setMinimumWidth(320)
        self.ui.train_terminal.setMinimumHeight(200)


if __name__ == '__main__':
    # QGuiApplication.setAttribute(Qt.HighDpiS
    # caleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    main = Trainer()
    sys.exit(app.exec_())