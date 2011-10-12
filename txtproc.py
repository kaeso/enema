"""
    Enema module: Text / Strings processing
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

#Convert string to HEX:
def strToHex(string):
    encoded = ''.join((hex(ord(symbol)) for symbol in string))
    encoded = encoded.replace("0x", "")
    return "0x" + encoded
    
#Convert string to SQL char:
def strToSqlChar(string, dbtype):
    if dbtype == "mysql":
        encoded = ','.join((str(ord(symbol)) for symbol in string))
    else:
        encoded = ')+char('.join((hex(ord(symbol)) for symbol in string))
    return 'char(' + encoded + ")"
    
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


