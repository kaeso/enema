"""
    Enema module: GUI events (main)
    Copyright (C) 2011 Kaeso
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

import os
import sys
import txtproc
import configparser
from core import ErrorBased
from PyQt4 import QtCore, QtGui 
from Ui_form import Ui_MainForm
from Ui_log_form import Ui_LogForm
from Ui_encoder_form import Ui_EncoderForm
from Ui_about_form import Ui_AboutForm
from Ui_query_editor import Ui_QueryEditorForm


#Query editor form GUI class
class QueryEditorForm(QtGui.QMainWindow):
    
    qstringsChanged = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_QueryEditorForm()
        self.ui.setupUi(self)
        self.loadQstrings()
#SIGNALS-----------------------------------------------------------------------
        self.ui.qsSave.triggered.connect(self.qsSave_OnClick)
        self.ui.qsRestore.triggered.connect(self.qsRestore_OnClick)
        
#Loading querystrings to GUI
    def loadQstrings(self):
        if os.path.exists(os.path.normcase("settings/") + "qstrings_custom.ini"):
            settings = QtCore.QSettings(os.path.normcase("settings/") + "qstrings_custom.ini", QtCore.QSettings.IniFormat)
        else:
            settings = QtCore.QSettings(os.path.normcase("settings/") + "qstrings.ini", QtCore.QSettings.IniFormat)
        #MSSQL------------------------------------------------------------------
        #bases
        self.ui.q_ms_curr_db_name.setText(settings.value('mssql_error_based/curr_db_name', ''))
        self.ui.q_ms_dbs_count.setText(settings.value('mssql_error_based/dbs_count', ''))
        self.ui.q_ms_get_db_name.setText(settings.value('mssql_error_based/get_db_name', ''))
        self.ui.q_ms_get_db_name2.setText(settings.value('mssql_error_based/get_db_name2', ''))
        #tables
        self.ui.q_ms_tbls_count.setText(settings.value('mssql_error_based/tbls_count', ''))
        self.ui.q_ms_get_tbl_name.setText(settings.value('mssql_error_based/get_tbl_name', ''))
        self.ui.q_ms_get_tbl_name2.setText(settings.value('mssql_error_based/get_tbl_name2', ''))
        #columns
        self.ui.q_ms_get_column_name.setText(settings.value('mssql_error_based/get_column_name', ''))
        self.ui.q_ms_columns_count.setText(settings.value('mssql_error_based/columns_count', ''))
        self.ui.q_ms_get_column_name2.setText(settings.value('mssql_error_based/get_column_name2', ''))
        self.ui.q_ms_get_column_name3.setText(settings.value('mssql_error_based/get_column_name3', ''))      
        #xp_cmdshell
        self.ui.q_ms_enable_xp_cmdshell.setText(settings.value('mssql_error_based/enable_xp_cmdshell', ''))
        self.ui.q_ms_create_tmp_tbl.setText(settings.value('mssql_error_based/create_tmp_tbl', ''))
        self.ui.q_ms_drop_tmp_tbl.setText(settings.value('mssql_error_based/drop_tmp_tbl', ''))
        self.ui.q_ms_insert_result.setText(settings.value('mssql_error_based/insert_result', ''))
        self.ui.q_ms_exec_cmdshell.setText(settings.value('mssql_error_based/exec_cmdshell', ''))
        self.ui.q_ms_tmp_count.setText(settings.value('mssql_error_based/tmp_count', ''))
        self.ui.q_ms_get_row.setText(settings.value('mssql_error_based/get_row', ''))
        #etc
        self.ui.q_ms_rows_count.setText(settings.value('mssql_error_based/rows_count', ''))
        self.ui.q_ms_query.setText(settings.value('mssql_error_based/query', ''))
        self.ui.q_ms_enable_openrowset.setText(settings.value('mssql_error_based/enable_openrowset', ''))
        self.ui.q_ms_add_sqluser.setText(settings.value('mssql_error_based/add_sqluser', ''))
        self.ui.q_ms_data_dump.setText(settings.value('mssql_error_based/data_dump', ''))
        #MySQL------------------------------------------------------------------
        #bases
        self.ui.q_my_curr_db_name.setText(settings.value('mysql_error_based/curr_db_name', ''))
        self.ui.q_my_dbs_count.setText(settings.value('mysql_error_based/dbs_count', ''))
        self.ui.q_my_get_db_name2.setText(settings.value('mysql_error_based/get_db_name2', ''))
        #tables
        self.ui.q_my_tbls_count.setText(settings.value('mysql_error_based/tbls_count', ''))
        self.ui.q_my_get_tbl_name2.setText(settings.value('mysql_error_based/get_tbl_name2', ''))
        #columns
        self.ui.q_my_columns_count.setText(settings.value('mysql_error_based/columns_count', ''))
        self.ui.q_my_get_column_name2.setText(settings.value('mysql_error_based/get_column_name2', ''))
        self.ui.q_my_get_column_name3.setText(settings.value('mysql_error_based/get_column_name3', ''))      
        #etc
        self.ui.q_my_rows_count.setText(settings.value('mysql_error_based/rows_count', ''))
        self.ui.q_my_query.setText(settings.value('mysql_error_based/query', ''))
        #---------------------------------------------------------------------------
        
    def qsSave_OnClick(self):
        #Saving customised querys
        settings = QtCore.QSettings(os.path.normcase("settings/") + "qstrings_custom.ini", QtCore.QSettings.IniFormat)
        #MSSQL------------------------------------------------------------------
        #bases
        settings.setValue('mssql_error_based/curr_db_name', self.ui.q_ms_curr_db_name.text())
        settings.setValue('mssql_error_based/dbs_count', self.ui.q_ms_dbs_count.text())
        settings.setValue('mssql_error_based/get_db_name', self.ui.q_ms_get_db_name.text())
        settings.setValue('mssql_error_based/get_db_name2', self.ui.q_ms_get_db_name2.text())
        #tables
        settings.setValue('mssql_error_based/tbls_count', self.ui.q_ms_tbls_count.text())
        settings.setValue('mssql_error_based/get_tbl_name', self.ui.q_ms_get_tbl_name.text())
        settings.setValue('mssql_error_based/get_tbl_name2', self.ui.q_ms_get_tbl_name2.text())
        #columns
        settings.setValue('mssql_error_based/get_column_name', self.ui.q_ms_get_column_name.text())
        settings.setValue('mssql_error_based/columns_count', self.ui.q_ms_columns_count.text())
        settings.setValue('mssql_error_based/get_column_name2', self.ui.q_ms_get_column_name2.text())
        settings.setValue('mssql_error_based/get_column_name3', self.ui.q_ms_get_column_name3.text())    
        #xp_cmdshell
        settings.setValue('mssql_error_based/enable_xp_cmdshell', self.ui.q_ms_enable_xp_cmdshell.text())
        settings.setValue('mssql_error_based/create_tmp_tbl', self.ui.q_ms_create_tmp_tbl.text())
        settings.setValue('mssql_error_based/drop_tmp_tbl', self.ui.q_ms_drop_tmp_tbl.text())
        settings.setValue('mssql_error_based/insert_result', self.ui.q_ms_insert_result.text())
        settings.setValue('mssql_error_based/exec_cmdshell', self.ui.q_ms_exec_cmdshell.text())
        settings.setValue('mssql_error_based/tmp_count', self.ui.q_ms_tmp_count.text())
        settings.setValue('mssql_error_based/get_row', self.ui.q_ms_get_row.text())
        #etc
        settings.setValue('mssql_error_based/rows_count', self.ui.q_ms_rows_count.text())
        settings.setValue('mssql_error_based/query', self.ui.q_ms_query.text())
        settings.setValue('mssql_error_based/enable_openrowset', self.ui.q_ms_enable_openrowset.text())
        settings.setValue('mssql_error_based/add_sqluser', self.ui.q_ms_add_sqluser.text())
        settings.setValue('mssql_error_based/data_dump', self.ui.q_ms_data_dump.text())
        #MySQL------------------------------------------------------------------
        #bases
        settings.setValue('mysql_error_based/curr_db_name', self.ui.q_my_curr_db_name.text())
        settings.setValue('mysql_error_based/dbs_count', self.ui.q_my_dbs_count.text())
        settings.setValue('mysql_error_based/get_db_name2', self.ui.q_my_get_db_name2.text())
        #tables
        settings.setValue('mysql_error_based/tbls_count', self.ui.q_my_tbls_count.text())
        settings.setValue('mysql_error_based/get_tbl_name2', self.ui.q_my_get_tbl_name2.text())
        #columns
        settings.setValue('mysql_error_based/columns_count', self.ui.q_my_columns_count.text())
        settings.setValue('mysql_error_based/get_column_name2', self.ui.q_my_get_column_name2.text())
        settings.setValue('mysql_error_based/get_column_name3', self.ui.q_my_get_column_name3.text())    
        #etc
        settings.setValue('mysql_error_based/rows_count', self.ui.q_my_rows_count.text())
        settings.setValue('mysql_error_based/query', self.ui.q_my_query.text())
        #---------------------------------------------------------------------------
        settings.sync()
        print("\n\n [+] Customised query strings saved to: " + os.path.normcase("settings/") + "qstrings_custom.ini")
        self.qstringsChanged.emit()

#Reset query strings to default
    def qsRestore_OnClick(self):
        customPath = os.path.normcase("settings/") + "qstrings_custom.ini"
        if os.path.exists(customPath):
            try:
                os.remove(customPath)
            except Exception:
                print("\n\n [x] Cannot remove file: " + customPath)
        else:
            return
        self.loadQstrings()
        print("\n\n [+] Query strings restored to default.")
        self.qstringsChanged.emit()
        
#Enccoder form GUI class
class EncoderForm(QtGui.QWidget):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_EncoderForm()
        self.ui.setupUi(self)
#SIGNALS------------------------------------------------------------------------
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

#About form GUI class
class AboutForm(QtGui.QWidget):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AboutForm()
        self.ui.setupUi(self)
        #Set current program version
        self.ui.versionLabel.setText("Version: 1.3")

#Log widget GUI class
class LogForm(QtGui.QWidget):
    
    uncheckLogSignal = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_LogForm()
        self.ui.setupUi(self)
#SIGNALS-----------------------------------------------------------------------
        self.ui.clearLogButton.clicked.connect(self.clearLogButton_OnClick)
        
    def closeEvent(self, event):
        self.uncheckLogSignal.emit()
        self.hide()
        event.ignore()

    def clearLogButton_OnClick(self):
        self.ui.logTxtEdit.clear()
        
#Main form GUI class
class EnemaForm(QtGui.QMainWindow):

    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.ui.progressBar.hide()
        self.ui.progressBarCmd.hide()
        self.ui.progressBarDump.hide()
        #Forms / widgets
        self.qeditor_frm = QueryEditorForm()
        self.enc_frm = EncoderForm()
        self.about_frm = AboutForm()
        self.log_frm = LogForm()
        configPath = os.path.normcase("settings/") + "enema.ini"
        #Loading settings if ini file exists
        if os.path.exists(configPath):
            settings = QtCore.QSettings(configPath, QtCore.QSettings.IniFormat)
            #FTP
            self.ui.lineIP.setText(settings.value('FTP/ip', ''))
            self.ui.lineFtpLogin.setText(settings.value('FTP/login', ''))
            self.ui.lineFtpPwd.setText(settings.value('FTP/password', ''))
            self.ui.lineFtpFile.setText(settings.value('FTP/files', ''))
            self.ui.lineFtpPath.setText(settings.value('FTP/path', ''))
            #SQL user
            self.ui.lineAddUserLogin.setText(settings.value('sql_user/login', ''))
            self.ui.lineAddUserPwd.setText(settings.value('sql_user/password', ''))
            #Etc
            self.ui.queryText.setText(settings.value('other/query', ''))
            #restore window state
            self.move(settings.value("GUI/mainWpos"))
            self.log_frm.move(settings.value("GUI/logWpos"))
        #Query strings loading
        self.readQstrings()
        #Showing log widget
        self.log_frm.show()
        
#SIGNAL CONNECTIONS--------------------------------------------------------------------------
        #Query changed in editor
        self.qeditor_frm.qstringsChanged.connect(self.readQstrings)
        self.ui.logCheckBox.stateChanged.connect(self.logChecked)
        self.log_frm.uncheckLogSignal.connect(self.uncheckLog)
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
        self.ui.save_cmdshell.triggered.connect(self.save_cmdshell_OnClick)
        self.ui.ssSettings.triggered.connect(self.saveSiteSettings_OnClick)
        self.ui.spSettings.triggered.connect(self.saveProgramSettings_OnClick)
#Load Menu-----------------
        self.ui.loadTables.triggered.connect(self.loadTables_OnClick)
        self.ui.loadBases.triggered.connect(self.loadBases_OnClick)
        self.ui.lsSettings.triggered.connect(self.loadSiteSettings_OnClick)
#Tools Menu----------------
        self.ui.menuEncoder.triggered.connect(self.menuEncoder_OnClick)
        self.ui.qEditor.triggered.connect(self.queryEditor_OnClick)
#Help menu-----------------
        self.ui.menuAbout.triggered.connect(self.menuAbout_OnClick)
#Db Type change-----------
        self.ui.comboBox_3.currentIndexChanged.connect(self.dbTypeChanged)

#===============================GENERAL-FUNCTIONS=====================================#
#When form closing
    def closeEvent(self, event):
        settings = QtCore.QSettings(os.path.normcase("settings/") + "enema.ini", QtCore.QSettings.IniFormat)
        settings.setValue('GUI/mainWpos', self.pos())
        settings.setValue('GUI/logWpos', self.log_frm.pos())
        sys.exit(0)

#Log Checkbox checked or unchecked
    def logChecked(self):
        if not self.ui.logCheckBox.isChecked():
            self.log_frm.hide()
        else:
            self.log_frm.show()
            
    def uncheckLog(self):
        self.ui.logCheckBox.setChecked(False)

#Add text to log
    @QtCore.pyqtSlot(str)
    def addLog(self, logStr):
        #Autoclean log when blocks more than 3000
        if self.log_frm.ui.logTxtEdit.document().blockCount() > 3000:
            self.log_frm.ui.logTxtEdit.clear()
        self.log_frm.ui.logTxtEdit.append("\n---------------------\n" + logStr)
        #Autoscrolling
        sb = self.log_frm.ui.logTxtEdit.verticalScrollBar()
        sb.setValue(sb.maximum())
        
#Get user defined parametes from GUI
    def webData(self):
        ftpPath = self.ui.lineFtpPath.text()
        if not self.ui.listOfTables.currentItem():
            currTable = ""
        else:
            currTable = self.ui.listOfTables.currentItem().text()
        if len(ftpPath) > 0:
            if ftpPath[-1] != "\\":
                ftpPath += "\\"
        wD = {
              'url' : self.ui.lineUrl.text(), 
              'method' : self.getMethod() , 
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
              'ftpPath' : ftpPath, 
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
                                                     ("CSV files (*.csv)"))
        self.writeToFile(filePath,  "csv")

#Click on menu save xp_cmdshell output
    def save_cmdshell_OnClick(self):
        filePath = QtGui.QFileDialog.getSaveFileName(self, "Save xp_cmdshell output",
                                                     QtCore.QDir.homePath(),
                                                     ("Text files (*.txt)"))
        self.writeToFile(filePath,  "cmd")
        
#Click on menu save settings
    def saveSiteSettings_OnClick(self):
        filePath = QtGui.QFileDialog.getSaveFileName(self, "Save xp_cmdshell output",
                                                     QtCore.QDir.homePath(),
                                                     ("INI files (*.ini)"))
        self.saveSiteSettings(filePath)
        
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
            elif save == "csv":
                strLine = ""
                for row in range(self.ui.tableWidget.rowCount()):
                    for column in range(self.ui.tableWidget.columnCount()):
                        strLine +=  str(self.ui.tableWidget.item(row, column).data(QtCore.Qt.DisplayRole)) + ";"
                    strLine = strLine[:-1] + "\n"
                file.write(strLine)
            else:
                for row in range(self.ui.cmdOutput.rowCount()):
                    buff = ""
                    buff += str(self.ui.cmdOutput.item(row, 1).data(QtCore.Qt.DisplayRole) + "\n")
                    file.write(buff)
            file.close()
        except Exception:
            return

#Saving program settings
    def saveProgramSettings_OnClick(self):
        settings = QtCore.QSettings(os.path.normcase("settings/") + "enema.ini", QtCore.QSettings.IniFormat)
        #FTP settings
        settings.setValue('FTP/ip', self.ui.lineIP.text())
        settings.setValue('FTP/login', self.ui.lineFtpLogin.text())
        settings.setValue('FTP/password', self.ui.lineFtpPwd.text())
        settings.setValue('FTP/files', self.ui.lineFtpFile.text())
        settings.setValue('FTP/path', self.ui.lineFtpPath.text())
        settings.setValue('FTP/get', self.ui.radioGet.isChecked())
        settings.setValue('FTP/send', self.ui.radioSend.isChecked())
        #Add sql user settings
        settings.setValue('sql_user/login', self.ui.lineAddUserLogin.text())
        settings.setValue('sql_user/password', self.ui.lineAddUserPwd.text())
        settings.setValue('other/query',  self.ui.queryText.toPlainText())
        settings.sync()
        
#Saving site settings
    def saveSiteSettings(self, filepath):
        settings = QtCore.QSettings(filepath, QtCore.QSettings.IniFormat)
        #Making tables list to config format - table1>>table2>>etc...
        tables = ""
        if self.ui.listOfTables.count() > 0:
            for i in range(self.ui.listOfTables.count()):
                tables += self.ui.listOfTables.item(i).text() + ">>"
        #Making bases list to config format - base1>>base2>>etc...
        bases = ""
        if self.ui.dbListComboBox.count() > 0:
            for i in range(self.ui.dbListComboBox.count()):
                bases += self.ui.dbListComboBox.itemText(i) + ">>"
        #db_strucure tab settings
        settings.setValue('db_structure/url', self.ui.lineUrl.text())
        settings.setValue('db_structure/method', self.ui.comboBox.currentIndex())
        settings.setValue('db_structure/data', self.ui.textEdit.toPlainText())
        settings.setValue('db_structure/cookies', self.ui.lineCookie.text())
        settings.setValue('db_structure/db_type', self.ui.comboBox_3.currentIndex())
        settings.setValue('db_structure/pattern', self.ui.lineMP.text())
        settings.setValue('db_structure/symbol', self.ui.lineMS.text())
        settings.setValue('db_structure/tables', tables)
        settings.setValue('db_structure/bases', bases)
        settings.setValue('db_structure/current_db', self.ui.dbListComboBox.currentIndex())
        settings.setValue('db_structure/threads', self.ui.threadBox.value())
        settings.setValue('db_structure/timeout', self.ui.lineTimeout.text())
        #dump tab settings
        settings.setValue('dump/table', self.ui.lineTable.text())
        settings.setValue('dump/columns', self.ui.lineColumns.text())
        settings.setValue('dump/key', self.ui.lineKey.text())
        settings.setValue('dump/from', self.ui.lineFrom.text())
        settings.setValue('dump/to', self.ui.lineTo.text())
        settings.sync()
        
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
        
#Click on menu load site settings  
    def loadSiteSettings_OnClick(self):
        filePath = QtGui.QFileDialog.getOpenFileName(self, "Load bases", 
                                                     QtCore.QDir.homePath(),
                                                     ("INI files (*.ini)"))
        self.loadSiteSettings(filePath)
        
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
                self.ui.totalLabel.setText(str(self.ui.listOfTables.count()))
            else:
                self.ui.dbListComboBox.clear()
                for line in buff:
                    self.ui.dbListComboBox.addItem(line)
            file.close()
        except Exception:
            return

#Loading site settings
    def loadSiteSettings(self, filepath):
        settings = QtCore.QSettings(filepath, QtCore.QSettings.IniFormat)
        #Reading tables from config
        tables = settings.value('db_structure/tables', '').split('>>')
        self.ui.listOfTables.clear()
        for tbl in tables:
            if tbl !='':
                self.ui.listOfTables.addItem(tbl)
        self.ui.totalLabel.setText(str(self.ui.listOfTables.count()))
        #Reading bases from config
        bases = settings.value('db_structure/bases', '').split('>>')
        self.ui.dbListComboBox.clear()
        for db in bases:
            if  db !='':
                self.ui.dbListComboBox.addItem(db)
        #db_strucure tab settings
        self.ui.lineUrl.setText(settings.value('db_structure/url', ''))
        self.ui.comboBox.setCurrentIndex(int(settings.value('db_structure/method', 0)))
        self.ui.textEdit.setText(settings.value('db_structure/data', ''))
        self.ui.lineCookie.setText(settings.value('db_structure/cookies', ''))
        self.ui.comboBox_3.setCurrentIndex(int(settings.value('db_structure/db_type', 0)))
        self.ui.lineMP.setText(settings.value('db_structure/pattern', ''))
        self.ui.lineMS.setText(settings.value('db_structure/symbol', '~'))
        self.ui.dbListComboBox.setCurrentIndex(int(settings.value('db_structure/current_db', 0)))
        self.ui.threadBox.setValue(int(settings.value('db_structure/threads', 10)))
        self.ui.lineTimeout.setText(settings.value('db_structure/timeout', '30'))
        #dump tab settings
        self.ui.lineTable.setText(settings.value('dump/table', ''))
        self.ui.lineColumns.setText(settings.value('dump/columns', ''))
        self.ui.lineKey.setText(settings.value('dump/key', ''))
        self.ui.lineFrom.setText(settings.value('dump/from', '0'))
        self.ui.lineTo.setText(settings.value('dump/to', '10'))
        
#================================MENU=TOOLS======================================#
    def menuEncoder_OnClick(self):
        self.enc_frm.show()
    
    def queryEditor_OnClick(self):
        self.qeditor_frm.show()
        
#Reading default or custom query strings
    @QtCore.pyqtSlot()
    def readQstrings(self):
        cfgparser = configparser.ConfigParser()
        customPath = os.path.normcase("settings/") + "qstrings_custom.ini"
        defaultPath = os.path.normcase("settings/") + "qstrings.ini"
        if os.path.exists(customPath):
            cfgparser.read_file(open(customPath))
        else:
            cfgparser.read_file(open(defaultPath))
        self.qstrings = cfgparser

#================================MENU=ABOUT======================================#
    def menuAbout_OnClick(self):
        self.about_frm.show()

#=================================DB/TABLES=BLOCK================================#
#Getting request method
    def getMethod(self):
        if str(self.ui.comboBox.currentText()) == "POST":
            return "POST"
        else:
            return "GET"
 
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
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.dbSignal.connect(self.addBase, type=QtCore.Qt.QueuedConnection)
        self.t.progressSignal.connect(self.updatePb, type=QtCore.Qt.QueuedConnection)
        self.t.start()
                
#Updating main progressBar
    @QtCore.pyqtSlot(int, bool)
    def updatePb(self, pbMax, hidePb):
        if hidePb:
            self.ui.progressBar.hide()
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
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)    
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
        self.t = ErrorBased(wD, self.qstrings)       
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.msgSignal.connect(self.showInfoMsg)
        self.t.dbSignal.connect(self.addBase, type=QtCore.Qt.QueuedConnection)
        self.t.start()
        
#Show Informational MessageBox:
    @QtCore.pyqtSlot(str)
    def showInfoMsg(self, msg):
        QtGui.QMessageBox.information(self, "Enema", msg, 1, 0)

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
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
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
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.rowDataSignal.connect(self.addRowData, type=QtCore.Qt.QueuedConnection)
        self.t.progressSignal.connect(self.updatePbDump, type=QtCore.Qt.QueuedConnection)
        self.t.start()          

#Updating Dump progressBar
    @QtCore.pyqtSlot(int, bool)
    def updatePbDump(self, pbMax, hidePb):
        if hidePb:
            self.ui.progressBarDump.hide()
            self.ui.tabWidget.setTabEnabled(0, True)
            self.ui.tabWidget.setTabEnabled(2, True)
            self.ui.tabWidget.setTabEnabled(3, True)
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
        
#=============================XP_CMDSHELL=BLOCK=======================================# 
#Press Enter in lineCmd
    def lineCmd_OnPressEnter(self):
        wD = self.webData()
        wD['task'] = "cmd"
        self.ui.lineCmd.clear()
        self.ui.cmdOutput.clear()
        self.ui.progressBar.setValue(0)
        self.ui.progressBarCmd.setMaximum(0)
        self.ui.progressBarCmd.show()
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.cmdSignal.connect(self.cmdOutputAppend, type=QtCore.Qt.QueuedConnection)
        self.t.progressSignal.connect(self.updatePbCmd, type=QtCore.Qt.QueuedConnection)
        self.t.start()

#Updating CMD progressBar
    @QtCore.pyqtSlot(int, bool)
    def updatePbCmd(self, pbMax, hidePb):
        if hidePb:
            self.ui.progressBarCmd.hide()
            return
        self.ui.progressBarCmd.setMaximum(pbMax)
        self.ui.progressBarCmd.setValue(self.ui.progressBarCmd.value() + 1)
        
#Add text to textOutput
    @QtCore.pyqtSlot(int, str, bool, int)
    def cmdOutputAppend(self, rowNum, string, build, rowsCount):
        if build:
            self.ui.cmdOutput.setRowCount(rowsCount)
            return
        rData = QtGui.QTableWidgetItem()
        rData.setText(string)
        self.ui.cmdOutput.setItem(rowNum, 0, rData)

#Enable xp_cmdshell button click    
    def enableXpcmdButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "enable_cmd"
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.msgSignal.connect(self.showInfoMsg)
        self.t.start()
        
#==============================UPLOAD/QUERY=BLOCK=================================#
#FTP Upload button click        
    def ftpButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "ftp"
        if self.ui.radioGet.isChecked():
            wD['ftp_mode'] = 'get'
        else:
            wD['ftp_mode'] = 'send'
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.start()   
 
#Query button click    
    def queryButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "query"
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
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
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.msgSignal.connect(self.showInfoMsg)
        self.t.start()
        
#Add user button click 
    def addUserButton_OnClick(self):
        wD = self.webData()
        wD['task'] = "addSqlUser"
        self.t = ErrorBased(wD, self.qstrings)
        self.t.debugSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.reqLogSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        self.t.msgSignal.connect(self.showInfoMsg)
        self.t.start()
        
#========================================END==========================================#
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mform = EnemaForm()
    mform.show()
    sys.exit(app.exec_())
