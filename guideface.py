

from uicode.guide import Ui_Dialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GuideFace(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(GuideFace, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        self.setWindowTitle("Multi-MODS向导")
        self.ui.logo.setIcon(QIcon("variable/icons/logo_rbg.png"))
        self.ui.logo.setIconSize(QSize(160,80))
        self.resize(int(self.parent().width()*0.55),int(self.parent().height()*0.5))
        self.ui.guide_image.setStyleSheet("#guide_image{border-image:url(variable/icons/guide_image.png)}")
        self.ui.create_project.setIcon(QIcon("variable/icons/new_project.png"))
        self.ui.create_project.clicked.connect(self.parent().createProject)
        self.ui.open_project.setIcon(QIcon("variable/icons/import.png"))
        self.ui.open_project.clicked.connect(self.parent().openProject)
        self.ui.import_image.setIcon(QIcon("variable/type_icon/png.png"))
        self.ui.import_image.clicked.connect(lambda: self.parent().inputFiles(typ="image"))
        self.ui.import_video.setIcon(QIcon("variable/type_icon/mp4.png"))
        self.ui.import_video.clicked.connect(lambda: self.parent().inputFiles(typ="video"))
        # 双击打开项目
        self.ui.recently.doubleClicked.connect(lambda: self.parent().openProject(path=self.ui.recently.currentItem().text()\
                                                                                 ,index=self.ui.recently.currentRow()))

        # self.ui.recently.addItems(["暂无项目"])