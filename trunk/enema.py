"""
    Enema module: GUI events (main)
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
import core.txtproc
import configparser
#Plugins
#ftp
from plugins.mssql.ftp import FtpWidget
#add_user
from plugins.mssql.add_user import AddUserWidget
#openrowset
from plugins.mssql.openrowset import OpenrowsetWidget
#xp_cmdshell
from plugins.mssql.xp_cmdshell import CmdShellWidget

from core.e_const import VERSION
from core.injector import Injector
from core.injector import BlindInjector

from PyQt4 import QtCore, QtGui 

from gui.main.Ui_main import Ui_MainForm
from gui.main.Ui_preferences import Ui_preferencesWidget
from gui.main.Ui_encoder import Ui_EncoderForm
from gui.main.Ui_about import Ui_AboutForm
from gui.main.Ui_query_editor import Ui_QueryEditorForm

#Query editor form GUI class
class QueryEditorForm(QtGui.QMainWindow):
    
    qstringsChanged = QtCore.pyqtSignal()
    logSignal = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.WindowTitleHint)
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
        
        #ERROR-BASED---
        qstring_type = "mssql_error_based/"
        #bases
        self.ui.q_ms_curr_db_name.setText(settings.value(qstring_type + 'curr_db_name', ''))
        self.ui.q_ms_dbs_count.setText(settings.value(qstring_type + 'dbs_count', ''))
        self.ui.q_ms_get_db_name.setText(settings.value(qstring_type + 'get_db_name', ''))
        self.ui.q_ms_get_db_name2.setText(settings.value(qstring_type + 'get_db_name2', ''))
        #tables
        self.ui.q_ms_tbls_count.setText(settings.value(qstring_type + 'tbls_count', ''))
        self.ui.q_ms_get_tbl_name.setText(settings.value(qstring_type + 'get_tbl_name', ''))
        self.ui.q_ms_get_tbl_name2.setText(settings.value(qstring_type + 'get_tbl_name2', ''))
        #columns
        self.ui.q_ms_get_column_name.setText(settings.value(qstring_type + 'get_column_name', ''))
        self.ui.q_ms_columns_count.setText(settings.value(qstring_type + 'columns_count', ''))
        self.ui.q_ms_get_column_name2.setText(settings.value(qstring_type + 'get_column_name2', ''))
        self.ui.q_ms_get_column_name3.setText(settings.value(qstring_type + 'get_column_name3', ''))      
        #xp_cmdshell
        self.ui.q_ms_exec_cmdshell.setText(settings.value(qstring_type + 'exec_cmdshell', ''))
        #etc
        self.ui.q_ms_get_row.setText(settings.value(qstring_type + 'get_row', ''))
        self.ui.q_ms_rows_count.setText(settings.value(qstring_type + 'rows_count', ''))
        self.ui.q_ms_query.setText(settings.value(qstring_type + 'query', ''))
        self.ui.q_ms_data_dump.setText(settings.value(qstring_type + 'data_dump', ''))

        #UNION-BASED---
        qstring_type = "mssql_union_based/"
        #bases
        self.ui.q_union_ms_curr_db_name.setText(settings.value(qstring_type + 'curr_db_name', ''))
        self.ui.q_union_ms_dbs_count.setText(settings.value(qstring_type + 'dbs_count', ''))
        self.ui.q_union_ms_get_db_name.setText(settings.value(qstring_type + 'get_db_name', ''))
        self.ui.q_union_ms_get_db_name2.setText(settings.value(qstring_type + 'get_db_name2', ''))
        #tables
        self.ui.q_union_ms_tbls_count.setText(settings.value(qstring_type + 'tbls_count', ''))
        self.ui.q_union_ms_get_tbl_name.setText(settings.value(qstring_type + 'get_tbl_name', ''))
        self.ui.q_union_ms_get_tbl_name2.setText(settings.value(qstring_type + 'get_tbl_name2', ''))
        #columns
        self.ui.q_union_ms_get_column_name.setText(settings.value(qstring_type + 'get_column_name', ''))
        self.ui.q_union_ms_columns_count.setText(settings.value(qstring_type + 'columns_count', ''))
        self.ui.q_union_ms_get_column_name2.setText(settings.value(qstring_type + 'get_column_name2', ''))
        self.ui.q_union_ms_get_column_name3.setText(settings.value(qstring_type + 'get_column_name3', ''))      
        #etc
        self.ui.q_union_ms_get_row.setText(settings.value(qstring_type + 'get_row', ''))
        self.ui.q_union_ms_rows_count.setText(settings.value(qstring_type + 'rows_count', ''))
        self.ui.q_union_ms_query.setText(settings.value(qstring_type + 'query', ''))
        self.ui.q_union_ms_data_dump.setText(settings.value(qstring_type + 'data_dump', ''))
        
        #BLIND---
        #Time-Based
        qstring_type = "mssql_blind_time_based/"
        self.ui.q_blind_ms_single_row.setText(settings.value(qstring_type + 'single_row', ''))
        self.ui.q_blind_ms_multi_rows.setText(settings.value(qstring_type + 'multi_rows', ''))

        #MySQL------------------------------------------------------------------
        
        #ERROR-BASED----
        qstring_type = "mysql_error_based/"
        #bases
        self.ui.q_my_curr_db_name.setText(settings.value(qstring_type + 'curr_db_name', ''))
        self.ui.q_my_dbs_count.setText(settings.value(qstring_type + 'dbs_count', ''))
        self.ui.q_my_get_db_name2.setText(settings.value(qstring_type + 'get_db_name2', ''))
        #tables
        self.ui.q_my_tbls_count.setText(settings.value(qstring_type + 'tbls_count', ''))
        self.ui.q_my_get_tbl_name2.setText(settings.value(qstring_type + 'get_tbl_name2', ''))
        #columns
        self.ui.q_my_columns_count.setText(settings.value(qstring_type + 'columns_count', ''))
        self.ui.q_my_get_column_name2.setText(settings.value(qstring_type + 'get_column_name2', ''))
        self.ui.q_my_get_column_name3.setText(settings.value(qstring_type + 'get_column_name3', ''))      
        #etc
        self.ui.q_my_rows_count.setText(settings.value(qstring_type + 'rows_count', ''))
        self.ui.q_my_query.setText(settings.value(qstring_type + 'query', ''))
        
        #UNION-Based---
        qstring_type = "mysql_union_based/"
        #bases
        self.ui.q_union_my_curr_db_name.setText(settings.value(qstring_type + 'curr_db_name', ''))
        self.ui.q_union_my_dbs_count.setText(settings.value(qstring_type + 'dbs_count', ''))
        self.ui.q_union_my_get_db_name2.setText(settings.value(qstring_type + 'get_db_name2', ''))
        #tables
        self.ui.q_union_my_tbls_count.setText(settings.value(qstring_type + 'tbls_count', ''))
        self.ui.q_union_my_get_tbl_name2.setText(settings.value(qstring_type + 'get_tbl_name2', ''))
        #columns
        self.ui.q_union_my_columns_count.setText(settings.value(qstring_type + 'columns_count', ''))
        self.ui.q_union_my_get_column_name2.setText(settings.value(qstring_type + 'get_column_name2', ''))
        self.ui.q_union_my_get_column_name3.setText(settings.value(qstring_type + 'get_column_name3', ''))      
        #etc
        self.ui.q_union_my_rows_count.setText(settings.value(qstring_type + 'rows_count', ''))
        self.ui.q_union_my_query.setText(settings.value(qstring_type + 'query', ''))
        #---------------------------------------------------------------------------
        
    def qsSave_OnClick(self):
        #Saving customised querys
        settings = QtCore.QSettings("settings/qstrings_custom.ini", QtCore.QSettings.IniFormat)
        
        #MSSQL------------------------------------------------------------------
        
        #ERROR-BASED---
        qstring_type = "mssql_error_based/"
        #bases
        settings.setValue(qstring_type + 'curr_db_name', self.ui.q_ms_curr_db_name.text())
        settings.setValue(qstring_type + 'dbs_count', self.ui.q_ms_dbs_count.text())
        settings.setValue(qstring_type + 'get_db_name', self.ui.q_ms_get_db_name.text())
        settings.setValue(qstring_type + 'get_db_name2', self.ui.q_ms_get_db_name2.text())
        #tables
        settings.setValue(qstring_type + 'tbls_count', self.ui.q_ms_tbls_count.text())
        settings.setValue(qstring_type + 'get_tbl_name', self.ui.q_ms_get_tbl_name.text())
        settings.setValue(qstring_type + 'get_tbl_name2', self.ui.q_ms_get_tbl_name2.text())
        #columns
        settings.setValue(qstring_type + 'get_column_name', self.ui.q_ms_get_column_name.text())
        settings.setValue(qstring_type + 'columns_count', self.ui.q_ms_columns_count.text())
        settings.setValue(qstring_type + 'get_column_name2', self.ui.q_ms_get_column_name2.text())
        settings.setValue(qstring_type + 'get_column_name3', self.ui.q_ms_get_column_name3.text())    
        #xp_cmdshell
        settings.setValue(qstring_type + 'exec_cmdshell', self.ui.q_ms_exec_cmdshell.text())
        #etc
        settings.setValue(qstring_type + 'get_row', self.ui.q_ms_get_row.text())
        settings.setValue(qstring_type + 'rows_count', self.ui.q_ms_rows_count.text())
        settings.setValue(qstring_type + 'query', self.ui.q_ms_query.text())
        settings.setValue(qstring_type + 'data_dump', self.ui.q_ms_data_dump.text())
        
        #UNION-BASED---
        qstring_type = "mssql_union_based/"
        #bases
        settings.setValue(qstring_type + 'curr_db_name', self.ui.q_union_ms_curr_db_name.text())
        settings.setValue(qstring_type + 'dbs_count', self.ui.q_union_ms_dbs_count.text())
        settings.setValue(qstring_type + 'get_db_name', self.ui.q_union_ms_get_db_name.text())
        settings.setValue(qstring_type + 'get_db_name2', self.ui.q_union_ms_get_db_name2.text())
        #tables
        settings.setValue(qstring_type + 'tbls_count', self.ui.q_union_ms_tbls_count.text())
        settings.setValue(qstring_type + 'get_tbl_name', self.ui.q_union_ms_get_tbl_name.text())
        settings.setValue(qstring_type + 'get_tbl_name2', self.ui.q_union_ms_get_tbl_name2.text())
        #columns
        settings.setValue(qstring_type + 'get_column_name', self.ui.q_union_ms_get_column_name.text())
        settings.setValue(qstring_type + 'columns_count', self.ui.q_union_ms_columns_count.text())
        settings.setValue(qstring_type + 'get_column_name2', self.ui.q_union_ms_get_column_name2.text())
        settings.setValue(qstring_type + 'get_column_name3', self.ui.q_union_ms_get_column_name3.text())    
        #etc
        settings.setValue(qstring_type + 'get_row', self.ui.q_union_ms_get_row.text())
        settings.setValue(qstring_type + 'rows_count', self.ui.q_union_ms_rows_count.text())
        settings.setValue(qstring_type + 'query', self.ui.q_union_ms_query.text())
        settings.setValue(qstring_type + 'data_dump', self.ui.q_union_ms_data_dump.text())
        
        #BLIND---
        #Time-Based
        qstring_type = "mssql_blind_time_based/"
        settings.setValue(qstring_type + 'single_row', self.ui.q_blind_ms_single_row.text())
        settings.setValue(qstring_type + 'multi_rows', self.ui.q_blind_ms_multi_rows.text())
        
        #MySQL------------------------------------------------------------------
        
        #ERROR-BASED---
        qstring_type = "mysql_error_based/"
        #bases
        settings.setValue(qstring_type + 'curr_db_name', self.ui.q_my_curr_db_name.text())
        settings.setValue(qstring_type + 'dbs_count', self.ui.q_my_dbs_count.text())
        settings.setValue(qstring_type + 'get_db_name2', self.ui.q_my_get_db_name2.text())
        #tables
        settings.setValue(qstring_type + 'tbls_count', self.ui.q_my_tbls_count.text())
        settings.setValue(qstring_type + 'get_tbl_name2', self.ui.q_my_get_tbl_name2.text())
        #columns
        settings.setValue(qstring_type + 'columns_count', self.ui.q_my_columns_count.text())
        settings.setValue(qstring_type + 'get_column_name2', self.ui.q_my_get_column_name2.text())
        settings.setValue(qstring_type + 'get_column_name3', self.ui.q_my_get_column_name3.text())    
        #etc
        settings.setValue(qstring_type + 'rows_count', self.ui.q_my_rows_count.text())
        settings.setValue(qstring_type + 'query', self.ui.q_my_query.text())
        
        #UNION-BASED---
        qstring_type = "mysql_union_based/"
        #bases
        settings.setValue(qstring_type + 'curr_db_name', self.ui.q_union_my_curr_db_name.text())
        settings.setValue(qstring_type + 'dbs_count', self.ui.q_union_my_dbs_count.text())
        settings.setValue(qstring_type + 'get_db_name2', self.ui.q_union_my_get_db_name2.text())
        #tables
        settings.setValue(qstring_type + 'tbls_count', self.ui.q_union_my_tbls_count.text())
        settings.setValue(qstring_type + 'get_tbl_name2', self.ui.q_union_my_get_tbl_name2.text())
        #columns
        settings.setValue(qstring_type + 'columns_count', self.ui.q_union_my_columns_count.text())
        settings.setValue(qstring_type + 'get_column_name2', self.ui.q_union_my_get_column_name2.text())
        settings.setValue(qstring_type + 'get_column_name3', self.ui.q_union_my_get_column_name3.text())    
        #etc
        settings.setValue(qstring_type + 'rows_count', self.ui.q_union_my_rows_count.text())
        settings.setValue(qstring_type + 'query', self.ui.q_union_my_query.text())
        
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
                readyStr = core.txtproc.strToSqlChar(string, "MySQL")
            else:
                readyStr = core.txtproc.strToSqlChar(string, "MSSQL")
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


#Preferences widget
class PreferencesForm(QtGui.QMainWindow):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.WindowTitleHint)
        self.ui = Ui_preferencesWidget()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
    
    def closeEvent(self, event):
        settings = QtCore.QSettings("settings/enema.ini", QtCore.QSettings.IniFormat)
        settings.setValue('Main/match_symbol', self.ui.lineMS.text())
        settings.setValue('Main/match_pattern', self.ui.lineMP.text())
        settings.setValue('Main/threads', self.ui.threadBox.value())
        settings.setValue('Main/timeout', self.ui.lineTimeout.text())
        settings.setValue('Main/rnd_upcase', self.ui.isRndUpper.isChecked())
        settings.sync()
        
#Main form GUI class
class EnemaForm(QtGui.QMainWindow):
    
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowTitleHint)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        
        #Setting fixed form size
        self.setFixedSize(591, 624)
        #-----------------ICONS-----------------  
        #Tray and window icon
        trayIcon = QtGui.QIcon("gui/resources/icons/tray.png")
        self.setWindowIcon(trayIcon)
        #Tab icons
        self.ui.tabs.setTabIcon(0, QtGui.QIcon("gui/resources/icons/db_structure.png"))
        self.ui.tabs.setTabIcon(1, QtGui.QIcon("gui/resources/icons/query.png"))
        self.ui.tabs.setTabIcon(2, QtGui.QIcon("gui/resources/icons/dump.png"))

        #Tray menu
        self.actionQuit = QtGui.QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.setText("Quit")
        self.trayMenu = QtGui.QMenu()
        self.trayMenu.setObjectName("trayMenu")
        self.trayMenu.addAction(self.ui.menuEncoder)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(self.actionQuit)
        #System tray icon
        self.sysTray=QtGui.QSystemTrayIcon(trayIcon, self)
        self.sysTray.setToolTip("Enema " + VERSION)
        self.sysTray.setContextMenu(self.trayMenu)
        if self.sysTray.isSystemTrayAvailable():
            self.sysTray.show()
            
        self.ui.progressBar.hide()
        self.ui.blindMethodList.setVisible(False)
        self.ui.methodLabel.setVisible(False)
        self.ui.delayBox.setVisible(False)
        self.ui.isMultirows.setVisible(False)
        self.ui.testButton.setVisible(False)
        self.ui.delayLabel.setVisible(False)
        
        #Subforms
        self.qeditor_frm = QueryEditorForm(self)
        self.enc_frm = EncoderForm(self)
        self.about_frm = AboutForm(self)
        self.preferences_frm = PreferencesForm(self)
        
        #Show only one minimising message per program launch
        self.firstHide = True
        
        #Set current program version and logo
        self.about_frm.ui.versionLabel.setText("Version: " + VERSION)
        self.about_frm.ui.logoLabel.setPixmap(QtGui.QPixmap("gui/resources/logo.png"))
        
        configPath = "settings/enema.ini"
        #Loading settings if ini file exists
        if os.path.exists(configPath):
            settings = QtCore.QSettings(configPath, QtCore.QSettings.IniFormat)
            #query field
            self.ui.queryText.setText(settings.value('Main/query', ''))
            self.preferences_frm.ui.lineMS.setText(settings.value('Main/match_symbol', '~'))
            self.preferences_frm.ui.lineMP.setText(settings.value('Main/match_pattern', ''))
            self.preferences_frm.ui.threadBox.setValue(settings.value('Main/threads', 5, int))
            self.preferences_frm.ui.lineTimeout.setText(settings.value('Main/timeout', '60'))
            self.preferences_frm.ui.isRndUpper.setChecked(settings.value('Main/rnd_upcase', False, bool))
            #restoring widgets position
            widgetPosition = settings.value("Main/window_position")
            self.move(widgetPosition)
            self.enc_frm.move(widgetPosition)
            self.qeditor_frm.move(widgetPosition)
            self.about_frm.move(widgetPosition)
            self.preferences_frm.move(widgetPosition)
        #Query strings loading
        self.readQstrings()
        
#------------------------------------------------SIGNAL-CONNECTIONS------------------------------------------------------#

        #Query changed in editor
        self.qeditor_frm.qstringsChanged.connect(self.readQstrings)
        
        #DB_STRUCTURE-TAB
        self.ui.runButton.clicked.connect(self.runButton_OnClick)
        self.ui.cleanColumnsButton.clicked.connect(self.cleanColumnsButton_OnClick)
        self.ui.radioTables.toggled.connect(self.radioTables_Toggled)
        self.ui.radioColumns.toggled.connect(self.radioColumns_Toggled)
        self.ui.radioBases.toggled.connect(self.radioBases_Toggled)
        self.ui.logButton.clicked.connect(self.logButton_OnClick)
        self.ui.clearLogButton.clicked.connect(self.clearLogButton_OnClick)
        self.ui.killButton.clicked.connect(self.killTask)
        
        #DUMP-TAB
        self.ui.dmpButton.clicked.connect(self.dmpButton_OnClick)
        
        #QUERY-TAB
        self.ui.queryButton.clicked.connect(self.queryButton_OnClick)
        self.ui.testButton.clicked.connect(self.testButton_OnClick)
        
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
        self.ui.actionPreferences.triggered.connect(self.preferences_OnClick)
        
        #Help menu
        self.ui.menuAbout.triggered.connect(self.menuAbout_OnClick)
        self.ui.actionManual.triggered.connect(self.actionManual_OnClick)
        
        #Db Type change
        self.ui.dbTypeBox.currentIndexChanged.connect(self.dbTypeChanged)
        
        #Request method changed
        self.ui.comboBox.currentIndexChanged.connect(self.methodChanged)
        
        #Url edit finished
        self.ui.lineUrl.editingFinished.connect(self.urlEditFinished)
        
        #Current tab changed
        self.ui.tabs.currentChanged.connect(self.tabIndexChanged)
        
        #Tray icon
        self.actionQuit.triggered.connect(self.trayQuit_Clicked)
        self.sysTray.activated.connect(self.trayActivated)

#--------------------------------------------[MENU]PLUGINS-SIGNAL-CONNECTS-------------------------------------------------#

        #ftp
        self.ui.actionFtp.triggered.connect(self.actionFtp_OnClick)
        #add_user
        self.ui.actionAdd_user.triggered.connect(self.actionAdd_user_OnClick)
        #openrowset
        self.ui.actionOpenrowset.triggered.connect(self.actionOpenrowset_OnClick)
        #xp_cmdshell
        self.ui.actionXp_cmdshell.triggered.connect(self.actionXp_cmdshell_OnClick)
        
#------------------------------------------------[MENU]PLUGIN-MENU-SLOTS------------------------------------------------------#
        
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
        self.pluginWidget = CmdShellWidget(self.webData(), self.qstrings, self)
        self.pluginWidget.logSignal.connect(self.addLog)
        self.pluginWidget.show()
        self.pluginWidget.activateWindow()

#------------------------------------------------GENERAL-FUNCTIONS------------------------------------------------------#

    #Get user defined parametes from GUI
    def webData(self):
        if not self.ui.listOfTables.currentItem():
            currTable = ""
        else:
            currTable = self.ui.listOfTables.currentItem().text()
        wD = {
              'url' : self.ui.lineUrl.text(), 
              'method' : str(self.ui.comboBox.currentText()), 
              'mp' : self.preferences_frm.ui.lineMP.text(), 
              'ms' : self.preferences_frm.ui.lineMS.text(), 
              'threads' : self.preferences_frm.ui.threadBox.value(), 
              'timeOut' : int(self.preferences_frm.ui.lineTimeout.text()), 
              'delay' : self.ui.delayBox.value(), 
              'verbose' : self.ui.isVerbose.isChecked(),
              'blind_inj_type' : str(self.ui.blindMethodList.currentText()), 
              'isRandomUpCase' : self.preferences_frm.ui.isRndUpper.isChecked(), 
              'dbListCount' : self.ui.dbListComboBox.count(),
              'dbName' : str(self.ui.dbListComboBox.currentText()), 
              'notInArray' : self.ui.radioNotInArray.isChecked(),
              'notInSubstring' : self.ui.radioNotInSubstring.isChecked(),
              'ordinal_position' : self.ui.radioOrdinalPosition.isChecked(), 
              'selected_table' : currTable, 
              'LIMIT' : self.ui.radioLimit.isChecked(),
              'tblTreeCount' : self.ui.treeOfTables.topLevelItemCount(), 
              'query_cmd' : self.ui.queryText.toPlainText(), 
              'isStacked' : self.ui.isStacked.isChecked(), 
              'data' : self.ui.textData.toPlainText(), 
              'cookie' :  self.ui.lineCookie.text(), 
              'db_type' : str(self.ui.dbTypeBox.currentText()), 
              'inj_type' : str(self.ui.comboInjType.currentText()), 
              'table' : self.ui.lineTable.text(), 
              'key' : self.ui.lineKey.text(), 
              'columns' : self.ui.lineColumns.text().split(";"), 
              'fromPos' : int(self.ui.lineFrom.text()), 
              'toPos' :  int(self.ui.lineTo.text())}
        return wD

    #Connecting to signals and starting thread
    def connectAndStart(self, blind=False):       
        if not blind:
            #dbSignal
            self.qthread.dbSignal.connect(self.addBase, type=QtCore.Qt.QueuedConnection)

            #columnSignal
            self.qthread.columnSignal.connect(self.addColumn, type=QtCore.Qt.QueuedConnection)
        
            #rowDataSignal
            self.qthread.rowDataSignal.connect(self.addRowData, type=QtCore.Qt.QueuedConnection)

            #tblSignal
            self.qthread.tblSignal.connect(self.addTable, type=QtCore.Qt.QueuedConnection)
            
        self.ui.isVerbose.setEnabled(False)
        
        #logSignal
        self.qthread.logSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        
        #progressSignal
        self.qthread.progressSignal.connect(self.updatePb, type=QtCore.Qt.QueuedConnection)
        
        #querySignal
        self.qthread.querySignal.connect(self.queryResult, type=QtCore.Qt.QueuedConnection)
                
        self.ui.isVerbose.setEnabled(False)

        #Starting QThread
        self.qthread.start()
            
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

    #Show busy dialog
    def busyDialog(self):
        clicked = QtGui.QMessageBox.question(self, "Enema", "Program busy. Kill current task?",\
                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if clicked == QtGui.QMessageBox.Yes:
            self.killTask()
        else:
            return
            
#------------------------------------------------[MENU]SAVE/FUNCTIONS------------------------------------------------------#

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
        
    #Click on menu save site settings
    def saveSiteSettings_OnClick(self):
        filePath = QtGui.QFileDialog.getSaveFileName(self, "Save site settings",
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
        settings.setValue('db_structure/data', self.ui.textData.toPlainText())
        settings.setValue('db_structure/cookies', self.ui.lineCookie.text())
        settings.setValue('db_structure/db_type', self.ui.dbTypeBox.currentIndex())
        settings.setValue('db_structure/inj_type', self.ui.comboInjType.currentIndex())
        settings.setValue('db_structure/tables', tables)
        settings.setValue('db_structure/bases', bases)
        settings.setValue('db_structure/current_db', self.ui.dbListComboBox.currentIndex())
        #dump tab settings
        settings.setValue('dump/table', self.ui.lineTable.text())
        settings.setValue('dump/columns', self.ui.lineColumns.text())
        settings.setValue('dump/key', self.ui.lineKey.text())
        settings.setValue('dump/from', self.ui.lineFrom.text())
        settings.setValue('dump/to', self.ui.lineTo.text())
        settings.sync()
        
#------------------------------------------------[MENU]LOAD-SLOTS/FUNCTIONS------------------------------------------------------#

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
        filePath = QtGui.QFileDialog.getOpenFileName(self, "Load site settings", 
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
            else:
                self.ui.dbListComboBox.clear()
                for line in buff:
                    self.ui.dbListComboBox.addItem(line)
            file.close()
        except Exception:
            return

    #Loading site settings
    def loadSiteSettings(self, filepath):
        if len(filepath) < 1:
            return
        settings = QtCore.QSettings(filepath, QtCore.QSettings.IniFormat)
        #Reading tables from config
        tables = settings.value('db_structure/tables', '').split('>>')
        self.ui.listOfTables.clear()
        for tbl in tables:
            if tbl !='':
                self.ui.listOfTables.addItem(tbl)
        #Reading bases from config
        bases = settings.value('db_structure/bases', '').split('>>')
        self.ui.dbListComboBox.clear()
        for db in bases:
            if  db !='':
                self.ui.dbListComboBox.addItem(db)
        #db_strucure tab settings
        self.ui.lineUrl.setText(settings.value('db_structure/url', ''))
        self.ui.comboBox.setCurrentIndex(settings.value('db_structure/method', 0, int))
        self.ui.textData.setText(settings.value('db_structure/data', ''))
        self.ui.lineCookie.setText(settings.value('db_structure/cookies', ''))
        self.ui.dbTypeBox.setCurrentIndex(settings.value('db_structure/db_type', 0, int))
        self.ui.comboInjType.setCurrentIndex(settings.value('db_structure/inj_type', 0, int))
        self.preferences_frm.ui.lineMP.setText(settings.value('db_structure/pattern', ''))
        self.preferences_frm.ui.lineMS.setText(settings.value('db_structure/symbol', '~'))
        self.preferences_frm.ui.threadBox.setValue(settings.value('db_structure/threads', 10, int))
        self.preferences_frm.ui.lineTimeout.setText(settings.value('db_structure/timeout', '30'))
        self.ui.dbListComboBox.setCurrentIndex(settings.value('db_structure/current_db', 0, int))

        #dump tab settings
        self.ui.lineTable.setText(settings.value('dump/table', ''))
        self.ui.lineColumns.setText(settings.value('dump/columns', ''))
        self.ui.lineKey.setText(settings.value('dump/key', ''))
        self.ui.lineFrom.setText(settings.value('dump/from', '0'))
        self.ui.lineTo.setText(settings.value('dump/to', '10'))
        
        self.ui.tabs.setCurrentIndex(0)
        
#------------------------------------------------[MENU]TOOLS-SLOTS------------------------------------------------------#

    def menuEncoder_OnClick(self):
        self.enc_frm.show()
        self.enc_frm.activateWindow()
        
    def queryEditor_OnClick(self):
        self.qeditor_frm.logSignal.connect(self.addLog)
        self.qeditor_frm.show()
        self.qeditor_frm.activateWindow()
        
    def preferences_OnClick(self):
        self.preferences_frm.show()
        self.preferences_frm.activateWindow()
        
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
    
#------------------------------------------------[MENU]ABOUT-SLOTS------------------------------------------------------#
        
    #Show about form
    def menuAbout_OnClick(self):
        self.about_frm.show()
        self.about_frm.activateWindow()
        
    #Open documentation url:
    def actionManual_OnClick(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("http://code.google.com/p/enema/w/list"))
        
#----------------------------------------------BUTTONS-EVENTS----------------------------------------------------#

    #Run Task button    
    def runButton_OnClick(self):
        if self.isBusy():
            self.busyDialog()
            return
        wD = self.webData()
        
        #Tables task
        if self.ui.radioTables.isChecked():
            wD['task'] = 'tables'
            self.ui.listOfTables.clear()
            
        #Columns task
        if self.ui.radioColumns.isChecked():
            wD['task'] = 'columns'
            if self.ui.treeOfTables.topLevelItemCount() < 1:
                QtGui.QMessageBox.information(self, "Enema", "Drag and drop table from left field to right.", 1, 0)
                return
            tables = []
            for table in range(self.ui.treeOfTables.topLevelItemCount()):
                #Cleaning columns in tables
                for i in range(self.ui.treeOfTables.topLevelItem(table).childCount()):
                    self.ui.treeOfTables.topLevelItem(table).takeChildren()
                tables.append(self.ui.treeOfTables.topLevelItem(table).text(0))
            wD['tables'] = tables

        #Bases task
        if self.ui.radioBases.isChecked():
            wD['task'] = "bases"
            if self.ui.dbListComboBox.count() < 1:
                wD['dbName'] = ""
            elif self.ui.dbListComboBox.count() > 1:
                self.ui.dbListComboBox.clear()
                wD['dbName'] = ""
            else:
                wD['dbName'] = ",'" + str(self.ui.dbListComboBox.currentText()) + "'"
        
        #Show progress bar, connect to signals and start task
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        self.qthread = Injector(wD, self.qstrings)
        self.connectAndStart()
    
    #Cleaning right field
    def cleanColumnsButton_OnClick(self):
        self.ui.treeOfTables.clear()
        
    #Cleaning log
    def clearLogButton_OnClick(self):
        self.ui.logTxtEdit.clear()
        
    #Show or Hide log field
    def logButton_OnClick(self):
        if self.ui.logButton.text() == "Show log":
            self.setFixedSize(1121, 624)
            self.resize(1121, 624)
            self.ui.logButton.setText("Hide log")
        else:
            self.setFixedSize(591, 624)
            self.resize(591, 624)
            self.ui.logButton.setText("Show log")
            
    #Run button click (query tab)
    def queryButton_OnClick(self):
        if self.isBusy():
            self.busyDialog()
            return
        wD = self.webData()
        wD['task'] = "query"
        self.ui.queryOutput.clear()
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.show()
        if self.ui.blindMethodList.isHidden():
            self.qthread = Injector(wD, self.qstrings)
            self.connectAndStart()
        else:
            self.qthread = BlindInjector(wD, self.qstrings)
            self.connectAndStart(True)
            
    #Delay button click (query tab)
    def testButton_OnClick(self):
        if self.isBusy():
            self.busyDialog()
            return
        wD = self.webData()
        wD['task'] = "delay_test"
        self.ui.queryOutput.clear()
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.show()
        self.qthread = BlindInjector(wD, self.qstrings)
        self.connectAndStart(True)
        
    #GO button click (dump tab)        
    def dmpButton_OnClick(self):
        if self.isBusy():
            self.busyDialog()
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
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        self.ui.progressBar.setMaximum(self.ui.tableWidget.rowCount() * len(wD['columns']))
        self.qthread = Injector(wD, self.qstrings)
        self.connectAndStart()
        
#----------------------------------------------MAIN-EVENTS----------------------------------------------------#

    #When form closing
    def closeEvent(self, event):
        if self.sysTray.isSystemTrayAvailable():
            self.hide()
            if self.firstHide:
                self.sysTray.showMessage("Enema", "I'll wait here...", QtGui.QSystemTrayIcon.Information)
                self.firstHide = False
            event.ignore()
        else:
            sys.exit(0)

    def sqlOptions(self):
        if self.ui.radioColumns.isChecked():
            self.ui.radioOrdinalPosition.setEnabled(True)
        else:
            self.ui.radioOrdinalPosition.setEnabled(False)
        if str(self.ui.dbTypeBox.currentText())  == "MySQL":
            self.ui.radioLimit.setEnabled(True)
            self.ui.radioLimit.setChecked(True)
            self.ui.radioNotInSubstring.setEnabled(False)
            self.ui.radioNotInArray.setEnabled(False)
        else:
            self.ui.radioNotInSubstring.setEnabled(True)
            self.ui.radioNotInSubstring.setChecked(True)
            self.ui.radioNotInArray.setEnabled(True)
            self.ui.radioLimit.setEnabled(False)
            
    #Tables radio checked
    def radioTables_Toggled(self):
        if self.ui.radioTables.isChecked():
            self.sqlOptions()
            
    #Columns radio checked
    def radioColumns_Toggled(self):
        if self.ui.radioColumns.isChecked():
            self.sqlOptions()
     
    #Bases radio checked     
    def radioBases_Toggled(self):
        if self.ui.radioBases.isChecked():
            self.sqlOptions()
        
    #Tray icon clicked
    def trayActivated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            if self.isHidden():
                self.show()
            else:
                self.hide()
        
    #Tray menu "Quit" clicked
    def trayQuit_Clicked(self):
        #Saving main and log window position
        settings = QtCore.QSettings("settings/enema.ini", QtCore.QSettings.IniFormat)
        settings.setValue("Main/query", self.ui.queryText.toPlainText())
        settings.setValue('Main/window_position', self.pos())
        settings.sync()
        sys.exit(0)
    
    #Hide or show blind options
    def blindOptions(self, mode):
        if mode == "show":
            self.ui.blindMethodList.setVisible(True)
            self.ui.methodLabel.setVisible(True)
            self.ui.delayBox.setVisible(True)
            self.ui.isMultirows.setVisible(True)
            self.ui.testButton.setVisible(True)
            self.ui.delayLabel.setVisible(True)
            self.ui.isStacked.setVisible(False)
        else:
            self.ui.blindMethodList.setVisible(False)
            self.ui.methodLabel.setVisible(False)
            self.ui.delayBox.setVisible(False)
            self.ui.isMultirows.setVisible(False)
            self.ui.testButton.setVisible(False)
            self.ui.delayLabel.setVisible(False)
            self.ui.isStacked.setVisible(True)
            
    def tabIndexChanged(self):
        blind = False
        kw = "[blind]"
        if kw in self.ui.lineUrl.text():
            blind = True
        if kw in self.ui.lineCookie.text():
            blind = True
        if kw in self.ui.textData.toPlainText():
            blind = True
        if blind:
            self.blindOptions("show")
        else:
            self.blindOptions("hide")
            
    #URL, Post data, Cookies editing finished
    def urlEditFinished(self):
        self.ui.dbListComboBox.clear()
            
    #Request method changed
    def methodChanged(self):
        if str(self.ui.comboBox.currentText()) == "POST":
            self.ui.textData.setEnabled(True)
        else:
            self.ui.textData.setEnabled(False)
            
    #Db type changed
    def dbTypeChanged(self):
        if str(self.ui.dbTypeBox.currentText())  == "MySQL":
            self.ui.menuMssql.setEnabled(False)
        else:
            self.ui.menuMssql.setEnabled(True)
        self.sqlOptions()

#------------------------------------------------INJECTOR-SLOTS------------------------------------------------------#

    #Add text to log
    def addLog(self, logStr):
        #Autoclean log when blocks more than 3000
        if self.ui.logTxtEdit.document().blockCount() > 10000:
            self.ui.logTxtEdit.clear()
        self.ui.logTxtEdit.append("\n" + logStr)
        #Autoscrolling
        sb = self.ui.logTxtEdit.verticalScrollBar()
        sb.setValue(sb.maximum())
        
    #Updating main progressBar
    def updatePb(self, pbMax, taskDone):
        if taskDone:
            self.ui.progressBar.hide()
            self.ui.isVerbose.setEnabled(True)
            if self.isHidden():
                self.sysTray.showMessage("Enema", "Task finished.", QtGui.QSystemTrayIcon.Information)
            return
        if pbMax >= 0:
            self.ui.progressBar.setMaximum(pbMax)
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)
        
    #Add row data (dump tab)
    def addRowData(self,  tNum, num,  rowData):
        rData = QtGui.QTableWidgetItem()
        rData.setText(rowData)
        self.ui.tableWidget.setItem((tNum - int(self.ui.lineFrom.text()) - 1), num, rData)
        
    #Add db to listBox
    def addBase(self, db_name):
        self.ui.dbListComboBox.addItem(db_name)
            
    #Add table to ListWidget
    def addTable(self, table_name):
        self.ui.listOfTables.addItem(table_name)
    
    #Adding columns to TreeWidget
    def addColumn(self, column_name, i):
        column = QtGui.QTreeWidgetItem()
        column.setText(0, column_name)
        self.ui.treeOfTables.topLevelItem(i).addChild(column)

    #Set query result (query tab)
    def queryResult(self, result, blind):
        if not blind:
            self.ui.queryOutput.setText(result)
        else:
            self.ui.queryOutput.clear()
            self.ui.queryOutput.setText(result)
    
    def delayResult(self, delay):
        self.ui.delayBox.setValue(delay)
#------------------------------------------------END------------------------------------------------------#

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mform = EnemaForm()
    mform.show()
    sys.exit(app.exec_())
