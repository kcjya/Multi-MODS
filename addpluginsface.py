import json
import os.path
import shutil

from uicode.addplugins import Ui_Dialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Addplugins(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Addplugins, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.icon.setIcon(QIcon("./variable/icons/logo_rbg.png"))
        self.resize(int(self.parent().width()*0.75),int(self.parent().height()*0.75))

        #逻辑
        self.ui.cancel.clicked.connect(self.close)
        self.ui.save.clicked.connect(self.savePluginDir)
        #打开
        self.ui.open_icon_path.clicked.connect(self.openIconPath)
        self.ui.open_exe_path.clicked.connect(self.openExePath)


    def openExePath(self):
        path, filetype = QFileDialog.getOpenFileName(self, "选择可执行文件", "", "*.exe")
        if len(path) <= 0:
            return
        self.ui.exe_path.setText(path)


    def openIconPath(self):
        path, filetype = QFileDialog.getOpenFileName(self, "选择图标", "", "*.png;*.jpg")
        if len(path) <= 0:
            return
        self.ui.icon_path.setText(path)
        self.ui.icon.setIcon(QIcon(path))

    def savePluginDir(self):
        isOk = 1
        if self.ui.name.text() in [""," "]:
            QMessageBox.warning(self.parent(),"插件内容不完整","请填写插件的名称.",QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
            isOk = 0
        if not os.path.isfile(self.ui.icon_path.text()):
            QMessageBox.warning(self.parent(),"插件图标","插件图标已经损坏,请确保其可行行.",QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
            isOk = 0
        if not os.path.isfile(self.ui.exe_path.text())\
                or self.endwithp(self.ui.exe_path.text())!="exe":
            QMessageBox.warning(self.parent(),"插件","插件已经损坏，请检查*.exe文件.",QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
            isOk = 0
        if isOk:
            plugin_name = self.ui.name.text()
            plugin_icon = self.ui.icon_path.text()
            plugin_exe = self.ui.exe_path.text()
            #创建插件的文件夹
            plugin_dir = f"./variable/plugins/{plugin_name}"
            if not os.path.exists(plugin_dir):
                os.mkdir(plugin_dir)
            else:
                QMessageBox.information(self.parent(),"插件","插件已经存在,是否继续完成操作？")
                return

            #复制到插件的文件夹
            shutil.copyfile(plugin_icon, f"{plugin_dir}/{self.end(plugin_icon)}")
            shutil.copyfile(plugin_exe, f"{plugin_dir}/{self.end(plugin_exe)}")
            QMessageBox.information(self.parent(), "插件", "插件已经添加!")
            #添加到menuTool actions
            plugin_add_action = QAction(self.parent())
            plugin_add_action.setText(plugin_name)
            plugin_add_action.setIcon(QIcon(f"{plugin_dir}/{self.end(plugin_icon)}"))
            self.parent().ui.menu_Tools.insertAction(self.parent().ui.menu_Tools.actions()[-2],plugin_add_action)

            self.ui.icon_path.clear()
            self.ui.exe_path.clear()
            self.ui.name.clear()

            self.close()

            with open(f"./variable/configs/plugins.json", "r", encoding="utf-8") as fp:
                self.plugins = json.load(fp)

            plugin_dict = {
                "name": plugin_name,
                "icon": plugin_icon,
                "path": plugin_exe
            }
            self.plugins.append(plugin_dict)
            with open(f"./variable/configs/plugins.json", "w", encoding="utf-8") as fp:
                write_data = json.dumps(self.plugins, indent=0, ensure_ascii=False)
                fp.write(write_data)


    def end(self, str):
        name = str.split("/")[-1]
        return name

    def endwithp(self, str):
        return str.split(".")[-1]