# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)
import ui.res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1019, 497)
        MainWindow.setMinimumSize(QSize(719, 297))
        icon = QIcon()
        icon.addFile(u":/res/images/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QSize(30, 30))
        self.action_info = QAction(MainWindow)
        self.action_info.setObjectName(u"action_info")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.combo_tv_list = QComboBox(self.groupBox_2)
        self.combo_tv_list.setObjectName(u"combo_tv_list")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_tv_list.sizePolicy().hasHeightForWidth())
        self.combo_tv_list.setSizePolicy(sizePolicy)
        self.combo_tv_list.setMinimumSize(QSize(0, 41))
        self.combo_tv_list.setMaximumSize(QSize(16777215, 41))
        self.combo_tv_list.setEditable(True)
        self.combo_tv_list.setMaxVisibleItems(20)
        self.combo_tv_list.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        self.verticalLayout_3.addWidget(self.combo_tv_list)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textEdit_keys_list = QTextEdit(self.groupBox)
        self.textEdit_keys_list.setObjectName(u"textEdit_keys_list")

        self.verticalLayout_2.addWidget(self.textEdit_keys_list)


        self.verticalLayout_4.addWidget(self.groupBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_model = QLabel(self.groupBox_3)
        self.label_model.setObjectName(u"label_model")
        font = QFont()
        font.setPointSize(15)
        self.label_model.setFont(font)

        self.verticalLayout_5.addWidget(self.label_model)

        self.label_key_no_loaded = QLabel(self.groupBox_3)
        self.label_key_no_loaded.setObjectName(u"label_key_no_loaded")
        self.label_key_no_loaded.setFont(font)

        self.verticalLayout_5.addWidget(self.label_key_no_loaded)

        self.label_key_success_loaded = QLabel(self.groupBox_3)
        self.label_key_success_loaded.setObjectName(u"label_key_success_loaded")
        self.label_key_success_loaded.setFont(font)

        self.verticalLayout_5.addWidget(self.label_key_success_loaded)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_clear_all = QPushButton(self.groupBox_3)
        self.pushButton_clear_all.setObjectName(u"pushButton_clear_all")
        icon1 = QIcon()
        icon1.addFile(u":/res/images/select_window_closed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_clear_all.setIcon(icon1)
        self.pushButton_clear_all.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.pushButton_clear_all)

        self.pushButton_clear_list = QPushButton(self.groupBox_3)
        self.pushButton_clear_list.setObjectName(u"pushButton_clear_list")
        icon2 = QIcon()
        icon2.addFile(u":/res/images/disabled_by_default.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_clear_list.setIcon(icon2)
        self.pushButton_clear_list.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.pushButton_clear_list)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton_start_load = QPushButton(self.groupBox_3)
        self.pushButton_start_load.setObjectName(u"pushButton_start_load")
        icon3 = QIcon()
        icon3.addFile(u":/res/images/save.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_start_load.setIcon(icon3)
        self.pushButton_start_load.setIconSize(QSize(40, 40))

        self.verticalLayout.addWidget(self.pushButton_start_load)


        self.verticalLayout_6.addLayout(self.verticalLayout)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)


        self.horizontalLayout_2.addWidget(self.groupBox_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_info.setText(QCoreApplication.translate("MainWindow", u"\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0434\u043e\u0441\u0442\u0443\u043f\u043d\u0443\u044e \u043c\u043e\u0434\u0435\u043b\u044c:", None))
        self.combo_tv_list.setCurrentText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0441\u0442\u043e \u0434\u043b\u044f \u043a\u043b\u044e\u0447\u0435\u0439:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u043d\u0435\u043b\u044c \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u0432:", None))
        self.label_model.setText(QCoreApplication.translate("MainWindow", u"\u041c\u043e\u0434\u0435\u043b\u044c:", None))
        self.label_key_no_loaded.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043b\u044e\u0447\u0435\u0439 \u043d\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043e:", None))
        self.label_key_success_loaded.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043b\u044e\u0447\u0435\u0439 \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043e:", None))
        self.pushButton_clear_all.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0432\u0441\u0451", None))
        self.pushButton_clear_list.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a", None))
        self.pushButton_start_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
    # retranslateUi

