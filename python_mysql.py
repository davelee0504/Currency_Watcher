import mysql.connector
from config import *

class PythonMysql:
	config = Config()
	db_name = config.get_db_name()
	db_user = config.get_db_user()
	db_password = config.get_db_password()
	db_host = config.get_db_host()

	conn = mysql.connector.Connect(host=db_host, user=db_user,\
                        password=db_password,database=db_name, buffered=True)
	# constructor
	#def __init__(self):
		#print ('mysql connector born')
    
	def is_user_duplicated(self, telegram_user_id):
		cursor = self.conn.cursor()
		# see following url for sql usage		
		# http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
		sql = "SELECT * FROM user WHERE telegram_user_id = %(t_u_id)s"
		cursor.execute(sql, {'t_u_id': telegram_user_id})
		#print cursor._executed
		#print 'cursor.rowcount=%s' % (cursor.rowcount)
		if(cursor.rowcount):
			return True
		else:
			return False
		cursor.close

	def insert_new_user(self, telegram_user_id):
		cursor = self.conn.cursor()
		sql = "INSERT INTO user (telegram_user_id) VALUES (%(t_u_id)s)"
		cursor.execute(sql, {'t_u_id': str(telegram_user_id)})
		#print cursor._executed
		self.conn.commit()
		cursor.close

	def delete_user(self, telegram_user_id):
		cursor = self.conn.cursor()
		sql = "DELETE FROM user WHERE telegram_user_id = (%(t_u_id)s)"
		cursor.execute(sql, {'t_u_id': str(telegram_user_id)})
		#print cursor._executed
		self.conn.commit()
		cursor.close	

	def get_subscribe_users(self):
		cursor = self.conn.cursor()
		sql = "SELECT * FROM user"
		cursor.execute(sql)
		#data = cursor.fetchall()
		data = [item[0] for item in cursor.fetchall()]
		cursor.close
		return data

	# destructor
	def __del__(self):
		#self.conn.cursor.close
		self.conn.close
		#print ('mysql connector died')

	
