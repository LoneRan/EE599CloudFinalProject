from mysql.connector import MySQLConnection, Error
import json

#read db config
def read_db_config(filename='config/mysql_profile.json'):
	conf = None
	try:
		with open(f'{filename}') as f:
			conf = json.loads(f.read())
			conf['password'] = conf.pop('pass')
			conf['database'] = conf.pop('db')
			# print(conf)
	except (IOError, json.decoder.JSONDecodeError):
			print("there is some error",file = sys.stderr)
			conf = {}
	return conf

#test db connection
def connect():
	try:
		conf = read_db_config()
		conn = MySQLConnection(**conf)
		print('connected!')
		if not conn.is_connected():
			print('fail to connect')		
		conn.close()
	except Error as error:
		#exit with exit 4
		print('end 4')	
		# pass

#execute a query which modify db	
def execute(query):
	try:
		global_cursor.execute(query)
		global_conn.commit()
		# print(cursor.lastrowid)
	except Error as error:
		print(error)

#execute a query which read data from db
#return: a list of dictionary for each row of data
def readdb(query):
	res = []
	try:
		global_cursor.execute(query)
		rows = global_cursor.fetchall()
		for row in rows:
			res.append(row)
	except Error as error:
		print(error)		
	return res

def getFirstName(email):
	res = readdb('select fname from profiles where user_id = (select user_id from credentials where username = "{}")'.format(email))
	return res[0]['fname']

def close_db():
	global_cursor.close()
	global_conn.close()

def checkDupProfile(email):
	currProDB = readdb('select * from credentials')
	for dic in currProDB:
		if dic['username']==email:
			return True
	return False

def register(fname, lname, email, password):
	query = 'insert into profiles(fname, lname) VALUES("{}","{}")'.format(fname,lname)
	execute(query)
	query = 'insert into credentials(user_id, username, pass) VALUES({},"{}","{}")'.format(global_cursor.lastrowid,email,password)
	execute(query)

def checkCredential(email, password):
	query = 'select * from credentials where username="{}" and pass="{}"'.format(email,password)
	res	= readdb(query)
	return (len(res)>0)

def updateProfile(form, username):
	key = list(form.keys())[:-1]
	value = list(map(lambda x : '"'+x+'"',form.values()))[:-1]
	l = []
	for k,v in zip(key,value):
		if v!='""':
			l.append(k+'='+v)
	print(l)
	update = ','.join(l)
	query = 'update profiles set ' + update + ' where user_id = (select user_id from credentials where username = "{}");'.format(username)
	execute(query)

def generateInfo(username):
	info = readdb('select * from profiles where user_id=(select user_id from credentials where username="{}");'.format(username))[0]
	# print(info)
	userData = []
	for key,val in info.items():
		if key!='user_id' and val != None and val != '':
			if key =='fname':
				key='Firstname'
			elif key == 'lname':
				key = 'Lastname'
			key = key[0].upper() + key[1:]
			val = val[0].upper() + val[1:]
			userData.append((key,val))
	return userData;

def updatePassword(username,password):
	query = 'update credentials set pass="{}" where username="{}"'.format(password,username)
	execute(query)

global_conn = MySQLConnection(**read_db_config())
global_cursor = global_conn.cursor(dictionary=True)

# print(readdb("select * from profiles"))
# print(checkCredential("liask@usc.edu", "qwe12312"))
# print(getFirstName("ruiwenhe@usc.edu"))