"""
    Enema module (core): Text / Strings processing
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

import random
import base64
import string as strings

#Convert string to base64:
def base64proc(string, mode, encoding):
    if mode == "enc":
        readyStr = base64.b64encode(bytes(string, encoding))
    else:
        try:
            readyStr = base64.b64decode(bytes(string, encoding))
        except Exception:
            return " - invalid string - "
    return str(readyStr, encoding)
    
#Convert string to HEX:
def strToHex(string, isCmdHex):
    hexStr = ''.join((hex(ord(symbol)) for symbol in string))
    if isCmdHex:
        cmdhex = "0x" + hexStr.replace("0x", "")
        return cmdhex
    return hexStr
    
#Convert string to SQL char:
def strToSqlChar(string, dbtype):
    if dbtype == "MySQL":
        encoded = ','.join((str(ord(symbol)) for symbol in string))
    else:
        encoded = ')+char('.join((hex(ord(symbol)) for symbol in string))
    return 'char(' + encoded + ")"

#Random changing uppercase
def rndUpCase(string):
    string = ''.join(random.choice([s.upper(), s]) for s in string)
    return string

#Special keywords handler.
def extractString(string, specKw):
    keyword = "[" + specKw + "^"
    fromStr = string.find(keyword)
    fromStr += len(keyword)
    toStr = string.find("^]", fromStr, len(string))
    substring = string[fromStr:toStr]
    string = ''.join((string[:fromStr - len(keyword)] + "ERASEDSUBSTRING" + string[toStr + 2:]))
    return {'str' : string, 'substr' : substring, 'kword' : specKw}

def rndString(length):
	alpha_numeric_str = ''.join([random.choice(strings.ascii_letters + strings.digits) for s in range(length)])
	return alpha_numeric_str

#Symbols recovery to readable format
def recoverSymbols(cmdResult):
    symbols = {
    '&lt;' : '<',
    '&gt;' : '>',
    '&quot;' : '"', 
    '&nbsp;' : chr(160), 
    '&#160;' : chr(160)}
    for key in symbols:
        cmdResult = cmdResult.replace(key, symbols[key])
    return cmdResult

#Some settings in INI file between double quotes, removing qoutes
def correctQstr(qstring):
    if (qstring.startswith('"') and qstring.endswith('"')):
        return qstring[1:-1]
    return qstring

#Rounding time
def roundTime(tm):
    seconds = str(tm).split(".")
    try:
        seconds = int(seconds[0])
    except:
        return 0
    return seconds
    
