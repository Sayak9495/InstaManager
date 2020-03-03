import time
import random
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
#driver.find_element_by_xpath('//button[@tabindex=0]').click()

def login():
	#### HEADLESS ###
	#chrome_options = Options()  
	#chrome_options.add_argument("--headless")
	#################,chrome_options=chrome_options

	driver=webdriver.Chrome("D:\\chromedriver_win32\\chromedriver.exe")
	driver.get("https://www.instagram.com/accounts/login/")
	time.sleep(3)
	uname_field = driver.find_element_by_xpath("//input[@name='username']")
	uname=""
	uname_field.send_keys(uname)
	time.sleep(3)
	pwd_field = driver.find_element_by_xpath("//input[@name='password']")
	pwd=""
	pwd_field.send_keys(pwd)
	time.sleep(2)
	driver.find_element_by_xpath('//button[@type="submit"]').click()
	time.sleep(5)
	driver.find_element_by_xpath('//button[@tabindex=0]').click()
	time.sleep(1)
	return driver

def populate(driver,hashtags):
	base_url='https://www.instagram.com/explore/tags/'
	#hashtag=random.choice(hashtags)
	hashtag=hashtags[-1]
	url=base_url + hashtag
	driver.get(url)
	time.sleep(3)
	
	accts=[]
	for i in range(1,4):
		for j in range(1,4):
			temp=driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div['+str(i)+']/div['+str(j)+']')

			temp.click()
			time.sleep(4)
			try:
				driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/div/button').click()
			except:
				driver.find_element_by_xpath('//span[@tabindex="0"]').click()
			time.sleep(3)
			temp=driver.find_element_by_xpath('(//a[@class="FPmhX notranslate _0imsa "])['+str(randint(1, 11))+']')

			acct = temp.get_attribute('href')
			if acct not in accts: 	
				accts.append(acct)
			print(acct)
			driver.find_element_by_xpath('/html/body/div[3]/div/button').click()
			
			time.sleep(1)

	print('\n')
	print(accts)


driver=login()
hashtags=['alldayhustle','motivate','garyvee']
populate(driver,hashtags)
