
from uicode.setting import Ui_Dialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import torch

class SettingFace(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(SettingFace, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.runfor_icon.setIcon(QIcon("./variable/icons/run.png"))
        self.ui.env_icon.setIcon(QIcon("./variable/icons/env.png"))
        # self.setWindowIcon(QIcon("variable/icons/logo.png"))
        self.resize(int(self.parent().width()*0.75),int(self.parent().height()*0.75))
        self.setWindowTitle("全局设置")
        self.ui.save_configs.setShortcut("Ctrl+S")
        self.ui.save_configs_.setShortcut("Ctrl+S")

        #查看本设备是否支持CUDA加速
        is_support = torch.cuda.is_available()
        self.ui.gpu_support.setEnabled(is_support)
        supports = {
            "True":"支持CUDA加速",
            "False":"未支持CUDA加速"
        }
        self.ui.if_support_gpu.setText(f"使用GPU辅助能更快地得到结果({supports[str(is_support)]})")



    def closeEvent(self, event):
        # 窗口或控件失去焦点时执行的操作
        self.parent().setting.setChecked(False)
