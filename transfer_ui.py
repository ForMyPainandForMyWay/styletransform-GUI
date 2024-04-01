# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPlainTextEdit, QPushButton,
                               QSizePolicy, QWidget)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.NonModal)
        Form.resize(1400, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"\u7b49\u7ebf"])
        Form.setFont(font)
        Form.setCursor(QCursor(Qt.CrossCursor))
        Form.setStyleSheet(u"")
        self.address_content_img = QPlainTextEdit(Form)
        self.address_content_img.setObjectName(u"address_content_img")
        self.address_content_img.setGeometry(QRect(20, 20, 331, 71))
        font1 = QFont()
        font1.setFamilies([u"Simplex_IV50"])
        font1.setPointSize(8)
        self.address_content_img.setFont(font1)
        self.address_content_img.setPlaceholderText(u"please input the address of the content picture")
        self.show_picture = QPushButton(Form)
        self.show_picture.setObjectName(u"show_picture")
        self.show_picture.setGeometry(QRect(1090, 200, 221, 81))
        font2 = QFont()
        font2.setFamilies([u"\u7b49\u7ebf"])
        font2.setPointSize(14)
        self.show_picture.setFont(font2)
        self.show_picture.setMouseTracking(False)
        self.show_picture.setAutoFillBackground(False)
        self.show_picture.setAutoDefault(False)
        self.address_style_img = QPlainTextEdit(Form)
        self.address_style_img.setObjectName(u"address_style_img")
        self.address_style_img.setGeometry(QRect(560, 20, 351, 71))
        self.address_style_img.setFont(font1)
        self.address_style_img.setCursorWidth(1)
        self.address_style_img.setPlaceholderText(u"please input the address of the style picture")
        self.content_img = QLabel(Form)
        self.content_img.setObjectName(u"content_img")
        self.content_img.setGeometry(QRect(20, 120, 431, 271))
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(20)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.content_img.sizePolicy().hasHeightForWidth())
        self.content_img.setSizePolicy(sizePolicy1)
        self.content_img.setTextFormat(Qt.MarkdownText)
        self.content_img.setPixmap(QPixmap(u"../ph/C.png"))
        self.content_img.setScaledContents(True)
        self.content_img.setIndent(100)
        self.content_img.setOpenExternalLinks(False)
        self.style_img = QLabel(Form)
        self.style_img.setObjectName(u"style_img")
        self.style_img.setGeometry(QRect(560, 120, 451, 271))
        self.style_img.setTextFormat(Qt.MarkdownText)
        self.style_img.setPixmap(QPixmap(u"../ph/S.png"))
        self.style_img.setScaledContents(True)
        self.style_img.setWordWrap(False)
        self.style_img.setIndent(100)
        self.style_img.setOpenExternalLinks(False)
        self.result_img = QLabel(Form)
        self.result_img.setObjectName(u"result_img")
        self.result_img.setGeometry(QRect(250, 500, 451, 271))
        self.result_img.setTextFormat(Qt.MarkdownText)
        self.result_img.setPixmap(QPixmap(u"../ph/R.png"))
        self.result_img.setScaledContents(False)
        self.result_img.setWordWrap(False)
        self.result_img.setIndent(100)
        self.result_img.setOpenExternalLinks(False)
        self.show_picture_2 = QPushButton(Form)
        self.show_picture_2.setObjectName(u"show_picture_2")
        self.show_picture_2.setGeometry(QRect(1090, 570, 221, 81))
        font3 = QFont()
        font3.setFamilies([u"\u7b49\u7ebf"])
        font3.setPointSize(11)
        self.show_picture_2.setFont(font3)
        self.set_time = QPushButton(Form)
        self.set_time.setObjectName(u"set_time")
        self.set_time.setGeometry(QRect(1150, 40, 101, 71))
        font4 = QFont()
        font4.setFamilies([u"Yu Gothic Light"])
        self.set_time.setFont(font4)
        self.set_time.setStyleSheet(u"")
        self.c_t_b = QPushButton(Form)
        self.c_t_b.setObjectName(u"c_t_b")
        self.c_t_b.setGeometry(QRect(350, 20, 101, 71))
        self.s_t_b = QPushButton(Form)
        self.s_t_b.setObjectName(u"s_t_b")
        self.s_t_b.setGeometry(QRect(910, 20, 101, 71))
        self.Clear = QPushButton(Form)
        self.Clear.setObjectName(u"Clear")
        self.Clear.setGeometry(QRect(1170, 750, 75, 23))

        self.retranslateUi(Form)

        self.show_picture.setDefault(False)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"There is no bug", None))
        self.show_picture.setText(QCoreApplication.translate("Form", u"Input pictures", None))
        self.content_img.setText("")
        self.style_img.setText("")
        self.result_img.setText("")
        self.show_picture_2.setText(QCoreApplication.translate("Form", u"Show me the picture", None))
        self.set_time.setText(QCoreApplication.translate("Form", u"Set time", None))
        self.c_t_b.setText(QCoreApplication.translate("Form", u"Content", None))
        self.s_t_b.setText(QCoreApplication.translate("Form", u"Style", None))
        self.Clear.setText(QCoreApplication.translate("Form", u"Clear", None))
    # retranslateUi
