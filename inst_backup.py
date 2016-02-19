import selenium.webdriver as webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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
	
	conn = psycopg2.connect("dbname=postgres user=root password =postgres" )
	cur = conn.cursor()
	
	# dcap = dict(DesiredCapabilities.PHANTOMJS)
	# dcap["phantomjs.page.settings.userAgent"] = ( "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 " "(KHTML, like Gecko) Chrome/15.0.87")
	
	# accounts =[]
	# scan_sessions = []
	
	for url in urls[:3]:
	
		content_params =[]
		print url
		
		# driver = webdriver.PhantomJS(desired_capabilities=dcap)
		driver = webdriver.PhantomJS()
		driver.get(url)
		
		name = driver.find_element_by_xpath("//section/main/article/header/div[2]/div[1]/h1").text
		description = driver.find_element_by_xpath ("//section/main/article/header/div[2]/div[2]/span[2]").text
		publications = driver.find_element_by_xpath ("//section/main/article/ul/li[1]/span/span[2]").text
		subscribers = driver.find_element_by_xpath ("//section/main/article/ul/li[2]/span/span[2]").text
		subscribtions = driver.find_element_by_xpath ("//section/main/article/ul/li[3]/span/span[2]").text
		
		
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
					
					# content_params_add = {"name": name, "content_type": content_type, "description": alt, "likes":likes,"comments":comments}
					# content_params.append(content_params_add)
					
					
					
					# content_params_add = {"name": name, "content_type": content_type, "description": alt, "likes":likes,"comments":comments}
					# content_params.append(content_params_add)

		except NoSuchElementException:
			private = True
		
		accounts_add = (name, description, private)
		scan_sessions_add = (name, publications, subscribers,subscribtions)
		
		# check if name exists
		# if exists - get ID
		# else - insert and get ID
		
		# accounts_add = {"name": name, "description": description, "private": private}
		# scan_sessions_add = {"name": name, "publications": publications, "subscribers": subscribers, "subscribtions": subscribtions}
		
		
		# accounts_add = {"name": name, "description": description, "private": private}
		# scan_sessions_add = {"name": name, "publications": publications, "subscribers": subscribers, "subscribtions": subscribtions}
		
		# accounts_add = {"name": name, "description": description, "private": private}
		# scan_sessions_add = {"name": name, "publications": publications, "subscribers": subscribers, "subscribtions": subscribtions}
		
		# accounts.append(accounts_add)
		# scan_sessions.append(scan_sessions_add)
		
		# cur.executemany("INSERT INTO accounts (name,description,private) VALUES (%s, %s);,data")
		# conn.commit()
		# cur.close()
		# conn.close()
		
		driver.quit()
		time.sleep(2)
	
	# accounts = convert_lists(accounts)
	# scan_sessions = convert_lists(scan_sessions)
	# content_params = convert_lists(content_params)
	
	return accounts, scan_sessions
	

urls = collect_links()			
print instagram(urls)