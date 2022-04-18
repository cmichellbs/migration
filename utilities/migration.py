from databases import Database, Select,Insert, get_tables_columns


"""create a class thal will receive a database migration project whith project id, destination database, source database, and a list of tables and columns to migrate
then it will create a new database class with the destination database and a list of tables and columns to migrate"""
class Migrate(object):
    def __init__(self, project_id, destination_db, source_db):
        self.project_id = project_id
        self.destination_db = destination_db
        self.source_db = source_db
        self.destination_db = Database(destination_db.host, destination_db.db, destination_db.usr, destination_db.pwd, destination_db.port, destination_db.driver, **destination_db.kwargs)
        self.source_db = Database(source_db.host, source_db.db, source_db.usr, source_db.pwd, source_db.port, source_db.driver, **source_db.kwargs)
        self.source_tables, self.source_columns = get_tables_columns(self.source_db)
        self.destination_tables, self.destination_columns = get_tables_columns(self.destination_db)


"""create a function that will receive a Migrate class and select the data from each source table and columns and insert it to the destination database"""
def migrate(migrate):
    for table in migrate.source_tables['TABLE_NAME']:
        if table in migrate.destination_tables['TABLE_NAME']:
            print(f'{table} already exists in destination database')
        else:
            print(f'creating {table} table in destination database')
            migrate.destination_db.engine.execute(f'CREATE TABLE {table} ({", ".join(migrate.source_columns[migrate.source_columns["TABLE_NAME"] == table]["COLUMN_NAME"])})')
        print(f'inserting data from {table} table to destination database')
        migrate.destination_db.engine.execute(Insert(table, migrate.source_columns[migrate.source_columns["TABLE_NAME"] == table]["COLUMN_NAME"]).insert(), migrate.source_db.engine.execute(Select(table, migrate.source_columns[migrate.source_columns["TABLE_NAME"] == table]["COLUMN_NAME"]).select()).fetchall())
    print('migration completed')






"""initialize an AI to process natural language queries and return a response"""