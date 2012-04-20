# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projects\Enema Project\framework\ui\query_editor.ui'
#
# Created: Fri Apr 20 17:01:03 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_QueryEditorForm(object):
    def setupUi(self, QueryEditorForm):
        QueryEditorForm.setObjectName(_fromUtf8("QueryEditorForm"))
        QueryEditorForm.resize(652, 452)
        QueryEditorForm.setMinimumSize(QtCore.QSize(652, 452))
        QueryEditorForm.setMaximumSize(QtCore.QSize(652, 452))
        self.treeQueryStrings = QtGui.QTreeWidget(QueryEditorForm)
        self.treeQueryStrings.setGeometry(QtCore.QRect(10, 10, 631, 371))
        self.treeQueryStrings.setObjectName(_fromUtf8("treeQueryStrings"))
        item_0 = QtGui.QTreeWidgetItem(self.treeQueryStrings)
        item_0 = QtGui.QTreeWidgetItem(self.treeQueryStrings)
        item_0 = QtGui.QTreeWidgetItem(self.treeQueryStrings)
        item_0 = QtGui.QTreeWidgetItem(self.treeQueryStrings)
        self.treeQueryStrings.header().setVisible(True)
        self.treeQueryStrings.header().setMinimumSectionSize(27)
        self.label = QtGui.QLabel(QueryEditorForm)
        self.label.setGeometry(QtCore.QRect(10, 420, 161, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.replaceButton = QtGui.QPushButton(QueryEditorForm)
        self.replaceButton.setGeometry(QtCore.QRect(370, 420, 71, 20))
        self.replaceButton.setObjectName(_fromUtf8("replaceButton"))
        self.lineFindStr = QtGui.QLineEdit(QueryEditorForm)
        self.lineFindStr.setGeometry(QtCore.QRect(170, 420, 91, 20))
        self.lineFindStr.setObjectName(_fromUtf8("lineFindStr"))
        self.lineResplaceStr = QtGui.QLineEdit(QueryEditorForm)
        self.lineResplaceStr.setGeometry(QtCore.QRect(270, 420, 91, 20))
        self.lineResplaceStr.setObjectName(_fromUtf8("lineResplaceStr"))
        self.defaultsButton = QtGui.QPushButton(QueryEditorForm)
        self.defaultsButton.setGeometry(QtCore.QRect(570, 420, 71, 23))
        self.defaultsButton.setObjectName(_fromUtf8("defaultsButton"))
        self.lineQueryString = QtGui.QLineEdit(QueryEditorForm)
        self.lineQueryString.setGeometry(QtCore.QRect(10, 390, 631, 20))
        self.lineQueryString.setObjectName(_fromUtf8("lineQueryString"))

        self.retranslateUi(QueryEditorForm)
        QtCore.QMetaObject.connectSlotsByName(QueryEditorForm)

    def retranslateUi(self, QueryEditorForm):
        QueryEditorForm.setWindowTitle(QtGui.QApplication.translate("QueryEditorForm", "Query Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.treeQueryStrings.headerItem().setText(0, QtGui.QApplication.translate("QueryEditorForm", "Query strings", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.treeQueryStrings.isSortingEnabled()
        self.treeQueryStrings.setSortingEnabled(False)
        self.treeQueryStrings.topLevelItem(0).setText(0, QtGui.QApplication.translate("QueryEditorForm", "MSSQL", None, QtGui.QApplication.UnicodeUTF8))
        self.treeQueryStrings.topLevelItem(1).setText(0, QtGui.QApplication.translate("QueryEditorForm", "MySQL", None, QtGui.QApplication.UnicodeUTF8))
        self.treeQueryStrings.topLevelItem(2).setText(0, QtGui.QApplication.translate("QueryEditorForm", "Oracle", None, QtGui.QApplication.UnicodeUTF8))
        self.treeQueryStrings.topLevelItem(3).setText(0, QtGui.QApplication.translate("QueryEditorForm", "PostgreSQL", None, QtGui.QApplication.UnicodeUTF8))
        self.treeQueryStrings.setSortingEnabled(__sortingEnabled)
        self.label.setText(QtGui.QApplication.translate("QueryEditorForm", "Find & Replace (case sensitive):", None, QtGui.QApplication.UnicodeUTF8))
        self.replaceButton.setText(QtGui.QApplication.translate("QueryEditorForm", "Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultsButton.setText(QtGui.QApplication.translate("QueryEditorForm", "Defaults", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    QueryEditorForm = QtGui.QWidget()
    ui = Ui_QueryEditorForm()
    ui.setupUi(QueryEditorForm)
    QueryEditorForm.show()
    sys.exit(app.exec_())

