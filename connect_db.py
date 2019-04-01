from pymongo import MongoClient

def enqury_data():
	wordlist = []
	DBNAME = ''      #数据库名
	DBUSERNAME = ''  #数据库用户
	DBPASSWORD = ''  #数据库密码
	DB = ''          #数据库IP
	PORT = 27017
	db_conn = MongoClient(DB, PORT)
	na_db = getattr(db_conn, DBNAME)
	na_db.authenticate(DBUSERNAME, DBPASSWORD)
	return na_db

if __name__ == '__main__':
	enqury_data()