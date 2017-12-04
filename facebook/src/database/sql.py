import logging
import MySQLdb

from util.ConfigProcessor import ConfigProcessor


class sql :
    config_processor = ConfigProcessor()
    TABLE_NAME_SOURCE = config_processor.config_sql()[0]
    TABLE_NAME_PAGE = config_processor.config_sql()[1]
    TABLE_NAME_PAGE_VIDEO = config_processor.config_sql()[2]
    TABLE_NAME_VIDEO = config_processor.config_sql()[3]
    conn = None
    cursor = None

    def __init__(self):
        self.open()

    def open(self):
        try:
            self.conn = MySQLdb.connect(host='', user="", passwd="", db="",
                                        use_unicode=True, charset='utf8')
            self.cursor = self.conn.cursor()

        except Exception as e:
            logging.exception("Error connecting to database!")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def insert_mysql (self,table_name,str_val) :
        # Prepare SQL query to INSERT a record into the database.
        sql = "insert into "+table_name+" values ("+str_val+");"
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.conn.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.conn.rollback()
            logging.exception('-')

    def update_mysql (self,sources_id, link, total) :
        sql = "UPDATE sources_total_links SET total ="+str(total)+", link ='"+link.encode('utf-8', 'ignore')+"' WHERE id ="+str(sources_id)+";"
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.conn.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.conn.rollback()
            logging.exception('---')

    def add_page(self, row):
        if len(row[0]) > 250 :
            row[0] = row[0][:249]
        str_val = "'"+row[0]+"','"+row[1]+"'"
        self.insert_mysql(self.TABLE_NAME_PAGE,str_val.encode('utf-8', 'ignore'))

    def add_video_page(self, row):
        if len(row[0]) > 100 :
            row[0] = row[0][:99]
        str_val = "'" + row[0] + "','" + row[1] + "',"+str(row[2])
        self.insert_mysql(self.TABLE_NAME_PAGE_VIDEO, str_val.encode('utf-8', 'ignore'))

    def add_source(self, row):
        if len(row[1]) > 200 :
            row[1] = row[1][:199]
        str_val = "'" + row[0] + "','" + row[1] + "','" + row[2] + "','" + row[3] + "','" +row[4] +"'"
        self.insert_mysql(self.TABLE_NAME_SOURCE, str_val.encode('utf-8', 'ignore'))

    def add_video(self, row):
        str_val = "'" + row[0] + "','" + row[1] + "','" + row[2] + "'," + str(row[3]) + ",'" + row[4]+"'"
        self.insert_mysql(self.TABLE_NAME_VIDEO, str_val.encode('utf-8', 'ignore'))

    # return 0 if not exist
    def is_url_domain_exist (self, url) :
        self.cursor.execute('SELECT * FROM '+self.TABLE_NAME_SOURCE+" where domain like'%"+url.encode('utf-8', 'ignore')+"%'")
        rows = self.cursor.fetchall()
        return len(rows)

    # return 0 if not exist
    def is_url_video_exist (self, url) :
        self.cursor.execute('SELECT * FROM ' + self.TABLE_NAME_VIDEO + " where url_source like'%" + url.encode('utf-8', 'ignore') + "%'")
        rows = self.cursor.fetchall()
        return len(rows)

    # return 0 if not exist
    def is_url_page_exist (self, url) :
        self.cursor.execute('SELECT * FROM ' + self.TABLE_NAME_PAGE + " where url like'%" + url.encode('utf-8', 'ignore') + "%'")
        rows = self.cursor.fetchall()
        return len(rows)

    def is_url_page_video_exist (self, url) :
        self.cursor.execute('SELECT * FROM ' + self.TABLE_NAME_PAGE_VIDEO + " where url like'%" + url.encode('utf-8', 'ignore') + "%'")
        rows = self.cursor.fetchall()
        return len(rows)

    def get_page(self):
        self.cursor.execute('SELECT * FROM {} order by url'.format(self.TABLE_NAME_PAGE))
        rows = self.cursor.fetchall()
        return rows

    def get_page_video(self):
        self.cursor.execute('SELECT * FROM {} order by url'.format(self.TABLE_NAME_PAGE_VIDEO))
        rows = self.cursor.fetchall()
        return rows

    def get_source(self):
        self.cursor.execute('SELECT * FROM {} order by url_source'.format(self.TABLE_NAME_SOURCE))
        rows = self.cursor.fetchall()
        return rows

    def get_video(self):
        self.cursor.execute('SELECT * FROM {} order by url_source'.format(self.TABLE_NAME_VIDEO))
        rows = self.cursor.fetchall()
        return rows

    def delete_page(self, url_page) :
        self.cursor.execute("delete from "+self.TABLE_NAME_PAGE+" where url='"+url_page.encode('utf-8', 'ignore')+"'")
        self.conn.commit()

        return url_page
#
# test = sql()
# row = ('beritagar.com','beritagar.com','https://www.facebook.com/beritagarID/ ','berita',str(datetime.now().strftime('%Y-%m-%d')) )
# print test.add_source(row)