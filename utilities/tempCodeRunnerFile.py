db = Database('172.30.1.146', 'papakura_20210504', 'sa', 'Pass@word', 5434, 'mssql+pyodbc',{"driver": "ODBC Driver 17 for SQL Server",
        "charset": "utf8"})
tables, columns = get_tables_columns(db)