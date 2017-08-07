# This is just for checking facebook.db

from database.SqliteDao import SqliteDao
dao = SqliteDao()

rows = dao.get_page()
print(rows.__len__())
print(rows[1500])
print(dao.is_url_page_exist(rows[1500][0]))

# for row in rows :
#     print(row)
