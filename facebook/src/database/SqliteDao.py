# import sqlite3
# import os
# from util.ConfigProcessor import ConfigProcessor
#
# class SqliteDao:
#
#     config_processor = ConfigProcessor()
#     path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
#     DB_PATH = path+'/'+config_processor.config_sql()[0]
#     TABLE_NAME_SOURCE = config_processor.config_sql()[1]
#     TABLE_NAME_PAGE = config_processor.config_sql()[2]
#     TABLE_NAME_PAGE_VIDEO = config_processor.config_sql()[3]
#     TABLE_NAME_VIDEO = config_processor.config_sql()[4]
#     conn = None
#     cursor = None
#
#     def __init__(self):
#         self.conn = sqlite3.connect(self.DB_PATH)
#         self.cursor = self.conn.cursor()
#         self.create_table_source()
#         self.create_table_page()
#         self.create_table_video()
#         self.create_table_video_page()
#
#     def create_table_video(self):
#         self.conn.execute('''CREATE TABLE IF NOT EXISTS {} (url_source varchar(500), url_page varchar(100),keyword varchar(50),like int, date DATE );'''.format(self.TABLE_NAME_VIDEO))
#
#     def create_table_page(self):
#         self.conn.execute('''CREATE TABLE IF NOT EXISTS {} (url varchar(100),keyword varchar(50) );'''.format(self.TABLE_NAME_PAGE))
#
#     def create_table_video_page(self):
#         self.conn.execute('''CREATE TABLE IF NOT EXISTS {} (url varchar(100),keyword varchar(50),like int );'''.format(self.TABLE_NAME_PAGE_VIDEO))
#
#     def create_table_source(self):
#         self.conn.execute('''CREATE TABLE IF NOT EXISTS {} (domain varchar(50) , url_source varchar(200), url_page varchar(100),keyword varchar(50) , date DATE );'''.format(self.TABLE_NAME_SOURCE))
#
#     def add_page(self, row):
#         self.cursor.execute("INSERT INTO {} VALUES (?,?)".format(self.TABLE_NAME_PAGE), (row[0],row[1],))
#         self.conn.commit()
#
#     def add_video_page(self, row):
#         self.cursor.execute("INSERT INTO {} VALUES (?,?,?)".format(self.TABLE_NAME_PAGE_VIDEO), (row[0],row[1],row[2],))
#         self.conn.commit()
#
#     def add_source(self, row):
#         self.cursor.execute("INSERT INTO {} VALUES (?,?,?,?,?)".format(self.TABLE_NAME_SOURCE), (row[0],row[1],row[2],row[3],row[4],))
#         self.conn.commit()
#
#     def add_video(self, row):
#         self.cursor.execute("INSERT INTO {} VALUES (?,?,?,?,?)".format(self.TABLE_NAME_VIDEO), (row[0],row[1],row[2],row[3],row[4],))
#         self.conn.commit()
#
#     def custom_query(self, query):
#         self.cursor.execute(query)
#         self.conn.commit()
#
#     # return 0 if not exist
#     def is_url_source_exist (self, url) :
#         result = []
#         for row in self.cursor.execute('SELECT * FROM '+self.TABLE_NAME_SOURCE+' where url_source = "'+url+'"') :
#             result.append(row)
#
#         return result.__len__()
#
#     # return 0 if not exist
#     def is_url_video_exist (self, url) :
#         result = []
#         for row in self.cursor.execute('SELECT * FROM '+self.TABLE_NAME_VIDEO+' where url_source = "'+url+'"') :
#             result.append(row)
#
#         return result.__len__()
#
#     # return 0 if not exist
#     def is_url_page_exist (self, url) :
#         result = []
#         for row in self.cursor.execute('SELECT * FROM '+self.TABLE_NAME_PAGE+' where url = "'+url+'"') :
#             result.append(row)
#
#         return result.__len__()
#
#     def is_url_page_video_exist (self, url) :
#         result = []
#         for row in self.cursor.execute('SELECT * FROM '+self.TABLE_NAME_PAGE_VIDEO+' where url = "'+url+'"') :
#             result.append(row)
#
#         return result.__len__()
#
#     def get_page(self):
#         result = []
#         for row in self.cursor.execute('SELECT * FROM {} order by url'.format(self.TABLE_NAME_PAGE)):
#             result.append(row)
#
#         return result
#
#     def get_page_video(self):
#         result = []
#         for row in self.cursor.execute('SELECT * FROM {} order by url'.format(self.TABLE_NAME_PAGE_VIDEO)):
#             result.append(row)
#
#         return result
#
#     def get_source(self):
#         result = []
#         for row in self.cursor.execute('SELECT * FROM {} order by url_source'.format(self.TABLE_NAME_SOURCE)):
#             result.append(row)
#
#         return result
#
#     def get_video(self):
#         result = []
#         for row in self.cursor.execute('SELECT * FROM {} order by url_source'.format(self.TABLE_NAME_VIDEO)):
#             result.append(row)
#
#         return result
#     def delete_page(self, url_page) :
#         self.cursor.execute("delete from "+self.TABLE_NAME_PAGE+" where url='"+url_page+"'")
#         self.conn.commit()
#
#         return url_page
