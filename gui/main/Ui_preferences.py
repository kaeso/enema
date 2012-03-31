# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projects\enema\gui\main\preferences.ui'
#
# Created: Fri Mar 30 16:36:48 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_preferencesWidget(object):
    def setupUi(self, preferencesWidget):
        preferencesWidget.setObjectName(_fromUtf8("preferencesWidget"))
        preferencesWidget.resize(231, 161)
        preferencesWidget.setMinimumSize(QtCore.QSize(231, 161))
        preferencesWidget.setMaximumSize(QtCore.QSize(231, 161))
        self.groupBox = QtGui.QGroupBox(preferencesWidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 211, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.lineMP = QtGui.QLineEdit(self.groupBox)
        self.lineMP.setGeometry(QtCore.QRect(160, 20, 41, 20))
        self.lineMP.setText(_fromUtf8(""))
        self.lineMP.setObjectName(_fromUtf8("lineMP"))
        self.lineMS = QtGui.QLineEdit(self.groupBox)
        self.lineMS.setGeometry(QtCore.QRect(120, 20, 21, 20))
        self.lineMS.setMaxLength(1)
        self.lineMS.setObjectName(_fromUtf8("lineMS"))
        self.label_22 = QtGui.QLabel(self.groupBox)
        self.label_22.setGeometry(QtCore.QRect(10, 20, 111, 20))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.label_23 = QtGui.QLabel(self.groupBox)
        self.label_23.setGeometry(QtCore.QRect(150, 20, 16, 20))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 50, 51, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineTimeout = QtGui.QLineEdit(self.groupBox)
        self.lineTimeout.setGeometry(QtCore.QRect(160, 50, 41, 20))
        self.lineTimeout.setObjectName(_fromUtf8("lineTimeout"))
        self.threadBox = QtGui.QSpinBox(self.groupBox)
        self.threadBox.setGeometry(QtCore.QRect(60, 50, 41, 20))
        self.threadBox.setMinimum(1)
        self.threadBox.setMaximum(100)
        self.threadBox.setProperty("value", 5)
        self.threadBox.setObjectName(_fromUtf8("threadBox"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(110, 50, 51, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.isRndUpper = QtGui.QCheckBox(self.groupBox)
        self.isRndUpper.setGeometry(QtCore.QRect(10, 110, 111, 17))
        self.isRndUpper.setObjectName(_fromUtf8("isRndUpper"))
        self.lineEncoding = QtGui.QLineEdit(self.groupBox)
        self.lineEncoding.setGeometry(QtCore.QRect(60, 80, 81, 20))
        self.lineEncoding.setObjectName(_fromUtf8("lineEncoding"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 80, 61, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))

        self.retranslateUi(preferencesWidget)
        QtCore.QMetaObject.connectSlotsByName(preferencesWidget)

    def retranslateUi(self, preferencesWidget):
        preferencesWidget.setWindowTitle(QtGui.QApplication.translate("preferencesWidget", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("preferencesWidget", "Main", None, QtGui.QApplication.UnicodeUTF8))
        self.lineMS.setText(QtGui.QApplication.translate("preferencesWidget", "~", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("preferencesWidget", "Match symbol / string:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("preferencesWidget", "/", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("preferencesWidget", "Threads:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineTimeout.setText(QtGui.QApplication.translate("preferencesWidget", "60", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("preferencesWidget", "Timeout:", None, QtGui.QApplication.UnicodeUTF8))
        self.isRndUpper.setText(QtGui.QApplication.translate("preferencesWidget", "Random UpCase", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEncoding.setText(QtGui.QApplication.translate("preferencesWidget", "windows-1251", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("preferencesWidget", "Encoding:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    preferencesWidget = QtGui.QWidget()
    ui = Ui_preferencesWidget()
    ui.setupUi(preferencesWidget)
    preferencesWidget.show()
    sys.exit(app.exec_())

