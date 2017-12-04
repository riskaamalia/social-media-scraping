import timeout_decorator
import sys
import os
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
            self.conn = MySQLdb.connect('',"","","" )
            self.cursor = self.conn.cursor()

        except Exception as e:
            logging.exception("Error connecting to database!")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def insert_mysql (self,str_val) :
        # Prepare SQL query to INSERT a record into the database.
        sql = "insert into sources_total_links (id,sources_id,link,total) values ("+str_val+");"
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.conn.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.conn.rollback()
            logging.info(str(e.message))

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
            logging.info(str(e.message))

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
            logging.info(str(e.message))

    def update_mysql (self,sources_id, link, total) :
        sql = "UPDATE sources_total_links SET total ="+str(total)+", link ='"+link+"' WHERE id ="+str(sources_id)+";"
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.conn.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.conn.rollback()
            logging.info(str(e.message))

sea_db = sea_mysql.SeaDb()
sql = sql()

def insert_to_db (sources_id, link, total) :
        str_val = str(sources_id)+","+str(sources_id)+",'"+link+"',"+str(total)
        if is_exist(sources_id) == 0 :
            sql.insert_mysql(str_val)
            logging.info('#Insert : '+str_val)
            # print '#Insert : '+str_val
        else :
            logging.info('Update result with id : '+str(sources_id)+" and link : "+link)
            sql.update_mysql(sources_id, link, total)

def get_from_db (start,end) :
    return sea_db.query('select id,link from sources where id >='+str(start)+' and id <='+str(end))

def is_exist (sources_id) :
    row = sea_db.query('select * from sources_total_links where id = '+str(sources_id))
    return len(row)

def get_highest_id () :
    row = sea_db.query('select id from sources_total_links order by id desc limit 1')
    return row[0][0]

def get_keyword_status(keyword) :
    row = sea_db.query("select status from existing_keywords where keyword = '"+keyword+"'")
    if row :
        return row[0][0]
    else :
        return 0

def get_keyword() :
    row = sea_db.query("select keyword from existing_keywords order by id")
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

   logging.info("Exist : "+str(sea_check.is_exist(url,'google_search',keyword))+" url : "+url)

def close() :
    sql.close()
    sea_db.close()

# id = get_highest_id()
# print id+1
