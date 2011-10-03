"""
    Enema module: Text / Strings processing.
    Copyright (C) 2011  Valeriy Bogachuk
    
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
    
#SQL error parsing:
def contentParse(content, match_pattern, match_sybol):
    patternStr = content.find(match_pattern)
    fromStr = content.find(match_sybol, patternStr, len(content))
    fromStr += 1
    toStr = content.find(match_sybol, fromStr, len(content))
    if (fromStr or toStr) <= 0:
        file = open("err_response.html", "w")
        file.write(content)
        file.close()
        print("\n==================[SERVER RESPONSE]==================\n\n"\
                + content +\
                "\n\n=========[Saved to file: err_response.html===========")
        return "no_content"
    return content[fromStr:toStr]
    
#Convert string to CONVERT Error generation method:
def castToConvert(query, match_sybol):
    MS = strToSqlChar(match_sybol)
    query = query.replace(MS + '+cast(',  'convert(varchar, ' + MS + '+')
    query = query.replace(' as varchar)+' + MS, '+' + MS + ')')
    return query

    

