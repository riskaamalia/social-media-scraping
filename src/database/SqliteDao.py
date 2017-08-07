import sqlite3
from util.ConfigProcessor import ConfigProcessor

class SqliteDao:

    config_processor = ConfigProcessor()

    DB_PATH = config_processor.config_sqlite()[0]
    TABLE_NAME_SOURCE = config_processor.config_sqlite()[1]
    TABLE_NAME_PAGE = config_processor.config_sqlite()[2]
    print("==="+DB_PATH)
    print("==="+TABLE_NAME_PAGE)
    print("==="+TABLE_NAME_SOURCE)
    conn = None
    cursor = None

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_table_source()
        self.create_table_page()


    def create_table_page(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS {} (url varchar(100) );'''.format(self.TABLE_NAME_PAGE))

    def create_table_source(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS {} (domain varchar(50) , url_source varchar(200), url_page varchar(100) , date DATE );'''.format(self.TABLE_NAME_SOURCE))

    def add_page(self, row):
        self.cursor.execute("INSERT INTO {} VALUES (?)".format(self.TABLE_NAME_PAGE), (row,))
        self.conn.commit()

    def add_source(self, row):
        self.cursor.execute("INSERT INTO {} VALUES (?,?,?,?)".format(self.TABLE_NAME_SOURCE), (row[0],row[1],row[2],row[3],))
        self.conn.commit()

    def custom_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    # return 0 if not exist
    def is_url_source_exist (self, url) :
        result = []
        for row in self.cursor.execute('SELECT * FROM '+self.TABLE_NAME_SOURCE+' where url_source = "'+url+'"') :
            result.append(row)

        return result.__len__()

    # return 0 if not exist
    def is_url_page_exist (self, url) :
        result = []
        for row in self.cursor.execute('SELECT * FROM '+self.TABLE_NAME_PAGE+' where url = "'+url+'"') :
            result.append(row)

        return result.__len__()

    def get_page(self):
        result = []
        for row in self.cursor.execute('SELECT * FROM {}'.format(self.TABLE_NAME_PAGE)):
            result.append(row)

        return result

    def get_source(self):
        result = []
        for row in self.cursor.execute('SELECT * FROM {}'.format(self.TABLE_NAME_SOURCE)):
            result.append(row)

        return result
