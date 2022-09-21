from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from random import randint
from datetime import date

local_path = 'D:/exam_information/'
com = ['amazon','microsoft','google']
service = ['aws','azure','gcp']
date = date.today().strftime('%Y%m%d')

# for i in range(0,len(com)):
for i in range(0,3):
	a = open(local_path+service[i]+'_exam_information_20220422.txt','r')
	exam = []
	for k in a:
		k = k.strip().split('\t')
		temp = []
		for j in k:
			temp.append(j)
		exam.append(temp)
	a.close()
	chrome_options = Options()
	# chrome_options.add_argument("--headless")
	chrome_options.add_argument("--lang=zh-TW")
	driver = webdriver.Chrome('chromedriver',options=chrome_options)
	driver.get('https://www.examtopics.com/exams/'+com[i]+'/')
	time.sleep(randint(5,7))
	soup = BeautifulSoup(driver.page_source,'html.parser')
	exam_links = soup.find_all('a',class_='popular-exam-link')
	exam_codes = soup.find_all('span',class_='popular-exam-code')
	for k in range(len(exam_links)):
		exam_links[k] = exam_links[k].get('href').split('/')[-2]
		exam_codes[k] = exam_codes[k].text.split(':')[0]
	a = open(local_path+service[i]+'_exam_information_'+date+'.txt','w')
	for k in range(len(exam_links)):
		print(exam_links[k])
		for j in range(len(exam)):
			if exam[j][0] == exam_links[k]:
				driver.get('https://www.examtopics.com/exams/'+com[i]+'/'+exam[j][0]+'/view/')
				time.sleep(randint(5,7))
				soup = BeautifulSoup(driver.page_source,'html.parser')
				temp = soup.find('div',class_='card-text').text.split('of')
				pages = temp[1].split('p')[0].strip()
				questions = temp[-1].split('q')[0].strip()
				if pages != exam[j][2]:
					exam[j][2] = pages
				if questions != exam[j][3]:
					exam[j][3] = questions
				temp = exam_links[k]+'\t'+exam_codes[k]+'\t'+exam[j][2]+'\t'+exam[j][3]
				print(temp)
				a.write(temp+'\n')
				break
		time.sleep(randint(5,7))
	a.close()
	driver.quit()