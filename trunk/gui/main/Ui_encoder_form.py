# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Projects\enema-dev\gui\main\encoder_form.ui'
#
# Created: Sat Mar 10 14:46:28 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_EncoderForm(object):
    def setupUi(self, EncoderForm):
        EncoderForm.setObjectName(_fromUtf8("EncoderForm"))
        EncoderForm.resize(467, 226)
        EncoderForm.setMinimumSize(QtCore.QSize(467, 226))
        EncoderForm.setMaximumSize(QtCore.QSize(467, 226))
        EncoderForm.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.lineString = QtGui.QLineEdit(EncoderForm)
        self.lineString.setGeometry(QtCore.QRect(10, 10, 381, 20))
        self.lineString.setObjectName(_fromUtf8("lineString"))
        self.encodeButton = QtGui.QPushButton(EncoderForm)
        self.encodeButton.setGeometry(QtCore.QRect(400, 180, 61, 31))
        self.encodeButton.setObjectName(_fromUtf8("encodeButton"))
        self.textResult = QtGui.QTextEdit(EncoderForm)
        self.textResult.setGeometry(QtCore.QRect(10, 40, 451, 131))
        self.textResult.setReadOnly(True)
        self.textResult.setObjectName(_fromUtf8("textResult"))
        self.radioHex = QtGui.QRadioButton(EncoderForm)
        self.radioHex.setGeometry(QtCore.QRect(20, 180, 82, 17))
        self.radioHex.setChecked(True)
        self.radioHex.setObjectName(_fromUtf8("radioHex"))
        self.radioChar = QtGui.QRadioButton(EncoderForm)
        self.radioChar.setGeometry(QtCore.QRect(20, 200, 51, 17))
        self.radioChar.setChecked(False)
        self.radioChar.setObjectName(_fromUtf8("radioChar"))
        self.isUrlencoded = QtGui.QCheckBox(EncoderForm)
        self.isUrlencoded.setEnabled(True)
        self.isUrlencoded.setGeometry(QtCore.QRect(90, 180, 131, 17))
        self.isUrlencoded.setChecked(False)
        self.isUrlencoded.setObjectName(_fromUtf8("isUrlencoded"))
        self.comboBox = QtGui.QComboBox(EncoderForm)
        self.comboBox.setGeometry(QtCore.QRect(400, 10, 61, 21))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.isPlay = QtGui.QCheckBox(EncoderForm)
        self.isPlay.setEnabled(True)
        self.isPlay.setGeometry(QtCore.QRect(90, 200, 131, 17))
        self.isPlay.setChecked(False)
        self.isPlay.setObjectName(_fromUtf8("isPlay"))
        self.decodeButton = QtGui.QPushButton(EncoderForm)
        self.decodeButton.setGeometry(QtCore.QRect(330, 180, 61, 31))
        self.decodeButton.setObjectName(_fromUtf8("decodeButton"))

        self.retranslateUi(EncoderForm)
        QtCore.QMetaObject.connectSlotsByName(EncoderForm)

    def retranslateUi(self, EncoderForm):
        EncoderForm.setWindowTitle(QtGui.QApplication.translate("EncoderForm", "Encoder", None, QtGui.QApplication.UnicodeUTF8))
        self.encodeButton.setText(QtGui.QApplication.translate("EncoderForm", "Encode", None, QtGui.QApplication.UnicodeUTF8))
        self.radioHex.setText(QtGui.QApplication.translate("EncoderForm", "Hex", None, QtGui.QApplication.UnicodeUTF8))
        self.radioChar.setText(QtGui.QApplication.translate("EncoderForm", "Char", None, QtGui.QApplication.UnicodeUTF8))
        self.isUrlencoded.setText(QtGui.QApplication.translate("EncoderForm", "Url-encoded", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("EncoderForm", "MSSQL", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("EncoderForm", "MySQL", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("EncoderForm", "Base64", None, QtGui.QApplication.UnicodeUTF8))
        self.isPlay.setText(QtGui.QApplication.translate("EncoderForm", "Play with letters", None, QtGui.QApplication.UnicodeUTF8))
        self.decodeButton.setText(QtGui.QApplication.translate("EncoderForm", "Decode", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    EncoderForm = QtGui.QWidget()
    ui = Ui_EncoderForm()
    ui.setupUi(EncoderForm)
    EncoderForm.show()
    sys.exit(app.exec_())

