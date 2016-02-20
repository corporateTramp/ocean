import selenium.webdriver as webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import requests
import urllib2 
import html5lib
from bs4 import BeautifulSoup
import time
import psycopg2

def collect_links(link):
	pages  = []
	r = requests.get(link)
	soup = BeautifulSoup(r.text, 'html5lib')
	
	for tag in soup.find_all('td',class_="name"):
		page = tag.a.get('href')
		page = str('https://www.instagram.com/'+page[(page.rfind('/')+1):])
		pages.append(page)
	
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
	
def strInt(text):
	if "," in text:
		text = int(text.replace(',',''))
	elif "k" in text:
		text = int(float(text.replace('k',''))*1000)
	elif "m" in text:
		text = int(float(text.replace('m',''))*1000000)
	else:
		text = int(text)
	return text

def start_init(urls, db_data="dbname=postgres user=postgres password =postgres"):
	
	conn = psycopg2.connect("dbname=postgres user=postgres password =postgres")
	count = 1
	
	for url in urls:
		
		print url
		try:
			driver = webdriver.PhantomJS()
			driver.get(url)
			
			#parsing main info
			name = driver.find_element_by_xpath("//section/main/article/header/div[2]/div[1]/h1").text
			description = driver.find_element_by_xpath ("//section/main/article/header/div[2]/div[2]/span[2]").text
			publications = driver.find_element_by_xpath ("//section/main/article/ul/li[1]/span/span[2]").text
			subscribers = driver.find_element_by_xpath ("//section/main/article/ul/li[2]/span/span[2]").text
			subscribtions = driver.find_element_by_xpath ("//section/main/article/ul/li[3]/span/span[2]").text
			
			
			#parsing posts
			content_params_add =[]
			try:
				for x in range (1,5):
					for i in range(1,4):
						pic = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div"%(x,i))
						hover = ActionChains(driver).move_to_element(pic)
						hover.perform()
						try:
							likes = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[2]/ul/li/span[2]" %(x,i)).text
							comments = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[2]/ul/li[2]/span[2]" %(x,i)).text
							content_type = "photo"
							alt = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[1]/div[1]/img" %(x,i)).get_attribute("alt")
						except:
							likes = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[3]/ul/li/span[2]" %(x,i)).text
							comments = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[3]/ul/li[2]/span[2]" %(x,i)).text
							content_type = "video"
							alt = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[1]/div[1]/img" %(x,i)).get_attribute("alt")
						
						private = False
										
						content_params_new = [content_type, alt, strInt(likes), strInt(comments)]
						content_params_add.append(content_params_new)
						
			except NoSuchElementException:
				private = True
			
			##updating accounts
			account_add = (name, description, private)	
			cur = conn.cursor()
			cur.execute("INSERT INTO accounts(name, description, private, created_at) VALUES (%s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", account_add)
			conn.commit()
			cur.close()
					
			##mapping account id and updating scan_sessions	
			account_id = count
			scan_sessions_add = (account_id, strInt(publications), strInt(subscribers),strInt(subscribtions))
			cur = conn.cursor()
			cur.execute("INSERT INTO scan_sessions(account_id, publications, subscribers, subscribtions, created_at) VALUES (%s, %s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", scan_sessions_add)
			conn.commit()
			cur.close()
			
			
			##mapping scan_id
			scan_session_id = count
					
			##adding content params
			for w in range(0,len(content_params_add)):
				content_params_add[w].insert(0,scan_session_id)
				content_params_add[w].insert(0,account_id)
			
			content_params_add = [tuple(l) for l in content_params_add]
			cur = conn.cursor()
			cur.executemany("INSERT INTO content_params (account_id, scan_session_id, content_type, description, likes, comments, created_at) VALUES (%s, %s, %s, %s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", content_params_add)
			conn.commit()
			cur.close()

			driver.quit()
			count += 1
			time.sleep(10)
		
		except urllib2.HTTPError, err:
			if err.code == 403:
				print "Instagram denied access to", url
				time.sleep(20)
			else:
				print "Connection problem raised on", url
		
	conn.close()

	
def update_init(urls, db_data="dbname=postgres user=postgres password =postgres"):
	
	conn = psycopg2.connect(db_data)
	cur = conn.cursor()
	cur.execute("SELECT name, description, private FROM accounts;")
	begAccounts  = cur.fetchall()
	cur.close()
	
	for url in urls:
		
		print url
		try:
			
			driver = webdriver.PhantomJS()
			driver.get(url)
			
			#parsing main info
			name = driver.find_element_by_xpath("//section/main/article/header/div[2]/div[1]/h1").text
			description = driver.find_element_by_xpath ("//section/main/article/header/div[2]/div[2]/span[2]").text
			publications = driver.find_element_by_xpath ("//section/main/article/ul/li[1]/span/span[2]").text
			subscribers = driver.find_element_by_xpath ("//section/main/article/ul/li[2]/span/span[2]").text
			subscribtions = driver.find_element_by_xpath ("//section/main/article/ul/li[3]/span/span[2]").text
			
			
			#parsing posts
			content_params_add =[]
			try:
				for x in range (1,5):
					for i in range(1,4):
						pic = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div"%(x,i))
						hover = ActionChains(driver).move_to_element(pic)
						hover.perform()
						try:
							likes = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[2]/ul/li/span[2]" %(x,i)).text
							comments = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[2]/ul/li[2]/span[2]" %(x,i)).text
							content_type = "photo"
							alt = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[1]/div[1]/img" %(x,i)).get_attribute("alt")
						except:
							likes = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[3]/ul/li/span[2]" %(x,i)).text
							comments = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[3]/ul/li[2]/span[2]" %(x,i)).text
							content_type = "video"
							alt = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[1]/div[1]/img" %(x,i)).get_attribute("alt")
						
						private = False
										
						content_params_new = [content_type, alt, strInt(likes), strInt(comments)]
						content_params_add.append(content_params_new)
						
			except NoSuchElementException:
				private = True
			
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
			
			scan_sessions_add = (account_id, strInt(publications), strInt(subscribers),strInt(subscribtions))
			cur = conn.cursor()
			cur.execute("INSERT INTO scan_sessions(account_id, publications, subscribers, subscribtions, created_at) VALUES (%s, %s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", scan_sessions_add)
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

			driver.quit()
			time.sleep(10)
		
		except urllib2.HTTPError, err:
			if err.code == 403:
				print "Instagram denied access to", url
				time.sleep(20)
			else:
				print "Connection problem raised on", url		
		
	conn.close()

def create_tables(db_data="dbname=postgres user=postgres password =postgres"):	
	conn = psycopg2.connect(db_data)
	cur = conn.cursor()

	cur.execute("CREATE TABLE accounts ( id SERIAL PRIMARY KEY, name text, description text, private bool, created_at timestamp, updated_at timestamp);")
	cur.execute("CREATE TABLE scan_sessions ( id SERIAL PRIMARY KEY, account_id integer, publications integer,subscribers integer, subscribtions integer, created_at timestamp);")
	cur.execute("CREATE TABLE content_params ( id SERIAL PRIMARY KEY, account_id integer, scan_session_id integer,content_type text,description text, likes integer, comments integer, created_at timestamp);")

	conn.commit()
	cur.close()
	"Created"
	conn.close()

def delete_tables(db_data="dbname=postgres user=postgres password =postgres"):		
	conn = psycopg2.connect(db_data)
	cur = conn.cursor()
	cur.execute ("DROP TABLE IF EXISTS accounts, scan_sessions, content_params")
	conn.commit()
	cur.close()

	cur = conn.cursor()
	print "Deleted"
	conn.close()
	
def refresh_tables(db_data="dbname=postgres user=postgres password =postgres"):
	delete_tables (db_data)
	create_tables(db_data)
	
def see_table(table = accounts, db_data="dbname=postgres user=postgres password =postgres"):
	conn = psycopg2.connect(db_data)
	cur = conn.cursor()
	print "---------------------------------------------------------------------------------------"
	cur.execute("SELECT * FROM %s;", (table,))
	print cur.fetchall()
	cur.close()
	conn.close()

	
def start(link='http://www.t30p.ru/Instagram.aspx', db_data="dbname=postgres user=postgres password =postgres"):
	t0 = time.time()
	urls = collect_links(link)			
	start_init(urls, db_data)
	t1 = time.time()
	print "Code execution time is:" , time.strftime("%H:%M:%S", time.gmtime(t1-t0))
	
def update(link='http://www.t30p.ru/Instagram.aspx', db_data="dbname=postgres user=postgres password =postgres"):
	t0 = time.time()
	urls = collect_links(link)			
	update_init(urls, db_data)
	t1 = time.time()
	print "Code execution time is:" , time.strftime("%H:%M:%S", time.gmtime(t1-t0))