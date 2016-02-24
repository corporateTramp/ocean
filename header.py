import selenium.webdriver as webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import requests
import urllib2 
import html5lib
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

# dcap = dict(DesiredCapabilities.PHANTOMJS)


# header = ['Cache-Control', 'Accept', 'User - Agent', 'Referrer', 'Accept - Encoding']
# value = ['no-cache','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)', 'https://www.google.com/', 'gzip, deflate, sdch']


# del dcap['browserName']
# del dcap['version']
# del dcap['platform']
# print dcap
	
# driver = webdriver.PhantomJS(desired_capabilities=dcap)
# page = driver.get('https://www.instagram.com/staroverova/')

# name = driver.find_element_by_xpath("//section/main/article/header/div[2]/div[1]/h1").text
# description = driver.find_element_by_xpath ("//section/main/article/header/div[2]/div[2]/span[2]").text
# publications = driver.find_element_by_xpath ("//section/main/article/ul/li[1]/span/span[2]").text
# subscribers = driver.find_element_by_xpath ("//section/main/article/ul/li[2]/span/span[2]").text
# subscribtions = driver.find_element_by_xpath ("//section/main/article/ul/li[3]/span/span[2]").text
import selenium.webdriver as webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import requests
import urllib2 
import html5lib
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json


header = ['Cache-Control', 'Accept', 'User-Agent', 'Referrer', 'Accept-Encoding', 'Accept-Language']
value = ['no-cache','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 39.0.2171.95 Safari/537.36', 'https://www.google.com/', 'gzip, deflate, sdch', 'ru-RU,en-US,en;q=0.8']

custom_headers={}
for i in range(1,len(header)):
	custom_headers[header[i]] = value[i]

r = requests.get('https://www.instagram.com/timatiofficial/', headers=custom_headers)
soup = BeautifulSoup(r.text, 'html5lib')
json_data = soup.body.find_all(type="text/javascript")
json_data = json_data[0].text
json_data = json_data[21:(len(json_data)-1)]

data = json.loads(json_data)

private = data["entry_data"]["ProfilePage"][0]["user"]["is_private"]
publications = data["entry_data"]["ProfilePage"][0]["user"]["media"]["count"]
name = data["entry_data"]["ProfilePage"][0]["user"]["username"]
subscribers = data["entry_data"]["ProfilePage"][0]["user"]["followed_by"]["count"]
subscribtions = data["entry_data"]["ProfilePage"][0]["user"]["follows"]["count"]
fullName = data["entry_data"]["ProfilePage"][0]["user"]["full_name"]
bio = data["entry_data"]["ProfilePage"][0]["user"]["biography"]
external_url = data["entry_data"]["ProfilePage"][0]["user"]["external_url"]
description = fullName+" "+bio+" "+external_url


if private = False:
	for i in range (0,9):
		isVideo = data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"][0]["is_video"]
		content_type
		likes = data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"][0]["likes"]["count"]
		comments = data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"][0]["comments"]["count"]
		alt = data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"][0]["caption"]


# print name, description, publications, subscribers, subscriptions
# file_ = open('page4.txt', 'w')
# file_.write(driver.page_source.encode("utf-8"))
# file_.write(json_data)
# file_.close()

