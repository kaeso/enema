# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Projects\enema-dev\gui\mssql\addUser\addUser_widget.ui'
#
# Created: Wed Mar  7 19:23:07 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_addUserWidget(object):
    def setupUi(self, addUserWidget):
        addUserWidget.setObjectName(_fromUtf8("addUserWidget"))
        addUserWidget.resize(322, 78)
        addUserWidget.setMinimumSize(QtCore.QSize(322, 78))
        addUserWidget.setMaximumSize(QtCore.QSize(322, 78))
        self.groupBox_5 = QtGui.QGroupBox(addUserWidget)
        self.groupBox_5.setGeometry(QtCore.QRect(-10, -10, 411, 101))
        self.groupBox_5.setTitle(_fromUtf8(""))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.lineUsername = QtGui.QLineEdit(self.groupBox_5)
        self.lineUsername.setGeometry(QtCore.QRect(80, 20, 90, 20))
        self.lineUsername.setText(_fromUtf8(""))
        self.lineUsername.setObjectName(_fromUtf8("lineUsername"))
        self.label_16 = QtGui.QLabel(self.groupBox_5)
        self.label_16.setGeometry(QtCore.QRect(20, 20, 61, 20))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.linePassword = QtGui.QLineEdit(self.groupBox_5)
        self.linePassword.setGeometry(QtCore.QRect(80, 40, 90, 20))
        self.linePassword.setText(_fromUtf8(""))
        self.linePassword.setEchoMode(QtGui.QLineEdit.Password)
        self.linePassword.setObjectName(_fromUtf8("linePassword"))
        self.label_17 = QtGui.QLabel(self.groupBox_5)
        self.label_17.setGeometry(QtCore.QRect(20, 40, 61, 20))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.addUserButton = QtGui.QPushButton(self.groupBox_5)
        self.addUserButton.setGeometry(QtCore.QRect(260, 29, 61, 21))
        self.addUserButton.setObjectName(_fromUtf8("addUserButton"))
        self.radioSql = QtGui.QRadioButton(self.groupBox_5)
        self.radioSql.setGeometry(QtCore.QRect(180, 20, 51, 17))
        self.radioSql.setChecked(True)
        self.radioSql.setObjectName(_fromUtf8("radioSql"))
        self.radioWin = QtGui.QRadioButton(self.groupBox_5)
        self.radioWin.setGeometry(QtCore.QRect(180, 40, 91, 17))
        self.radioWin.setObjectName(_fromUtf8("radioWin"))
        self.progressBar = QtGui.QProgressBar(self.groupBox_5)
        self.progressBar.setGeometry(QtCore.QRect(20, 70, 301, 10))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.retranslateUi(addUserWidget)
        QtCore.QMetaObject.connectSlotsByName(addUserWidget)

    def retranslateUi(self, addUserWidget):
        addUserWidget.setWindowTitle(QtGui.QApplication.translate("addUserWidget", "Add user", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("addUserWidget", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("addUserWidget", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.addUserButton.setText(QtGui.QApplication.translate("addUserWidget", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.radioSql.setText(QtGui.QApplication.translate("addUserWidget", "sql", None, QtGui.QApplication.UnicodeUTF8))
        self.radioWin.setText(QtGui.QApplication.translate("addUserWidget", "windows", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    addUserWidget = QtGui.QWidget()
    ui = Ui_addUserWidget()
    ui.setupUi(addUserWidget)
    addUserWidget.show()
    sys.exit(app.exec_())

