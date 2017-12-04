import timeout_decorator
import os
import sys
import logging
import MySQLdb

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_libr import sea_mysql
from sea_libr import sea_check

class sql :

    conn = None
    cursor = None

    def __init__(self):
        self.open()

    def open(self):
        try:
            self.conn = MySQLdb.connect()
            self.cursor = self.conn.cursor()

        except Exception as e:
            logging.exception("Error connecting to database!")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def insert_keyword (self,str_val) :
        # Prepare SQL query to INSERT a record into the database.
        sql = "insert into existing_keywords (id,keyword,status) values ("+str_val+");"
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.conn.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.conn.rollback()
            logging.exception(str(e.message))

    def update_keyword (self,keyword, status) :
        sql = "UPDATE existing_keywords SET status ="+str(status)+" WHERE keyword ='"+str(keyword)+"';"
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.conn.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.conn.rollback()
            logging.exception(str(e.message))

sea_db = sea_mysql.SeaDb()
sql = sql()

def get_keyword_status(keyword) :
    row = sea_db.query("select status from existing_keywords where keyword = '"+keyword+"'")
    if row :
        return row[0][0]
    else :
        return 0

def get_keyword() :
    row = sea_db.query("select keyword from existing_keywords order by id desc")
    return row

def get_url() :
    row = sea_db.query("select id,link from sources order by id limit 1000")
    return row

def change_keyword_status(keyword, status) :
     str_val = "null,'"+str(keyword)+"',"+str(status)
     row = sea_db.query("select status from existing_keywords where keyword = '"+keyword+"'")
     if row :
        sql.update_keyword(keyword,status)
     else :
        sql.insert_keyword(str_val)

# @timeout_decorator.timeout(30, use_signals=True,exception_message='reach timeout ....')
def send (url,keyword) :

    logging.info("Exist : "+str(sea_check.is_exist(url,'bing',keyword))+" url : "+url)

def close() :
    sql.close()
    sea_db.close()
