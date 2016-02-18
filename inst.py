
import selenium.webdriver as webdriver
from selenium.webdriver.common.action_chains import ActionChains
import requests
import html5lib
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException

def collect():
	pages  = []
	r = requests.get('http://www.t30p.ru/Instagram.aspx')
	soup = BeautifulSoup(r.text, 'html5lib')
	# print r.text
	
	for tag in soup.find_all('td',class_="name"):
		page = tag.a.get('href')
		page = str('https://www.instagram.com/'+page[(page.rfind('/')+1):])
		pages.append(page)
	
	return pages


def instagram(urls):

	for url in urls:
		# time.sleep(7)
		driver = webdriver.PhantomJS()
		driver.get(url)


		user = driver.find_element_by_xpath("//section/main/article/header/div[2]/div[1]/h1")
		desc = driver.find_element_by_xpath ("//section/main/article/header/div[2]/div[2]/span[2]")
		posts = driver.find_element_by_xpath ("//section/main/article/ul/li[1]/span/span[2]")
		followers = driver.find_element_by_xpath ("//section/main/article/ul/li[2]/span/span[2]")

			
		print user.text
		print desc.text
		print posts.text
		print followers.text
		
		try:
			for x in range (1,5):
				for i in range(1,4):
					pic = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div"%(x,i))
					hover = ActionChains(driver).move_to_element(pic)
					hover.perform()
					try:
						likes = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[2]/ul/li/span[2]" %(x,i))
						comments = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[2]/ul/li[2]/span[2]" %(x,i))
						type = "Photo"
						alt = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[1]/div[1]/img" %(x,i))
					except:
						likes = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[3]/ul/li/span[2]" %(x,i))
						comments = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[3]/ul/li[2]/span[2]" %(x,i))
						type = "Video"
						alt = driver.find_element_by_xpath("//section/main/article/div[1]/div/div[%d]/a[%d]/div[1]/div[1]/img" %(x,i))
					print likes.text
					print comments.text
					print type
					print alt.get_attribute("alt")
		except NoSuchElementException:
					print "invisible page"
				
		driver.quit()
				

urls = collect()			
instagram(urls)