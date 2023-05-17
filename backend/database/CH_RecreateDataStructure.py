import psycopg2 as pc2
from CH_DBRequiredInformation import POSTGRES # 資料庫連線的必要設定資訊

def getConn():
    conn = pc2.connect(
        user = POSTGRES['user'],
        password = POSTGRES['password'],
        host = POSTGRES['host'],
        port = POSTGRES['port']
    )
    return conn

def database_isExist():
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = '%(database)s'" % POSTGRES)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return True if result is not None else False

def database_create():
    conn = getConn()
    conn.autocommit = True # 先理解「事務：transaction」，這個動作確保未來創建 Database 的時候要在 transaction block 之外
    cursor = conn.cursor()
    try:
        # 需要特別注意，字典 values 欄位的文字需要特別在單引號內加雙引號，不然寫進資料庫的資料將會「對大小寫不敏感」，換句話說就是只會寫進小寫
        cursor.execute('CREATE DATABASE "%(database)s"' % POSTGRES)
    except:
        print("數據庫 %(database)s 創建失敗" % POSTGRES)
    else:
        print("數據庫 %(database)s 創建成功" % POSTGRES)

    cursor.close()
    conn.close()

def schema_exists(cursor):
    # 特別注意，這查詢 schema 的時候要將名稱設置元 tuple，GPT 教我的，所以為什麼？我也不知道
    cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (POSTGRES["schema"],))
    result = cursor.fetchone()

    return True if result is not None else False

def create_schema(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('CREATE SCHEMA "%(schema)s"' % POSTGRES)
    except:
        print("schema %(schema)s 創建失敗" % POSTGRES)
    else:
        print("schema %(schema)s 創建成功" % POSTGRES)
    conn.commit()

def table_exists(cursor):
    # 特別注意，這查詢 schema 的時候要將名稱設置元 tuple，GPT 教我的，所以為什麼？我也不知道
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_name = %s", (POSTGRES["schema"], POSTGRES["table"]))
    result = cursor.fetchone()

    return True if result is not None else False

def create_table(conn):
    cursor = conn.cursor()

    try:
        # 給定一個 list 來保存 column 相關定義
        column_definitions = []
        # 給定一個 list 來保存 PK
        primary_key_columns = []

        # 迭代 POSTGRES 字典中的 tableColumn 項目
        for column in POSTGRES["tableColumn"].values():
            column_name = column["name"]
            data_type = column["dataType"]
            can_null = "NULL" if column["canNull"] else "NOT NULL"
            is_PK = column["isPK"]
            
            # 將 column 相關定義添加到 list 中
            column_definitions.append(f"{column_name} {data_type} {can_null}")

            # 如果 isPK 為 True，將欄位名稱添加到 PK list
            if is_PK:
                primary_key_columns.append(column_name)
        
        # 用逗號將列定義連接在一起
        columns_string = ", ".join(column_definitions)

        # 用逗號將 PK 欄位連接在一起
        primary_key_string = ", ".join(primary_key_columns)
        
        # 合成 SQL 語法
        SQL_cmd = ('CREATE TABLE "%(schema)s"."%(table)s"('
                f"{columns_string}"
                f",PRIMARY KEY ({primary_key_string})"
            ')' % POSTGRES)

        # 建立資料表，連欄位也一起建
        cursor.execute(SQL_cmd)
    except:
        print("資料表 %(table)s 創建失敗" % POSTGRES)
    else:
        print("資料表 %(table)s 創建成功" % POSTGRES)
    conn.commit()

if __name__ == '__main__':
    
    # 檢查資料庫是否存在
    if database_isExist():
        print("數據庫 %(database)s 存在" % POSTGRES)
    else:
        print("數據庫 %(database)s 不存在，將開始創建數據庫" % POSTGRES)
        database_create()
    
    
    # 連接到 PostgreSQL
    conn = pc2.connect(
        host = POSTGRES["host"],
        database = POSTGRES["database"],
        user = POSTGRES["user"],
        password = POSTGRES["password"],
        port = POSTGRES['port']
    )
    cursor = conn.cursor()
    
    # 檢查 schema 是否存在
    if schema_exists(cursor):
        print("schema %(schema)s 存在" % POSTGRES)
    else:
        print("schema %(schema)s 不存在，將開始創建 schema" % POSTGRES)
        create_schema(conn)

    # 檢查 資料表 是否存在
    if table_exists(cursor):
        print("資料表 %(table)s 存在" % POSTGRES)
    else:
        print("資料表 %(table)s 不存在，將開始創建資料表" % POSTGRES)
        create_table(conn)

    # 提交更改並關閉連接
    cursor.close()
    conn.close()