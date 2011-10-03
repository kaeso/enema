"""
    $Id$
    Enema http-request module
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

import os
import sys
import e_const
import txtproc
import socket
from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlencode

#Server response debugging
def debug(strValue):
    print("\n - [x] 'no_content' returned by function", strValue)
    question = "\n - [!] View html file in browser? [y/n]: "
    answer = input(question)
    while (answer !="y" or answer != "n"):
        if (answer =="n"):
            print("\nOK. Aborted.")
            break
        elif answer == "y":
            os.system("err_response.html")
            break
        else:
            answer = input(question)

#Injection in cookies?:
def isCookieInjection(cookie):
    if ("[sub]" or "[cmd]") in cookie:
        return True

def buildUrl(strVar, query, isCmd, isCookie):
    if isCookie:
        query = request.quote(query)
        strVar = strVar.replace("=[sub]", "%3d[sub]")
        strVar = strVar.replace("=[cmd]", "%3d[cmd]")
    if isCmd:
        if "[cmd]" in strVar:
            strVar = strVar.replace("[cmd]", query)
            if "[sub]" in strVar:
                strVar = strVar.replace("[sub]", "1")
        else:
            print("\n\n [sub] or [cmd] variables not found")                
    else:
        if "[cmd]" in strVar:
            strVar = strVar.replace(";[cmd]", "")
        strVar = strVar.replace("[sub]", query)
    return strVar

#Preparing POST data
def preparePostData(data,  query,  isCmd):
    data = data.replace("=[sub]",  "[shgrp_sub]")   #saving sensetive data  
    data = ''.join([x.replace("=",  ":") for x in data])
    data = data.replace("[shgrp_sub]",  "=[sub]")   #restore sensetive data
    if isCmd:
        if "[cmd]" in data:
            data = data.replace("[cmd]", query)
            if "[sub]" in data:
                data = data.replace("[sub]", "1")
            else:
                print("\n\n [sub] or [cmd] variables not found")                
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
def webRequest(args, query, isCmd):
    urlOpener = request.build_opener()
    data = request.unquote(args['data'])
    cookie = args['cookie']
    data = data.replace("+",  " ")
    data = data.replace(":",  "")
    if args['method'] == "POST":
        postData = preparePostData(data, query, isCmd)
        if isCookieInjection(cookie):
            cookie = buildUrl(cookie, query, isCmd, True)
        print("\n[POST]", args['url'] + "\n" + postData.decode(e_const.ENCODING))
        if len(cookie) > 0:
            print ("Cookie:", cookie)
            urlOpener.addheaders = [('User-Agent', e_const.USER_AGENT), ('Cookie', cookie)]
        else:
            urlOpener.addheaders = [('User-Agent', e_const.USER_AGENT)]
        try:
            response = urlOpener.open(args['url'], postData, args['timeOut'])
            content = response.read()
        except HTTPError as httpErr: 
            content = httpErr.read()
        #Handling timeout. 
        except socket.error:
            errno, errstr = sys.exc_info()[:2]
            if errno == socket.timeout:
                print("\n\n[Timed out]")
                return "[---Timed out---]"
        except URLError as uerr:
            if isinstance(uerr.reason, socket.timeout):
                print("\n\n[Timed out]")
                return "[---Timed out---]"
    else:
        if isCookieInjection(cookie):
            cookie = buildUrl(cookie, query, isCmd, True)
        else:
            data = buildUrl(data, query, isCmd, False)
        data = ''.join(data)
        data = request.quote(data)
        #Replacing important symbols
        data = data.replace("%3D", "=")
        data = data.replace("%26", "&")
        url = args['url'] + "?" + data
        print("\n[GET]",  url)
        if len(cookie) > 0:
            print ("Cookie:", cookie)
            urlOpener.addheaders = [('User-Agent', e_const.USER_AGENT), ('Cookie', cookie)]
        else:
            urlOpener.addheaders = [('User-Agent', e_const.USER_AGENT)]
        try:
            response = urlOpener.open(url, None, args['timeOut'])
            content = response.read()
        except HTTPError as httpErr: 
            content = httpErr.read()
        #Handling timeout
        except socket.error:
            errno, errstr = sys.exc_info()[:2]
            if errno == socket.timeout:
                print("\n\n[Timed out]")
                return "[---Timed out---]"
        except URLError as uerr:
            if isinstance(uerr.reason, socket.timeout):
                print("\n\n[Timed out]")
                return "[---Timed out---]"
    if not isCmd:
        if e_const.QUOTED_CONTENT:
            content = request.unquote(content)
        try:
            content = content.decode(e_const.ENCODING)
        except:
            print("\n\nCan't decode content!\nDefined charset='" + e_const.ENCODING + "'")
            return "no_content"
        db_data = txtproc.contentParse(content, args['mp'], args['ms'])
    else:
        db_data = 0
    return db_data
    
