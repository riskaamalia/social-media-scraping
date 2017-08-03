import sqlite3

class SqliteDao:
    DB_PATH = 'facebook.db'
    TABLE_NAME_SOURCE = 'source_from_fb'
    TABLE_NAME_PAGE = 'page_from_fb'
    conn = None
    cursor = None

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()


    def create_table_page(self):
        self.conn.execute('''CREATE TABLE {} (url varchar(100) );'''.format(self.TABLE_NAME_PAGE))

    def create_table_source(self):
        self.conn.execute('''CREATE TABLE {} (domain varchar(50) , url_source varchar(200) , url_page varchar(100) , date DATE );'''.format(self.TABLE_NAME_SOURCE))

    def add_page(self, row):
        self.cursor.execute("INSERT INTO {} VALUES (?)".format(self.TABLE_NAME_PAGE), (row,))
        self.conn.commit()

    def add_source(self, row):
        self.cursor.execute("INSERT INTO {} VALUES (?,?,?,?)".format(self.TABLE_NAME_SOURCE), (row[0],row[1],row[2],row[3],))
        self.conn.commit()

    def get_page(self):
        result = []
        for row in self.cursor.execute('SELECT * FROM {}'.format(self.TABLE_NAME_PAGE)):
            print (row)
            result.append(row)

        return result

    def get_source(self):
        result = []
        for row in self.cursor.execute('SELECT * FROM {}'.format(self.TABLE_NAME_SOURCE)):
            print (row)
            result.append(row)

        return result



dao = SqliteDao()
# row = ('www.kompas.com','www.kompas.com/berita','https://www.facebook.com/kompascom','2016-01-01 10:20:05.123')
# result = dao.add_source(row)
dao.get_page()
dao.get_source()
