# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Projects\enema-dev\gui\mssql\xp_cmdshell\xp_cmdshell.ui'
#
# Created: Mon Mar 19 16:22:13 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_cmdshellWidget(object):
    def setupUi(self, cmdshellWidget):
        cmdshellWidget.setObjectName(_fromUtf8("cmdshellWidget"))
        cmdshellWidget.resize(591, 618)
        cmdshellWidget.setMinimumSize(QtCore.QSize(591, 618))
        cmdshellWidget.setMaximumSize(QtCore.QSize(591, 618))
        self.tableWidget = QtGui.QTableWidget(cmdshellWidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 29, 571, 551))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.tableWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(1500)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(1500)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(19)
        self.killButton = QtGui.QToolButton(cmdshellWidget)
        self.killButton.setGeometry(QtCore.QRect(130, 590, 91, 20))
        self.killButton.setObjectName(_fromUtf8("killButton"))
        self.lineCmd = QtGui.QLineEdit(cmdshellWidget)
        self.lineCmd.setGeometry(QtCore.QRect(50, 8, 531, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.lineCmd.setFont(font)
        self.lineCmd.setText(_fromUtf8(""))
        self.lineCmd.setObjectName(_fromUtf8("lineCmd"))
        self.enableButton = QtGui.QPushButton(cmdshellWidget)
        self.enableButton.setGeometry(QtCore.QRect(10, 590, 111, 20))
        self.enableButton.setObjectName(_fromUtf8("enableButton"))
        self.label_8 = QtGui.QLabel(cmdshellWidget)
        self.label_8.setGeometry(QtCore.QRect(10, 9, 41, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.progressBar = QtGui.QProgressBar(cmdshellWidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(230, 590, 351, 20))
        self.progressBar.setAcceptDrops(False)
        self.progressBar.setToolTip(_fromUtf8(""))
        self.progressBar.setStatusTip(_fromUtf8(""))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", 4769)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.BottomToTop)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.retranslateUi(cmdshellWidget)
        QtCore.QMetaObject.connectSlotsByName(cmdshellWidget)

    def retranslateUi(self, cmdshellWidget):
        cmdshellWidget.setWindowTitle(QtGui.QApplication.translate("cmdshellWidget", "xp_cmdshell", None, QtGui.QApplication.UnicodeUTF8))
        self.killButton.setText(QtGui.QApplication.translate("cmdshellWidget", "Kill", None, QtGui.QApplication.UnicodeUTF8))
        self.enableButton.setText(QtGui.QApplication.translate("cmdshellWidget", "Enabe xp_cmdshell", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("cmdshellWidget", "CMD>", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setFormat(QtGui.QApplication.translate("cmdshellWidget", "%p%", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    cmdshellWidget = QtGui.QWidget()
    ui = Ui_cmdshellWidget()
    ui.setupUi(cmdshellWidget)
    cmdshellWidget.show()
    sys.exit(app.exec_())

