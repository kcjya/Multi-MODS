from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from uicode import new
import os

class Project(QDialog, new.Ui_Dialog):
    def __init__(self, parent=None):
        super(Project, self).__init__(parent)
        self.ui = new.Ui_Dialog()
        self.ui.setupUi(self)
        self.resize(850, 500)
        self.setWindowTitle("项目-创建一个项目")
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.ui.project_brief.setFont(QFont("微软雅黑",10))

        self.path = ""
        self.ui.tip.hide()
        self.timer = QTimer(self)
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.SHOW)
        self.project = dict()
        self.project["CREATED"] = False
        self.ui.cancel.clicked.connect(self.close)
        self.ui.create.clicked.connect(self.createProject)
        self.ui.select_project_path.clicked.connect(self.selectPath)

        self.exec()

    def showMsg(self, content, tim=2000):
        self.timer.setInterval(tim)
        self.ui.tip.show()
        self.ui.tip.setText(content)
        self.timer.start()

    def SHOW(self):
        self.ui.tip.hide()
        self.timer.stop()

    def createProject(self):
        name = self.ui.project_name.text()
        self.project["brief"] = self.ui.project_brief.toPlainText()
        if len(name) > 0:
            self.project["name"] = self.ui.project_name.text()
        else:
            self.showMsg("请重新输入合适的项目名称")
            return
        path = self.ui.project_path.text()
        if os.path.isdir(self.path):
            self.project["path"] = f"{self.path}/{name}"
            self.project["CREATED"] = True
            self.close()
        else:
            self.showMsg("请选择正确的路径.")

    def selectPath(self):
        name = self.ui.project_name.text()
        if len(name) <= 0:
            self.showMsg("请重新输入合适的项目名称")
            return
        self.path = QFileDialog.getExistingDirectory(self, "选择项目路径", "YPB")
        if len(self.path) == 0:
            return
        path = f"{self.path}/{name}/{name}.json"
        self.ui.project_path.setText(path)
