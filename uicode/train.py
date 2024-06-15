# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'train.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(805, 520)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName("mdiArea")
        self.horizontalLayout.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.train_manager = QtWidgets.QDockWidget(MainWindow)
        self.train_manager.setObjectName("train_manager")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.prerdict_or_train = QtWidgets.QTabWidget(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.prerdict_or_train.setFont(font)
        self.prerdict_or_train.setObjectName("prerdict_or_train")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_8)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_7 = QtWidgets.QFrame(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.frame_7.setFont(font)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.frame_47 = QtWidgets.QFrame(self.frame_7)
        self.frame_47.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_47.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_47.setObjectName("frame_47")
        self.horizontalLayout_40 = QtWidgets.QHBoxLayout(self.frame_47)
        self.horizontalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_40.setSpacing(4)
        self.horizontalLayout_40.setObjectName("horizontalLayout_40")
        self.train_datas = QtWidgets.QTextBrowser(self.frame_47)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.train_datas.setFont(font)
        self.train_datas.setStyleSheet("QTextBrowser{\n"
"border:none;\n"
"\n"
"}")
        self.train_datas.setObjectName("train_datas")
        self.horizontalLayout_40.addWidget(self.train_datas)
        self.verticalLayout_18.addWidget(self.frame_47)
        self.frame_3 = QtWidgets.QFrame(self.frame_7)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_27 = QtWidgets.QLabel(self.frame_3)
        self.label_27.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_2.addWidget(self.label_27)
        self.label_23 = QtWidgets.QLabel(self.frame_3)
        self.label_23.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_2.addWidget(self.label_23)
        self.train_epoch = QtWidgets.QSpinBox(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.train_epoch.sizePolicy().hasHeightForWidth())
        self.train_epoch.setSizePolicy(sizePolicy)
        self.train_epoch.setMinimumSize(QtCore.QSize(0, 0))
        self.train_epoch.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.train_epoch.setFont(font)
        self.train_epoch.setMaximum(1000)
        self.train_epoch.setProperty("value", 100)
        self.train_epoch.setObjectName("train_epoch")
        self.horizontalLayout_2.addWidget(self.train_epoch)
        self.label_24 = QtWidgets.QLabel(self.frame_3)
        self.label_24.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setWordWrap(False)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_2.addWidget(self.label_24)
        self.min_loss = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.min_loss.setMinimumSize(QtCore.QSize(0, 26))
        self.min_loss.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.min_loss.setFont(font)
        self.min_loss.setProperty("value", 0.5)
        self.min_loss.setObjectName("min_loss")
        self.horizontalLayout_2.addWidget(self.min_loss)
        self.verticalLayout_18.addWidget(self.frame_3)
        self.frame_38 = QtWidgets.QFrame(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.frame_38.setFont(font)
        self.frame_38.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_38.setObjectName("frame_38")
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout(self.frame_38)
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_33.setSpacing(4)
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.train_model_path = QtWidgets.QLineEdit(self.frame_38)
        self.train_model_path.setMinimumSize(QtCore.QSize(0, 28))
        self.train_model_path.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.train_model_path.setFont(font)
        self.train_model_path.setObjectName("train_model_path")
        self.horizontalLayout_33.addWidget(self.train_model_path)
        self.select_train_model_path = QtWidgets.QPushButton(self.frame_38)
        self.select_train_model_path.setMinimumSize(QtCore.QSize(100, 0))
        self.select_train_model_path.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.select_train_model_path.setFont(font)
        self.select_train_model_path.setStyleSheet("QPushButton{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(125, 125, 125);\n"
"    color: rgb(255, 255, 255);\n"
"    border:none;\n"
"    height:28px;\n"
"}\n"
"QPushButton:hover{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(111, 111, 111);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}\n"
"QPushButton:pressed{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(86, 86, 86);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}")
        self.select_train_model_path.setObjectName("select_train_model_path")
        self.horizontalLayout_33.addWidget(self.select_train_model_path)
        self.verticalLayout_18.addWidget(self.frame_38)
        self.frame_37 = QtWidgets.QFrame(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.frame_37.setFont(font)
        self.frame_37.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_37.setObjectName("frame_37")
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout(self.frame_37)
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 4)
        self.horizontalLayout_32.setSpacing(4)
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.train_configs = QtWidgets.QLineEdit(self.frame_37)
        self.train_configs.setMinimumSize(QtCore.QSize(0, 28))
        self.train_configs.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.train_configs.setFont(font)
        self.train_configs.setObjectName("train_configs")
        self.horizontalLayout_32.addWidget(self.train_configs)
        self.select_train_configs = QtWidgets.QPushButton(self.frame_37)
        self.select_train_configs.setMinimumSize(QtCore.QSize(100, 0))
        self.select_train_configs.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.select_train_configs.setFont(font)
        self.select_train_configs.setStyleSheet("QPushButton{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(125, 125, 125);\n"
"    color: rgb(255, 255, 255);\n"
"    border:none;\n"
"    height:28px;\n"
"}\n"
"QPushButton:hover{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(111, 111, 111);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}\n"
"QPushButton:pressed{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(86, 86, 86);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}")
        self.select_train_configs.setObjectName("select_train_configs")
        self.horizontalLayout_32.addWidget(self.select_train_configs)
        self.verticalLayout_18.addWidget(self.frame_37)
        self.frame_28 = QtWidgets.QFrame(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.frame_28.setFont(font)
        self.frame_28.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_28.setObjectName("frame_28")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout(self.frame_28)
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 4)
        self.horizontalLayout_26.setSpacing(4)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.input_images = QtWidgets.QPushButton(self.frame_28)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.input_images.setFont(font)
        self.input_images.setStyleSheet("QPushButton{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(125, 125, 125);\n"
"    color: rgb(255, 255, 255);\n"
"    border:none;\n"
"    height:28px;\n"
"}\n"
"QPushButton:hover{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(111, 111, 111);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}\n"
"QPushButton:pressed{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(86, 86, 86);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}")
        self.input_images.setObjectName("input_images")
        self.horizontalLayout_26.addWidget(self.input_images)
        self.open_labeling = QtWidgets.QPushButton(self.frame_28)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.open_labeling.setFont(font)
        self.open_labeling.setStyleSheet("QPushButton{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(125, 125, 125);\n"
"    color: rgb(255, 255, 255);\n"
"    border:none;\n"
"    height:28px;\n"
"}\n"
"QPushButton:hover{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(111, 111, 111);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}\n"
"QPushButton:pressed{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(86, 86, 86);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}")
        self.open_labeling.setObjectName("open_labeling")
        self.horizontalLayout_26.addWidget(self.open_labeling)
        self.pre_check = QtWidgets.QPushButton(self.frame_28)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pre_check.setFont(font)
        self.pre_check.setStyleSheet("QPushButton{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(125, 125, 125);\n"
"    color: rgb(255, 255, 255);\n"
"    border:none;\n"
"    height:28px;\n"
"}\n"
"QPushButton:hover{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(111, 111, 111);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}\n"
"QPushButton:pressed{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(86, 86, 86);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}")
        self.pre_check.setObjectName("pre_check")
        self.horizontalLayout_26.addWidget(self.pre_check)
        self.terminate_train = QtWidgets.QPushButton(self.frame_28)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.terminate_train.setFont(font)
        self.terminate_train.setStyleSheet("QPushButton{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(255, 0, 0);\n"
"    color: rgb(255, 255, 255);\n"
"    border:none;\n"
"    height:28px;\n"
"}\n"
"QPushButton:hover{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(158, 0, 0);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}\n"
"QPushButton:pressed{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(255, 0, 0);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}")
        self.terminate_train.setObjectName("terminate_train")
        self.horizontalLayout_26.addWidget(self.terminate_train)
        self.start_train = QtWidgets.QPushButton(self.frame_28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_train.sizePolicy().hasHeightForWidth())
        self.start_train.setSizePolicy(sizePolicy)
        self.start_train.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.start_train.setFont(font)
        self.start_train.setStyleSheet("QPushButton{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(0, 172, 83);\n"
"    color: rgb(255, 255, 255);\n"
"    border:none;\n"
"    height:28px;\n"
"}\n"
"QPushButton:hover{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(0, 134, 67);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}\n"
"QPushButton:pressed{\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: rgb(0, 172, 83);\n"
"    color: rgb(255, 255, 255);\n"
"    height:28px;\n"
"}")
        self.start_train.setObjectName("start_train")
        self.horizontalLayout_26.addWidget(self.start_train)
        self.horizontalLayout_26.setStretch(0, 1)
        self.horizontalLayout_26.setStretch(1, 1)
        self.horizontalLayout_26.setStretch(2, 1)
        self.horizontalLayout_26.setStretch(3, 1)
        self.horizontalLayout_26.setStretch(4, 1)
        self.verticalLayout_18.addWidget(self.frame_28)
        self.verticalLayout_2.addWidget(self.frame_7)
        self.prerdict_or_train.addTab(self.tab_8, "")
        self.verticalLayout.addWidget(self.prerdict_or_train)
        self.train_manager.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.train_manager)
        self.train_terminal = QtWidgets.QDockWidget(MainWindow)
        self.train_terminal.setObjectName("train_terminal")
        self.dockWidgetContents_5 = QtWidgets.QWidget()
        self.dockWidgetContents_5.setObjectName("dockWidgetContents_5")
        self.frame_48 = QtWidgets.QFrame(self.dockWidgetContents_5)
        self.frame_48.setGeometry(QtCore.QRect(460, 10, 102, 112))
        self.frame_48.setMinimumSize(QtCore.QSize(100, 0))
        self.frame_48.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_48.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_48.setObjectName("frame_48")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.frame_48)
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 4)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.train_terminal.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.train_terminal)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.prerdict_or_train.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "文件(F)"))
        self.label_27.setText(_translate("MainWindow", "参数设置"))
        self.label_23.setText(_translate("MainWindow", "Epoch"))
        self.train_epoch.setStatusTip(_translate("MainWindow", "迭代次数"))
        self.label_24.setText(_translate("MainWindow", "Loss"))
        self.min_loss.setStatusTip(_translate("MainWindow", "类型损失最小值"))
        self.train_model_path.setPlaceholderText(_translate("MainWindow", "模型结构(*.yaml;*.pt)"))
        self.select_train_model_path.setStatusTip(_translate("MainWindow", "选中模型"))
        self.select_train_model_path.setText(_translate("MainWindow", "选择"))
        self.train_configs.setPlaceholderText(_translate("MainWindow", "类文件(*.yaml)"))
        self.select_train_configs.setStatusTip(_translate("MainWindow", "选择类文件"))
        self.select_train_configs.setText(_translate("MainWindow", "选择"))
        self.input_images.setText(_translate("MainWindow", "导入"))
        self.open_labeling.setText(_translate("MainWindow", "标定"))
        self.pre_check.setText(_translate("MainWindow", "检查"))
        self.terminate_train.setText(_translate("MainWindow", "中断"))
        self.start_train.setText(_translate("MainWindow", "开始训练"))
        self.prerdict_or_train.setTabText(self.prerdict_or_train.indexOf(self.tab_8), _translate("MainWindow", "训练"))
