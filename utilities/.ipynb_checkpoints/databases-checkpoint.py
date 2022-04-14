import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import pyodbc
import pymysql
import sys


""" create a class that will receive the connection parameters"""   
class Database(object):
    def __init__(self, host, db, usr, pwd, port, context, query = None,**kwargs):
        self.host = host
        self.db = db
        self.usr = usr
        self.pwd = pwd
        self.port = port
        self.context = context
        self.query = query
        self.kwargs = kwargs
        self.url= sqlalchemy.engine.URL.create(
            self.context,
            username= self.usr,
            password= self.pwd,
            host= self.host,
            port= self.port,
            database=  self.db,
            query = self.query,)


"""" create a function thal will return all tables of a Database class for a postgres database sqlalchemy"""
def get_tables_postgres(db):
    conn = sqlalchemy.create_engine(f'{db.context}://{db.usr}:{db.pwd}@{db.host}:{db.port}/{db.db}')
    tables = pd.read_sql_query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES", conn)
    return tables

"""" create a function thal will return all columns of a Database class for a postgres database sqlalchemy"""
def get_columns_postgres(db):
    conn = sqlalchemy.create_engine(f'{db.context}://{db.usr}:{db.pwd}@{db.host}:{db.port}/{db.db}')
    columns = pd.read_sql_query("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS", conn)
    return columns
    
"""create a function that will return all tables of a Database class for a mssql database"""
def get_tables_mssql(db):
    conn = sqlalchemy.create_engine(f'{db.context}://{db.usr}:{db.pwd}@{db.host}:{db.port}/{db.db}')
    tables = pd.read_sql_query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES", conn)
    return tables
"""create a function that will return all columns of a Database class for a mssql database"""
def get_columns_mssql(db):
    conn = sqlalchemy.create_engine(f'{db.context}://{db.usr}:{db.pwd}@{db.host}:{db.port}/{db.db}')
    columns = pd.read_sql_query("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS", conn)
    return columns

"""create a function that will return all tables of a Database class for a mysql database"""
def get_tables_mysql(db):
    conn = sqlalchemy.create_engine(f'{db.context}://{db.usr}:{db.pwd}@{db.host}:{db.port}/{db.db}')
    tables = pd.read_sql_query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES", conn)
    return tables
"""create a function that will return all columns of a Database class for a mysql database"""
def get_columns_mysql(db):
    conn = sqlalchemy.create_engine(f'{db.context}://{db.usr}:{db.pwd}@{db.host}:{db.port}/{db.db}')
    columns = pd.read_sql_query("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS", conn)
    return columns
    
"""create a endpoint that will receive a database class and return all tables and all columns of a given database"""
def get_tables_columns(db):
    if db.context == 'postgresql+psycopg2':
        tables = get_tables_postgres(db)
        columns = get_columns_postgres(db)
    elif db.context == 'mssql+pyodbc':
        tables = get_tables_mssql(db)
        columns = get_columns_mssql(db)
    elif db.context == 'mysql+pymysql':
        tables = get_tables_mysql(db)
        columns = get_columns_mysql(db)
    else:
        print('driver not supported')
        sys.exit()
    return tables, columns

"""create a class that will receive two columns, then  format a insert instruction from the second column to the first column"""
class Insert(object):
    def __init__(self, table, columns):
        self.table = table
        self.columns = columns
    def insert(self):
        return f"INSERT INTO {self.table} ({', '.join(self.columns)}) VALUES ({', '.join(['%s' for _ in self.columns])})"

"""create a class that will receive a table and columns, then format a select instruction from the columns to the table"""
class Select(object):
    def __init__(self, table, columns):
        self.table = table
        self.columns = columns
    def select(self):
        return f"SELECT {', '.join(self.columns)} FROM {self.table}"
        

if __name__ == '__main__':
    db = Database('172.30.1.146', 'papakura_20210504', 'sa', 'Pass@word', 5434, 'mssql+pyodbc',{"driver": "ODBC Driver 17 for SQL Server"})
    tables, columns = get_tables_columns(db)
    print(tables)
    print(columns)
    print(db.query)