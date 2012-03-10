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
import core.txtproc
import configparser
#Plugins
#ftp
from plugins.mssql.ftp import FtpWidget
#add_user
from plugins.mssql.addUser import AddUserWidget
#openrowset
from plugins.mssql.openrowset import OpenrowsetWidget
#xp_cmdshell
from plugins.mssql.xp_cmdshell import CmdShellWidget
#---
from core.injector import ErrorBased
from PyQt4 import QtCore, QtGui 
from gui.main.Ui_form import Ui_MainForm
from gui.main.Ui_encoder_form import Ui_EncoderForm
from gui.main.Ui_about_form import Ui_AboutForm
from gui.main.Ui_query_editor import Ui_QueryEditorForm

#Query editor form GUI class
class QueryEditorForm(QtGui.QMainWindow):
    
    qstringsChanged = QtCore.pyqtSignal()
    logSignal = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.Tool)
        self.ui = Ui_QueryEditorForm()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.loadQstrings()
        #SIGNALS-----------------------------------------------------------------------
        self.ui.qsSave.triggered.connect(self.qsSave_OnClick)
        self.ui.qsRestore.triggered.connect(self.qsRestore_OnClick)
        
    #Loading querystrings to GUI
    def loadQstrings(self):
        if os.path.exists("settings/qstrings_custom.ini"):
            settings = QtCore.QSettings("settings/qstrings_custom.ini", QtCore.QSettings.IniFormat)
        else:
            settings = QtCore.QSettings("settings/qstrings.ini", QtCore.QSettings.IniFormat)
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
        self.ui.q_ms_exec_cmdshell.setText(settings.value('mssql_error_based/exec_cmdshell', ''))
        self.ui.q_ms_get_row.setText(settings.value('mssql_error_based/get_row', ''))
        #etc
        self.ui.q_ms_rows_count.setText(settings.value('mssql_error_based/rows_count', ''))
        self.ui.q_ms_query.setText(settings.value('mssql_error_based/query', ''))
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
        settings = QtCore.QSettings("settings/qstrings_custom.ini", QtCore.QSettings.IniFormat)
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
        settings.setValue('mssql_error_based/exec_cmdshell', self.ui.q_ms_exec_cmdshell.text())
        settings.setValue('mssql_error_based/get_row', self.ui.q_ms_get_row.text())
        #etc
        settings.setValue('mssql_error_based/rows_count', self.ui.q_ms_rows_count.text())
        settings.setValue('mssql_error_based/query', self.ui.q_ms_query.text())
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
        self.logSignal.emit("[+] Customised query strings saved to: " + os.path.abspath("settings/qstrings_custom.ini"))
        self.qstringsChanged.emit()

    #Reset query strings to default
    def qsRestore_OnClick(self):
        customPath = "settings/qstrings_custom.ini"
        if os.path.exists(customPath):
            try:
                os.remove(customPath)
            except Exception:
                self.logSignal.emit("[x] Cannot remove file (access denied): " + os.path.abspath(customPath))
        else:
            return
        self.loadQstrings()
        self.logSignal.emit("[+] Query strings restored to default.")
        self.qstringsChanged.emit()
        
#Enccoder form GUI class
class EncoderForm(QtGui.QWidget):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.Tool)
        self.ui = Ui_EncoderForm()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui.decodeButton.hide()
    #SIGNALS------------------------------------------------------------------------
        self.ui.encodeButton.clicked.connect(self.encodeButton_OnClick)
        self.ui.decodeButton.clicked.connect(self.decodeButton_OnClick)
        self.ui.comboBox.currentIndexChanged.connect(self.comboChanged)
        
    #Encode button click
    def encodeButton_OnClick(self):
        string = self.ui.lineString.text()
        if len(string) < 1:
            return
        if self.ui.isPlay.isChecked():
            string = core.txtproc.rndUpCase(string)
        if self.ui.comboBox.currentText() == "Base64":
            readyStr = core.txtproc.base64proc(string, "enc")
            self.ui.textResult.setText(readyStr)
            return
        if self.ui.radioHex.isChecked():
            hexStr = core.txtproc.strToHex(string, False)
            if self.ui.isUrlencoded.isChecked():
                readyStr = hexStr.replace("0x", "%")
            else:
                readyStr = core.txtproc.strToHex(string, True)
        else:
            if self.ui.comboBox.currentText() == "MySQL":
                readyStr = core.txtproc.strToSqlChar(string, "mysql")
            else:
                readyStr = core.txtproc.strToSqlChar(string, "mssql")
                if self.ui.isUrlencoded.isChecked():
                    readyStr = readyStr.replace("+",  "%2b")
        self.ui.textResult.setText(readyStr)

    #Encode button click
    def decodeButton_OnClick(self):
        string = self.ui.lineString.text()
        readyStr = core.txtproc.base64proc(string, "dec")
        self.ui.textResult.setText(readyStr)
        
    #ComboBox changed:
    def comboChanged(self):
        if self.ui.comboBox.currentText() == "Base64":
            self.ui.decodeButton.show()
            self.ui.radioChar.setEnabled(False)
            self.ui.radioHex.setEnabled(False)
            self.ui.isUrlencoded.setEnabled(False)
        else:
            self.ui.decodeButton.hide()
            self.ui.radioChar.setEnabled(True)
            self.ui.radioHex.setEnabled(True)
            self.ui.isUrlencoded.setEnabled(True)
        
#About form GUI class
class AboutForm(QtGui.QWidget):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent,\
                               QtCore.Qt.Tool |\
                               QtCore.Qt.WindowTitleHint |\
                               QtCore.Qt.CustomizeWindowHint)
        self.ui = Ui_AboutForm()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        #Set current program version
        self.ui.versionLabel.setText("Version: 1.5")

#Main form GUI class
class EnemaForm(QtGui.QMainWindow):
    
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.setFixedSize(591, 618)
        self.ui.progressBar.hide()
        self.ui.progressBarDump.hide()
        #Forms / widgets
        self.qeditor_frm = QueryEditorForm(self)
        self.enc_frm = EncoderForm(self)
        self.about_frm = AboutForm(self)
        configPath = "settings/enema.ini"
        #Loading settings if ini file exists
        if os.path.exists(configPath):
            settings = QtCore.QSettings(configPath, QtCore.QSettings.IniFormat)
            #Etc
            self.ui.queryText.setText(settings.value('other/query', ''))
            #restoring widgets position
            widgetPosition = settings.value("GUI/mainWpos")
            self.move(widgetPosition)
            self.enc_frm.move(widgetPosition)
            self.qeditor_frm.move(widgetPosition)
            self.about_frm.move(widgetPosition)
        #Query strings loading
        self.readQstrings()
        
        
        #self.errBased.setVars(None, None)
#SIGNAL CONNECTIONS--------------------------------------------------------------------------
        #Query changed in editor
        self.qeditor_frm.qstringsChanged.connect(self.readQstrings)
        #DB_STRUCTURE-TAB
        self.ui.getBasesButton.clicked.connect(self.getBasesButton_OnClick)
        self.ui.tablesButton.clicked.connect(self.tablesButton_OnClick)
        self.ui.countButton.clicked.connect(self.countButton_OnClick)
        self.ui.getColumnsButton.clicked.connect(self.getColumnsButton_OnClick)
        self.ui.cleanThreeButton.clicked.connect(self.cleanThreeButton_OnClick)
        self.ui.logButton.clicked.connect(self.logButton_OnClick)
        self.ui.clearLogButton.clicked.connect(self.clearLogButton_OnClick)
        self.ui.killButton.clicked.connect(self.killTask)
        self.ui.killDumpButton.clicked.connect(self.killTask)
        #DUMP-TAB
        self.ui.dmpButton.clicked.connect(self.dmpButton_OnClick)
        #QUERY-TAB
        self.ui.queryButton.clicked.connect(self.queryButton_OnClick)
        #Save Menu 
        self.ui.saveTables.triggered.connect(self.saveTables_OnClick)
        self.ui.saveColumns.triggered.connect(self.saveColumns_OnClick)
        self.ui.saveBases.triggered.connect(self.saveBases_OnClick)
        self.ui.csvExport.triggered.connect(self.csvExport_OnClick)
        self.ui.ssSettings.triggered.connect(self.saveSiteSettings_OnClick)
        #Load Menu
        self.ui.loadTables.triggered.connect(self.loadTables_OnClick)
        self.ui.loadBases.triggered.connect(self.loadBases_OnClick)
        self.ui.lsSettings.triggered.connect(self.loadSiteSettings_OnClick)
        #Tools Menu
        self.ui.menuEncoder.triggered.connect(self.menuEncoder_OnClick)
        self.ui.qEditor.triggered.connect(self.queryEditor_OnClick)
        #Help menu
        self.ui.menuAbout.triggered.connect(self.menuAbout_OnClick)
        #Db Type change
        self.ui.comboBox_3.currentIndexChanged.connect(self.dbTypeChanged)
        
#-+++++++++++PLUGIN-SIGNAL-CONNECTS++++++++++++#
        #ftp
        self.ui.actionFtp.triggered.connect(self.actionFtp_OnClick)
        #add_user
        self.ui.actionAdd_user.triggered.connect(self.actionAdd_user_OnClick)
        #openrowset
        self.ui.actionOpenrowset.triggered.connect(self.actionOpenrowset_OnClick)
        #xp_cmdshell
        self.ui.actionXp_cmdshell.triggered.connect(self.actionXp_cmdshell_OnClick)
#++++++++++++PLUGIN+SLOTS++++++++++++#
    #ftp    
    def actionFtp_OnClick(self):
        self.pluginWidget = FtpWidget(self.webData(), self.qstrings['mssql_error_based']['exec_cmdshell'], self)
        self.pluginWidget.logSignal.connect(self.addLog)
        self.pluginWidget.show()
        self.pluginWidget.activateWindow()

    #add_user       
    def actionAdd_user_OnClick(self):
        self.pluginWidget = AddUserWidget(self.webData(), self.qstrings['mssql_error_based']['exec_cmdshell'], self)
        self.pluginWidget.logSignal.connect(self.addLog)
        self.pluginWidget.show()
        self.pluginWidget.activateWindow()
        
    #openrowset      
    def actionOpenrowset_OnClick(self):
        self.pluginWidget = OpenrowsetWidget(self.webData(), self.qstrings['mssql_error_based']['exec_cmdshell'], self)
        self.pluginWidget.logSignal.connect(self.addLog)
        self.pluginWidget.show()
        self.pluginWidget.activateWindow()
    
    
    def actionXp_cmdshell_OnClick(self):
        self.pluginWidget = CmdShellWidget(self.webData(), self.qstrings['mssql_error_based'], self)
        self.pluginWidget.logSignal.connect(self.addLog)
        self.pluginWidget.show()
        self.pluginWidget.activateWindow()
#+++++++++++++++++++++++++++++++#

    #When form closing
    def closeEvent(self, event):
        #Saving main and log window position
        settings = QtCore.QSettings("settings/enema.ini", QtCore.QSettings.IniFormat)
        settings.setValue('GUI/mainWpos', self.pos())
        sys.exit(0)

    #Add text to log
    def addLog(self, logStr):
        #Autoclean log when blocks more than 3000
        if self.ui.logTxtEdit.document().blockCount() > 3000:
            self.ui.logTxtEdit.clear()
        self.ui.logTxtEdit.append("\n" + logStr)
        #Autoscrolling
        sb = self.ui.logTxtEdit.verticalScrollBar()
        sb.setValue(sb.maximum())
    
    #Get user defined parametes from GUI
    def webData(self):
        if not self.ui.listOfTables.currentItem():
            currTable = ""
        else:
            currTable = self.ui.listOfTables.currentItem().text()
        wD = {
              'url' : self.ui.lineUrl.text(), 
              'method' : self.getMethod() , 
              'mp' : self.ui.lineMP.text(), 
              'ms' : self.ui.lineMS.text(), 
              'threads' : int(self.ui.threadBox.value()), 
              'timeOut' : int(self.ui.lineTimeout.text()), 
              'isRandomUpCase' : self.ui.isRndUpper.isChecked(), 
              'dbListCount' : self.ui.dbListComboBox.count(),
              'dbName' : str(self.ui.dbListComboBox.currentText()), 
              'notInArray' : self.ui.radioNotInArray.isChecked(),
              'notInSubstring' : self.ui.radioNotInSubstring.isChecked(),
              'ordinal_position' : self.ui.radioOrdinalPosition.isChecked(), 
              'selected_table' : currTable, 
              'tblTreeCount' : self.ui.treeOfTables.topLevelItemCount(), 
              'query_cmd' : self.ui.queryText.toPlainText(), 
              'querySelect' : self.ui.radioSelect.isChecked(), 
              'data' : self.ui.textEdit.toPlainText(), 
              'cookie' :  self.ui.lineCookie.text(), 
              'db_type' : self.getDbType(), 
              'table' : self.ui.lineTable.text(), 
              'key' : self.ui.lineKey.text(), 
              'columns' : self.ui.lineColumns.text().split(";"), 
              'fromPos' : int(self.ui.lineFrom.text()), 
              'toPos' :  int(self.ui.lineTo.text())}
        return wD

    #Sending kill flag to qthread
    def killTask(self):
        try:
            self.qthread.kill()
        except AttributeError:
            return

    #Is program busy at this moment
    def isBusy(self):
        try:
            if self.qthread.isRunning():
                return True
        except AttributeError:
            return False

    #Connecting to signals and starting thread
    def connectAndStart(self):
        #logSignal
        self.qthread.logSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        #progressSignal
        self.qthread.progressSignal.connect(self.updatePb, type=QtCore.Qt.QueuedConnection)
        #dumpProgressSignal
        self.qthread.dumpProgressSignal.connect(self.updatePbDump, type=QtCore.Qt.QueuedConnection)
        #msgSignal
        self.qthread.msgSignal.connect(self.showInfoMsg, type=QtCore.Qt.QueuedConnection)
        #dbSignal
        self.qthread.dbSignal.connect(self.addBase, type=QtCore.Qt.QueuedConnection)
        #columnSignal
        self.qthread.columnSignal.connect(self.addColumn, type=QtCore.Qt.QueuedConnection)
        #rowDataSignal
        self.qthread.rowDataSignal.connect(self.addRowData, type=QtCore.Qt.QueuedConnection)
        #querySignal
        self.qthread.querySignal.connect(self.queryResult, type=QtCore.Qt.QueuedConnection)
        #tblCountSignal
        self.qthread.tblCountSignal.connect(self.setTblCount, type=QtCore.Qt.QueuedConnection)
        #tblSignal
        self.qthread.tblSignal.connect(self.addTable, type=QtCore.Qt.QueuedConnection)
        #Starting QThread
        self.qthread.start()

    #Show busy dialog
    def busyDialog(self):
        clicked = QtGui.QMessageBox.question(self, "Enema", "Program busy. Kill current task?",\
                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if clicked == QtGui.QMessageBox.Yes:
            self.killTask()
        else:
            return
            
    #Db type changed event:
    def dbTypeChanged(self):
        if self.getDbType() == "mysql":
            self.ui.radioNotInSubstring.setText("LIMIT")
            self.ui.radioNotInSubstring.setChecked(True)
            self.ui.radioNotInArray.hide()
            self.ui.tabs.setTabEnabled(3, False)
            self.ui.menuMssql.setEnabled(False)
        else:
            self.ui.tabs.setTabEnabled(3, True)
            self.ui.radioNotInSubstring.setText("not in(substring)")
            self.ui.radioNotInArray.show()
            self.ui.radioNotInArray.setChecked(True)
            self.ui.menuMssql.setEnabled(True)
            
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
            file.close()
        except Exception:
            return
        
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
        self.enc_frm.activateWindow()
        
    def queryEditor_OnClick(self):
        self.qeditor_frm.logSignal.connect(self.addLog)
        self.qeditor_frm.show()
        self.qeditor_frm.activateWindow()
        
    #Reading default or custom query strings
    def readQstrings(self):
        cfgparser = configparser.ConfigParser()
        customPath = "settings/qstrings_custom.ini"
        defaultPath = "settings/qstrings.ini"
        if os.path.exists(customPath):
            cfgparser.read_file(open(customPath))
        else:
            cfgparser.read_file(open(defaultPath))
        self.qstrings = cfgparser
    
#================================MENU=ABOUT======================================#
    def menuAbout_OnClick(self):
        self.about_frm.show()
        self.about_frm.activateWindow()

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
        if self.isBusy():
            self.busyDialog()
            return
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
        self.qthread = ErrorBased(wD, self.qstrings)
        self.connectAndStart()
        
        
    #Updating main progressBar
    def updatePb(self, pbMax, taskDone):
        if taskDone:
            self.ui.progressBar.hide()
            return
        self.ui.progressBar.setMaximum(pbMax)
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)
        
    #Get Tables button click      
    def tablesButton_OnClick(self):
        if self.isBusy():
            self.busyDialog()
            return
        wD = self.webData()
        wD['task'] = 'tables'
        if self.ui.radioOrdinalPosition.isChecked():
            self.showInfoMsg("ordinal_position method valid only for columns.")
            return
        if len(self.ui.lineUrl.text()) < 6 or not ("http" in self.ui.lineUrl.text()):
            return
        self.ui.listOfTables.clear()
        self.ui.totalLabel.setText("0")
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        self.qthread = ErrorBased(wD, self.qstrings)
        self.connectAndStart()
        
    #Add db to listBox
    def addBase(self, db_name):
        self.ui.dbListComboBox.addItem(db_name)

    #Set label value to count of tables in current db
    def setTblCount(self, tblCount):
        self.ui.totalLabel.setText(tblCount)

    #Add table to ListWidget
    def addTable(self, table_name):
        self.ui.listOfTables.addItem(table_name)
            
    #Count button click
    def countButton_OnClick(self):
        if self.isBusy():
            self.busyDialog()
            return
        wD = self.webData()
        wD['task'] = 'count'
        if not self.ui.listOfTables.currentItem():
            return
        self.qthread = ErrorBased(wD, self.qstrings)
        self.connectAndStart()

        
    #Show or Hide log field
    def logButton_OnClick(self):
        if self.ui.logButton.text() == "Show log":
            self.setFixedSize(1112, 618)
            self.resize(1112, 618)
            self.ui.logButton.setText("Hide log")
        else:
            self.setFixedSize(591, 618)
            self.resize(591, 618)
            self.ui.logButton.setText("Show log")
        
    #Cleaning log
    def clearLogButton_OnClick(self):
        self.ui.logTxtEdit.clear()

    #Show Informational MessageBox:
    def showInfoMsg(self, msg):
        QtGui.QMessageBox.information(self, "Enema", msg, 1, 0)

#==============================COLUMNS=BLOCK=========================================#    
    #Get columns button click       
    def getColumnsButton_OnClick(self):
        if self.isBusy():
            self.busyDialog()
            return
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
        self.qthread = ErrorBased(wD, self.qstrings)
        self.connectAndStart()
                
    #Adding columns to TreeWidget
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
        if self.isBusy():
            self.busyDialog()
            return
        if len(self.ui.lineUrl.text()) < 6 or not ("http" in self.ui.lineUrl.text()):
            return
        if len(self.ui.lineTable.text()) < 1\
        or len(self.ui.lineColumns.text()) < 1\
        or len(self.ui.lineKey.text()) < 1:
            return
        wD = self.webData()
        wD['task'] = 'dump'
        self.ui.tableWidget.clear()
        #Building table
        self.ui.tableWidget.setColumnCount(len(wD['columns']))
        self.ui.tableWidget.setHorizontalHeaderLabels(wD['columns'])
        self.ui.tableWidget.setRowCount(wD['toPos'] - wD['fromPos'])
        self.ui.progressBarDump.setValue(0)
        self.ui.progressBarDump.show()
        self.ui.progressBarDump.setMaximum(self.ui.tableWidget.rowCount() * len(wD['columns']))
        self.qthread = ErrorBased(wD, self.qstrings)
        self.connectAndStart()    

    #Updating Dump progressBar
    def updatePbDump(self, pbMax, taskDone):
        if taskDone:
            self.ui.progressBarDump.hide()
            return
        self.ui.progressBarDump.setValue(self.ui.progressBarDump.value() + 1)
        
    #Add row data
    def addRowData(self,  tNum, num,  rowData):
        rData = QtGui.QTableWidgetItem()
        rData.setText(rowData)
        self.ui.tableWidget.setItem((tNum - int(self.ui.lineFrom.text()) - 1), num, rData)
#==============================QUERY=BLOCK=================================#
    #Query button click    
    def queryButton_OnClick(self):
        if self.isBusy():
            return
        wD = self.webData()
        wD['task'] = "query"
        self.qthread = ErrorBased(wD, self.qstrings)
        self.connectAndStart()

    #Set query result
    def queryResult(self, result):
        self.ui.queryOutput.setText(result)
#========================================END==========================================#

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mform = EnemaForm()
    mform.show()
    sys.exit(app.exec_())
