
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Tree(QTreeWidget):
    def __init__(self, parent=None):
        super(Tree, self).__init__(parent)
        self.parent = parent
        self.setStyleSheet("QTreeWidget{border:none;}")
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        project_name = self.parent.configs["PROJECT_NAME"]
        datas = str(event.mimeData().text()).replace("file:///", "").split("\n")
        for file in datas:
            fname = file.split("/")[-1]
            typ = file.split(".")[-1]
            images = self.parent.project[project_name]["images"]
            videos = self.parent.project[project_name]["videos"]
            if ({fname: file} in images) or ({fname: file} in videos):
                continue
            if typ in ["png", "jpg", "jpeg", "bmp"]:
                self.parent.project[project_name]["images"].append({fname: file})
                _ = QTreeWidgetItem(self.parent.images_folder, [fname])
                _.setIcon(0, QIcon(f"./variable/type_icon/{typ}.png"))
                _.setToolTip(0, file)
            elif typ in ["mp4", "avi"]:
                self.parent.project[project_name]["videos"].append({fname: file})
                _ = QTreeWidgetItem(self.parent.videos_folder, [fname])
                _.setIcon(0, QIcon(f"./variable/type_icon/{typ}.png"))
                _.setToolTip(0, file)
