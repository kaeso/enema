# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Projects\enema\log_form.ui'
#
# Created: Wed Oct 12 13:34:28 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LogForm(object):
    def setupUi(self, LogForm):
        LogForm.setObjectName(_fromUtf8("LogForm"))
        LogForm.resize(761, 390)
        LogForm.setMinimumSize(QtCore.QSize(761, 390))
        LogForm.setMaximumSize(QtCore.QSize(761, 390))
        self.logTxtEdit = QtGui.QTextEdit(LogForm)
        self.logTxtEdit.setGeometry(QtCore.QRect(10, 10, 741, 341))
        self.logTxtEdit.setObjectName(_fromUtf8("logTxtEdit"))
        self.clearLogButton = QtGui.QPushButton(LogForm)
        self.clearLogButton.setGeometry(QtCore.QRect(670, 360, 81, 23))
        self.clearLogButton.setObjectName(_fromUtf8("clearLogButton"))

        self.retranslateUi(LogForm)
        QtCore.QMetaObject.connectSlotsByName(LogForm)

    def retranslateUi(self, LogForm):
        LogForm.setWindowTitle(QtGui.QApplication.translate("LogForm", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.clearLogButton.setText(QtGui.QApplication.translate("LogForm", "Clear", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    LogForm = QtGui.QWidget()
    ui = Ui_LogForm()
    ui.setupUi(LogForm)
    LogForm.show()
    sys.exit(app.exec_())

