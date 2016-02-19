import selenium.webdriver as webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import requests
import html5lib
from bs4 import BeautifulSoup
import time
import collections
import psycopg2

def collect_links():
	pages  = []
	r = requests.get('http://www.t30p.ru/Instagram.aspx')
	soup = BeautifulSoup(r.text, 'html5lib')
	
	for tag in soup.find_all('td',class_="name"):
		page = tag.a.get('href')
		page = str('https://www.instagram.com/'+page[(page.rfind('/')+1):])
		pages.append(page)
	
	print "Urls are collected"
	
	return pages

def strInt(text):
	if "," in text:
		text = int(text.replace(',',''))
	elif "k" in text:
		text = int(float(text.replace('m',''))*1000)
	elif "m" in text:
		text = int(float(text.replace('m',''))*1000000)
	else:
		text = int(text)
	return text
	
def convert_lists(data):
	for dic in range(0,len(data)):
		for key in data[dic]:
			x = data[dic][key]
			if isinstance(x, basestring):
				x = x.decode('utf-8')
	return data
	

def instagram(urls):
	
	# conn = psycopg2.connect("dbname=postgres user=postgres password =postgres" )
	
	for url in urls["https://www.instagram.com/samburskaya/"]:
	
		print url


import selenium.webdriver as webdriver
from selenium.webdriver.common.action_chains import ActionChains		
driver = webdriver.PhantomJS()
driver.get('https://www.instagram.com/samburskaya/')
		
name = driver.find_element_by_xpath("//section/main/article/header/div[2]/div[1]/h1").text
description = driver.find_element_by_xpath ("//section/main/article/header/div[2]/div[2]/span[2]").text
		
		content_params_add =[]
		
		try:
			for x in range (1,5):
				for i in range(1,4):
					private = False
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
									
					content_params_new = [content_type, alt, strInt(likes), strInt(comments)]
					content_params_add.append(content_params_new)
					
		except NoSuchElementException:
			private = True
		
		accounts_add = (name, description, private)
		# scan_sessions_add = (strInt(publications), strInt(subscribers),strInt(subscribtions))
		# content_params_add = [tuple(l) for l in content_params_add]
		
		
		
		# cur = conn.cursor()
		# cur.execute("INSERT INTO accounts(name, description, private, created_at, updated_at) VALUES (%s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP), date_trunc('second',CURRENT_TIMESTAMP));", accounts_add)

		# cur.execute("INSERT INTO scan_sessions(publications, subscribers, subscribtions, created_at) VALUES (%s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", scan_sessions_add)
		
		# cur.executemany("INSERT INTO content_params (content_type, description, likes, comments, created_at) VALUES (%s, %s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", content_params_add)
				
		# conn.commit()
		# cur.close()

		# driver.quit()
		# time.sleep(10)
	
	# conn.close()
	
	
t0 = time.time()
urls = collect_links()			
instagram(urls)
t1 = time.time()
print "Code execution time is:" , time.strftime("%H:%M:%S", time.gmtime(t1-t0))
