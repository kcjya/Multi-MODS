import sys
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from function.predict import (Predict, measureObject, closePredict)
from function.tcp import TCP_Server,TCP_Cilent
from function.project import Project
from function.textedit import Editor
from function.media import mediaView
from function.title import Titlebar
from function.tree import Tree
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from pygrabber.dshow_graph import *
from email.header import Header
from multiprocessing import *
from uicode.ui import Ui_MainWindow
from function.labeling_main import lab_main
from function.viewer import Imager
from function.callback import *
from faces.settingface import SettingFace
from faces.guideface import GuideFace
from faces.addpluginsface import Addplugins
from faces.startface import Start
from faces.trainface import Trainer
from function.train import train
import multiprocessing
import pyqtgraph as pg
import numpy as np
import subprocess
import datetime
import smtplib
import shutil
import socket
import json
import cv2




class Windows(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Windows, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.desktop = QApplication.desktop()
        self.resize(int(self.desktop.width()*0.8),int(self.desktop.height()*0.8))
        self.pathesInit()
        # 窗口初始化，闭合dock栏之类的窗口
        self.globalValuesInit()
        self.windowsInit()
        # 初始化WiFi个功能
        self.wifiInit()
        # 定时器初始化
        self.timersInit()
        # 软件运行之前必须初始化各个变量
        self.poptipInit()
        self.valuesInit()
        self.actionsInit()
        self.softInit()
        # 表格初始化主要用来显示预测的结果等
        self.tableWidgetInit()
        # 软件的工具栏初始化
        self.menusInit()
        self.mtoolsInit()
        self.toolbarInit()
        self.etoolsInit()
        self.pluginsInit()

        self.buttonsInit()
        self.treeWidgetInit()
        self.setObjectState("STA")
        self.show()

        if self.configs["GUIDE"]:
            self.guide_face.exec()


    def menusInit(self):
        # 文件菜单-File
        self.ui.action_new.triggered.connect(self.createProject)
        self.ui.action_new.setShortcut("Ctrl+N")
        self.ui.action_open.triggered.connect(self.openProject)
        self.ui.action_open.setShortcut("Ctrl+O")
        self.ui.action_save.triggered.connect(self.saveDatas)
        self.ui.action_save.setShortcut("Ctrl+S")
        self.ui.action_saveas.triggered.connect(self.saveProjectAs)
        self.ui.action_saveas.setShortcut("Ctrl+A")
        self.ui.action_close_project.triggered.connect(self.closeCurtProject)
        # 打开项目路径
        self.ui.action_open_project_path.triggered.connect(self.openProjectPath)
        # 打印窗口
        self.ui.action_print_menus.triggered.connect(self.printScreen)
        self.ui.action_save_image.triggered.connect(
            lambda: QMessageBox.information(self, "提示", "请使用打印功能!", QMessageBox.Yes | QMessageBox.No))
        self.ui.action_settings.triggered.connect(lambda: self.showSettingWindow(True))
        self.ui.action_power_save.triggered.connect(self.autoSaveMode)
        self.ui.action_close.triggered.connect(self.close)
        self.ui.action_quit.triggered.connect(self.close)
        # 重启
        self.ui.action_rerun.triggered.connect(self.restart)

        # 打开模型设置界面
        self.ui.action_train_model.triggered.connect(lambda: self.ui.prerdict_or_train.setCurrentIndex(1))
        self.ui.action_import_model.triggered.connect(self.importModels)
        model_path = self.cwd.replace("/", "\\") + "\\variable\\models"
        self.ui.action_open_model_path.triggered.connect(lambda: os.system(f"explorer {model_path}"))
        # 模型详解
        self.ui.action_about_model.triggered.connect(self.showModelDetails)
        # 打开设置
        self.ui.action_setting.triggered.connect(lambda: self.showSettingWindow(True))

    def showModelDetails(self):
        model_details = QDialog(self)
        model_details.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        model_details.resize(1000, 600)
        model_details.setWindowTitle("关于模型解释")

        details = QTextBrowser(self)
        # details = QWebEngineView(self)
        # details.load(QUrl("https://github.com/ultralytics/ultralytics/blob/main/README.zh-CN.md"))
        with open("./variable/details/about_model.html", "r", encoding="utf-8") as fp:
            details.setHtml(fp.read())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(details)
        model_details.setLayout(layout)

        model_details.exec_()

    def importModels(self):
        path, filetype = QFileDialog.getOpenFileNames(self, "选择模型权重", "", "*.pt;*.onnx")
        if len(path) <= 0:
            return
        for dst in path:
            try:
                model_name = dst.split("/")[-1]
                shutil.copy(dst, f"./variable/models/{model_name}")
            except Exception as e:
                self.globalLog(f"导入模型出错:{e}", "error")

    def autoSaveMode(self, checked):
        if checked:
            pass
        else:
            pass

    def openProjectPath(self):
        path = self.configs["PROJECT_PATH"].replace("/", "\\")
        os.system(f'explorer {path}')

    def printScreen(self, action):
        all = False
        if action is self.ui.action_print_viewport:
            all = True
        path = QFileDialog.getSaveFileName(self, "选择保存路径", f"viewport" if not all else "surface", "*.png")
        if len(path[0]) > 0:
            screenshot = QApplication.primaryScreen().grabWindow(self.viewport.winId() if not all else self.winId())
            outputRegion = screenshot.copy(self.viewport.rect() if not all else self.rect())
            outputRegion.save(path[0], format='PNG', quality=100)

    def closeCurtProject(self):
        self.tree.takeTopLevelItem(1)

    def poptipInit(self):
        self.poptip = QWidget(None)
        layout = QHBoxLayout(self.poptip)
        self.popup = QLabel(self.poptip)
        self.popup.setStyleSheet("color:#FFFAFA;font: 9pt '微软雅黑';")
        self.poptip_icon = QPushButton(self.poptip)
        self.poptip_icon.setIcon(QIcon("variable/icons/pop_warning.png"))
        self.poptip_icon.setFixedSize(QSize(40, 40))
        self.poptip_icon.setStyleSheet("border:none;")
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.poptip_icon)
        layout.addWidget(self.popup)

        self.poptip.resize(200, 40)
        self.poptip.setStyleSheet("background-color:#FF0000;border-radius:5px;")
        self.poptip.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def poptipAnimate(self, conten="None errors", typ="normal"):
        self.poptip.setStyleSheet("background-color:#FF0000;border-radius:5px;")
        if typ == "normal":
            self.poptip.setStyleSheet("background-color:#24b021;border-radius:5px;")
            self.poptip_icon.setIcon(QIcon("./variable/icons/normal.png"))
        else:
            self.warning_timer.start()
        self.popup.setText(conten)
        self.tip_timer.start()
        self.poptip.show()
        start_x = self.pos().x() + self.width() - self.poptip.width() - 15
        start_y = self.pos().y() + self.height() - self.poptip.height()
        self.poptip_animate = QPropertyAnimation(self.poptip, b'geometry')
        self.poptip_animate.setDuration(200)  # 设定动画时间
        self.poptip_animate.setStartValue(QRect(start_x, start_y, 200, 40))  # 设置起始大小
        self.poptip_animate.setEndValue(QRect(start_x, start_y - 50, 200, 40))  # 设置终止大小
        self.poptip_animate.start()  # 动画开始

    def tipState(self):
        self.anim = QPropertyAnimation(self.poptip, b"windowOpacity")
        self.anim.setDuration(350)
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)
        self.anim.start()
        self.tip_timer.stop()
        self.anim.finished.connect(self.opacityFinished)

    def opacityFinished(self):
        # 恢复透明
        self.poptip.close()
        self.anim_ = QPropertyAnimation(self.poptip, b"windowOpacity")
        self.anim_.setDuration(1)
        self.anim_.setStartValue(0)
        self.anim_.setEndValue(1)
        self.anim_.start()

    def globalLog(self, content, typ="success"):
        try:
            if self.configs["SOFTLOG"]:
                local = self.setting_face.ui.save_log_local.isChecked()
                self.log("管理员", content=content, typ=typ, local=local)
        except Exception as e:
            # print(e)
            pass

    def saveMailConfigs(self):
        mail = {}
        mail["host"] = self.ui.mail_server_type.text()
        mail["user"] = self.ui.mail_sender.text()
        mail["code"] = self.ui.mail_server_code.text()
        mail["recvs"] = self.ui.mail_receiver.text()
        with open("./variable/configs/mail.json", "w", encoding="utf-8") as fp:
            mail_ = json.dumps(mail, indent=0, ensure_ascii=False)
            fp.write(mail_)
        self.globalLog("保存邮件服务器设置成功!")

    def mailInit(self):
        with open("./variable/configs/mail.json", "r", encoding="utf-8") as fp:
            mail = json.load(fp)
            self.ui.mail_server_type.setText(mail["host"])
            self.ui.mail_sender.setText(mail["user"])
            self.ui.mail_server_code.setText(mail["code"])
            self.ui.mail_receiver.setText(mail["recvs"])
        self.globalLog("邮件模块加载成功!")

    def mailSendWithImage(self, subject, content_txt, path=""):
        msg_from = self.ui.mail_sender.text()
        # print(msg_from)
        passwd = self.ui.mail_server_code.text()
        # passwd = 'dzjpdcciayjdbbda'  # 填入发送方邮箱的授权码
        msg_to = self.ui.mail_receiver.text()
        # print(msg_to)
        msg = MIMEMultipart('related')
        content = MIMEText(f'<html><body><p>{content_txt}</p><img src="cid:imageid" alt="imageid"></body></html>',
                           'html', 'utf-8')  # 正文
        # msg = MIMEText(content)
        msg.attach(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to

        with open(path, "rb") as fp:
            img_data = fp.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', 'imageid')
            msg.attach(img)
            try:
                s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
                s.login(msg_from, passwd)
                s.sendmail(msg_from, msg_to, msg.as_string())
                self.globalLog(f"已检测到目标，正在发送到客户邮箱.")
            except Exception as e:
                self.globalLog(f"发送失败:{e}", typ="error")
                # print("发送失败:", e)

    def mailSend(self, name, subject, content, im=""):
        host = self.ui.mail_server_type.text()
        user = self.ui.mail_sender.text()
        code = self.ui.mail_server_code.text()
        recvs = self.ui.mail_receiver.text()
        receivers = None
        sender = user
        if self.ui.self_send_content.isEnabled():
            name = self.ui.self_send_content.text()
        try:
            receivers = recvs.split(",")
        except Exception as e:
            self.globalLog(f"邮件发送失败 error:'{e}'!", typ="error")
            self.poptipAnimate("Error in mail", "error")
            return
        message = MIMEText(content, "plain", "utf-8")
        message["From"] = f"{name} <{user}>"
        message["To"] = f"{name} <{user}>"
        message["Subject"] = Header(subject, "utf-8")

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(host, 25)
            smtpObj.login(user, code)
            smtpObj.sendmail(sender, receivers, message.as_string())
            self.globalLog(f"邮件发送成功 主题:'{subject}'!")
        except smtplib.SMTPException as e:
            self.globalLog(f"邮件发送失败 error:'{e}'!", typ="error")
            self.poptipAnimate("Error in mail", "error")

    def titleColor(self, color):
        # self.title.lower()
        self.titleBar.setStyleSheet(f"background-color:%s;" % color)
        self.titleBar.icon.setStyleSheet(f"background-color:%s;border:none;" % color)
        self.setStyleSheet(
            "QMainWindow{border: 2px solid %s;font: 9pt '微软雅黑';}QWidget{color:#505050;font: 9pt '微软雅黑';}" % color)

    def pathesInit(self):
        # desktop = QApplication.desktop()
        # print(desktop.height())
        # self.resize(int(desktop.width()*0.7), int(desktop.height()*0.8))
        self.cwd = os.getcwd().replace('\\', '/')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(self.qss("default", "theme"))

        self.titleBar = Titlebar(self)
        self.titleColor("#7F00FF")  # 7F00FF|0080ff
        self.setWindowIcon(QIcon("./variable/icons/logo.jpg"))
        self.titleBar.icon.setIcon(QIcon("./variable/icons/logo.jpg"))
        #
        layout = QVBoxLayout(self)
        self.setContentsMargins(4, 45, 4, 0)
        layout.setSpacing(0)
        layout.addWidget(self.titleBar)
        layout.addStretch()
        self.setLayout(layout)
        self.titleBar.show()
        self.titleBar.setFixedWidth(self.width())

    def globalValuesInit(self):
        # 设置一个全局变量该变量，包括预测任务的变量都是用
        # 各进程之间的数据共享
        self.manager = Manager()
        self.Sources = self.manager.list()
        self.Globals = self.manager.dict()
        self.Results = self.manager.list()
        # 全局变量
        # 这个全局变量，再软件区安监局计算的时候直接迭代这两个变量
        # 摄像头信息
        self.Globals["CAMERASTREAM"] = None
        # 是否可以训练
        self.Globals["READYFORTRAIN"] = True
        # 加载模型是否成功
        self.Globals["LOADMODELFINISH"] = False
        self.Globals["VIEW_MODE"] = False
        self.Globals["PREDICT_INFO"] = []
        self.Globals["VIDEOMODE"] = False

        # 普通变量
        self.log_tyes = [0, 0, 0]
        self.globalLog(f"全局变量初始化成功!")
        self.tcp_conncted_socket = {}

        #全局tabs
        self.alltabs = []
        self.alltabs.append("媒体视口")


    def viewPart(self, action):
        windows = [self.ui.source_window, self.ui.result_window, self.ui.draw_window, self.ui.mtools,
                   self.ui.etools, self.ui.plugins, self.ui.predict_window]
        index = self.ui.view_menu.actions().index(action)
        if action.isChecked():
            windows[index].show()
        else:
            windows[index].close()

    def actionsInit(self):
        # 窗口显示与隐藏按钮初始化
        self.ui.view_menu.triggered.connect(self.viewPart)

        # 模型动作按钮初始化
        index = self.configs["CURRENTMODEL"]
        models = os.listdir(f"{self.cwd}/variable/models")
        self.ui.menu_models.triggered.connect(self.selectModel)
        for name in models:
            model_action = QAction(self)
            model_action.setText(name)
            model_action.setCheckable(True)
            self.ui.menu_models.addAction(model_action)

        self.current_model_action = self.ui.menu_models.actions()[index]
        self.current_model_action.setChecked(True)
        model_name = self.ui.menu_models.actions()[index].text()
        model_path = f"{self.cwd}/variable/models/{model_name}"
        # 启动进程预先加载模型
        if self.configs["PRELOAD"]:
            self.changeModel(model_path, index)
            self.globalLog(f"已开启启动预加载模型，正在加载模型:'{model_name}'")

    def selectModel(self, action):
        for _ in self.ui.menu_models.actions():
            _.setChecked(False)
        action.setChecked(True)
        self.current_model_action = action
        index = self.ui.menu_models.actions().index(action)
        model_name = action.text()
        model_path = f"{self.cwd}/variable/models/{model_name}"
        self.changeModel(model_path, index)
        self.globalLog(f"模型:'{model_name}'")

    def createDefaultFolder(self, name):
        """
        再软件初始化时，在只要创建项目就要调用该方法创建默认的文件夹
        2023-7-24 无修改
        :param name:
        :return:
        """
        self.configs["PROJECT_NAME"] = name
        self.devices_folder = QTreeWidgetItem(self.tree, ["设备组(#)"])
        self.devices_folder.setIcon(0, QIcon(f"{self.cwd}/variable/icons/device.png"))
        self.devices_folder.setFlags(self.devices_folder.flags() & ~Qt.ItemIsEditable)
        # 这里优先加载设备
        self.loadDevices(self.devices_folder)
        self.root_folder = QTreeWidgetItem(self.tree, [name])
        self.root_folder.setIcon(0, QIcon(f"{self.cwd}/variable/icons/workspace.png"))
        # 这是根目录也就是项目的名称
        # 然后每一次创建项目都需要创建五个子文件夹
        # 分别是设备、图片、视频、用户文件夹，他们都不支持修改是默认的阿文件夹
        self.images_folder = QTreeWidgetItem(self.root_folder, ["图像"])
        self.videos_folder = QTreeWidgetItem(self.root_folder, ["视频"])
        self.user_folder = QTreeWidgetItem(self.root_folder, ["用户"])
        # 展开self.root_folder
        self.tree.expandItem(self.root_folder)
        # 将这几个目录设置为不可以重命名
        for folder in [self.images_folder, self.videos_folder, self.user_folder]:
            folder.setFlags(folder.flags() & ~Qt.ItemIsEditable)
            folder.setIcon(0, QIcon(f"{self.cwd}/variable/type_icon/dir.png"))

    def createProject(self):
        """
        创建一个新项目
        2023-7-24 无修改
        :return:
        """
        # 创建一个新项目，使用ProjectDialog()方法，将会弹出创建项目的新窗口
        # 他继承于QDialog对话，当该窗口关闭时会有两种状态，get关键字CREATED
        # 查看项目的创建状态，要获取项目的相关信{"name","path","brief"}
        p = Project(self).project
        if not p.get("CREATED"):
            self.globalLog(f"已取消创建项目!", typ="warning")
            return
        # 如果创建项目成功-先删除上次的目录,创建空的目录
        for _ in range(self.tree.topLevelItemCount()):
            self.tree.takeTopLevelItem(0)
        # 创建项目是应该一起创建项目文件后缀名.ylbprj
        self.project = {
            f"{p.get('name')}": {
                "images": [],
                "videos": [],
                "brief": p.get('brief')
            }
        }
        # 更新设置值信息
        self.configs["PROJECT_PATH"] = p.get('path')
        self.configs["PROJECT_NAME"] = p.get('name')
        if not os.path.exists(p.get('path')):
            # 创建默认的文件夹
            self.createDefaultFolder(p.get("name"))
            try:
                os.makedirs(p.get('path'))
                with open(f"{p.get('path')}/{p.get('name')}.ylbpj", "w", encoding="utf-8") as fp:
                    data = json.dumps(self.project, indent=1, ensure_ascii=False)
                    fp.write(data)
                # 并创建一个beief文件
                readme = """this is brief document."""
                with open(f"{p.get('path')}/README.md", "w", encoding="utf-8") as fp:
                    fp.write(readme)
                self.globalLog(f"项目创建成功:'{p.get('name')}'")
                self.updateRecentProject()
            except Exception as e:
                QMessageBox.critical(self, '项目创建', f"{e}", QMessageBox.Close | QMessageBox.Cancel)
                self.globalLog(f"项目创建失败 error:'{e}'", typ="error")
                self.poptipAnimate("Error in project", "error")
                return
        else:
            # 项目已经存在直接打开项目
            reply = QMessageBox.warning(self, '项目创建', "项目已经存在，是否打开存在的项目?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            self.openProject(f"{p.get('path')}/{p.get('name')}.ylbpj")

    def tableWidgetInit(self):
        """
        表单初始化，上设置表单的样式等
        2023-7-24 无修改
        :return:
        """
        # 单机事件
        self.ui.result.doubleClicked.connect(self.tableDoubleClick)
        self.ui.result.clicked.connect(self.tableSingleClick)
        self.ui.result.entered.connect(self.tableHover)
        self.ui.result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.result.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.ui.result.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.result.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选择
        self.ui.result.resizeColumnsToContents()
        self.ui.result.resizeRowsToContents()
        self.ui.result.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.ui.result.setRowCount(0)
        self.ui.result.setColumnCount(2)
        self.ui.result.verticalHeader().hide()
        self.ui.result.setShowGrid(False)
        self.ui.result.setFocusPolicy(Qt.NoFocus)

    def tableHover(self):
        pass


    def tableSingleClick(self, item):
        row = self.ui.result.currentRow()
        ret = self.ui.result.item(row, 1).text()
        if "暂无描述." == ret:
            self.setObjectState("UN")
            return
        self.setObjectState("EN")


    def tableDoubleClick(self):
        """
        2023-7-24 无修改
        :return:
        """
        item = self.ui.result.currentItem()
        typ = item.toolTip().split(".")[-1]
        if typ in self.types["video"]:
            self.viewport.showVideo(item.toolTip())
            self.pause_play.setIcon(QIcon("variable/icons/pause.png"))
            self.pause_play.triggered.connect(self.videoPause)
            return
        self.viewport.showImage(item.toolTip())

    def wifiInit(self):
        """
        2023-7-24 无修改
        :return:
        """
        # self.wifi = pywifi.PyWiFi()
        pass

    def timersInit(self):
        """
        2023-7-24 无修改
        :return:
        """
        # 插件是否关闭检测
        self.labeling_run_timer = QTimer(self)
        self.labeling_run_timer.setInterval(500)
        self.labeling_run_timer.timeout.connect(self.updatalabelingState)

        self.capture_camera_timer = QTimer(self)
        self.capture_camera_timer.setInterval(50)
        self.capture_camera_timer.timeout.connect(self.capture)

        self.predict_timer = QTimer(self)
        self.predict_timer.setInterval(10)
        self.predict_timer.timeout.connect(self.predictState)

        self.train_timer = QTimer(self)
        self.train_timer.setInterval(200)
        self.train_timer.timeout.connect(self.trainState)

        self.load_timer = QTimer(self)
        self.load_timer.setInterval(800)
        self.load_timer.timeout.connect(self.loadState)

        # 提示框关闭定时器
        self.tip_timer = QTimer(self)
        self.tip_timer.setInterval(1500)
        self.tip_timer.timeout.connect(self.tipState)

        # 自动保存-5min
        self.autosave_timer = QTimer(self)
        self.autosave_timer.setInterval(300000)
        self.autosave_timer.timeout.connect(self.saveDatas)
        # 边框闪速警告
        self.warning_timer = QTimer(self)
        self.warning_timer.setInterval(1)
        self.warning_timer.timeout.connect(self.borderWarning)
        self.waring_count = 0

    def borderWarning(self):
        self.waring_count += 1
        if self.waring_count % 2 == 0:
            self.titleColor("#FF0000")
        elif self.waring_count >= 5:
            self.waring_count = 0
            self.warning_timer.stop()
            self.titleColor("#7F00FF")
        else:
            self.titleColor("#7F00FF")

    def softInit(self):
        """
        软件的初始化，一些必要的加载，如加载上几次的项目
        2023-7-24 无修改
        :return:
        """
        # 最近项目的加载
        self.ui.menu_recently.triggered.connect(self.openRecentProject)
        # self.showImage(f"{self.workspace}/{self.images[0].replace('None/','')}")
        # for item in self.configs["RECENT_PROJECT"]:
        #     action = QAction(item.get("NAME"),self)
        #     self.ui.menu_recently.addAction(action)
        self.updateRecentProject()
        # 加载对象检测的类型
        labels = ["尺寸测量", "封闭性检测"]
        icons = ["measure", "close_predict", "circle_predict", "auto_predict", "line_predict"]
        self.ui.objects.addItems(labels)
        self.ui.objects.itemClicked.connect(self.objectsClicked)
        self.ui.predict_settings.currentChanged.connect(self.predictStChange)
        for i in range(self.ui.objects.count()):
            self.ui.objects.item(i).setIcon(QIcon(f"./variable/icons/{icons[i]}.png"))
            # self.ui.predict_settings.setTabIcon(i, QIcon(f"./variable/icons/{icons[i]}.png"))
            self.ui.predict_settings.setTabText(i, f"{labels[i]}设置")
        # 摄像头list初始化
        self.ui.camera_preview.setStyleSheet("#camera_preview{border-image:url(img.png);}")
        # 初始化TCP连接主机的信息
        # 函数 gethostname() 返回当前正在执行 Python 的系统主机名
        self.ui.host_state.setIcon(QIcon("./variable/icons/no_running"))
        ip = socket.gethostbyname(socket.gethostname())
        self.ui.host_ip.setText(f"{ip}")
        self.ui.port.setText("8888")
        self.ui.start_host.clicked.connect(self.startTcpServer)
        self.ui.stop_host.clicked.connect(self.stopHost)
        self.ui.update_connect.clicked.connect(self.updateConnected)

        # 加载插件
        self.ui.menu_Tools.triggered.connect(self.runPlugin)
        self.loadPlugins()

    def updateConnected(self):
        QMessageBox.information(self, "刷新", f"刷新成功", QMessageBox.Yes | QMessageBox.No)

    def stopHost(self):
        try:
            self.tcp_server.terminate()
            self.ui.host_state.setIcon(QIcon("./variable/icons/no_running"))
            self.globalLog(f"TCP 服务器已暂停")
        except Exception as e:
            pass

    def startTcpServer(self):
        # 获取IP和端口
        self.tcp_ip = self.ui.host_ip.text()
        self.tcp_port = int(self.ui.port.text())
        # 获取连接的最大数量
        self.connect_max = int(self.ui.connect_max.text())
        #  创建socket
        try:
            self.tcp_server = TCP_Server(self.tcp_ip, self.tcp_port, self.connect_max)
            self.tcp_server.start()
            # 信号槽连接
            self.tcp_server.connected.connect(self.tcpConnected)
            self.tcp_server.recieved.connect(self.tcpRecieved)
            self.globalLog(f"TCP 服务器创建成功!等待设备连接..")
            self.ui.host_state.setIcon(QIcon("./variable/icons/running"))
        except Exception as e:
            self.globalLog(f"TCP error:{e}", typ="error")

    def tcpRecieved(self, content):
        format = f"<span><b>{content[0]}:{content[1]}</b></span><br>"
        self.ui.log.insertHtml(format)
        self.ui.log.moveCursor(QTextCursor.End)

    def tcpConnected(self, content):
        self.ui.connect_list.addItem(f"{content[1]}:{content[2]}")
        self.globalLog(f"{content[1]}:{content[2]} 已连接!")
        # 以IP命名已经连接的TCP SOCKET
        self.tcp_conncted_socket[content[1]] = content[0]

    def predictStChange(self, index):
        self.ui.objects.setCurrentRow(index)

    def objectsClicked(self, item):
        if self.ui.predict_settings.isHidden():
            self.ui.predict_settings.show()
        index = self.ui.objects.currentRow()
        self.ui.predict_settings.setCurrentIndex(index)
        labels = ["尺寸测量", "封闭性检测"]
        for i in range(self.ui.objects.count()):
            self.ui.objects.item(i).setText(labels[i])
        item.setText(f"{item.text()}")
        object_brief = [
            "用于检测一些轮廓比较简单的线性零件的尺寸。",
            "检测待检测物体的轮廓的封闭性，适用于一些扩阔较为清晰的线性物体、图案。",
            "检测待检测物体轮廓的圆度以及一些相关信息。",
            "主要是通过自定义模型训练，来实现缺陷的自定义",
            "适用于裂缝、开口一类的去欸按检测。"
        ]
        self.ui.object_brief.setText(object_brief[index])

    def openRecentProject(self, action):
        """
        打开最近的项目-暂停维护
        :param action:
        :return:
        """
        index = self.ui.menu_recently.actions().index(action)
        if os.path.exists(action.text()):
            self.openProject(action.text(), index)
        else:
            ret = QMessageBox.critical(self, "项目失效", "项目已经不存在,是否删除出？", QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.Yes:
                self.guide_face.ui.recently.takeItem(index)
                self.guide_face.ui.recently.update()
                self.ui.menu_recently.removeAction(action)
                self.configs["RECENT_PROJECT"].pop(index)
        # project_name = action.text()
        # for item in self.configs["RECENT_PROJECT"]:
        #     if item.get("NAME") == project_name:
        #         self.openProject(item.get(project_name))
        #         break

    def buttonsInit(self):
        """
        主要是按键的初始化
        2023-7-24 无修改
        :return:
        """
        # 训练按钮初始化
        self.ui.open_labeling.clicked.connect(self.runLabeling)
        self.ui.pre_check.clicked.connect(self.preTrainCheck)
        self.ui.input_images.clicked.connect(self.inputImages)
        self.ui.start_train.clicked.connect(self.startTrainWork)
        self.ui.terminate_train.clicked.connect(self.terminateTrainWork)
        # 重新选择当前对象
        self.ui.select_image.clicked.connect(self.selectImage)
        # 开始闭合检测
        self.ui.close_predict.clicked.connect(self.closePredict)
        # 发送邮箱测试
        # self.ui.send_mail_test.clicked.connect(lambda :self.mailSend("YOLOBOX","YOLOBOX 邮箱测试","测试成功!"))
        self.ui.send_mail_test.clicked.connect(
            lambda: self.mailSendWithImage("Multi-MODS", f"{datetime.datetime.now().strftime('%H:%M:%S')} 邮箱测试",
                                           r"variable/configs/mail_test.png"))
        self.ui.save_mail_setting.clicked.connect(self.saveMailConfigs)
        # 选择训练的权重文件和yaml文件
        self.ui.select_train_model_path.clicked.connect(self.selectTrainModel)
        self.ui.select_train_configs.clicked.connect(self.selectTrainConfigs)
        # 测量尺寸
        self.ui.measure_predict.clicked.connect(self.measurePredict)

        # 设置里面的btn
        self.setting_face.ui.select_workspace.clicked.connect(self.selectWorkspace)
        self.setting_face.ui.select_model_path.clicked.connect(self.selectModelpath)
        self.setting_face.ui.select_python.clicked.connect(self.selectPythonpath)
        # 保存设置
        self.setting_face.ui.save_configs.clicked.connect(lambda: self.saveConfigs(self.configs))
        self.setting_face.ui.save_configs_.clicked.connect(lambda: self.saveConfigs(self.configs))
        # DO 链接信号槽
        self.setting_face.ui.check_update.clicked.connect(self.checkUpdate)
        #QTabWidget双击事件
        self.ui.center.tabBar().tabBarDoubleClicked.connect(self.centerBarDoubleClick)

    def selectTrainConfigs(self):
        path, filetype = QFileDialog.getOpenFileName(self, "选择yaml文件", "", "*.yaml")
        if filetype != "*.yaml" and len(path) <= 0:
            return
        self.ui.train_configs.setText(path)
        self.globalLog(f"已选Yaml File:{path.split('/')[-1]}!")

    def selectTrainModel(self):
        path, filetype = QFileDialog.getOpenFileName(self, "选择权重文件", "", "*.pt;*.yaml")
        if filetype != "*.pt" and len(path) <= 0:
            return
        self.ui.train_model_path.setText(path)
        self.globalLog(f"已选Train Model:{path.split('/')[-1]}!")

    def selectWorkspace(self):
        path = QFileDialog.getExistingDirectory(self, "选择路径", "")
        if len(path) == 0:
            return
        self.ui.workspace_path.setText(path)
        self.globalLog(f"更新了工作路径")

    def selectModelpath(self):
        path = QFileDialog.getExistingDirectory(self, "选择模型文件夹", "")
        if len(path) == 0:
            return
        self.ui.model_path.setText(path)
        self.globalLog(f"更新了模型路径")

    def selectPythonpath(self):
        path, filetype = QFileDialog.getOpenFileName(self, "选择python解释器", "python", "*.exe")
        if filetype != "*.exe":
            return
        self.ui.python_path.setText(path)
        self.globalLog(f"更新了ptyhon解释器路径")

    def measurePredict(self):
        data = {}
        data["image"] = self.tree.currentItem().toolTip(0) \
            if not self.ui.pre_measure_image.text() else self.ui.pre_measure_image.text()
        data["linewidth"] = int(self.ui.measure_line_width.text())
        data["fontsize"] = int(self.ui.measure_plot_fontsize.text())
        data["rate"] = float(self.ui.measure_rate.text())
        ret = measureObject(data)

        self.viewport.showImage(f"./workspace/results/measure/{ret['name']}")

    def closePredict(self):
        line_width = int(self.ui.line_width.text()) if self.ui.line_width.text() else 1
        dats = {
            "IMAGE": self.tree.currentItem().toolTip(0) \
                if not self.ui.pre_close_image.text() else self.ui.pre_close_image.text(),
            "BITNOT": self.ui.bit_not.isChecked(),
            "LINEWIDTH": line_width,

        }
        ret = closePredict(dats=dats)
        name = self.ui.pre_close_image.text().split('/')[-1]
        self.viewport.showImage(f"./workspace/results/closed/{ret['name']}")
        # 绘制图像灰度直方图
        # self.plotRgbMap(f"./workspace/results/closed/{name}")
        self.log("封闭检测", f"{name}已完成检测.")

    def selectImage(self):
        path, filetype = QFileDialog.getOpenFileName(self, "选择保存路径", f"", "*.png;*.jpg;*.jpeg")
        if len(path) == 0:
            return
        self.ui.pre_close_image.setText(path)

    def inputImages(self):
        if os.path.exists(f"./workspace/train"):
            shutil.rmtree(f"./workspace/train")
        names = ["images", "labels", "vals"]
        for item in names:
            os.makedirs(f"./workspace/train/{item}")
        path, filetype = QFileDialog.getOpenFileNames(self, "选择图片源", "", "*.png;*.jpg;*.jpeg")
        if len(path) <= 0:
            return
        for item in path:
            shutil.copy(item, "./workspace/train/images")
        QMessageBox.information(self, "导入成功", f"共导入图片:{len(path)}", QMessageBox.Yes | QMessageBox.No)

    def preTrainCheck(self):
        format = f"""path: {self.cwd}/workspace/train
train: images
val: images
test: 
names:
"""
        if not os.path.exists(f"{self.cwd}/workspace/train/labels/classes.txt"):
            self.Globals["READYFORTRAIN"] = False
            self.globalLog(f"classes.txt文件可能不存在!请检查!", typ="error")
            return 0
        with open(f"{self.cwd}/workspace/train/labels/classes.txt", "r") as fp:
            classes = fp.readlines()
            index = 0
            for name in classes:
                format += f"  {str(index)}: {str(name)}"
                index += 1
            with open(f"{self.cwd}/workspace/train/config.yaml", "w") as f:
                f.write(format)
                # 在这个地方将训练的configs添加到主界面
                self.ui.train_datas.setPlainText(format)
                self.Globals["READYFORTRAIN"] = True
        QMessageBox.information(self, "预检查", f"检测完成，现在可以开始训练任务", QMessageBox.Yes | QMessageBox.No)
        self.globalLog(f"一切准备就绪，块开始训练吧!")

    def savePixmap(self):
        """
        弹出对话框-用户选择保存路径，调用子类的保存pixmap方法
        :return:
        """
        path, filetype = QFileDialog.getSaveFileName(self, "选择保存路径", f"draw", "*.png;*.jpg;*.jpeg")
        if len(path) == 0:
            return
        # 如果路径合法直接保存到该路径-判断一下路径是否存在(False)
        _path_ = os.path.dirname(path)
        if not os.path.exists(_path_):
            self.globalLog(f"路径不存在!", typ="warning")
            os.makedirs(_path_)
        # self.viewport.savePixmap(path)
        # TODO
        # 全局信息提示
        self.global_info.setText(f"成功保存到:{path}.")
        self.globalLog(f"已保存图片!", typ="warning")

    def saveProjectAs(self):
        name = self.configs["PROJECT_NAME"]
        path, filetype = QFileDialog.getSaveFileName(self, "选择项目文件", f"{name}", "*.ylbpj")
        if len(path) == 0:
            return
        save_as_name = (path.split("/")[-1]).split(".")[0]
        # 创建一个一项目名未名称的项目文件夹
        save_as_path = f"{os.path.dirname(path)}/{save_as_name}"
        temp_project = self.project
        temp_project["name"] = save_as_name
        try:
            os.makedirs(save_as_path)
        except Exception as e:
            QMessageBox.critical(self, '项目创建', f"❌创建失败!由于:{e}", QMessageBox.Close | QMessageBox.Cancel)
            self.globalLog(f"另存失败 error:'{e}'!", typ="error")
            self.poptipAnimate("Error in save", "error")
            return
        with open(f"{save_as_path}/{save_as_name}.ylbpj", "w", encoding="utf-8") as fp:
            project_ = json.dumps(temp_project, indent=0, ensure_ascii=False)
            fp.write(project_)
            self.globalLog(f"另存成功！")

    def checkUpdate(self, ):
        """
        检查更新-目前没有合适的平台，暂时无维护
        2023-7-24 无修改
        :param checked:
        :return:
        """
        pass
        # 检查云版本
        QMessageBox.information(self, '检查更新', f"当前版本:{self.configs['VERSION']} 暂无更新!",
                                QMessageBox.Close | QMessageBox.Cancel)

    def projectMediaData(self):
        """
        导入上一次项目保存的地址，前提是他存在
        导入媒体时，确保项目信息已经加载，因为上一次的媒体信息保存在了项目信息中
        2023-7-24 无修改
        :return:
        """

        try:
            # 解析项目信息-project里面本来就有，不用继续更新
            name = self.configs["PROJECT_NAME"]
            for media in self.project[name]["images"]:
                # 需要保证每个都是有效的存在的，不存在直接删除
                media_name = list(media.keys())[0]
                media_type = media_name.split(".")[-1]
                if not os.path.exists(media[media_name]):
                    self.project[name]["images"].remove(media)
                    continue
                _ = QTreeWidgetItem(self.images_folder, [media_name])
                _.setIcon(0, QIcon(f"{self.cwd}/variable/type_icon/{media_type}.png"))
                _.setToolTip(0, media[media_name])
            # 这里只显示了图片的名称，tooltip用来储存完成的路径使用的时候直接访问.item.toolTip(0)
            for media in self.project[name]["videos"]:
                media_name = list(media.keys())[0]
                media_type = media_name.split(".")[-1]
                if not os.path.exists(media[media_name]):
                    self.project[name]["videos"].remove(media)
                    continue
                _ = QTreeWidgetItem(self.videos_folder, [media_name])
                _.setIcon(0, QIcon(f"{self.cwd}/variable/type_icon/{media_type}.png"))
                _.setToolTip(0, media[media_name])
            # 加载用户项目文件夹下面的文件
            self.loadUserFiles()

        except Exception as e:
            self.globalLog(f"加载项目时出错 error:'{e}'!", typ="error")
            self.poptipAnimate("Error in loader", "error")

    def loadUserFiles(self):
        for userfile in os.listdir(self.configs["PROJECT_PATH"]):
            file_type = self.end(userfile)
            if file_type in self.types["text"]:
                _ = QTreeWidgetItem(self.user_folder, [userfile])
                _.setIcon(0, QIcon(f"{self.cwd}/variable/type_icon/{file_type}.png"))
                _.setToolTip(0, f"{self.configs['PROJECT_PATH']}/{userfile}")

    def valuesInit(self):
        """
        软件的重要变量的初始化
        2023-7-24 无修改
        :return:
        """
        # 加载软件支持的图片或者其他类型
        self.types = self.loadFileType()
        # 加载设置信息 self.configs是软件的设置信息，里面保存用户的
        # 软件的设置信息
        self.configs = dict()
        # todo
        self.configs = self.loadSettings()
        # mail configs init
        self.mailInit()
        # 分析过的
        # 项目-每次值加载一个项目，项目的信息就包括图片和视频的路径
        # 也就是说用户打开的图片实际上并没有导入到当前工作路径，只是记录他的路径而已
        # 软件的设置信息保存在默认路径
        self.project = dict()
        FOLDER_CREATED = False
        try:
            path = f"{self.configs.get('PROJECT_PATH')}/{self.configs.get('PROJECT_NAME')}.ylbpj"
            self.project = self.loadProjectData(path)
            # 初始化成功之后同样创建五个默认文件夹
            self.createDefaultFolder(self.configs["PROJECT_NAME"])
            FOLDER_CREATED = True
            # 文件夹创建成功以后还需要导入上次保存的图片视频信息
            self.projectMediaData()
            # 显示第一个项目
            if self.images_folder.childCount() > 0:
                frt = self.images_folder.child(0)
                self.tree.setCurrentItem(frt)
                self.viewport.showImage(self.images_folder.child(0).toolTip(0))
                self.plotRgbMap(self.images_folder.child(0).toolTip(0))
            # 展开全部
            self.tree.expandAll()
            self.globalLog(f"设置信息初始化成功✅")
        except Exception as e:
            self.globalLog(f"❌初始化项目失败,已创建默认项目 error:'{e}'!", typ="error")
            # self.poptipAnimate("Error in init","error")
            # 导入上次的项目失败就默认打开软件默认的工作目录
            # 重置默认数据
            self.resetConfigsData(self.configs)
            # 以下是检查路径是否存在，软件要启动就必须满足以下条件
            if not os.path.exists(f"{self.cwd}/workspace/默认项目"):
                os.makedirs(f"{self.cwd}/workspace/默认项目")
            self.configs["PROJECT_PATH"] = f"{self.cwd}/workspace/默认项目"
            self.configs["PROJECT_NAME"] = "默认项目"
            # 初始化失败也同样创建五个默认文件夹
            if not FOLDER_CREATED:
                self.createDefaultFolder("默认项目")

    def deleteProject(self):
        """
        清空当前的项目文件相当于创建一个新的项目并且将该项目的信息清空(恢复默认值)
        2023-7-24 无修改
        :return:
        """
        anser = QMessageBox.warning(self, "清空项目警告", f"确定清空当前项目？", QMessageBox.Yes | QMessageBox.No)
        if anser == QMessageBox.No:
            return
        # 删除当前的root所有文件夹
        for _ in range(self.tree.topLevelItemCount()):
            self.tree.takeTopLevelItem(0)
        # self.createDefaultFolder("默认项目")
        # self.tree.expandAll()
        # 如果时默认的文件夹就不删除实际的文件夹
        if self.configs["PROJECT_PATH"] == f"{self.cwd}/workspace/默认项目":
            self.resetConfigsData(self.configs)
            self.resetProjectData(self.configs["PROJECT_NAME"])
            return
        shutil.rmtree(self.configs["PROJECT_PATH"])

    def resetProjectData(self, name):
        """
        2023-7-24 无修改
        :param name:
        :return:
        """
        self.project = {
            name: {
                "images": [],
                "videos": [],
                "brief": ""
            }
        }

    def resetConfigsData(self, configs):
        """
        2023-7-24 无修改
        :param configs:
        :return:
        """
        configs = {
            "VERSION": "alpha-23.1.0",
            "PROJECT_PATH": "",
            "PROJECT_NAME": "",
            "WORKSPACE": "",
            "MODELPATH": "",
            "PYTHON": "",
            "QUITSAVE": True,
            "PRELOAD": False,
            "GPU": False,
            "CURRENTMODEL": 0,
            "SOFTLOG": True,
            "LOCALLOG": True,
            "AUTOCLOSE": True,
            "PLOTPENSIZE": "1",
            "GUIDE": True,
            "STARTFACE": True,
            "RECENT_PROJECT": []
            }

    def selfMailHeader(self, checked):
        self.ui.self_send_content.setEnabled(checked)

    # 设置脚本窗口初始化
    def scriptsWindowInit(self):
        self.ui.commands.installEventFilter(self)
        self.ui.commands.append("我们将提供一些内置的方法供操作-使用'help'命令以查看帮助文档.")
        self.ui.commands.append(">>>")
        self.ui.commands.cursorPositionChanged.connect(self.cursorChanged)

    def cursorChanged(self):
        self.ui.commands.moveCursor(QTextCursor.End)

    def windowsInit(self):
        """
        2023-7-24 无修改
        :return:
        """
        # 软件图标
        self.setWindowIcon(QIcon("./variable/icons/logo.jpg"))
        # 创建训练窗口
        self.train_model_window = Trainer(self)
        # 默认不显示检测与训练的操作窗口
        # self.ui.predict_window.hide()
        # 树列表结构
        self.tree = Tree(self)
        self.ui.source_window.setWidget(self.tree)
        # 脚本窗口初始化
        self.scriptsWindowInit()
        # 命令行窗口关闭
        self.ui.commands.hide()
        # 自定义mail标题
        self.ui.self_send.setChecked(False)
        self.ui.self_send_content.setEnabled(False)
        self.ui.self_send.clicked.connect(self.selfMailHeader)
        # 设置底部dock栏的极限
        # 右边
        self.ui.result_window.setMinimumWidth(320)
        self.ui.result_window.setMaximumWidth(380)
        # 左边
        self.ui.source_window.setMinimumWidth(350)
        self.ui.source_window.setMaximumWidth(420)
        self.ui.draw_window.setFixedHeight(240)

        # 关闭插件设置
        self.ui.predict_settings.hide()
        # 关闭控制台
        # self.ui.cmd.hide()
        # self.ui.bottom_dock.setTitleBarWidget(QWidget())
        # 默认显示结果页面
        self.viewport = mediaView(self)
        self.viewport.stateChange.connect(self.playerChange)
        self.viewport.posChange.connect(self.posChange)
        # 为viewport安装事件过滤器
        self.viewport.installEventFilter(self)
        self.installEventFilter(self)
        # 图片视频浏览器
        self.VIDEOPLAY = False
        self.image_index = 0
        self.video_index = 0
        # self.ui.center.addWidget(self.viewport)
        self.ui.center.addTab(self.viewport, QIcon("./variable/icons/viewport.png"), "媒体视口")
        # 自定义左边的标题栏
        self.global_ansysis = QPushButton(self)
        self.global_ansysis.clicked.connect(self.globalAnsysis)
        self.global_ansysis.setIcon(QIcon(""))
        self.global_ansysis.setText("全局分析")
        self.global_ansysis.setStyleSheet(self.qss("global_ansysis_button"))
        self.global_ansysis.setMaximumSize(160, 25)
        source_icon = QPushButton(self)
        source_icon.setText("资源管理器")
        source_icon.setIcon(QIcon("./variable/icons/management.png"))
        source_icon.setStyleSheet(self.qss("icon_default"))
        # source_label = QLabel("资源管理器")
        # source_label.setAlignment(Qt.AlignCenter)
        left_layout = QHBoxLayout(self)
        left_layout.setContentsMargins(0, 2, 0, 2)
        widget = QWidget(self)
        left_layout.addWidget(source_icon, 0, Qt.AlignLeft | Qt.AlignTop)
        # left_layout.addWidget(source_label, 0, Qt.AlignLeft | Qt.AlignTop)
        left_layout.addWidget(self.global_ansysis, 0, Qt.AlignRight | Qt.AlignTop)
        widget.setLayout(left_layout)
        self.ui.source_window.setTitleBarWidget(widget)

        icon = QIcon(f"{self.cwd}/variable/icons/xylogo.png")
        xy = QPushButton(self)
        xy.setText("江小鱼科创")
        xy.setStyleSheet(self.qss("xylogo_button"))
        xy.setIcon(icon)
        # 显示信息
        self.global_info = QLabel(self)
        self.global_info.setAlignment(Qt.AlignLeft)
        self.global_info.setFont(QFont("微软雅黑"))
        # 初始化进度条
        self.progress = QProgressBar()
        self.progress.setStyleSheet(self.qss("bottom_progress"))
        self.progress.setFixedWidth(160)
        # 进度条hide
        self.progress.hide()
        self.ui.status.addPermanentWidget(xy)
        self.ui.status.addWidget(self.progress)
        self.ui.status.addWidget(self.global_info)
        self.global_info.setText("✅环境加载成功.")

        # 底部dock栏标题栏自定义
        # 标题
        self.view_label = QPushButton(self)
        self.view_label.setText("日志信息")
        # self.view_label.setFixedSize(QSize(120, 35))
        self.view_label.setStyleSheet(self.qss("icon_default"))
        self.view_label.setCheckable(True)
        self.view_label.clicked.connect(self.viewOrscript)
        self.view_label.setIcon(QIcon("./variable/icons/line_log.png"))
        # 成功info
        self.success_info = QPushButton("成功(0条)")
        # self.success_info.setFixedSize(QSize(120, 35))
        self.success_info.setIcon(QIcon("./variable/icons/right.png"))
        self.success_info.setStyleSheet(self.qss("icon_default"))
        # 警告info
        self.warning_info = QPushButton("警告(0条)")
        # self.warning_info.setFixedSize(QSize(120, 35))
        self.warning_info.setIcon(QIcon("./variable/icons/warning.png"))
        self.warning_info.setStyleSheet(self.qss("icon_default"))
        # 错误info
        self.error_info = QPushButton("错误(0条)")
        # self.error_info.setFixedSize(QSize(120, 35))
        self.error_info.setIcon(QIcon("./variable/icons/error.png"))
        self.error_info.setStyleSheet(self.qss("icon_default"))

        self.info_content = QPushButton()
        self.info_content.setStyleSheet(self.qss("icon_default"))


        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.view_label, 0)
        layout.addWidget(self.success_info, 0)
        layout.addWidget(self.warning_info, 0)
        layout.addWidget(self.error_info, 0)
        layout.addWidget(self.info_content, 0)

        widget = QWidget(self)
        widget.setLayout(layout)
        self.ui.logger_window.setTitleBarWidget(widget)

        # 共创窗口的标题栏自定义
        left_layout = QHBoxLayout(self)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setAlignment(Qt.AlignLeft)
        widget = QWidget(self)
        # widget.setContentsMargins(0,2,0,2)
        # 添加图像按钮
        add_images_btn = QPushButton("添加图像")
        add_images_btn.setStyleSheet(self.qss("button_default"))
        add_images_btn.clicked.connect(lambda: self.inputFiles(typ="image"))
        # 添加视频按钮
        add_videos_btn = QPushButton("添加视频")
        add_videos_btn.clicked.connect(lambda: self.inputFiles(typ="video"))
        add_videos_btn.setStyleSheet(self.qss("button_default"))
        # 刷新设备按钮
        update_device_btn = QPushButton("更新设备")
        update_device_btn.clicked.connect(self.updateDevice)
        update_device_btn.setStyleSheet(self.qss("button_default"))
        # 重新加载模型按钮
        load_weight_btn = QPushButton("加载权重")
        load_weight_btn.clicked.connect(self.reLoadModel)
        load_weight_btn.setToolTip("点击重新加载权重文件")
        load_weight_btn.setStyleSheet(self.qss("button_green"))

        left_layout.addWidget(add_images_btn, 0)
        left_layout.addWidget(add_videos_btn, 0)
        left_layout.addWidget(update_device_btn, 0)
        left_layout.addWidget(load_weight_btn, 0)

        widget.setLayout(left_layout)
        self.ui.tool_window.setTitleBarWidget(widget)
        # 检测和训练的窗口初始化QTabelWidget
        self.ui.prerdict_or_train.currentChanged.connect(self.predOrtrainw)

        # 共创窗口的标题栏自定义
        left_layout = QHBoxLayout(self)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setAlignment(Qt.AlignRight|Qt.AlignCenter)
        widget = QWidget(self)

        self.rgb_draw_mode = QComboBox(self)
        self.rgb_draw_mode.addItems(["灰度图", "RGB图", "绘制以上"])
        self.rgb_draw_mode.setFixedSize(QSize(100, 25))
        self.rgb_draw_mode.setFont(QFont("微软雅黑", 9))

        self.rgb_draw_mode.currentIndexChanged.connect(lambda: self.plotRgbMap(self.tree.currentItem().toolTip(0)))

        left_layout.addWidget(self.rgb_draw_mode, 0)

        widget.setLayout(left_layout)
        self.ui.draw_window.setTitleBarWidget(widget)

        # 结果窗口标题栏自定义
        # 当前结果是否检测到对象
        self.have_object_state = QLabel(self)
        self.have_object_state.setStyleSheet(
            "background-color: rgb(145, 145, 145);color: rgb(220, 220, 220);font: 10pt '微软雅黑';")
        self.have_object_state.setFixedSize(40, 20)
        self.have_object_state.setAlignment(Qt.AlignCenter)
        self.have_object_state.setToolTip("是否有检测到对象")
        self.setObjectState()
        # 当前结果检测的时间
        self.time_consuming = QLabel(self)
        self.time_consuming.setStyleSheet("font: 10pt '微软雅黑';")
        self.time_consuming.setMaximumSize(60, 20)
        self.time_consuming.setAlignment(Qt.AlignLeft)
        self.time_consuming.setToolTip("当前结果检测消耗的时间")
        self.setConsuming(0.0)

        self.query_result = QLineEdit(self)
        clear_all = QAction(self.query_result)
        query_icon = QAction(self.query_result)
        query_icon.setIcon(QIcon("variable/icons/query.png"))
        clear_all.setIcon(QIcon("variable/icons/clear_input.png"))
        query_icon.setToolTip("搜索结果")
        clear_all.setToolTip("清空输入")
        self.query_result.addAction(query_icon, QLineEdit.LeadingPosition)
        self.query_result.addAction(clear_all, QLineEdit.TrailingPosition)
        # 信号槽
        clear_all.triggered.connect(self.query_result.clear)
        self.query_result.returnPressed.connect(self.queryResults)
        self.query_result.textChanged.connect(self.dynamicQuery)

        # 显示当前的模型
        self.current_model = QLabel(self)
        self.current_model.setStyleSheet("font: 9pt '微软雅黑';")
        self.current_model.setAlignment(Qt.AlignRight)
        self.current_model.setText(f"M:N")

        # 添加右边的到标题栏
        right_layout = QHBoxLayout(self)
        right_layout.setContentsMargins(0, 5, 0, 0)
        widget = QWidget(self)
        right_layout.addWidget(self.have_object_state, 0, Qt.AlignLeft | Qt.AlignTop)
        right_layout.addWidget(self.time_consuming, 1, Qt.AlignLeft | Qt.AlignTop)
        right_layout.addWidget(self.current_model, 1, Qt.AlignRight | Qt.AlignTop)
        right_layout.addWidget(self.query_result, 2, Qt.AlignLeft | Qt.AlignTop)

        widget.setLayout(right_layout)
        self.ui.result_window.setTitleBarWidget(widget)

        # 创建图像直方图的窗口
        # 创建一个PlotWidget用于显示直方图
        self.rgb_plot = pg.PlotWidget()
        # self.rgb_plot.addLegend()
        self.ui.image_data_view_layout.addWidget(self.rgb_plot)
        # 绘制直方图
        self.rgb_plot.setBackground("w")
        self.rgb_plot.setMouseEnabled(False, False)
        # self.rgb_plot.hideAxis('bottom')
        self.rgb_plot.hideAxis('left')
        self.rgb_plot.showGrid(x=True, y=True)
        # 添加LabelItem来显示当前值
        self.current_hist = pg.LabelItem(bold=True)
        self.rgb_plot.scene().addItem(self.current_hist)
        self.rgb_plot.plotItem.vb.scene().sigMouseMoved.connect(self.update_hist_value)
        # 窗口资源加载成功
        self.globalLog("窗口资源加载成功")
        # 视口右键
        self.viewport.setContextMenuPolicy(Qt.CustomContextMenu)
        self.viewport.customContextMenuRequested.connect(self.viewerRightmenu)  # 连接到菜单显示函数

        # 初始化设置窗口
        self.setting_face = SettingFace(self)
        # 导向窗口
        self.guide_face = GuideFace(self)
        #添加插件窗口
        self.add_plugins_face = Addplugins(self)

        #center view
        self.ui.center.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.center.customContextMenuRequested.connect(self.centerTabmenu)

    def dynamicQuery(self):
        for r in range(self.ui.result.rowCount()):
            for c in range(self.ui.result.columnCount()):
                self.ui.result.item(r, c).setBackground(QBrush(QColor("#FFFFFF")))

        content = self.query_result.text()
        if len(content) > 0 and self.ui.result.rowCount()>0:
            items = self.ui.result.findItems(content, Qt.MatchStartsWith)
            queried_items = list(filter(lambda x: not x.column(), items))
            self.ui.result.verticalScrollBar().setValue(queried_items[0].row())
            for item in queried_items:
                row = item.row()
                self.ui.result.item(row, 0).setBackground(QBrush(QColor("#6600CC")))
                self.ui.result.item(row, 1).setBackground(QBrush(QColor("#6600CC")))

    def queryResults(self):
        self.dynamicQuery()

    def viewOrscript(self, checked):
        if checked:
            self.view_label.setText("脚本窗口")
            self.view_label.setIcon(QIcon("./variable/icons/line_scripts.png"))
            self.ui.commands.show()
            self.ui.log.hide()
            self.success_info.hide()
            self.warning_info.hide()
            self.error_info.hide()
        else:
            self.view_label.setText("日志信息")
            self.view_label.setIcon(QIcon("./variable/icons/line_log.png"))
            self.ui.commands.hide()
            self.ui.log.show()
            self.success_info.show()
            self.warning_info.show()
            self.error_info.show()


    def centerBarDoubleClick(self,index):
        if index!=0:
            self.alltabs.pop(index)
            self.ui.center.removeTab(index)

    def closeTab(self,mode="current"):
        # 获取当前选中的选项卡的索引
        index = self.ui.center.currentIndex()
        count = self.ui.center.count()
        if mode=="all":
            self.ui.center.setCurrentIndex(0)
            for _ in range(1,count):
                self.alltabs.pop(1)
                self.ui.center.removeTab(1)

        elif mode=="other":
            index = self.ui.center.currentIndex()
            #删除其他数据
            del self.alltabs[index+1:count]
            del self.alltabs[1:index]

            #删除tab
            for i in range(index+1,count):
                self.ui.center.removeTab(index+1)
            for _ in range(1,index):
                self.ui.center.removeTab(1)
        else:
            if count>1:
                self.alltabs.pop(index)
                self.ui.center.removeTab(index)

    def centerTabmenu(self):
        self.tab_menu = QMenu(self)

        close_current = QAction(QIcon(""), u"关闭", self)
        self.tab_menu.addAction(close_current)
        close_current.triggered.connect(self.closeTab)

        close_other = QAction(QIcon(""), u"关闭其他", self)
        self.tab_menu.addAction(close_other)
        close_other.triggered.connect(lambda :self.closeTab("other"))

        close_all = QAction(QIcon(""), u"关闭所有", self)
        self.tab_menu.addAction(close_all)
        close_all.triggered.connect(lambda :self.closeTab("all"))

        # 显示菜单
        self.tab_menu.exec(QCursor.pos())


    def viewerRightmenu(self):
        # 菜单对象
        self.viewer_menu = QMenu(self)

        predict = QAction(QIcon(""), u"对象检测", self)
        self.viewer_menu.addAction(predict)
        predict.triggered.connect(self.singlePredict)
        predict.setEnabled(True)
        if not self.Globals["LOADMODELFINISH"]:
            predict.setEnabled(False)

        predict_tomail = QAction(QIcon(""), u"检测并发送至邮箱(测试)", self)
        self.viewer_menu.addAction(predict_tomail)
        predict_tomail.triggered.connect(lambda :self.singlePredict(True))
        predict_tomail.setEnabled(True)

        close_predict = QAction(QIcon(""), u"封闭性检查", self)
        self.viewer_menu.addAction(close_predict)
        close_predict.triggered.connect(self.closePredict)

        measure_predict = QAction(QIcon(""), u"测量尺寸", self)
        self.viewer_menu.addAction(measure_predict)
        measure_predict.triggered.connect(self.measurePredict)

        self.viewer_menu.addSeparator()
        video_state = QAction(QIcon(""), u"暂停", self)
        self.viewer_menu.addAction(video_state)
        # video_state.triggered.connect()
        # 批量导入文件
        inputfs = QAction(QIcon(""), u"批量导入文件", self)
        inputfs.setShortcut("Ctrl+I")
        self.viewer_menu.addAction(inputfs)
        # inputfs.triggered.connect()
        # 图像另存为
        pix_saveas = QAction(QIcon(""), u"图像另存为", self)
        pix_saveas.setShortcut("Ctrl+P")
        self.viewer_menu.addAction(pix_saveas)
        # pix_saveas.triggered.connect()
        # 打开本地路径
        pix_path = QAction(QIcon(""), u"打开本地路径", self)
        self.viewer_menu.addAction(pix_path)
        # pix_path.triggered.connect()
        # 截图
        screen_shot = QAction(QIcon(""), u"截图", self)
        self.viewer_menu.addAction(screen_shot)
        # screen_shot.triggered.connect()
        # 关闭显示
        close_viewer = QAction(QIcon(""), u"清空显示", self)
        self.viewer_menu.addAction(close_viewer)
        # close_viewer.triggered.connect()

        self.viewer_menu.addSeparator()
        # 训练任务中止
        train_terminate = QAction(QIcon(""), u"训练任务中止", self)
        self.viewer_menu.addAction(train_terminate)
        # train_terminate.triggered.connect()

        # 预测任务中止
        predict_terminate = QAction(QIcon(""), u"预测任务中止", self)
        self.viewer_menu.addAction(predict_terminate)
        # predict_terminate.triggered.connect()

        self.viewer_menu.popup(QCursor.pos())

    def update_hist_value(self, pos):
        mouse_point = self.rgb_plot.plotItem.vb.mapSceneToView(pos)
        self.current_hist.setText(f"x={mouse_point.x():.1f}, y={mouse_point.y():.1f}")

    def setLogTypes(self, counts):
        self.success_info.setText(f"成功({counts[0]}条)")
        self.warning_info.setText(f"警告({counts[1]}条)")
        self.error_info.setText(f"错误({counts[2]}条)")

    def setCurrentModelTip(self, name, state="🚀"):
        self.current_model.setText(f"M:{name}-{state}")

    def reLoadModel(self):
        index = self.ui.menu_models.actions().index(self.current_model_action)
        model_name = self.current_model_action.text()
        model_path = f"{self.cwd}/variable/models/{model_name}"
        if self.Globals["LOADMODELFINISH"]:
            anser = QMessageBox.information(self, "模型加载", f"您已成功加载过模型:{model_name}确定重新加载？",
                                            QMessageBox.Yes | QMessageBox.No)
            if anser == QMessageBox.No:
                return
        self.changeModel(model_path, index)

    def posChange(self, point):
        self.info_content.setText(f"显示坐标x:{str(point.x())} y:{str(point.y())}")

    def playerChange(self, duration):
        self.info_content.setText(duration)

    def tipper(self, content: str):
        """
        2023-7-24 无修改
        :param content:
        :return:
        """
        self.info_content.setText(content)
        self.info_content.setAlignment(Qt.AlignCenter)

    def pluginsInit(self):
        """
        插件的初始化，这里的插件时软件内部的插件并不是外部插件，比如标签工具等
        2023-7-24 无修改
        :return:
        """
        self.ui.plugins.setIconSize(QSize(32, 32))
        # self.ui.plugins.setFixedHeight(32)
        self.labeling = QAction(QIcon(f"{self.cwd}/variable/icons/labeling_logo.png"), '拉框工具', self)
        self.labeling.triggered.connect(self.runLabeling)
        self.labeling.setCheckable(True)
        self.LABELINGSTATE = False
        self.ui.plugins.addAction(self.labeling)

        self.trainer = QAction(QIcon(f"{self.cwd}/variable/icons/model.png"), '模型训练', self)
        self.trainer.triggered.connect(self.modelTrainer)
        self.trainer.setCheckable(True)
        self.TRAINERSTATE = False
        self.ui.plugins.addAction(self.trainer)
        self.ui.plugins.addSeparator()
        #刷新插件

        self.ui.plugins.addSeparator()
        #默认添加插件事件

    def showSettingWindow(self, checked):
        if checked:
            self.setting_face.exec()
        else:
            self.setting_face.close()

    # 当前结果是否检测到对象
    def setObjectState(self, have="U"):
        """
        主要是用来显示检测结果的状态的，比如有缺陷将其设置为红色
        2023-7-24 无修改
        :param have:
        :return:
        """
        self.have_object_state.setText(have)
        rgbx = "(220, 220, 220)"
        if have == "UN":
            rgbx = "(255, 0, 0)"
        elif have == "EN":
            rgbx = "(0, 220, 0)"
        self.have_object_state.setStyleSheet(
            f"background-color: rgb{rgbx};color: rgb(240,240,240);font: 10pt '微软雅黑';")

    def setConsuming(self, _ms):
        """
        2023-7-24 无修改
        :param _ms:
        :return:
        """
        self.time_consuming.setText(f"{_ms}ms")

    def showResultsWindow(self):
        """
        2023-7-24 无修改
        :return:
        """
        # 显示dock栏
        # self.ui.results_frame.show()
        self.setting_face.hide()
        # 显示log窗口
        # self.ui.draw_window.show()

    def qss(self, qss_name, typ="style"):
        """
        加载Qt程序的qss样式文件
        2023-7-24 无修改
        :param qss_name:
        :return:
        """
        with open(f"{self.cwd}/variable/{typ}/{qss_name}.qss", "r", encoding="utf-8") as fp:
            return fp.read()

    # ensure_ascii=False
    def etoolsInit(self):
        """
        2023-7-24 无修改
        :return:
        """
        self.ui.etools.setIconSize(QSize(32, 32))
        self.action_undo = QAction(QIcon(f"{self.cwd}/variable/icons/undo.png"), '撤销', self)
        # self.action_undo.triggered.connect(self.viewport.undo)
        self.action_undo.setShortcut("Ctrl+Z")
        self.ui.etools.addAction(self.action_undo)
        self.action_redo = QAction(QIcon(f"{self.cwd}/variable/icons/redo.png"), '回退', self)
        # self.action_redo.triggered.connect(self.viewport.redo)
        self.action_redo.setShortcut("Ctrl+Y")
        self.ui.etools.addAction(self.action_redo)
        self.ui.etools.addSeparator()

        # self.cut = QAction(QIcon(f"{self.cwd}/variable/icons/cut.png"), '剪切', self)
        # self.cut.triggered.connect(self.cutText)
        # self.ui.etools.addAction(self.cut)
        #
        # self.copy = QAction(QIcon(f"{self.cwd}/variable/icons/copy.png"), '复制文本', self)
        # self.copy.triggered.connect(self.copyText)
        # self.ui.etools.addAction(self.copy)
        #
        # self.paste = QAction(QIcon(f"{self.cwd}/variable/icons/paste.png"), '粘贴', self)
        # self.paste.triggered.connect(self.pasteText)
        # self.ui.etools.addAction(self.paste)

        self.edit_font = QFontComboBox(self)
        # self.edit_font.setStyleSheet("QFontComboBox{border:none;}")
        self.edit_font.setMaximumWidth(160)
        self.ui.etools.addWidget(self.edit_font)
        self.ui.etools.addSeparator()

    def pasteText(self):
        pass

    # def copyText(self):
    #     if not self.viewport.edit.isHidden():
    #         text = self.viewport.edit.toPlainText()
    #         clipboard = QApplication.clipboard()
    #         clipboard.setText(text)
    #         self.poptipAnimate("内容已经复制", typ="normal")

    # def cutText(self):
    #     if not self.viewport.edit.isHidden():
    #         text = self.viewport.edit.toPlainText()
    #         self.viewport.edit.setText("")
    #         clipboard = QApplication.clipboard()
    #         clipboard.setText(text)
    #         self.poptipAnimate("已剪切到剪切板", typ="normal")

    def printFile(self):
        pass

    def saveAs(self):
        pass

    def toolbarInit(self):
        self.ui.action_settings.setIcon(QIcon(f"{self.cwd}/variable/icons/setting.png"))
        self.ui.action_quit.setIcon(QIcon(f"{self.cwd}/variable/icons/quit.png"))
        self.ui.action_save.setIcon(QIcon(f"{self.cwd}/variable/icons/save.png"))
        self.ui.action_print_menus.setIcon(QIcon(f"{self.cwd}/variable/icons/print.png"))

    def mtoolsInit(self):
        """
        2023-7-24 无修改
        :return:
        """
        self.ui.mtools.setIconSize(QSize(32, 32))
        self.new = QAction(QIcon(f"{self.cwd}/variable/icons/new_project.png"), '新建项目(Ctrl+N)', self)
        self.new.setShortcut("Ctrl+N")
        self.new.triggered.connect(self.createProject)
        self.ui.mtools.addAction(self.new)
        self.open = QAction(QIcon(f"{self.cwd}/variable/icons/open_project.png"), '打开项目(Ctrl+O)', self)
        self.open.triggered.connect(self.openProject)
        self.open.setShortcut("Ctrl+O")
        self.ui.mtools.addAction(self.open)
        self.save = QAction(QIcon(f"{self.cwd}/variable/icons/save.png"), '保存项目(Ctrl+S)', self)
        self.save.setShortcut("Ctrl+S")
        self.save.triggered.connect(self.saveDatas)
        self.ui.mtools.addAction(self.save)
        self.printf = QAction(QIcon(f"{self.cwd}/variable/icons/save_as.png"), '打印(Ctrl+P)', self)
        self.printf.triggered.connect(self.saveAs)
        self.save.setShortcut("Ctrl+P")
        self.ui.mtools.addAction(self.printf)
        self.ui.mtools.addSeparator()

        self.input = QAction(QIcon(f"{self.cwd}/variable/icons/import.png"), '导入文件(Ctrl+I)', self)
        self.input.triggered.connect(self.inputFiles)
        self.input.setShortcut("Ctrl+I")
        self.ui.mtools.addAction(self.input)

        self.home = QAction(QIcon(f"{self.cwd}/variable/icons/home.png"), "打开主页向导", self)
        self.home.triggered.connect(self.guide_face.exec)
        self.ui.mtools.addAction(self.home)
        self.ui.mtools.addSeparator()

        self.start_camera = QAction(QIcon(f"{self.cwd}/variable/icons/start.png"), '开始摄像头检测', self)
        self.start_camera.triggered.connect(lambda: self.startCamera(0))
        self.ui.mtools.addAction(self.start_camera)
        self.start_camera.setEnabled(False)

        self.stop = QAction(QIcon(f"{self.cwd}/variable/icons/terminate.png"), '中止任务(Ctrl+Q)', self)
        self.stop.triggered.connect(self.Stop)
        self.stop.setEnabled(False)
        self.stop.setShortcut("Ctrl+Q")

        self.ui.mtools.addSeparator()

        self.amplify = QAction(QIcon(f"{self.cwd}/variable/icons/amplify.png"), '放大', self)
        self.amplify.triggered.connect(self.Amplify)
        self.ui.mtools.addAction(self.amplify)
        self.reduce = QAction(QIcon(f"{self.cwd}/variable/icons/reduce.png"), '缩小', self)
        self.reduce.triggered.connect(self.Reduce)
        self.ui.mtools.addAction(self.reduce)
        self.suitable = QAction(QIcon(f"{self.cwd}/variable/icons/suitable.png"), '适应屏幕', self)
        self.suitable.triggered.connect(self.Suitable)
        self.ui.mtools.addAction(self.suitable)
        self.move = QAction(QIcon(f"{self.cwd}/variable/icons/move.png"), '移动', self)
        self.move.triggered.connect(self.Move)
        self.move.setCheckable(True)
        self.MOVEFLAG = False
        self.ui.mtools.addAction(self.move)

        self.show_rt = QAction(QIcon(f"{self.cwd}/variable/icons/show.png"), '显示结果', self)
        self.show_rt.setCheckable(True)
        self.SHOWRT = True
        self.ui.mtools.addAction(self.show_rt)
        self.ui.mtools.addSeparator()

        self.last_item = QAction(QIcon(f"{self.cwd}/variable/icons/last.png"), '上一项', self)
        self.last_item.triggered.connect(self.lastItem)
        self.ui.mtools.addAction(self.last_item)
        self.pause_play = QAction(QIcon(f"{self.cwd}/variable/icons/play.png"), '暂停播放', self)
        self.pause_play.triggered.connect(self.videoPause)
        self.pause_play.setEnabled(False)
        self.ui.mtools.addAction(self.pause_play)

        self.next_item = QAction(QIcon(f"{self.cwd}/variable/icons/next.png"), '下一项', self)
        self.next_item.triggered.connect(self.nextItem)
        self.ui.mtools.addAction(self.next_item)
        self.ui.mtools.addSeparator()

        self.run_scripts = QAction(QIcon(f"{self.cwd}/variable/icons/python_editor.png"), '运行python脚本', self)
        self.run_scripts.triggered.connect(self.runScripts)
        self.ui.mtools.addAction(self.run_scripts)


        # self.results = QAction(QIcon(f"{self.cwd}/variable/icons/result.png"), '可视化结果', self)
        # self.results.triggered.connect(self.showResultsWindow)
        # self.ui.mtools.addAction(self.results)

        self.setting = QAction(QIcon(f"{self.cwd}/variable/icons/setting.png"), '设置', self)
        self.setting.setCheckable(True)
        self.ui.mtools.addAction(self.setting)
        self.setting.triggered.connect(self.showSettingWindow)

        self.quit_ = QAction(QIcon(f"{self.cwd}/variable/icons/quit.png"), '退出', self)
        self.quit_.triggered.connect(self.close)
        self.quit_.setShortcut("ESC")
        self.ui.mtools.addAction(self.quit_)

        self.help = QAction(QIcon(f"{self.cwd}/variable/icons/help.png"), '帮助', self)
        self.ui.mtools.addAction(self.help)
        # 默尔维尼显示
        # self.ui.etools.hide()
        # 添加widget
        # 菜单栏按钮添加代码
        frame = QFrame(self.ui.menubar)
        layout = QHBoxLayout(self.ui.menubar)
        layout.setContentsMargins(0, 2, 0, 0)
        frame.setLayout(layout)
        # 添加进程COM
        qcom = QComboBox(self.ui.menubar)
        qcom.setFixedSize(QSize(120, 28))
        qcom.setFont(QFont("微软雅黑", 9))
        qcom.addItems(["app", "训练进程", "检测进程"])
        for i in range(0, 3):
            qcom.setItemIcon(i, QIcon("./variable/icons/logo.jpg"))
        qcom.setFont(QFont("微软雅黑"))

        layout.addWidget(qcom)
        self.ui.menubar.setCornerWidget(frame, corner=Qt.TopRightCorner)
        tooltips = ["全局搜索", "访问官网"]
        for i, icon in enumerate(["gquery", "browser"]):
            btn = QPushButton(self.ui.menubar)
            btn.setToolTip(tooltips[i])
            btn.setIcon(QIcon(f"./variable/icons/{icon}.png"))
            btn.setStyleSheet(self.qss("menubar_button"))
            btn.setFixedSize(QSize(25, 25))
            layout.addWidget(btn)


    def controlCamera(self, checked):
        if checked:
            self.startCamera(0)
        else:
            self.stopCamera()

    def runScripts(self):
        """
        运行pyton脚本，暂停维护
        2023-7-24 无修改
        :return:
        """
        path, filetype = QFileDialog.getOpenFileName(self, "选择图片源", "", "*.py")
        if filetype != "*.py":
            return
        with open(path, "r", encoding="utf-8") as fp:
            python_exe = self.setting_face.ui.python_path.text()
            if not "python.exe" in python_exe:
                self.globalLog("你还没有设置python解释器。", typ="error")
                return
            process = subprocess.Popen([python_exe, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            # Print the output
            if len(stdout.decode()) > 0:
                self.globalLog(f"运行成功✅:")
                format = f"<span><b>'{stdout.decode()}'</b></span><br>"
                self.ui.log.insertHtml(format)
            if len(stderr.decode()) > 0:
                self.globalLog(f"运行错误❌", typ="error")
                format = f"<span><b>'{stderr.decode()}'</b></span><br>"
                self.ui.log.insertHtml(format)
            return_code = process.returncode
            format = f"<span><b>process finished with exit code {return_code}</b></span><br>"
            self.ui.log.insertHtml(format)
            self.ui.log.moveCursor(QTextCursor.End)

    def lastItem(self):
        """
        上一个项目：需要根据全局变量VIEW_MODE的值调整，假设用户正在使用摄像头，那么就加载上一个摄像头
        2023-7-24 无修改
        :return:
        """
        if self.Globals["VIEW_MODE"] == "IMAGE":
            if self.image_index > 0:
                self.image_index -= 1
            else:
                self.image_index = self.images_folder.childCount() - 1
            image_item = self.images_folder.child(self.image_index)
            self.viewport.showImage(image_item.toolTip(0))
            self.tree.setCurrentItem(image_item)

        elif self.Globals["VIEW_MODE"] == "VIDEO":
            if self.video_index > 0:
                self.video_index -= 1
            else:
                self.video_index = self.videos_folder.childCount() - 1
            video_item = self.videos_folder.child(self.video_index)
            self.viewport.showVideo(video_item.toolTip(0))
            self.tree.setCurrentItem(video_item)

    def videoPause(self):
        """
        2023-7-24 无修改
        :return:
        """
        self.viewport.stop()
        self.pause_play.setIcon(QIcon("variable/icons/play.png"))
        self.pause_play.triggered.connect(self.videoPlay)

    def videoPlay(self):
        self.viewport.play()
        self.pause_play.setIcon(QIcon("variable/icons/pause.png"))
        self.pause_play.triggered.connect(self.videoPause)

    def nextItem(self):
        """
        2023-7-24 无修改
        :return:
        """
        # 照片显示模式
        if self.Globals["VIEW_MODE"] == "IMAGE":
            if self.image_index < self.images_folder.childCount() - 1:
                self.image_index += 1
            else:
                self.image_index = 0
            image_item = self.images_folder.child(self.image_index)
            self.viewport.showImage(image_item.toolTip(0))
            self.tree.setCurrentItem(image_item)
        # 如果当前显示的模式为视频显示就执行时评显示的
        elif self.Globals["VIEW_MODE"] == "VIDEO":
            if self.video_index < self.videos_folder.childCount() - 1:
                self.video_index += 1
            else:
                self.video_index = 0
            video_item = self.videos_folder.child(self.video_index)
            self.viewport.showVideo(video_item.toolTip(0))
            self.tree.setCurrentItem(video_item)

    def modelTrainer(self):
        """
        modelTrainer插件打开插件训练模型
        2023-7-24 无修改
        :return:
        """
        if not self.TRAINERSTATE:
            self.TRAINERSTATE = True
            self.trainer.setChecked(True)
            self.train_model_window.show()
        else:
            self.TRAINERSTATE = False
            self.trainer.setChecked(False)
            self.train_model_window.close()
            #不关闭训练进程，训练完成以后自动关闭

    def updatalabelingState(self):
        """
        检测用户是否从Labeling软件关闭
        2023-7-24 无修改
        :return:
        """
        if not self.labeling_proc.is_alive():
            self.LABELINGSTATE = False
            self.labeling.setChecked(False)
            self.labeling_run_timer.stop()

    def runLabeling(self, cheked):
        """
        在运行该插件时需要设置几个量，需修改
        2023-7-24 无修改
        :param cheked:
        :return:
        """
        env = {}
        # TODO 在GUI界面修改这几个变量
        env["TRAINPATH"] = f"{self.cwd}/workspace/train/images"
        env["LABELPATH"] = f"{self.cwd}/workspace/train/labels"
        env["PREDEFCLASS"] = f"{self.cwd}/labeling/data/predefined_classes.txt"
        if not self.LABELINGSTATE:
            self.LABELINGSTATE = True
            self.labeling.setChecked(True)
            # DO 启动Labeling进程
            self.labeling_proc = multiprocessing.Process(target=lab_main, args=(env,))
            self.labeling_proc.start()
            self.labeling_run_timer.start()
        else:
            self.LABELINGSTATE = False
            self.labeling.setChecked(False)
            # DO 关闭Labeling进程
            try:
                self.labeling_proc.terminate()
                self.labeling_proc.join()
                self.globalLog(f"标签工具已关闭!")
            except Exception as e:
                self.globalLog(f"运行错误 error:{e}", typ="error")
                self.poptipAnimate("Error in Labeling", "error")

    def inputFiles(self, typ="both"):
        """
        导入文件需要更新两个地方
            self.project
            GUI.self.tree
        2023-7-24 无修改
        :return:
        """
        suffix = "*.png;*.jpg;*.jpeg;;*.mp4"
        if typ == "image":
            suffix = "*.png;*.jpg;*.jpeg"
        elif typ == "video":
            suffix = "*.mp4;*.avi"
        files, filetype = QFileDialog.getOpenFileNames(self, "选择图片悬着视频", "", suffix)
        if len(files) == 0:
            return
        video_count, image_count = 0, 0
        project_name = self.configs["PROJECT_NAME"]
        for media in files:
            media_name = (media.split("/")[-1])
            type_ = self.end(media)
            # 判断是否存在存在即返回
            images = self.project[project_name]["images"]
            videos = self.project[project_name]["videos"]
            if ({media_name: media} in images) or ({media_name: media} in videos):
                continue
            if type_ in self.types["video"]:
                self.project[project_name]["videos"].append({media_name: media})
                _ = QTreeWidgetItem(self.videos_folder, [media_name])
                _.setIcon(0, QIcon(f"{self.cwd}/variable/type_icon/{type_}.png"))
                _.setToolTip(0, media)
                video_count += 1
            elif type_ in self.types["image"]:
                self.project[project_name]["images"].append({media_name: media})
                _ = QTreeWidgetItem(self.images_folder, [media_name])
                _.setIcon(0, QIcon(f"{self.cwd}/variable/type_icon/{type_}.png"))
                _.setToolTip(0, media)
                self.viewport.showImage(media)
                image_count += 1
        self.globalLog(f"共导入资源{len(files)}项，其中图像{image_count}项 视频{video_count}项!")
        QMessageBox.information(self, "导入资源", f"共导入资源{len(files)}项，其中图像{image_count}项 视频{video_count}项!",
                                QMessageBox.Yes | QMessageBox.No)

    def Stop(self):
        pass

    def Amplify(self):
        self.viewport.imager.zoomIn()

    def Reduce(self):
        self.viewport.imager.zoomOut()

    def Move(self):
        pass

    def Suitable(self):
        self.viewport.imager.resetTransform()

    def loadDevices(self, parent):
        """
        加载设备信息
        2023-7-24 无修改
        :param parent:self.tree
        :return:
        """
        # 初始化设备组-加载摄像头
        graph = FilterGraph()
        devices = graph.get_input_devices()
        # 加载网卡(暂不加载网卡)
        # self.iface = self.wifi.interfaces()
        # for item in self.iface:
        #     devices.append(item.name())
        for device in devices:
            _ = QTreeWidgetItem(parent, [device])
            _.setIcon(0, QIcon(f"{self.cwd}/variable/icons/camera.png"))

    def treeWidgetInit(self):
        """
        tree视图的初始化、设置样式等
        2023-7-24 无修改
        :return:
        """
        # self.tree.setStyle(QStyleFactory.create("windows"))
        self.tree.setHeaderHidden(True)
        # do 设置列数
        self.tree.setColumnCount(1)
        # 设置、右键菜单的初始化
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.treeRightClick)
        self.tree.clicked.connect(self.onTreeClicked)
        self.tree.doubleClicked.connect(self.onTreedoubleClicked)
        # self.tree.expandAll()

    def capture(self):
        """
        opencv捕捉摄像头画片
        2023-7-24 无修改
        :return:
        """
        ret, frame = self.cap.read()
        if ret:
            self.plotRgbMap(frame, stream=True)
            if self.Globals["LOADMODELFINISH"]:
                self.Globals["CAMERASTREAM"] = [frame]
                try:
                    self.viewport.showImage("./workspace/results/predict/current.png")
                except:
                    pass
            else:
                self.viewport.showImage(self.cv2Pixmap(frame))

    def cv2Pixmap(self, cvimg):
        """
        静态函数-将opencv捕捉到的画面想换成位图
        2023-7-24 无修改
        :param cvimg:
        :return:
        """
        height, width, depth = cvimg.shape
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        qimage = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)  # 转换成QImage
        pixmap = QPixmap(qimage).scaled(qimage.width(), qimage.height())  # 转换成QPixmap
        return pixmap

    def onTreeClicked(self):
        pass

    def plotRgbMap(self, path, stream=False):
        try:
            # 读取图像
            image = path
            if not stream:
                image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
                # 修改中文路径报错问题
                # image = cv2.imread(path)
            # 将图像转换为灰度图像
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            self.rgb_plot.clear()
            # # 计算直方图
            hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
            # # 将直方图数组转换为一维数组
            hist = np.ravel(hist)
            gary_plot = pg.PlotCurveItem(hist, stepMode=False, fillLevel=0, brush=(0, 0, 255, 80))
            # 将RGB图像数据转换为三个通道的数据
            red_channel = image_rgb[:, :, 0].flatten()
            green_channel = image_rgb[:, :, 1].flatten()
            blue_channel = image_rgb[:, :, 2].flatten()
            r = cv2.calcHist([red_channel], [0], None, [256], [0, 256])
            g = cv2.calcHist([green_channel], [0], None, [256], [0, 256])
            b = cv2.calcHist([blue_channel], [0], None, [256], [0, 256])
            # 绘制RGB三色图
            ps = 2
            try:
                ps = int(self.ui.plot_pensize.text())
            except:
                ps = 2
            r_plot = pg.PlotCurveItem(np.ravel(r), pen=pg.mkPen(width=ps, color='r'), name='Red')
            g_plot = pg.PlotCurveItem(np.ravel(g), pen=pg.mkPen(width=ps, color='g'), name='Green')
            b_plot = pg.PlotCurveItem(np.ravel(b), pen=pg.mkPen(width=ps, color='b'), name='Blue')
            gy_plot = pg.PlotCurveItem(hist, pen=pg.mkPen(width=ps, color="#000000", name='gray'))
            if self.rgb_draw_mode.currentIndex() == 0:
                self.rgb_plot.addItem(gary_plot)
                self.globalLog(f"绘制:'{path.split('/')[-1]}'的灰度直方图.")
            elif self.rgb_draw_mode.currentIndex() == 1:
                self.rgb_plot.addItem(r_plot)
                self.rgb_plot.addItem(g_plot)
                self.rgb_plot.addItem(b_plot)
                self.globalLog(f"绘制:'{path.split('/')[-1]}'的RGB通道直方图.")
            elif self.rgb_draw_mode.currentIndex() == 2:
                self.rgb_plot.addItem(r_plot)
                self.rgb_plot.addItem(g_plot)
                self.rgb_plot.addItem(b_plot)
                self.rgb_plot.addItem(gy_plot)
                self.globalLog(f"绘制:'{path.split('/')[-1]}'的灰度、RGB通道直方图.")
        except:
            pass

    def onTreedoubleClicked(self):
        """
        tree的双击处理事件
        2023-7-24 无修改
        :return:
        """
        # 湖片区当前的item和item上的字符串
        item = self.tree.currentItem()
        text = item.text(0)
        if item.parent() is self.devices_folder:
            self.videoPause()
            index = self.devices_folder.indexOfChild(item)
            self.cap = cv2.VideoCapture(index)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.ui.status.showMessage(f"已经准备好接入视频流FPS(MAX):{fps}.", 5000)
            self.start_camera.setEnabled(True)
            # 打开摄像头
            self.startCamera(index)
            self.ui.center.setCurrentIndex(0)
        elif self.end(item.toolTip(0)) in self.types["image"]:
            # 关闭视频播放
            self.Globals["VIEW_MODE"] = "IMAGE"
            self.pause_play.setEnabled(False)

            self.videoPause()
            self.capture_camera_timer.stop()  # 关闭摄像头读取
            self.stopCamera()  # 关闭摄像头读取
            self.viewport.showImage(item.toolTip(0))
            # 绘制图像灰度直方图
            self.plotRgbMap(item.toolTip(0))
            self.image_index = self.images_folder.indexOfChild(item)
            # 当前对象
            self.ui.pre_close_image.setText(item.toolTip(0))
            self.ui.pre_measure_image.setText(item.toolTip(0))
            # 这里显示图片的同时展示图片的消息
            # image = cv2.imread(item.toolTip(0))
            # 修改中文路径报错
            image = cv2.imdecode(np.fromfile(item.toolTip(0), dtype=np.uint8), -1)
            # image = cv2.imdecode(np.fromfile(item.toolTip(0)), cv2.IMREAD_UNCHANGED)
            self.info_content.setText(f"原始大小:{image.shape}")
            self.ui.center.setCurrentIndex(0)

        elif self.end(item.toolTip(0)) in self.types["video"]:
            self.Globals["VIEW_MODE"] = "VIDEO"
            self.pause_play.setEnabled(True)
            self.pause_play.setIcon(QIcon("variable/icons/pause.png"))

            self.capture_camera_timer.stop()
            self.stopCamera()
            self.viewport.showVideo(item.toolTip(0))
            self.video_index = self.videos_folder.indexOfChild(item)
            self.ui.center.setCurrentIndex(0)
        # 加载文本数据
        elif self.end(item.toolTip(0)) in self.types["text"]:
            self.capture_camera_timer.stop()
            self.stopCamera()
            self.videoPause()
            # 显示文本编辑器器
            text = self.loadText(item.text(0))
            if item.text(0) not in self.alltabs:
                self.alltabs.append(item.text(0))
                # 全局编辑器
                self.editor = Editor(self)
                self.editor.setStyleSheet("QTextEdit{color:#000000;}")
                self.editor.setText(text)
                self.editor.textChanged.connect(self.saveText)
                self.ui.center.addTab(self.editor, QIcon(f"./variable/type_icon/{self.end(item.text(0))}.png"), item.text(0))
                self.ui.center.setCurrentIndex(len(self.alltabs)-1)
            else:
                #加1是因为默认有一个视口页面
                index = self.alltabs.index(item.text(0))
                self.ui.center.setCurrentIndex(index)

    def saveText(self):
        index = self.ui.center.currentIndex()
        filename = self.ui.center.tabText(index)
        path = f"{self.configs['PROJECT_PATH']}/{filename}"
        with open(path,"w",encoding="utf-8")as fp:
            fp.write(self.editor.toPlainText())

    def loadText(self, name):
        """
        2023-7-24 无修改
        :param name:
        :return:
        """
        self.viewport.edit_file = f"{self.configs['PROJECT_PATH']}/{name}"
        with open(self.viewport.edit_file, "r", encoding="utf-8") as fp:
            return fp.read()

    def stopCamera(self):
        try:
            self.start_camera.setIcon(QIcon(f"{self.cwd}/variable/icons/play.png"))
            self.capture_camera_timer.stop()
            self.cap.release()
            self.start_camera.triggered.connect(lambda: self.startCamera(0))
        except Exception as e:
            pass

    def startCamera(self, index):
        try:
            self.cap = cv2.VideoCapture(index)
            self.start_camera.setIcon(QIcon(f"{self.cwd}/variable/icons/pause.png"))
            self.capture_camera_timer.start()
            self.start_camera.triggered.connect(self.stopCamera)
        except Exception as e:
            self.globalLog(f"Camera error:{e}", typ="error")
            self.poptipAnimate("Error in camera", "error")

    def updateDevice(self):
        # 先删除device文件夹夹下面的文件
        self.devices_folder.takeChildren()
        # 再加载
        self.loadDevices(self.devices_folder)
        self.global_info.setText("✅设备刷新成功.")
        QMessageBox.information(self, "设备更新", f"设备更新成功!共:{self.devices_folder.childCount()}个设备.",
                                QMessageBox.Yes | QMessageBox.No)

    def initdeviceMenu(self):
        self.device_menu = QMenu(self)
        self.update_device = QAction(QIcon(f"{self.cwd}/variable/icons/update.png"), u'刷新', self)
        self.update_device.triggered.connect(self.updateDevice)
        self.device_menu.addAction(self.update_device)

    def initRootMenu(self):
        self.root_menu = QMenu(self)
        self.infile = QAction(QIcon(f"{self.cwd}/variable/icons/import.png"), u'导入文件      Ctrl+I', self)
        self.infile.triggered.connect(self.addExsittoProject)
        self.root_menu.addAction(self.infile)

        self.delete_project = QAction(QIcon(f"{self.cwd}/variable/icons/clear.png"), u'删除项目', self)
        self.delete_project.triggered.connect(self.deleteProject)
        self.root_menu.addAction(self.delete_project)

    def initItemMenu(self):
        self.item_menu = QMenu(self)

        self.pridict = QAction(QIcon(f"{self.cwd}/variable/icons/start.png"), u'对象检测', self)
        self.pridict.triggered.connect(self.singlePredict)
        self.item_menu.addAction(self.pridict)
        if not self.Globals["LOADMODELFINISH"]:
            self.pridict.setEnabled(False)

        self.contour = QAction(QIcon(f"{self.cwd}/variable/icons/scratch.png"), u'划痕检测', self)
        self.contour.triggered.connect(self.contourDetection)
        self.item_menu.addAction(self.contour)

        self.delete_item = QAction(QIcon(f"{self.cwd}/variable/icons/delete.png"), u'删除', self)
        self.delete_item.triggered.connect(self.deleteTreeItem)
        self.item_menu.addAction(self.delete_item)

        self.delete_all_item = QAction(QIcon(f"{self.cwd}/variable/icons/clear.png"), u'删除', self)
        self.delete_all_item.triggered.connect(self.deleteTreeAllItem)
        self.item_menu.addAction(self.delete_all_item)


    def predOrtrainw(self, index):
        if index == 0:
            pass
        elif index == 1:
            pass
            model_name = self.ui.menu_models.actions()[self.configs["CURRENTMODEL"]].text()
            self.ui.train_model_path.setText(f"{self.cwd}/variable/models/{model_name}")
            self.ui.train_configs.setText(f"{self.cwd}/workspace/train/config.yaml")


    def terminateTrainWork(self):
        reply = QMessageBox.critical(self, "中断训练", f"是否终止本次训练任务!", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        try:
            self.train_proc.terminate()
            # # 开启更新定时器
            self.train_timer.stop()
            self.globalLog(f"任务已经中断!")
        except Exception as e:
            self.globalLog(f"中断失败，请检查是否已经开始了训练或者训练已停止:{e}")


    def startTrainWork(self):
        env = {}
        self.Globals["TRAIN_X"] = []
        self.Globals["TRAIN_Y"] = []
        self.Globals['CURRENTEPOCH'] = 0
        self.last_text = self.ui.log.toHtml()
        env["EPOCHS"] = int(self.ui.train_epoch.text())
        env["RAW"] = self.ui.train_model_path.text()
        env["YAML"] = self.ui.train_configs.text()
        if not env["EPOCHS"] or not env["RAW"] or not env["YAML"]:
            QMessageBox.critical(self, "训练参数", f"训练参数错误，请重新设置!", QMessageBox.Yes | QMessageBox.No)
            return
        self.train_proc = multiprocessing.Process(target=train, args=(self.Globals, env))
        self.train_proc.start()
        # # 开启更新定时器
        self.train_timer.start()
        self.globalLog(f"训练任务已启动,Epoch:{env['EPOCHS']}")

    def trainState(self):
        # 设置训练进度
        class_loss = 100.00
        compare = ">"
        try:
            class_loss = self.Globals['TRAIN_Y'][2][-1]
        except:
            pass
        if class_loss < float(self.ui.min_loss.text()):
            compare = "<"
            self.train_timer.stop()
            self.train_proc.terminate()
            self.train_proc.join()
        epc = int(self.ui.train_epoch.text())
        current_text = self.last_text + f"<p style='color:#7F00FF'><b>训练进度:[{round((self.Globals['CURRENTEPOCH'] * 100 / epc), 2)}%] " \
                                        f"class loss:{round(class_loss, 3)}{compare}{round(float(self.ui.min_loss.text()), 3)}</b></p><br>"
        self.ui.log.setHtml(current_text)
        self.ui.log.moveCursor(QTextCursor.End)
        # 绘制train plot
        if len(self.Globals["TRAIN_X"]) < 2:
            self.viewport.plotTrainDatas([1, 2], [[0, 0], [0, 0], [0, 0], [0, 0]])
            return
        self.viewport.plotTrainDatas(self.Globals["TRAIN_X"], self.Globals["TRAIN_Y"])
        # 检查是否训练完成
        if not self.train_proc.is_alive():
            self.globalLog(f"训练完成，请查看:./workspace/train")
            self.train_timer.stop()

    def singlePredict(self, tomail=False):
        self.Globals["PREDICT_INFO"] = []
        self.Sources.append(self.tree.currentItem().toolTip(0))
        self.predict_timer.start()
        self.Globals["TOMAIL"] = False
        if tomail:
            self.Globals["TOMAIL"] = True

    def globalAnsysis(self):
        if not self.Globals["LOADMODELFINISH"]:
            QMessageBox.warning(self, "模型加载", f"还没有加载模型，请先加载模型！", QMessageBox.Yes | QMessageBox.No)
            self.globalLog(f"还没有加载权重!", typ="warning")
            return
        self.Globals["PREDICT_INFO"] = []
        for i in range(self.images_folder.childCount()):
            self.Sources.append(self.images_folder.child(i).toolTip(0))
        self.predict_timer.start()

    def changeModel(self, model_path, index):
        # 如果进程处于活跃状态，先将其中断在重新开启
        self.Globals["MODEL"] = model_path
        # 判断模型是否加载成功
        self.Globals["LOADMODELFINISH"] = False

        try:
            self.predict_proc.terminate()
            self.predict_proc.join()
        except Exception as e:
            self.globalLog(f"Change Model error:{e}",typ="warning")

        self.predict_proc = multiprocessing.Process(target=Predict, args=(self.Sources, self.Results, self.Globals))
        self.predict_proc.start()

        self.load_timer.start()
        self.configs["CURRENTMODEL"] = index
        self.progress.show()
        self.progress.setRange(0, 0)
        model_name = model_path.split('/')[-1]
        self.global_info.setText(f"🚀正在加载模型:{model_name}")
        self.setCurrentModelTip(model_name)

    def loadState(self):
        if self.Globals["LOADMODELFINISH"]:
            self.load_timer.stop()
            self.progress.hide()
            model_name = self.current_model_action.text()
            self.global_info.setText(f"✅模型:{model_name}加载成功.")

    def predictState(self):
        if self.Globals["VIDEOMODE"]:
            self.viewport.showImage("workspace/results/predict/current.png")
        if len(self.Results) > 0:
            if self.Results[0] == "finished":
                self.predict_timer.stop()
                del self.Results[:]
                return
            data = self.Results[0]
            row = self.ui.result.rowCount()
            self.ui.result.setRowCount(row + 1)
            self.ui.result.setRowHeight(row, 18)
            name_item = QTableWidgetItem(data["name"])  # 对象栏
            name_item.setToolTip(f"{self.cwd}/workspace/results/predict/{data['name']}")
            brief_item = QTableWidgetItem(data["brief"])  # 描述栏
            brief_item.setToolTip(f"{self.cwd}/workspace/results/predict/{data['name']}")
            if data["brief"] != "":
                name_item.setIcon(QIcon(f"{self.cwd}/variable/icons/right.png"))
            else:
                brief_item.setText("暂无描述.")
                name_item.setIcon(QIcon(f"{self.cwd}/variable/icons/error.png"))
            self.ui.result.setItem(row, 0, name_item)
            self.ui.result.setItem(row, 1, brief_item)
            self.ui.result.setCurrentItem(name_item)
            curt = self.ui.result.currentItem().toolTip()
            # 发送洁厕信息
            try:
                if self.Globals["TOMAIL"] and not self.Globals["VIDEOMODE"]:
                    self.mailSendWithImage("Multi-MODS",f"'{data['name']}'检测完成！结果如下:{data['brief']}",curt)
            except Exception as e:
                pass
            # 打印日志
            self.globalLog(f"'{data['name']}'检测完成.")
            self.viewport.showImage(curt)
            self.Results.pop(0)


    def log(self, object, content, typ="success", local=False):
        COLOR = ""
        if typ == "error":
            COLOR = "color:#FF0000;"
            self.log_tyes[2] += 1
            self.warning_timer.start()
        elif typ == "warning":
            COLOR = "color:#FF8C00;"
            self.log_tyes[1] += 1
        elif typ == "success":
            COLOR = "color:#228B22;"
            self.log_tyes[0] += 1
        current = datetime.datetime.now().strftime('%H:%M:%S')
        format = f"<span style='{COLOR}'><b>{current} @{typ} -[{object}]- {content}</b></span><br>\n"
        self.ui.log.insertHtml(format)
        self.ui.log.moveCursor(QTextCursor.End)
        self.setLogTypes(counts=self.log_tyes)
        # 写入本地文件
        if local:
            with open(f"{self.configs['PROJECT_PATH']}/Log.html", "a+", encoding="utf-8") as fp:
                fp.write(format)

    def contourDetection(self):
        item = self.tree.currentItem()
        # result = closePredict(item.toolTip(0))
        # pixmap = self.cv2Pixmap(result)
        # self.viewport.showImage(pixmap)

    def addExsittoProject(self):
        pass

    
    def deleteTreeAllItem(self):
        """
        删除tree中所有的item
        :return:
        """
        # 批量删除图片
        current_item = self.tree.currentItem()
        project_name = self.configs["PROJECT_NAME"]
        image_count = self.images_folder.childCount()
        if current_item.parent() is self.images_folder:
            for _ in range(image_count):
                item = self.images_folder.child(0)
                fname = item.text(0)
                self.images_folder.removeChild(item)
                self.project[project_name]["images"].remove({fname: item.toolTip(0)})
        # 批量删除视频
        video_count = self.videos_folder.childCount()
        if current_item.parent() is self.videos_folder:
            for _ in range(video_count):
                item = self.videos_folder.child(0)
                fname = item.text(0)
                self.videos_folder.removeChild(item)
                self.project[project_name]["videos"].remove({fname: item.toolTip(0)})

        

    def deleteTreeItem(self):
        """
        删除tree中的item
        :return:
        """
        item = self.tree.currentItem()
        try:
            reply = QMessageBox.warning(self, u"删除", u"同时删除本地文件？",
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                os.remove(item.toolTip(0))
            elif reply == QMessageBox.Cancel:
                return
            parent = item.parent()
            parent.removeChild(item)
            fname = item.text(0)
            typ = self.end(item.text(0))
            project_name = self.configs["PROJECT_NAME"]
            # 从本地数据库里面删除
            if typ in self.types["image"]:
                self.project[project_name]["images"].remove({fname: item.toolTip(0)})
            elif typ in self.types["video"]:
                self.project[project_name]["videos"].remove({fname: item.toolTip(0)})
        except Exception as e:
            QMessageBox.critical(self, "删除错误", f"{e}", QMessageBox.Yes | QMessageBox.Cancel)
            self.poptipAnimate("Delete error", "error")

    def treeRightClick(self, pos):
        """
        右键菜单
        :param pos:
        :return:
        """
        self.initRootMenu()
        self.initItemMenu()
        self.initdeviceMenu()
        try:
            # 不允许默认文件夹和项目文件夹、以及设备文件夹右键菜单
            current_dir = self.tree.itemAt(pos)
            if current_dir is self.root_folder:
                self.root_menu.popup(QCursor.pos())  # 项目的根目录
            elif current_dir is self.devices_folder:
                self.device_menu.popup(QCursor.pos())  # 项目的设备目录
            elif (current_dir.parent()).parent() is self.root_folder:
                self.item_menu.popup(QCursor.pos())  # 项目的子项
        except Exception as e:
            pass

    def loadSettings(self):
        """
        加载设置信息：从本地文件加载
        :return:
        """
        with open(f"{self.cwd}/variable/configs/config.json", 'r', encoding="utf-8") as fp:
            self.configs = json.load(fp)
            # 初始化设置界面
            self.setting_face.ui.quit_save.setChecked(self.configs["QUITSAVE"])
            self.setting_face.ui.pre_loadm.setChecked(self.configs["PRELOAD"])
            self.setting_face.ui.gpu_support.setChecked(self.configs["GPU"])
            self.setting_face.ui.workspace_path.setText(self.configs["WORKSPACE"])
            self.setting_face.ui.model_path.setText(self.configs["MODELPATH"])
            self.setting_face.ui.python_path.setText(self.configs["PYTHON"])
            self.setting_face.ui.process_log.setChecked(self.configs["SOFTLOG"])
            self.setting_face.ui.guideface.setChecked(self.configs["GUIDE"])
            self.setting_face.ui.start_face.setChecked(self.configs["STARTFACE"])
            self.setting_face.ui.save_log_local.setChecked(self.configs["LOCALLOG"])
            self.setting_face.ui.auto_close.setChecked(self.configs["AUTOCLOSE"])
            self.setting_face.ui.plot_pensize.setText(self.configs["PLOTPENSIZE"])

            return self.configs

    def saveConfigs(self, configs):
        """
        保存设置信息到本地
        :param configs:字典
        :return:
        """
        configs["WORKSPACE"] = self.setting_face.ui.workspace_path.text()
        configs["MODELPATH"] = self.setting_face.ui.model_path.text()
        configs["PYTHON"] = self.setting_face.ui.python_path.text()
        configs["QUITSAVE"] = self.setting_face.ui.quit_save.isChecked()
        configs["PRELOAD"] = self.setting_face.ui.pre_loadm.isChecked()
        configs["GPU"] = self.setting_face.ui.gpu_support.isChecked()
        configs["SOFTLOG"] = self.setting_face.ui.process_log.isChecked()
        configs["LOCALLOG"] = self.setting_face.ui.save_log_local.isChecked()
        configs["AUTOCLOSE"] = self.setting_face.ui.auto_close.isChecked()
        configs["PLOTPENSIZE"] = self.setting_face.ui.plot_pensize.text()
        configs["GUIDE"] = self.setting_face.ui.guideface.isChecked()
        configs["STARTFACE"] = self.setting_face.ui.start_face.isChecked()

        with open(f"{self.cwd}/variable/configs/config.json", "w", encoding="utf-8") as fp:
            settings = json.dumps(configs, indent=0, ensure_ascii=False)
            fp.write(settings)
            self.poptipAnimate("设置保存成功!")

    def saveProject(self, project):
        # 遍历两个文件夹保存信息
        path = f"{self.configs['PROJECT_PATH']}/{self.configs['PROJECT_NAME']}.ylbpj"
        # 写入文档
        with open(path, "w", encoding="utf-8") as fp:
            project_ = json.dumps(project, indent=0, ensure_ascii=False)
            fp.write(project_)

    def loadProjectData(self, path):
        with open(path, "r+", encoding="utf-8") as fp:
            return json.load(fp)

    def end(self, str: str):
        if "." in str:
            return str.split(".")[-1]
        else:
            return "f"

    def loadFileType(self):
        with open(f"{self.cwd}/variable/configs/types.json", "r", encoding="utf-8") as fp:
            return json.load(fp)

    def openProject(self, path=None, index=0):
        """
        打开项目，如果没有给路径则跳出对话框
        :param path:
        :return:
        """
        if not path:
            path, filetype = QFileDialog.getOpenFileName(self, "选择项目文件", self.configs["WORKSPACE"], "*.ylbpj")
            if len(path) == 0:
                return
        try:
            project_name = (path.split("/")[-1]).split(".")[0]
            project_path = os.path.dirname(path)
            if project_name == self.configs["PROJECT_NAME"] and \
                    self.tree.topLevelItemCount() > 1:
                pass
            self.configs["PROJECT_PATH"] = project_path
            self.configs["PROJECT_NAME"] = project_name
            self.project = self.loadProjectData(path)
            # 如果加载成功就删除原来的tree
            for _ in range(self.tree.topLevelItemCount()):
                self.tree.takeTopLevelItem(0)
            # 然后重新创建
            self.createDefaultFolder(name=project_name)
            # 由于是加载项目文件，所以要加载信息
            self.projectMediaData()
            # 展开
            self.tree.expandAll()
            # 默认显示第一张图片
            if self.images_folder.childCount() > 0:
                path = self.images_folder.child(0).toolTip(0)
                self.viewport.showImage(path)
            else:
                self.viewport.showImage("none")
            # 如果guide face显示就关闭
            if not self.guide_face.isHidden():
                self.guide_face.close()

        except Exception as e:
            ret = QMessageBox.critical(self, "打开项目", f"erorr:{e} 项目文件已损坏! 是否删除？",
                                       QMessageBox.Yes | QMessageBox.No)
            self.global_info.setText(f"❌未打开项目:{project_name}.")
            self.poptipAnimate("Open error", "error")
            if ret == QMessageBox.Yes:
                self.guide_face.ui.recently.takeItem(index)
                self.guide_face.ui.recently.update()
                self.configs["RECENT_PROJECT"].pop(index)
            return

    def saveDatas(self):
        try:
            # 保存项目和设置
            self.saveProject(self.project)
            self.saveConfigs(self.configs)
            self.global_info.setText("✅设置已保存.")
            self.poptipAnimate("保存成功", typ="normal")
        except Exception as e:
            print(e)
            self.global_info.setText(f"❌设置未保存.{e}")
            self.poptipAnimate("Error in saving", "error")

    def Help(self):
        pass

    def quitRelease(self):
        try:
            self.predict_proc.terminate()
            self.predict_proc.join()
        except Exception as e:
            pass
        try:
            self.labeling_proc.terminate()
            self.labeling_proc.join()
        except Exception as e:
            pass
        try:
            self.train_proc.terminate()
            self.train_proc.join()
        except Exception as e:
            pass

    def updateRecentProject(self):
        recently = {
            "NAME": self.configs["PROJECT_NAME"],
            self.configs["PROJECT_NAME"]: f"{self.configs['PROJECT_PATH']}/{self.configs['PROJECT_NAME']}.ylbpj"
        }
        if recently in self.configs["RECENT_PROJECT"]:
            index = self.configs["RECENT_PROJECT"].index(recently)
            self.configs["RECENT_PROJECT"].pop(index)
        self.configs["RECENT_PROJECT"].insert(0, recently)
        # 更新
        self.ui.menu_recently.clear()
        self.guide_face.ui.recently.clear()
        self.guide_face.ui.recently.setIconSize(QSize(32, 32))
        for item in self.configs["RECENT_PROJECT"]:
            action = QAction(item.get(item.get("NAME")), self)
            action.setIcon(QIcon("./variable/icons/project_icon.png"))
            self.ui.menu_recently.addAction(action)
            pro_item = QListWidgetItem()
            pro_item.setIcon(QIcon("./variable/icons/project_icon.png"))
            pro_item.setText(item.get(item.get("NAME")))
            # pro_item.setSizeHint(QSize(0, 32))
            self.guide_face.ui.recently.addItem(pro_item)


    def runPlugin(self, action):
        self.ui.menu_Tools.actions().index(action)
        if action is self.plugin_add_action:
            self.add_plugins_face.exec()

    def loadPlugins(self):
        with open(f"./variable/configs/plugins.json", "r", encoding="utf-8") as fp:
            self.plugins = json.load(fp)
            for plugin in self.plugins:
                plugin_action = QAction(self)
                plugin_action.setText(plugin["name"])
                plugin_action.setIcon(QIcon(f"./variable/plugins/{plugin['name']}/{plugin['icon']}"))

                self.ui.menu_Tools.addAction(plugin_action)
        if len(self.ui.menu_Tools.actions())>0:
            self.ui.menu_Tools.addSeparator()
        #添加默认按钮
        self.plugin_add_action = QAction(self)
        self.plugin_add_action.setText("管理插件")
        self.plugin_add_action.setIcon(QIcon(f"./variable/icons/plugin.png"))
        self.ui.menu_Tools.addAction(self.plugin_add_action)


    def closeEvent(self, event):
        reply = QMessageBox.warning(self, '管理员', "即将退出，请确保数据已保存！", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                # 保存设置的信息
                self.quitRelease()
                self.saveConfigs(self.configs)
                self.saveProject(self.project)
            except Exception as e:
                pass
            event.accept()
        else:
            event.ignore()

    # def resizeEvent(self, event):
    #     self.titleBar.setFixedWidth(self.width())

    # def changeEvent(self, event):
    #     if event.type() == QEvent.WindowStateChange:
    #         if self.isMinimized():
    #             pass
    #         elif self.isMaximized():
    #             self.titleBar.showmaxed = True
    #         elif self.isActiveWindow():
    #             self.titleBar.showmaxed = False
    #         else:
    #             self.titleBar.showmaxed = False
        # self.changeEvent(self, event)

    def eventFilter(self, object, event):
        if object == self.ui.commands and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Backspace:
                if self.ui.commands.textCursor().columnNumber() <= 3:
                    return True
            elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
                line = self.ui.commands.document().lineCount()
                current_command = self.ui.commands.document().findBlockByLineNumber(line - 1).text()
                command = current_command.replace(">>>", "")
                if command == "":
                    self.ui.commands.append(">>>")
                    return True
                try:
                    getattr(Windows, command)(self, )
                except Exception as e:
                    self.ui.commands.append(f"{e}")
                # 从新加入新行
                self.ui.commands.append(">>>")
                return True
            elif event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Right, Qt.Key_Left):
                return True
        elif object == self and event.type() == QEvent.MouseButtonPress:
            if self.configs["AUTOCLOSE"]:
                self.ui.predict_settings.close()

        return False

    def help(self):
        self.ui.commands.append("###")
        self.ui.commands.append("这是帮助文档")
        self.ui.commands.append("###")

    def restart(self):
        QApplication.quit()
        QProcess.startDetached(sys.executable, sys.argv)
        # subprocess.Popen([sys.executable] + sys.argv)


if __name__ == '__main__':
    freeze_support()
    #使用下面的方式一定程度上可以解决界面模糊问题--解决电脑缩放比例问题
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)

    # 欢迎页面
    # Start()
    # 主程序页面
    main = Windows()
    sys.exit(app.exec_())

