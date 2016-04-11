# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lsst_explorer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_lsst_explorer(object):
    def setupUi(self, lsst_explorer):
        lsst_explorer.setObjectName(_fromUtf8("lsst_explorer"))
        lsst_explorer.setEnabled(True)
        lsst_explorer.resize(500, 542)
        lsst_explorer.setMinimumSize(QtCore.QSize(350, 0))
        self.verticalLayout_3 = QtGui.QVBoxLayout(lsst_explorer)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.PropertiesWidget = QtGui.QWidget(lsst_explorer)
        self.PropertiesWidget.setEnabled(False)
        self.PropertiesWidget.setObjectName(_fromUtf8("PropertiesWidget"))
        self.verticalLayout.addWidget(self.PropertiesWidget)
        self.InputWidget = QtGui.QWidget(lsst_explorer)
        self.InputWidget.setObjectName(_fromUtf8("InputWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.InputWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.InputWidget)
        self.label.setMaximumSize(QtCore.QSize(100, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.InputEdit = QtGui.QLineEdit(self.InputWidget)
        self.InputEdit.setEnabled(True)
        self.InputEdit.setObjectName(_fromUtf8("InputEdit"))
        self.gridLayout.addWidget(self.InputEdit, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.InputWidget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.DataIdEdit = QtGui.QLineEdit(self.InputWidget)
        self.DataIdEdit.setEnabled(True)
        self.DataIdEdit.setObjectName(_fromUtf8("DataIdEdit"))
        self.gridLayout.addWidget(self.DataIdEdit, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.InputWidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.ImageTypeEdit = QtGui.QLineEdit(self.InputWidget)
        self.ImageTypeEdit.setObjectName(_fromUtf8("ImageTypeEdit"))
        self.gridLayout.addWidget(self.ImageTypeEdit, 5, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.InputWidget)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.CatalogTypeEdit = QtGui.QLineEdit(self.InputWidget)
        self.CatalogTypeEdit.setObjectName(_fromUtf8("CatalogTypeEdit"))
        self.gridLayout.addWidget(self.CatalogTypeEdit, 7, 0, 1, 1)
        self.AcceptButton = QtGui.QPushButton(self.InputWidget)
        self.AcceptButton.setEnabled(True)
        self.AcceptButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.AcceptButton.setObjectName(_fromUtf8("AcceptButton"))
        self.gridLayout.addWidget(self.AcceptButton, 8, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.InputWidget)
        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(lsst_explorer)
        QtCore.QMetaObject.connectSlotsByName(lsst_explorer)

    def retranslateUi(self, lsst_explorer):
        lsst_explorer.setWindowTitle(_translate("lsst_explorer", "Form", None))
        self.label.setText(_translate("lsst_explorer", "Input Repository", None))
        self.label_2.setText(_translate("lsst_explorer", "DataId (Single Item only eg {\'vist\':100,\'ccd\':20})", None))
        self.label_3.setText(_translate("lsst_explorer", "Image Type (eg calexp)", None))
        self.label_4.setText(_translate("lsst_explorer", "Catalog Type (optional)", None))
        self.AcceptButton.setText(_translate("lsst_explorer", "OK", None))

