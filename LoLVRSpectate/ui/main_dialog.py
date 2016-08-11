# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_dialog.ui'
#
# Created: Thu Aug 11 17:44:20 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainDialog(object):
    def setupUi(self, MainDialog):
        MainDialog.setObjectName("MainDialog")
        MainDialog.resize(242, 128)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(MainDialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(MainDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.labelLoLRunning = QtGui.QLabel(MainDialog)
        self.labelLoLRunning.setStyleSheet("color: rgb(255, 0, 0)")
        self.labelLoLRunning.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelLoLRunning.setObjectName("labelLoLRunning")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.labelLoLRunning)
        self.label_3 = QtGui.QLabel(MainDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.labelVorpXRunning = QtGui.QLabel(MainDialog)
        self.labelVorpXRunning.setStyleSheet("color: rgb(255, 0, 0)")
        self.labelVorpXRunning.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelVorpXRunning.setObjectName("labelVorpXRunning")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.labelVorpXRunning)
        self.verticalLayout.addLayout(self.formLayout)
        self.pushButtonStart = QtGui.QPushButton(MainDialog)
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.verticalLayout.addWidget(self.pushButtonStart)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(MainDialog)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)

    def retranslateUi(self, MainDialog):
        MainDialog.setWindowTitle(QtGui.QApplication.translate("MainDialog", "LoLVRSpectate", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainDialog", "LoLVRSpectate", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainDialog", "League of Legends client:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLoLRunning.setText(QtGui.QApplication.translate("MainDialog", "Not Running", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainDialog", "VorpX:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelVorpXRunning.setText(QtGui.QApplication.translate("MainDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStart.setText(QtGui.QApplication.translate("MainDialog", "Start", None, QtGui.QApplication.UnicodeUTF8))

