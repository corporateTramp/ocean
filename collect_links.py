import requests
import html5lib
from bs4 import BeautifulSoup

def collect():
	pages  = []
	r = requests.get('http://www.t30p.ru/Instagram.aspx')
	soup = BeautifulSoup(r.text, 'html5lib')
	# print r.text
	
	for tag in soup.find_all('td',class_="name"):
		page = tag.a.get('href')
		page = str(page[(page.rfind('/')+1):])
		pages.append(page)
	
	return pages
	
	

print collect()
	

	

