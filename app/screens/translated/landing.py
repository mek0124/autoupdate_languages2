# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'landing.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QScrollArea,
    QSizePolicy, QStatusBar, QWidget)
import Icons_rc

class Ui_w_Landing(object):
    def setupUi(self, w_Landing):
        if not w_Landing.objectName():
            w_Landing.setObjectName(u"w_Landing")
        w_Landing.resize(800, 600)
        font = QFont()
        font.setPointSize(10)
        w_Landing.setFont(font)
        icon = QIcon()
        icon.addFile(u":/main/original.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        w_Landing.setWindowIcon(icon)
        self.actionRefresh = QAction(w_Landing)
        self.actionRefresh.setObjectName(u"actionRefresh")
        self.actionRefresh.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        self.actionExit = QAction(w_Landing)
        self.actionExit.setObjectName(u"actionExit")
        self.actionExit.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        self.centralwidget = QWidget(w_Landing)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.scroll_language_list = QScrollArea(self.frame_2)
        self.scroll_language_list.setObjectName(u"scroll_language_list")
        self.scroll_language_list.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 356, 475))
        self.scroll_language_list.setWidget(self.scrollAreaWidgetContents_5)

        self.gridLayout_3.addWidget(self.scroll_language_list, 1, 0, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.scroll_language_preview = QScrollArea(self.frame_3)
        self.scroll_language_preview.setObjectName(u"scroll_language_preview")
        self.scroll_language_preview.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 356, 475))
        self.scroll_language_preview.setWidget(self.scrollAreaWidgetContents_6)

        self.gridLayout_4.addWidget(self.scroll_language_preview, 1, 0, 1, 1)

        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_3, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        w_Landing.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(w_Landing)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        w_Landing.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(w_Landing)
        self.statusbar.setObjectName(u"statusbar")
        w_Landing.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionRefresh)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionExit)

        self.retranslateUi(w_Landing)

        QMetaObject.connectSlotsByName(w_Landing)
    # setupUi

    def retranslateUi(self, w_Landing):
        w_Landing.setWindowTitle(QCoreApplication.translate("w_Landing", u"Programming Languages Dictionary", None))
        self.actionRefresh.setText(QCoreApplication.translate("w_Landing", u"Refresh", None))
#if QT_CONFIG(shortcut)
        self.actionRefresh.setShortcut(QCoreApplication.translate("w_Landing", u"Ctrl+F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("w_Landing", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("w_Landing", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("w_Landing", u"Currently Known Languages", None))
        self.label_2.setText(QCoreApplication.translate("w_Landing", u"Language Information", None))
        self.menuMenu.setTitle(QCoreApplication.translate("w_Landing", u"Menu", None))
    # retranslateUi

