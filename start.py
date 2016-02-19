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
	
	print "collection is finished"
	
	return pages
	
			
def instagram(urls):
	
	conn = psycopg2.connect("dbname=postgres user=postgres password =postgres" )
	
	for url in urls[3:5]:
	
		print url
		
		driver = webdriver.PhantomJS()
		driver.get(url)
		
		name = driver.find_element_by_xpath("//section/main/article/header/div[2]/div[1]/h1").text
		description = driver.find_element_by_xpath ("//section/main/article/header/div[2]/div[2]/span[2]").text
		publications = driver.find_element_by_xpath ("//section/main/article/ul/li[1]/span/span[2]").text
		subscribers = driver.find_element_by_xpath ("//section/main/article/ul/li[2]/span/span[2]").text
		subscribtions = driver.find_element_by_xpath ("//section/main/article/ul/li[3]/span/span[2]").text
		
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
									
					content_params_new = [content_type, alt, likes, comments]
					content_params_add = zip (content_params_add, content_params_new)
					

		except NoSuchElementException:
			private = True
		
		accounts_add = (name, description, private)
		scan_sessions_add = (publications, subscribers,subscribtions)
		
		
		# write to database
		cur = conn.cursor()
		cur.execute("INSERT INTO accounts(name, description, private, created_at, updated_at) VALUES (%s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP), date_trunc('second',CURRENT_TIMESTAMP));", accounts_add)

		cur.execute("INSERT INTO accounts(publications, subscribers, subscribtions, created_at) VALUES (%s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", scan_sessions_add)
		
		cur.executemany("INSERT INTO content_params(account_id, scan_session_id, content_type, description, likes, comments, created_at) VALUES (1, 1, %s, %s, %s, %s, date_trunc('second',CURRENT_TIMESTAMP));", content_params_add)
				
		conn.commit()
		cur.close()

		driver.quit()
		time.sleep(7)
	
	conn.close()
	
	

urls = collect_links()			
instagram(urls)