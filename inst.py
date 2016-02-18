import selenium.webdriver as webdriver
from selenium.webdriver.common.action_chains import ActionChains

urls = ['http://instagram.com/umnpics/']
# driver = webdriver.Firefox()
driver = webdriver.PhantomJS()


for y in urls:
	driver.get(y)
	# driver.save_screenshot('screenie2.png')

	user = driver.find_element_by_xpath("//section/main/article/header/div[2]/div[1]/h1")
	desc = driver.find_element_by_xpath ("//section/main/article/header/div[2]/div[2]/span[2]")
	posts = driver.find_element_by_xpath ("//section/main/article/ul/li[1]/span/span[2]")
	followers = driver.find_element_by_xpath ("//section/main/article/ul/li[2]/span/span[2]")

	
	print (user.text)
	print (desc.text)
	print (posts.text)
	print (followers.text)
	
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
			print (likes.text)
			print (comments.text)
			print (type)
			print (alt.get_attribute("alt").encode("cp866 ","replace"))

