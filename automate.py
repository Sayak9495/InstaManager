import random
from random import randint
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 

def login():
	#### HEADLESS ###
	chrome_options = Options()  
	chrome_options.add_argument("--headless")
	#################,chrome_options=chrome_options

	#driver=webdriver.Chrome("D:\\chromedriver_win32\\chromedriver.exe",chrome_options=chrome_options)
	driver=webdriver.Chrome("D:\\chromedriver_win32\\chromedriver.exe")
	#driver=webdriver.Chrome("chromedriver",chrome_options=chrome_options)
	driver.get("https://www.instagram.com/accounts/login/")

	time.sleep(5)
	uname_field = driver.find_element_by_xpath("//input[@name='username']")
	uname="insta_handle"
	uname_field.send_keys(uname)
	time.sleep(2)
	pwd_field = driver.find_element_by_xpath("//input[@name='password']")
	pwd="your_password"
	pwd_field.send_keys(pwd)
	time.sleep(3)
	driver.find_element_by_xpath('//button[@type="submit"]').click()
	time.sleep(4)
	try:
		driver.find_element_by_xpath('//button[@tabindex=0]').click()
	except:
		l=5
	time.sleep(1)
	print("LoggedIn")
	return driver


def populate_FollowList(driver,hashtags):
	#Should append n_acs to list in txt in folder.
	#Should take 20Min to execute.
	
	base_url='https://www.instagram.com/explore/tags/'
	hashtag=random.choice(hashtags)
	#hashtag=hashtags[-1]
	url=base_url + hashtag
	driver.get(url)
	time.sleep(3)
	
	with open('IGList.txt','rb') as f:
		lst_ = pickle.load(f)
	#print(lst_)
	lst,x,y=lst_
	#accts=[]
	for col in range(1,4):
		for row in range(1,4):
			#print(col ,"-> Col ",row,"-> Row")
			path='//*[@id="react-root"]/section/main/article/div[1]/div/div/div['+str(col)+']/div['+str(row)+']' #select the i,jth img
			temp=driver.find_element_by_xpath(path)
			temp.click() #open that img
			time.sleep(4)
			try:
				driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/div/button').click() #click on likes
			except:
				#driver.find_element_by_xpath('//span[@tabindex="0"]').click()
				driver.find_element_by_xpath('/html/body/div[3]/div/button').click() #if video, then closes and starts next iteration
				#print("ERROR: Video")
				continue
			time.sleep(3)

			scroll=driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]')
			for i in range(4):
				driver.execute_script("arguments[0].scrollTo({ top:"+str(400*i)+", behavior: 'smooth' })", scroll)
				time.sleep(3)


			acct = getAcct(driver,lst,path) #will check duplicate and closed acct
			#print(acct)

			if (acct == "video"):
				driver.find_element_by_xpath('/html/body/div[3]/div/button').click()
				#print("ERROR: Video (shouldn't come here")
				continue
			lst.append(acct)
			

			driver.find_element_by_xpath('/html/body/div[3]/div/button').click()
			time.sleep(2)

	
	IGLst=[]
	IGLst.append(lst)
	IGLst.append(x)
	IGLst.append(y)

	with open('IGList.txt', 'wb') as f:
		pickle.dump(IGLst,f)
	print(len(lst)," Acct Appended Successfully to IGlist")
	time.sleep(11)#80
	return


def getAcct(driver,accts,path):
	try:
		temp=driver.find_element_by_xpath('(//a[@class="FPmhX notranslate _0imsa "])['+str(randint(1, 31))+']')
	except:
		return "video"
	acct = temp.get_attribute('href')
	if (acct in accts) :
		#print("Duplicate ", acct)
		return getAcct(driver,accts,path)
	else:
		if (checkProfile(driver,acct,path)):
			#print("Closed ", acct)
			return getAcct(driver,accts,path)
		#else:
			#print("PASSED ", acct)
	return acct


def checkProfile(driver,acct,path):
	#open tab
	
	#driver.send_keys(Keys.CONTROL + 't')
	#driver.execute_script('''window.open("https://some.site/", "_blank");''')

	time.sleep(2)
	#print("Checking.... ",acct)
	driver.get(acct)
	time.sleep(4)
	try:
		driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span/span[1]/button')
		flag=0
	except:
		flag=1
	time.sleep(2)
	#print(flag)
	
	#driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
	#driver.switch_to.window(driver.window_handles[0])
	driver.execute_script("window.history.go(-2)")
	temp=driver.find_element_by_xpath(path)
	temp.click()
	time.sleep(4)
	try:
		driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/div/button').click()
	except:
		driver.find_element_by_xpath('//span[@tabindex="0"]').click()
	time.sleep(3)

	scroll=driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]')
	for i in range(4):
		driver.execute_script("arguments[0].scrollTo({ top:"+str(400*i)+", behavior: 'smooth' })", scroll)
		time.sleep(3)
	
	# 0-> Open | 1 -> Closed
	return flag


def follow(driver,n_times):
	#From follow_node start following the ACs.
	#increment follow_node and update to txt.
	#Should take 10Min to execute.

	with open('IGList.txt','rb') as f:
		IGLst = pickle.load(f)
	IGLst,i,j=IGLst
	while n_times:
		#for 3 Acs
		n_times-=1
		acc=IGLst[i]
		#print("Follow ",acc)
		i+=1
		time.sleep(5)
		driver.get(acc)
		time.sleep(5)
		try:
			lola=10
			#if that follow button doesn't exists, then skip
			driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span/span[1]/button').click() #followed
			print(i," Followed ",acc)
			time.sleep(5) 
			try:
				#like 2 random posts from 2 - 16 .
				driver.find_element_by_xpath('((//div[@style="flex-direction: column; padding-bottom: 0px; padding-top: 0px;"])/div)[1]/div['+str(randint(1, 3))+']').click() #selected
				time.sleep(2)
				driver.find_element_by_xpath('(//span[@aria-label="Like"])[1]').click() #liked
				time.sleep(2)
				driver.find_element_by_xpath('/html/body/div[3]/div/button').click() #closed
				time.sleep(1)
				driver.find_element_by_xpath('((//div[@style="flex-direction: column; padding-bottom: 0px; padding-top: 0px;"])/div)[2]/div['+str(randint(1, 3))+']').click() #selected
				time.sleep(2)
				driver.find_element_by_xpath('(//span[@aria-label="Like"])[1]').click() #liked
				time.sleep(2)
				driver.find_element_by_xpath('/html/body/div[3]/div/button').click() #closed
				print("Liked 2 Posts of ",acc)
				time.sleep(5)
			except:
				print("ERROR: Couldn't like 2 Posts for ",acc)
		except:
			print("ERROR at ", i,acc)
			n_times+=1


	lst=[]
	lst.append(IGLst)
	lst.append(i)
	lst.append(j)

	with open('IGList.txt', 'wb') as f:
		pickle.dump(lst,f)
	#print("---",i,j)
	return

 
def unfollow(driver,n_times):
	#From UNfollow_node start UNfollowing the ACs.
	#increment Unfollow_node and update to txt.
	#Should take 10Min to execute.

	with open('IGList.txt','rb') as f:
		IGLst = pickle.load(f)
	IGLst,i,j=IGLst

	while n_times:
		#for 3 Acs
		n_times-=1
		acc=IGLst[j]
		j+=1
		#print(j,n_times)
		#time.sleep(5)
		driver.get(acc)
		time.sleep(5) #100
		try:
			#if that unfollow button doesn't exists, then skip
			driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span/span[1]/button').click()
			time.sleep(2)
			driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[3]/button[1]').click()
			print(j," UNFollowed ",acc)
			time.sleep(3) #93
		except:
			print("ERROR at ", j,acc)
			n_times+=1

	lst=[]
	lst.append(IGLst)
	lst.append(i)
	lst.append(j)

	with open('IGList.txt', 'wb') as f:
		pickle.dump(lst,f)
	return


def populate_PostList(driver,hashtags):
	base_url='https://www.instagram.com/explore/tags/'
	hashtag=random.choice(hashtags)
	url=base_url + hashtag
	driver.get(url)
	time.sleep(3)
	
	
	with open('PostList.txt','rb') as f:
		lst_ = pickle.load(f)
	#print(lst_)
	lst,x=lst_
	
	for col in range(1,4):
		for row in range(1,4):
			#print(col ,"-> Col ",row,"-> Row")
			path='//*[@id="react-root"]/section/main/article/div[1]/div/div/div['+str(col)+']/div['+str(row)+']/a'
			temp = driver.find_element_by_xpath(path)
			post = temp.get_attribute('href')
			#print(post)
			if post in lst:
				print("Duplicate")
			else:
				lst.append(post)



	with open('PostList.txt', 'wb') as f:
		pickle.dump([lst,x],f)
	print(len(lst)," Posts Appended Successfully to PostList")
	time.sleep(11)#80
	
	return


def likeComment(driver,comments,n):
	with open('PostList.txt','rb') as f:
		lst_ = pickle.load(f)
	#print(lst_)
	lst,x=lst_
	x_temp=x
	for post in lst[x_temp:x_temp+n]:
		#print("checking...",x_temp,x)
		x+=1
		driver.get(post)
		time.sleep(4)
		comment=random.choice(comments)
		driver.find_element_by_xpath('(//span[@aria-label="Like"])[1]').click() #liked
		time.sleep(1)
		comment_field = driver.find_element_by_xpath('//textarea[@aria-label="Add a comment…"]')
		driver.find_element_by_xpath('//textarea[@aria-label="Add a comment…"]').click()
		driver.find_element_by_xpath('//textarea[@aria-label="Add a comment…"]').send_keys(comment)
		driver.find_element_by_xpath('//textarea[@aria-label="Add a comment…"]').send_keys(Keys.RETURN) #commented
		print("Liked and Commented ",x)
		time.sleep(4)
		with open('PostList.txt', 'wb') as f:
			pickle.dump([lst,x],f)


def start():

	with open('IGList.txt', 'wb') as f:
		pickle.dump([[],0],f)

	with open('IGList.txt', 'wb') as f:
		pickle.dump([[],0,0],f)

	driver=login()
	hashtags=['entrepreneurquotes','alldayhustle','financialfreedom','motivate','garyvee','millionairemindset','hustlelikegaryvee','businessmind','keytosuccess','brainpower','achievebig','businesstips', 'entrepreneurgoals', 'successtips', 'unconditionalmotivation' ,'iwillwin', 'dreambig',   'luxury', 'millionairequotes' ,'quoteoftheday', 'success' ,'successquote' ,'quotestags' 'motivationalquotes',  'motivationalspeaker' ,'mindshift' ,'mindset',  'goalcast', 'tedtalks', 'simonsinek', 'grantcordone', 'tailopez', 'financialliteracy','richdadpoordad']

	comments=["Great post, loved it. Follow @insta_handle for more inspiring content it\'s worth it.","Perfect {silently applauses}","This is awesome. Follow @insta_handle for more hustling content it\'s a must visit.","Lovely post. If you love to hustle, you should visit @insta_handle , you would love it.","Truly Amazing.","This will make me hustle even more.try @insta_handle for more hustling content.","ooh! that's lit. you got to follow @insta_handle, you will love it.","And that's what I came here for. Great! Follow @insta_handle for more inspiring content","Just wow!!!"]

	temp_=0
	while True:
		temp_+=1
		print("----- New Iteration ------ ",temp_)
		#current time
		start = time.time()
		try:
			populate_FollowList(driver,hashtags)
		except:
			print("ERROR -> populate_FollowList") 
		try:
			populate_PostList(driver,hashtags)
		except:
			print("ERROR -> populate_PostList") 
		try:
			likeComment(driver,comments,5)
		except:
			print("ERROR -> likeComment") 
		try:
			follow(driver,3)
		except:
			print("ERROR -> follow") 
		stop = time.time()
		duration = stop-start
		print("DURATION = ",duration)
		time.sleep(300-duration)
		#sleep(3600-(current_time - prev_current_time))
		#unfollow(driver,node,list_,3)  #10Min -> 3 ACs UNfollow 


start()