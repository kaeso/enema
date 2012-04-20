"""
    Enema main: GUI events
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

from core.e_const import *
from core.injector import Injector
from core.injector import BlindInjector
from core.plugins import PluginHandler

from PyQt4 import QtCore, QtGui 
from importlib import import_module

from ui.Ui_main import Ui_MainForm
from ui.Ui_preferences import Ui_preferencesWidget
from ui.Ui_headers import Ui_HeadersWidget
from ui.Ui_encoder import Ui_EncoderForm
from ui.Ui_about import Ui_AboutForm
from ui.Ui_query_editor import Ui_QueryEditorForm


#Query editor form GUI class
class QueryEditorForm(QtGui.QWidget):
    
    qstringsChanged = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.Tool)
        self.ui = Ui_QueryEditorForm()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.edited = False
        self.loadQstrings()
        
        #SIGNALS-----------------------------------------------------------------------
        self.ui.replaceButton.clicked.connect(self.replaceButton_OnClick)
        self.ui.defaultsButton.clicked.connect(self.defaultsButton_OnClick)
        self.ui.treeQueryStrings.itemClicked.connect(self.loadQueryToLine)
        self.ui.lineQueryString.textEdited.connect(self.qstringsEdited)
        self.ui.lineQueryString.editingFinished.connect(self.lineEditingFinished)
        
        #Setting icons for Databases
        self.ui.treeQueryStrings.topLevelItem(0).setIcon(0, QtGui.QIcon("ui/resources/icons/query_editor/mssql.png"))
        self.ui.treeQueryStrings.topLevelItem(1).setIcon(0, QtGui.QIcon("ui/resources/icons/query_editor/mysql.png"))
        self.ui.treeQueryStrings.topLevelItem(2).setIcon(0, QtGui.QIcon("ui/resources/icons/query_editor/oracle.png"))
        self.ui.treeQueryStrings.topLevelItem(3).setIcon(0, QtGui.QIcon("ui/resources/icons/query_editor/postgresql.png"))
        
    def qstringsEdited(self):
        self.edited = True
    
    def lineEditingFinished(self):
        if self.edited:
            try:
                self.custom_settings.setValue(self.ui.treeQueryStrings.currentItem().parent().text(0)\
                                          + "/" + self.ui.treeQueryStrings.currentItem().text(0), self.ui.lineQueryString.text())
            except AttributeError:
                self.edited = False
                return
            self.replaceAndSave(True)
            self.edited = False
            
    def loadQueryToLine(self):          
        try:
            editableString = self.ui.treeQueryStrings.currentItem().parent().text(0) + "/" + self.ui.treeQueryStrings.currentItem().text(0)
            self.ui.lineQueryString.setText(self.settings.value(editableString))
        except AttributeError:
            pass
     
    #Creating settings clone
    def cloneSettings(self, settings, newPath):
        cloned_settings = QtCore.QSettings(newPath, QtCore.QSettings.IniFormat)
        for key in settings.allKeys():
            cloned_settings.setValue(key, settings.value(key))
        return cloned_settings
        
    def replaceAndSave(self, save_only=False):
        if save_only:
            self.custom_settings.sync()
            self.loadQstrings()
            self.qstringsChanged.emit()
            return
            
        findStr = self.ui.lineFindStr.text()
        replaceStr = self.ui.lineResplaceStr.text()
        stringsFound = 0
        for query in self.custom_settings.allKeys():
            stringsFound += self.custom_settings.value(query).find(findStr)
            self.custom_settings.setValue(query, self.custom_settings.value(query).replace(findStr, replaceStr))
        if stringsFound <= 0:
            QtGui.QMessageBox.information(self, "Enema - Query Editor", "Nothing to replace.", 1, 0)
            return
        else:
            QtGui.QMessageBox.information(self, "Enema - Query Editor", "Replaced: " + str(stringsFound), 1, 0)
            
        self.custom_settings.sync()
       
    def loadQstrings(self):
        if os.path.exists(QSTRINGS_CUSTOM_PATH):
            path = QSTRINGS_CUSTOM_PATH
        else:
            path = QSTRINGS_DEFAULT_PATH
        
        self.settings = QtCore.QSettings(path, QtCore.QSettings.IniFormat)
        self.custom_settings = self.cloneSettings(self.settings, QSTRINGS_CUSTOM_PATH)
        
        if not self.edited:
            #Cleaning tree
            for db in range(self.ui.treeQueryStrings.topLevelItemCount()):
                for i in range(self.ui.treeQueryStrings.topLevelItem(db).childCount()):
                    self.ui.treeQueryStrings.topLevelItem(db).takeChildren()
                    
            for group in self.settings.childGroups():
                grp =  QtGui.QTreeWidgetItem()
                grp.setText(0, group)  
            
                #Setting icons for injection types
                if "_blind_boolean_" in group:
                    grp.setIcon(0, QtGui.QIcon("ui/resources/icons/query_editor/blind_boolean.png"))
                elif "_blind_time_" in group:
                    grp.setIcon(0, QtGui.QIcon("ui/resources/icons/query_editor/blind_time.png"))
                elif "_error_" in group:
                    grp.setIcon(0, QtGui.QIcon("ui/resources/icons/query_editor/error.png"))
                else:
                    grp.setIcon(0, QtGui.QIcon("ui/resources/icons/query_editor/other.png"))
                
                #Adding injection types for each db
                if "mssql_" in group:
                    self.ui.treeQueryStrings.topLevelItem(0).addChild(grp)
                if "mysql_" in group:
                    self.ui.treeQueryStrings.topLevelItem(1).addChild(grp)
                if "oracle_" in group:
                    self.ui.treeQueryStrings.topLevelItem(2).addChild(grp)
                if "postgresql_" in group:
                    self.ui.treeQueryStrings.topLevelItem(3).addChild(grp)
            
                self.settings.beginGroup(group)
                for key in self.settings.childKeys():
                    grp_child =  QtGui.QTreeWidgetItem(grp)
                    grp_child.setText(0, key)
                    grp_child.setIcon(0, QtGui.QIcon("ui/resources/icons/query_editor/query_str.png"))
                self.settings.endGroup()
        
    #Finding and Replacing in query strings
    def replaceButton_OnClick(self):          
        self.replaceAndSave()
        self.loadQstrings()
        self.qstringsChanged.emit()
    
    #Reset query strings to default
    def defaultsButton_OnClick(self):
        if os.path.exists(QSTRINGS_CUSTOM_PATH):
            try:
                os.remove(QSTRINGS_CUSTOM_PATH)
            except Exception:
                pass
        else:
            return
        self.loadQstrings()
        self.qstringsChanged.emit()
        

#Enccoder form GUI class
class EncoderForm(QtGui.QWidget):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.Tool)
        self.ui = Ui_EncoderForm()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui.decodeButton.hide()
        
        self.preferences_frm = PreferencesForm()
        
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
            readyStr = core.txtproc.base64proc(string, "enc", self.preferences_frm.ui.lineEncoding.text())
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
        readyStr = core.txtproc.base64proc(string, "dec", self.preferences_frm.ui.lineEncoding.text())
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
class PreferencesForm(QtGui.QWidget):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.Tool)
        self.ui = Ui_preferencesWidget()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
    
    def closeEvent(self, event):
        settings = QtCore.QSettings(CONFIG_PATH, QtCore.QSettings.IniFormat)
        settings.setValue('Main/match_symbol', self.ui.lineMS.text())
        settings.setValue('Main/match_pattern', self.ui.lineMP.text())
        settings.setValue('Main/threads', self.ui.threadBox.value())
        settings.setValue('Main/timeout', self.ui.lineTimeout.text())
        settings.setValue('Main/encoding', self.ui.lineEncoding.text())
        settings.setValue('Main/rnd_upcase', self.ui.isRndUpper.isChecked())
        settings.setValue('Main/accept_cookies', self.ui.acceptCookies.isChecked())
        settings.sync()

#HTTP Headers widget
class HeadersForm(QtGui.QWidget):
    
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.Tool)
        self.ui = Ui_HeadersWidget()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        
        self.ui.Cookie.stateChanged.connect(self.headersStateChanged)
        self.ui.Referer.stateChanged.connect(self.headersStateChanged)
        self.ui.XForwardedFor.stateChanged.connect(self.headersStateChanged)
        self.ui.Custom.stateChanged.connect(self.headersStateChanged)
        
    def headersStateChanged(self):
        #Cookie header
        if self.ui.Cookie.isChecked():
            self.ui.CookieLabel.setEnabled(True)
            self.ui.lineCookie.setEnabled(True)
        else:
            self.ui.CookieLabel.setEnabled(False)
            self.ui.lineCookie.setEnabled(False)
            
        #Referer header
        if self.ui.Referer.isChecked():
            self.ui.RefererLabel.setEnabled(True)
            self.ui.lineReferer.setEnabled(True)
        else:
            self.ui.RefererLabel.setEnabled(False)
            self.ui.lineReferer.setEnabled(False)
            
        #X-Forwarded-For header
        if self.ui.XForwardedFor.isChecked():
            self.ui.XForwardedLabel.setEnabled(True)
            self.ui.lineXForwardedFor.setEnabled(True)
        else:
            self.ui.XForwardedLabel.setEnabled(False)
            self.ui.lineXForwardedFor.setEnabled(False)
            
        #Custom header
        if self.ui.Custom.isChecked():
            self.ui.lineCustomHeaderName.setEnabled(True)
            self.ui.lineCustomHeader.setEnabled(True)
            self.ui.urlencode.setEnabled(True)
        else:
            self.ui.lineCustomHeaderName.setEnabled(False)
            self.ui.lineCustomHeader.setEnabled(False)
            self.ui.urlencode.setEnabled(False)
            
            
#Main form GUI class
class EnemaForm(QtGui.QMainWindow):
    
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        
        #-----------------ICONS-----------------  
        #Tray and window icon
        trayIcon = QtGui.QIcon("ui/resources/icons/tray.png")
        self.setWindowIcon(trayIcon)
        #Tab icons
        self.ui.tabs.setTabIcon(0, QtGui.QIcon("ui/resources/icons/db_structure.png"))
        self.ui.tabs.setTabIcon(1, QtGui.QIcon("ui/resources/icons/query.png"))
        self.ui.tabs.setTabIcon(2, QtGui.QIcon("ui/resources/icons/dump.png"))

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
        self.ui.methodLabel.setVisible(False)
        self.ui.blindMethodList.setVisible(False)
        self.ui.timeGroup.setVisible(False)
        self.ui.booleanGroup.setVisible(False)
        self.ui.resultGroup.setGeometry(QtCore.QRect(10, 220, 571, 171))
        
        #Three horizontal scroll fix
        self.ui.treeOfTables.header().setStretchLastSection(False)
        self.ui.treeOfTables.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.treeOfTables.setColumnWidth(0, 500)
        
        #Subforms
        self.qeditor_frm = QueryEditorForm(self)
        self.enc_frm = EncoderForm(self)
        self.about_frm = AboutForm(self)
        self.preferences_frm = PreferencesForm(self)
        self.headers_frm = HeadersForm(self)
        
        #Show only one minimising message per program launch
        self.firstHide = True
        
        #Set current program version and logo
        self.about_frm.ui.versionLabel.setText("Version: " + VERSION)
        self.about_frm.ui.logoLabel.setPixmap(QtGui.QPixmap("ui/resources/logo.png"))
        
        self.headers_frm.ui.lineUserAgent.setText(DEFAULT_USER_AGENT)
        
        #Loading settings if ini file exists
        if os.path.exists(CONFIG_PATH):
            settings = QtCore.QSettings(CONFIG_PATH, QtCore.QSettings.IniFormat)
            self.preferences_frm.ui.lineMS.setText(settings.value('Main/match_symbol', '~'))
            self.preferences_frm.ui.lineMP.setText(settings.value('Main/match_pattern', ''))
            self.preferences_frm.ui.threadBox.setValue(settings.value('Main/threads', 5, int))
            self.preferences_frm.ui.lineTimeout.setText(settings.value('Main/timeout', '60'))
            self.preferences_frm.ui.lineEncoding.setText(settings.value('Main/encoding', 'windows-1251'))
            self.preferences_frm.ui.isRndUpper.setChecked(settings.value('Main/rnd_upcase', False, bool))
            self.preferences_frm.ui.acceptCookies.setChecked(settings.value('Main/accept_cookies', False, bool))
            
            #restoring widgets position
            widgetPosition = settings.value("Main/window_position")
            
            if widgetPosition is not None: 
                self.move(widgetPosition)
                self.enc_frm.move(widgetPosition)
                self.qeditor_frm.move(widgetPosition)
                self.about_frm.move(widgetPosition)
                self.preferences_frm.move(widgetPosition)
                self.headers_frm.move(widgetPosition)
                
        #Query strings loading
        self.loadQstrings()
        #Plugins loading
        if os.path.exists("plugins"):
            self.ui.menuPlugins.clear()
            self.loadPlugins()
        else:
            dw_plugins = QtGui.QAction("Download", self)
            self.ui.menuPlugins.addAction(dw_plugins)
            dw_plugins.triggered.connect(self.downloadPlugins_Clicked)
            
#------------------------------------------------SIGNAL-CONNECTIONS------------------------------------------------------#

        #Query changed in editor
        self.qeditor_frm.qstringsChanged.connect(self.loadQstrings)
        
        #DB_STRUCTURE-TAB
        self.ui.runButton.clicked.connect(self.runButton_OnClick)
        self.ui.cleanColumnsButton.clicked.connect(self.cleanColumnsButton_OnClick)
        self.ui.radioTables.toggled.connect(self.radioTables_Toggled)
        self.ui.radioColumns.toggled.connect(self.radioColumns_Toggled)
        self.ui.radioBases.toggled.connect(self.radioBases_Toggled)
        self.ui.clearLogButton.clicked.connect(self.clearLogButton_OnClick)
        self.ui.killButton.clicked.connect(self.killTask)
        self.ui.headersButton.clicked.connect(self.headersButton_OnClick)
        
        #DUMP-TAB
        self.ui.dmpButton.clicked.connect(self.dmpButton_OnClick)
        
        #QUERY-TAB
        self.ui.queryButton.clicked.connect(self.queryButton_OnClick)
        self.ui.testButton.clicked.connect(self.testButton_OnClick)
        self.ui.isStacked.stateChanged.connect(self.stacked_Changed)
        self.ui.isHexed.stateChanged.connect(self.hex_Changed)
        self.ui.isAuto.stateChanged.connect(self.autodetect_Changed)
        self.ui.blindMethodList.currentIndexChanged.connect(self.blindMethodChanged)
        
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
        
#------------------------------------------------PLUGINS------------------------------------------------------#

    #download plugins from repository
    def downloadPlugins_Clicked(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("http://code.google.com/p/enema-plugins/downloads/list"))
        
    #Load plugins
    def loadPlugins(self):
        self.ui.menuPlugins.clear()
        
        P_Handler = PluginHandler()
        P_Handler.logSignal.connect(self.addLog)
        
        import_strings = P_Handler.findPlugins("plugins")
        all_info = P_Handler.getPluginsInfo(import_strings)
        
        self.plugin_groups = []
        self.modules = {}
        for path, cls_name in all_info['import_info'].items():
            module = import_module(path)
            self.modules[cls_name] = getattr(module, cls_name)
        for p_info in all_info['plugins_info']:
            self.addPluginAction(p_info['PLUGIN_GROUP'], p_info['PLUGIN_NAME'], p_info['PLUGIN_CLASS_NAME'])
            
    #Adding plugin action to menu
    def addPluginAction(self, plugin_group, plugin_name, plugin_class):
        p_action = QtGui.QAction(plugin_name.lower(), self)
        p_action.setObjectName("pluginAction_" + plugin_name)
        
        if len(self.plugin_groups) < 1:
            self.p_group = QtGui.QMenu(plugin_group.lower(), self)
            self.ui.menuPlugins.addMenu(self.p_group)
            self.p_group.addAction(p_action)
            self.plugin_groups.append(self.p_group)
            self.pluginSlotConnect(p_action, plugin_class)
            return
        else:
            for grp in self.plugin_groups:
                if grp.title() == plugin_group:
                    self.p_group = grp
            if self.p_group.title() == plugin_group:
                self.p_group.addAction(p_action)
            else:
                self.p_group = QtGui.QMenu(plugin_group, self)
                self.ui.menuPlugins.addMenu(self.p_group)
                self.p_group.addAction(p_action)
                self.plugin_groups.append(self.p_group)
            self.pluginSlotConnect(p_action, plugin_class)
    
    #Connecting to action.triggered signal
    def pluginSlotConnect(self, p_action,  plugin_class):
        signalMapper = QtCore.QSignalMapper(self)
        signalMapper.setMapping(p_action, plugin_class)
        p_action.triggered.connect(signalMapper.map)
        signalMapper.mapped[str].connect(self.pluginAction_Triggered)
    
    #Slot for action.triggered signal
    def pluginAction_Triggered(self, cls):
        self.pluginWidget = self.modules[cls](self.webData(), self.qstrings, self)
        self.pluginWidget.logSignal.connect(self.addLog)
        self.pluginWidget.show()
        self.pluginWidget.activateWindow()
    
#------------------------------------------------GENERAL-FUNCTIONS------------------------------------------------------#

    #Get user defined parametes from GUI
    def webData(self):           
        if self.headers_frm.ui.Cookie.isChecked():
            cookie = self.headers_frm.ui.lineCookie.text()
        else:
            cookie = ""
            
        if self.headers_frm.ui.Referer.isChecked():
            referer = self.headers_frm.ui.lineReferer.text()
        else:
            referer = ""
            
        if self.headers_frm.ui.XForwardedFor.isChecked():
            x_forwarded_for = self.headers_frm.ui.lineXForwardedFor.text()
        else:
            x_forwarded_for = ""

        if self.headers_frm.ui.Custom.isChecked():
            custom_header = self.headers_frm.ui.lineCustomHeader.text()
            header_urlencode =  self.headers_frm.ui.urlencode.isChecked()
        else:
            custom_header = ""
            header_urlencode = False
            
        wD = {
              'url' : self.ui.lineUrl.text(), 
              'method' : str(self.ui.comboBox.currentText()), 
              'mp' : self.preferences_frm.ui.lineMP.text(), 
              'ms' : self.preferences_frm.ui.lineMS.text(), 
              'threads' : self.preferences_frm.ui.threadBox.value(), 
              'timeOut' : int(self.preferences_frm.ui.lineTimeout.text()), 
              'time' : self.ui.delayBox.value(), 
              'blind_inj_type' : str(self.ui.blindMethodList.currentText()),
              'bool_pattern' : self.ui.lineTruePattern.text(), 
              'max_lag' : self.ui.lagBox.value(), 
              'hexed' : self.ui.isHexed.isChecked(), 
              'auto_detect' : self.ui.isAuto.isChecked(), 
              'true_time' : self.ui.trueTimeBox.value(), 
              'encoding' : self.preferences_frm.ui.lineEncoding.text(), 
              'isRandomUpCase' : self.preferences_frm.ui.isRndUpper.isChecked(), 
              'accept_cookies' : self.preferences_frm.ui.acceptCookies.isChecked(),
              'dbListCount' : self.ui.dbListComboBox.count(),
              'dbName' : str(self.ui.dbListComboBox.currentText()), 
              'notInArray' : self.ui.radioNotInArray.isChecked(),
              'notInSubstring' : self.ui.radioNotInSubstring.isChecked(),
              'ordinal_position' : self.ui.radioOrdinalPosition.isChecked(), 
              'LIMIT' : self.ui.radioLimit.isChecked(),
              'tblTreeCount' : self.ui.treeOfTables.topLevelItemCount(), 
              'query_cmd' : self.ui.queryText.toPlainText(), 
              'isStacked' : self.ui.isStacked.isChecked(), 
              'data' : self.ui.textData.toPlainText(), 
              #HTTP Headers
              'user_agent' :  self.headers_frm.ui.lineUserAgent.text(),
              'cookie' :  cookie,
              'referer' :  referer,
              'x_forwarded_for' : x_forwarded_for,
              'custom_header_name' : self.headers_frm.ui.lineCustomHeaderName.text(), 
              'custom_header' : custom_header, 
              'header_urlencode' : header_urlencode,
              #---------
              'db_type' : str(self.ui.dbTypeBox.currentText()), 
              'inj_type' : str(self.ui.comboInjType.currentText()), 
              'table' : self.ui.lineTable.text(), 
              'key' : self.ui.lineKey.text(), 
              'columns' : self.ui.lineColumns.text().split(";"), 
              'fromPos' : int(self.ui.lineFrom.text()), 
              'toPos' :  int(self.ui.lineTo.text())}
              
        return wD
    
    #checking for keywords
    def keywordsCheck(self, kw):
        kwFound = False
        if kw in self.ui.lineUrl.text():
            kwFound = True
        if kw in self.ui.textData.toPlainText():
            kwFound = True
        if kw in self.headers_frm.ui.lineUserAgent.text():
            kwFound = True
        if kw in self.headers_frm.ui.lineCookie.text():
            kwFound = True
        if kw in self.headers_frm.ui.lineReferer.text():
            kwFound = True
        if kw in self.headers_frm.ui.lineXForwardedFor.text():
            kwFound = True
        if kw in self.headers_frm.ui.lineCustomHeader.text():
            kwFound = True
        return kwFound
            
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
        else:
            #Setting 'True' time
            self.qthread.trueTimeSignal.connect(self.setTrueTime, type=QtCore.Qt.QueuedConnection)
            
        #logSignal
        self.qthread.logSignal.connect(self.addLog, type=QtCore.Qt.QueuedConnection)
        #progressSignal
        self.qthread.progressSignal.connect(self.updatePb, type=QtCore.Qt.QueuedConnection)
        #querySignal
        self.qthread.querySignal.connect(self.queryResult, type=QtCore.Qt.QueuedConnection)
        
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
        clicked = QtGui.QMessageBox.question(self, "Enema", "Program is busy. Kill current task?",\
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
        
        #headers
        settings.setValue('db_structure/user_agent', self.headers_frm.ui.lineUserAgent.text())
        if self.headers_frm.ui.Cookie.isChecked():
            settings.setValue('db_structure/cookies', self.headers_frm.ui.lineCookie.text())
        if self.headers_frm.ui.Referer.isChecked():
            settings.setValue('db_structure/referer', self.headers_frm.ui.lineReferer.text())
        if self.headers_frm.ui.XForwardedFor.isChecked():
            settings.setValue('db_structure/x_forwarded_for', self.headers_frm.ui.lineXForwardedFor.text())
        if self.headers_frm.ui.Custom.isChecked():
            settings.setValue('db_structure/custom_header_name', self.headers_frm.ui.lineCustomHeaderName.text())
            settings.setValue('db_structure/custom_header', self.headers_frm.ui.lineCustomHeader.text())
            settings.setValue('db_structure/custom_header_urlenc', self.headers_frm.ui.urlencode.isChecked())
            
        settings.setValue('db_structure/db_type', self.ui.dbTypeBox.currentIndex())
        settings.setValue('db_structure/inj_type', self.ui.comboInjType.currentIndex())
        settings.setValue('db_structure/tables', tables)
        settings.setValue('db_structure/bases', bases)
        settings.setValue('db_structure/current_db', self.ui.dbListComboBox.currentIndex())
        
        #query tab settings
        settings.setValue('query/query_str', self.ui.queryText.toPlainText())
        settings.setValue('query/stacked_enabled', self.ui.isStacked.isChecked())
        settings.setValue('query/hex_enabled', self.ui.isHexed.isChecked())
        settings.setValue('query/blind_method', self.ui.blindMethodList.currentIndex())
        settings.setValue('query/delay', self.ui.delayBox.value())
        settings.setValue('query/true_time', self.ui.trueTimeBox.value())
        settings.setValue('query/auto_enabled', self.ui.isAuto.isChecked())
        settings.setValue('query/max_lag', self.ui.lagBox.value())
        
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
        
        #headers
        self.headers_frm.ui.lineUserAgent.setText(settings.value('db_structure/user_agent', DEFAULT_USER_AGENT))
        self.headers_frm.ui.lineCookie.setText(settings.value('db_structure/cookies', ''))
        self.headers_frm.ui.lineReferer.setText(settings.value('db_structure/referer', ''))
        self.headers_frm.ui.lineXForwardedFor.setText(settings.value('db_structure/x_forwarded_for', ''))
        self.headers_frm.ui.lineCustomHeaderName.setText(settings.value('db_structure/custom_header_name', ''))
        self.headers_frm.ui.lineCustomHeader.setText(settings.value('db_structure/custom_header', ''))
        #Enabling headers if defined
        if settings.value('db_structure/cookies') is not None:
            self.headers_frm.ui.Cookie.setChecked(True)
            self.headers_frm.ui.CookieLabel.setEnabled(True)
            self.headers_frm.ui.lineCookie.setEnabled(True)
        if settings.value('db_structure/referer') is not None:
            self.headers_frm.ui.Referer.setChecked(True)
            self.headers_frm.ui.RefererLabel.setEnabled(True)
            self.headers_frm.ui.lineReferer.setEnabled(True)
        if settings.value('db_structure/x_forwarded_for') is not None:
            self.headers_frm.ui.XForwardedFor.setChecked(True)
            self.headers_frm.ui.XForwardedLabel.setEnabled(True)
            self.headers_frm.ui.lineXForwardedFor.setEnabled(True)
        if settings.value('db_structure/custom_header_name') is not None:
            self.headers_frm.ui.Custom.setChecked(True)
            self.headers_frm.ui.lineCustomHeaderName.setEnabled(True)
            self.headers_frm.ui.lineCustomHeader.setEnabled(True)
            self.headers_frm.ui.urlencode.setEnabled(True)
            self.headers_frm.ui.urlencode.setChecked(settings.value('db_structure/custom_header_urlenc', False, bool))

        self.ui.dbTypeBox.setCurrentIndex(settings.value('db_structure/db_type', 0, int))
        self.ui.comboInjType.setCurrentIndex(settings.value('db_structure/inj_type', 0, int))
        self.preferences_frm.ui.lineMP.setText(settings.value('db_structure/pattern', ''))
        self.preferences_frm.ui.lineMS.setText(settings.value('db_structure/symbol', '~'))
        self.preferences_frm.ui.threadBox.setValue(settings.value('db_structure/threads', 10, int))
        self.preferences_frm.ui.lineTimeout.setText(settings.value('db_structure/timeout', '30'))
        self.ui.dbListComboBox.setCurrentIndex(settings.value('db_structure/current_db', 0, int))
        
        #query tab settings
        self.ui.queryText.setText(settings.value('query/query_str', ''))
        self.ui.isStacked.setChecked(settings.value('query/stacked_enabled', False, bool))
        self.ui.isHexed.setChecked(settings.value('query/hex_enabled', False, bool))
        self.ui.blindMethodList.setCurrentIndex(settings.value('query/blind_method', 0, int))
        self.ui.delayBox.setValue(settings.value('query/delay', 2, int))
        self.ui.trueTimeBox.setValue(settings.value('query/true_time', 0.00, float))
        self.ui.isAuto.setChecked(settings.value('query/auto_enabled', True, bool))
        self.ui.lagBox.setValue(settings.value('query/max_lag', 5.00, float))
        
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
        self.qeditor_frm.show()
        self.qeditor_frm.activateWindow()
        
    def preferences_OnClick(self):
        self.preferences_frm.show()
        self.preferences_frm.activateWindow()
        
    #Loading default or custom query strings
    def loadQstrings(self):
        if os.path.exists(QSTRINGS_CUSTOM_PATH):
            qs_path = QSTRINGS_CUSTOM_PATH
        else:
            qs_path = QSTRINGS_DEFAULT_PATH
        qstrings = QtCore.QSettings(qs_path, QtCore.QSettings.IniFormat)
        self.qstrings = qstrings
    
#------------------------------------------------[MENU]ABOUT-SLOTS------------------------------------------------------#
        
    #Show about form
    def menuAbout_OnClick(self):
        self.about_frm.show()
        self.about_frm.activateWindow()
        
    #Open documentation url:
    def actionManual_OnClick(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("http://code.google.com/p/enema/w/list"))
        
#----------------------------------------------BUTTONS-EVENTS----------------------------------------------------#

    def headersButton_OnClick(self):
        self.headers_frm.show()
        self.headers_frm.activateWindow()
        
    #Run Task button    
    def runButton_OnClick(self):
        if self.isBusy():
            self.busyDialog()
            return
        if not self.keywordsCheck("[sub]"):
            self.addLog("[!] No keywords found.\n\n[sub] keyword required for this task. (sub means Subquery)")
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
                wD['dbName'] = ""
                self.ui.dbListComboBox.clear()
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
  
    #Run button click (query tab)
    def queryButton_OnClick(self):
        if self.isBusy():
            self.busyDialog()
            return
        wD = self.webData()
        wD['task'] = "query"
        blind_flag = False
        if self.ui.blindMethodList.isHidden():
            if self.ui.isStacked.isChecked():
                if not self.keywordsCheck("[cmd]"):
                    self.addLog("[!] No keywords found.\n\n[cmd] keyword required for this task. (cmd means Stacked query)")
                    return
            else:
                if not self.keywordsCheck("[sub]"):
                    self.addLog("[!] No keywords found.\n\n[sub] keyword required for this task. (sub means Subquery)")
                    return
            self.qthread = Injector(wD, self.qstrings)
        else:
            self.qthread = BlindInjector(wD, self.qstrings)
            blind_flag = True
        self.ui.queryOutput.clear()
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.show()
        self.connectAndStart(blind_flag)
            
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
        if not self.keywordsCheck("[sub]"):
            self.addLog("[!] No keywords found.\n\n[sub] keyword required for this task. (sub means Subquery)")
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

    #close() event handler
    def closeEvent(self, event):
        if self.sysTray.isSystemTrayAvailable():
            self.hide()
            if self.firstHide:
                self.sysTray.showMessage("Enema", "I'll wait here...", QtGui.QSystemTrayIcon.Information)
                self.firstHide = False
            event.ignore()

    def sqlOptions(self):
        if self.ui.radioColumns.isChecked():
            self.ui.treeOfTables.setEnabled(True)
            self.ui.radioOrdinalPosition.setEnabled(True)
        else:
            self.ui.radioOrdinalPosition.setEnabled(False)
            self.ui.treeOfTables.setEnabled(False)
            
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
                self.activateWindow()
            else:
                self.hide()
        
    #Tray menu "Quit" clicked
    def trayQuit_Clicked(self):
        #Saving main and log window position
        settings = QtCore.QSettings(CONFIG_PATH, QtCore.QSettings.IniFormat)
        settings.setValue('Main/window_position', self.pos())
        settings.sync()
        sys.exit(0)

    #Hex checked
    def hex_Changed(self):
        if self.ui.isHexed.isChecked():
            self.ui.isStacked.setChecked(True)

    #Stacked checked
    def stacked_Changed(self):
        if not self.ui.isStacked.isChecked():
            self.ui.isHexed.setChecked(False)
            
    #Autodetect checked or unchecked
    def autodetect_Changed(self):
        if not self.ui.isAuto.isChecked():
            self.ui.trueTimeBox.setEnabled(True)
        else:
            self.ui.trueTimeBox.setEnabled(False)
    
    #Blind method changed
    def blindMethodChanged(self):
        if str(self.ui.blindMethodList.currentText()) == "Boolean":
            self.ui.timeGroup.setVisible(False)
            self.ui.booleanGroup.setGeometry(QtCore.QRect(10, 220, 571, 51))
            self.ui.booleanGroup.setVisible(True)
        else:
            self.ui.booleanGroup.setVisible(False)
            self.ui.timeGroup.setVisible(True)
            
    #Hide or show blind options
    def blindOptions(self, mode):
        if mode == "show":
            self.ui.methodLabel.setVisible(True)
            self.ui.blindMethodList.setVisible(True)
            self.ui.resultGroup.setGeometry(QtCore.QRect(10, 280, 571, 171))
            if self.ui.booleanGroup.isHidden():
                self.ui.timeGroup.setVisible(True)
        else:
            self.ui.methodLabel.setVisible(False)
            self.ui.blindMethodList.setVisible(False)
            self.ui.resultGroup.setGeometry(QtCore.QRect(10, 220, 571, 171))
            self.ui.timeGroup.setVisible(False)
            self.ui.booleanGroup.setVisible(False)
            
    def tabIndexChanged(self):
        blind = False
        kw = "[blind]"
        if kw in self.ui.lineUrl.text():
            blind = True
            
        #Checking for blind keayword in headers
        if kw in self.headers_frm.ui.lineUserAgent.text():
            blind = True
        if kw in self.headers_frm.ui.lineCookie.text():
            blind = True
        if kw in self.headers_frm.ui.lineReferer.text():
            blind = True
        if kw in self.headers_frm.ui.lineXForwardedFor.text():
            blind = True
        if kw in self.headers_frm.ui.lineCustomHeader.text():
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
            self.ui.isHexed.setChecked(False)
            self.ui.isHexed.setVisible(False)
        else:
            self.ui.menuMssql.setEnabled(True)
            self.ui.isHexed.setVisible(True)
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
            if (self.isHidden() or self.windowState() == QtCore.Qt.WindowMinimized):
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
    
    def setTrueTime(self, trueTime):
        self.ui.trueTimeBox.setValue(trueTime)
        
#------------------------------------------------END------------------------------------------------------#

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mform = EnemaForm()
    mform.show()
    sys.exit(app.exec_())
