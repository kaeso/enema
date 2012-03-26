# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projects\enema\gui\mssql\ftp\ftp.ui'
#
# Created: Mon Mar 26 15:56:23 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ftpWidget(object):
    def setupUi(self, ftpWidget):
        ftpWidget.setObjectName(_fromUtf8("ftpWidget"))
        ftpWidget.resize(431, 98)
        ftpWidget.setMinimumSize(QtCore.QSize(431, 98))
        ftpWidget.setMaximumSize(QtCore.QSize(431, 98))
        self.groupBox_2 = QtGui.QGroupBox(ftpWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(-10, -10, 451, 121))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(20, 20, 31, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.lineIP = QtGui.QLineEdit(self.groupBox_2)
        self.lineIP.setGeometry(QtCore.QRect(50, 20, 101, 20))
        self.lineIP.setText(_fromUtf8(""))
        self.lineIP.setObjectName(_fromUtf8("lineIP"))
        self.lineFtpLogin = QtGui.QLineEdit(self.groupBox_2)
        self.lineFtpLogin.setGeometry(QtCore.QRect(80, 40, 71, 20))
        self.lineFtpLogin.setText(_fromUtf8(""))
        self.lineFtpLogin.setObjectName(_fromUtf8("lineFtpLogin"))
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(20, 40, 61, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.lineFtpPwd = QtGui.QLineEdit(self.groupBox_2)
        self.lineFtpPwd.setGeometry(QtCore.QRect(80, 60, 71, 20))
        self.lineFtpPwd.setText(_fromUtf8(""))
        self.lineFtpPwd.setEchoMode(QtGui.QLineEdit.Password)
        self.lineFtpPwd.setObjectName(_fromUtf8("lineFtpPwd"))
        self.label_11 = QtGui.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(20, 60, 61, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.lineFtpFile = QtGui.QLineEdit(self.groupBox_2)
        self.lineFtpFile.setGeometry(QtCore.QRect(200, 20, 231, 20))
        self.lineFtpFile.setText(_fromUtf8(""))
        self.lineFtpFile.setObjectName(_fromUtf8("lineFtpFile"))
        self.label_12 = QtGui.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(160, 20, 31, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(160, 40, 41, 20))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.lineFtpPath = QtGui.QLineEdit(self.groupBox_2)
        self.lineFtpPath.setGeometry(QtCore.QRect(200, 40, 231, 20))
        self.lineFtpPath.setText(_fromUtf8(""))
        self.lineFtpPath.setObjectName(_fromUtf8("lineFtpPath"))
        self.ftpButton = QtGui.QPushButton(self.groupBox_2)
        self.ftpButton.setGeometry(QtCore.QRect(340, 60, 91, 21))
        self.ftpButton.setFlat(False)
        self.ftpButton.setObjectName(_fromUtf8("ftpButton"))
        self.radioGet = QtGui.QRadioButton(self.groupBox_2)
        self.radioGet.setGeometry(QtCore.QRect(200, 60, 51, 17))
        self.radioGet.setChecked(True)
        self.radioGet.setObjectName(_fromUtf8("radioGet"))
        self.radioSend = QtGui.QRadioButton(self.groupBox_2)
        self.radioSend.setGeometry(QtCore.QRect(270, 60, 71, 17))
        self.radioSend.setObjectName(_fromUtf8("radioSend"))
        self.progressBar = QtGui.QProgressBar(self.groupBox_2)
        self.progressBar.setGeometry(QtCore.QRect(20, 90, 411, 10))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.retranslateUi(ftpWidget)
        QtCore.QMetaObject.connectSlotsByName(ftpWidget)

    def retranslateUi(self, ftpWidget):
        ftpWidget.setWindowTitle(QtGui.QApplication.translate("ftpWidget", "FTP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("ftpWidget", "IP:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("ftpWidget", "Login:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("ftpWidget", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("ftpWidget", "Files:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("ftpWidget", "Path:", None, QtGui.QApplication.UnicodeUTF8))
        self.ftpButton.setText(QtGui.QApplication.translate("ftpWidget", "GO", None, QtGui.QApplication.UnicodeUTF8))
        self.radioGet.setText(QtGui.QApplication.translate("ftpWidget", "GET", None, QtGui.QApplication.UnicodeUTF8))
        self.radioSend.setText(QtGui.QApplication.translate("ftpWidget", "SEND", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ftpWidget = QtGui.QWidget()
    ui = Ui_ftpWidget()
    ui.setupUi(ftpWidget)
    ftpWidget.show()
    sys.exit(app.exec_())

