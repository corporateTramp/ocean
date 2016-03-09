from __future__ import division
import requests
import urllib2 
import html5lib
from bs4 import BeautifulSoup
import time
import psycopg2
import json

def collect_links(page):
	pages  = []
	for i in range (1,page+1):
		r = requests.get("http://www.t30p.ru/Instagram.aspx?p="+str(i))
		soup = BeautifulSoup(r.text, 'html5lib')
	
		for tag in soup.find_all('td',class_="name"):
			page = tag.a.get('href')
			page = str('https://www.instagram.com/'+page[(page.rfind('/')+1):])
			pages.append(page)
		print "Urls are collected from page: " + str(i)
		
	print "Urls are collected"
	
	return pages

def convert_tuple_to_unicode(data):
	list =[]
	for dic in range(0,len(data)):
		x = data[dic]
		if isinstance(x, basestring):
			list.append(x.decode('utf-8'))
		else:
			list.append(x)
	return tuple(list)

def start_init(urls, wait, db_data="dbname=alex user=alex password=alexdb"):
	
	conn = psycopg2.connect(db_data)
	cur = conn.cursor()
	cur.execute("SELECT name, description, private FROM accounts;")
	begAccounts  = cur.fetchall()
	cur.close()
	
	# set http headers
	header = ['Cache-Control', 'Accept', 'User-Agent', 'Referrer', 'Accept-Encoding', 'Accept-Language']
	value = ['no-cache','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 39.0.2171.95 Safari/537.36', 'https://www.google.com/', 'gzip, deflate, sdch', 'ru-RU,en-US,en;q=0.8']
	custom_headers={}
	for i in range(1,len(header)):
		custom_headers[header[i]] = value[i]
	
	counter = 1
	
	for url in urls:
		
		print "Started: " + url + " (" + str(counter) +")"
		counter = counter + 1
		try:
			
			r = requests.get(url, headers=custom_headers)
			soup = BeautifulSoup(r.text, 'html5lib')
			json_data = soup.body.find_all(type="text/javascript")
			json_data = json_data[0].text
			json_data = json_data[21:(len(json_data)-1)]
			
			data = json.loads(json_data)
			
			#parsing main info
			private = data["entry_data"]["ProfilePage"][0]["user"]["is_private"]
			publications = data["entry_data"]["ProfilePage"][0]["user"]["media"]["count"]
			name = data["entry_data"]["ProfilePage"][0]["user"]["username"]
			subscribers = data["entry_data"]["ProfilePage"][0]["user"]["followed_by"]["count"]
			subscriptions = data["entry_data"]["ProfilePage"][0]["user"]["follows"]["count"]
			try:
				fullName = data["entry_data"]["ProfilePage"][0]["user"]["full_name"]
			except:
				fullName = " "
			
			try:
				bio = data["entry_data"]["ProfilePage"][0]["user"]["biography"]
			except:
				bio = " "
				
			try:
				external_url = data["entry_data"]["ProfilePage"][0]["user"]["external_url"]
			except:
				external_url = " "

			if not fullName: fullName = ""
			if not bio: bio = ""
			if not external_url: external_url = ""

			description = fullName + " " + bio + " " + external_url
			
			likes_sum = 0
			
			#parsing posts
			content_params_add =[]
			if private == False:
				for i in range (0,10):
					try:
						isVideo = data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"][i]["is_video"]
						if isVideo == False:
							content_type = "Photo"
						else:
							content_type = "Video"
						likes = data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"][i]["likes"]["count"]
						comments = data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"][i]["comments"]["count"]
						try:
							alt = data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"][i]["caption"]
						except:
							alt = ""	
						
						content_params_new = [content_type, alt, likes, comments]
						content_params_add.append(content_params_new)
						likes_sum = likes_sum + int(likes)
					except:
						pass
			
			##filtering of what to add and updating accounts
			account_add = (name, description, private)
			cur = conn.cursor()
			flag = 0
			
			for acc in range(0,len(begAccounts)):
				if name == (convert_tuple_to_unicode(begAccounts[acc]))[0]:
					cur.execute("UPDATE accounts SET (name, description, private, updated_at) = (%s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP)) WHERE name = %s ;", (name, description, private, name,))
					conn.commit()
					flag = 1
					
			if flag == 0:
					cur.execute("INSERT INTO accounts(name, description, private, created_at) VALUES (%s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", account_add)
					conn.commit()
					
			cur.close()
					
			##mapping account id and updating scan_sessions
			cur = conn.cursor()
			cur.execute("SELECT id, name FROM accounts;")
			updatedAccounts  = cur.fetchall()
			updatedAccounts = convert_tuple_to_unicode(updatedAccounts)
			cur.close()
			
			account_id = 999999
			for i in range(0,len(updatedAccounts)):
				if name == updatedAccounts[i][1].decode('utf-8'):
					account_id = updatedAccounts[i][0]
			
			scan_sessions_add = (account_id, publications, subscribers, subscriptions, likes_sum/10, likes_sum/subscribers, publications/subscribers)
			cur = conn.cursor()
			cur.execute("INSERT INTO scan_sessions(account_id, publications, subscribers, subscriptions, created_at, active_subscribers, er, avg) VALUES (%s, %s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP), %s, %s, %s);", scan_sessions_add)
			conn.commit()
			cur.close()
			
			
			##mapping scan_id
			cur = conn.cursor()
			cur.execute("SELECT id, account_id FROM scan_sessions;")
			updatedSessions  = cur.fetchall()
			cur.close()
			
			scan_session_id = 999999
			for q in range(0,len(updatedSessions)):
				if account_id == updatedSessions[q][1]:
					scan_session_id = updatedSessions[q][0]
					
			##adding content params
			for w in range(0,len(content_params_add)):
				content_params_add[w].insert(0,scan_session_id)
				content_params_add[w].insert(0,account_id)			
			
			content_params_add = [tuple(l) for l in content_params_add]
			cur = conn.cursor()
			cur.executemany("INSERT INTO content_params (account_id, scan_session_id, content_type, description, likes, comments, created_at) VALUES (%s, %s, %s, %s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", content_params_add)
			conn.commit()
			cur.close()

			time.sleep(wait)
		
		except urllib2.HTTPError, err:
			if err.code == 403:
				time.sleep(20)
				print "Instagram denied access to", url
			else:
				print "Connection problem raised on", url
		except:
			print "Exception on link: ", url
		
	conn.close()

def create_tables(db_data="dbname=alex user=alex password=alexdb"):	
	conn = psycopg2.connect(db_data)
	cur = conn.cursor()

	cur.execute("CREATE TABLE accounts ( id SERIAL PRIMARY KEY, name text, description text, private bool, created_at timestamp, updated_at timestamp);")
	cur.execute("CREATE TABLE scan_sessions ( id SERIAL PRIMARY KEY, account_id integer, publications integer,subscribers integer, subscriptions integer, created_at timestamp, active_subscribers real , er real , avg real );")
	cur.execute("CREATE TABLE content_params ( id SERIAL PRIMARY KEY, account_id integer, scan_session_id integer,content_type text,description text, likes integer, comments integer, created_at timestamp);")

	conn.commit()
	cur.close()
	print "Created"
	conn.close()

def delete_tables(db_data="dbname=alex user=alex password=alexdb"):		
	conn = psycopg2.connect(db_data)
	cur = conn.cursor()
	cur.execute ("DROP TABLE IF EXISTS accounts, scan_sessions, content_params")
	conn.commit()
	cur.close()

	cur = conn.cursor()
	print "Deleted"
	conn.close()
	
def refresh_tables(db_data="dbname=alex user=alex password=alexdb"):
	delete_tables (db_data)
	create_tables(db_data)
	
def see_table(table = "accounts", db_data="dbname=alex user=alex password=alexdb"):
	conn = psycopg2.connect(db_data)
	cur = conn.cursor()
	print "---------------------------------------------------------------------------------------"
	if table == 'accounts':
		cur.execute("SELECT id, name, created_at, updated_at FROM accounts;")
	elif table == "scan_sessions":
		cur.execute("SELECT id, account_id, publications, subscribers, created_at FROM scan_sessions;")
	elif table == "content_params":
		cur.execute("SELECT id, account_id, scan_session_id, content_type, likes, comments, created_at FROM content_params;")
	
	print cur.fetchall()
	cur.close()
	conn.close()
	
def start(page=20, wait = 10, db_data="dbname=alex user=alex password=alexdb"):
	t0 = time.time()
	urls = collect_links(page)			
	start_init(urls, wait, db_data)
	t1 = time.time()
	print "Code execution time is:" , time.strftime("%H:%M:%S", time.gmtime(t1-t0))
