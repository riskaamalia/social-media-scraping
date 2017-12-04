from os.path import abspath

import logging
import MySQLdb

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

    def insert_data (self,str_val) :
        # Prepare SQL query to INSERT a record into the database.
        sql = "insert into alodokter_questions (metadata_id, metadata_source, metadata_url, metadata_title,metadata_article_tag," \
              "questioner_image, questioner_name, questioner_profile_link, questioner_question,questioner_date," \
              "expert_image, expert_name, expert_profile_link, expert_answer,expert_date) " \
              "values ("+str_val+");"
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.conn.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.conn.rollback()
            logging.exception(str(e.message))

    def get_latest_id (self) :
        self.cursor.execute('select metadata_id from alodokter_questions order by metadata_id desc limit 1')
        rows = self.cursor.fetchall()
        return rows[0]

    def get_url (self, url) :
        self.cursor.execute("select * from alodokter_questions where metadata_url = '"+url+"'")
        rows = self.cursor.fetchall()
        return rows
sql = sql()

def insert (metadata_url, metadata_title, metadata_article_tag, questioner_image, questioner_name, questioner_profile_link,
            questioner_question,questioner_date, expert_image, expert_name, expert_profile_link, expert_answer,expert_date) :
    if expert_date == '' :
        expert_date = 'null'
    else :
        expert_date = "'"+expert_date+"'"

    if questioner_date == '' :
        questioner_date = 'null'
    else :
        questioner_date = "'"+questioner_date+"'"

    str_val = "null,'alodokter','"+ metadata_url +"','"+ metadata_title +"','"+ metadata_article_tag +"','"+ questioner_image +"','" \
    + questioner_name +"','"+ questioner_profile_link +"','"+ questioner_question +"',"+ questioner_date +",'" \
    + expert_image +"','"+ expert_name +"','"+ expert_profile_link +"','"+ expert_answer +"',"+ expert_date

    sql.insert_data(str_val)

def latest_id () :
    return sql.get_latest_id()

def get_url (url) :
    return sql.get_url(url)

def close() :
    sql.close()


# insert('','','','','','','2017-08-23 14:56:47','','','','','')

# print str(get_url('http://www.alodokter.com/komunitas/topic/mual-87/'))
