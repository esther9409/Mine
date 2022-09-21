from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from random import randint
import os
import re


def crawler_page():
	driver.get(href)
	# time.sleep(randint(2,4))
	soup = BeautifulSoup(driver.page_source,'html.parser') 
	c = open('D:/examtopic/'+service+'_exam/'+folder+'/'+folder+'_page_'+str(num)+'.html','w', encoding="utf-8")
	c.write(soup.prettify())
	c.close()
	question_fin = soup.find_all('div',class_='card-header text-white bg-primary')
	for j in range(len(question_fin)):
		temp1 = question_fin[j].text.split('#')[-1]
		question_fin[j] ='T'+temp1.split('T')[-1].strip()+'_Question_'+temp1.split('T')[0].strip()
	element_fin = soup.find_all('a', class_='btn btn-secondary question-discussion-button d-print-none')
	time.sleep(randint(60,90))
	return question_fin,element_fin

def crawler_discussion():
	qu_num = 0
	for k in element:
		temp = k.get('href')
		if '#' in temp:
			a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
			a.write('page_'+str(num)+'\t'+str(question[qu_num])+'\n')
			a.close()
			print(str(num)+'\n'+exam[p][1]+'\n'+question[qu_num]+'\n'+temp+'\nError\n')
		else:
			try:
				try:
					driver.get('http://www.google.com/search?q=https://www.examtopics.com'+temp)
					time.sleep(randint(5,7))
					soup = BeautifulSoup(driver.page_source,'html.parser')
					link = soup.find(href=re.compile(f'.*webcache.*{temp}.*'))
					href_d = link.get('href')
					driver.get(href_d)
					soup = BeautifulSoup(driver.page_source,'html.parser') 
					b = open('D:/examtopic/'+service+'_exam/'+folder+'/Discussion/'+folder+'_'+str(question[qu_num])+'_discussion.html','w', encoding="utf-8")
					b.write(soup.prettify())
					b.close()
					print(str(num)+'\n'+exam[p][1]+'\n'+question[qu_num]+'\n'+temp+'\nFinish\n')
				except:
					a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
					a.write(question[qu_num]+'\thttps://www.examtopics.com'+temp+'\n')
					a.close()
					print(str(num)+'\n'+exam[p][1]+'\n'+question[qu_num]+'\n'+temp+'\nError\n')
			except:
				a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
				a.write(question[qu_num]+'\thttps://www.examtopics.com'+temp+'\n')
				a.close()
				print(str(num)+'\n'+exam[p][1]+'\n'+question[qu_num]+'\n'+temp+'\nError\n')
			time.sleep(randint(60,90))
		qu_num += 1
	return True


com = 'amazon'
service = 'aws'
exam = []
local_path = 'D:/exam_information/'
a = open(local_path+service+'_exam_information_20220422.txt','r')
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
os.mkdir('D:/examtopic/'+service+'_exam/')
for p in range(0,len(exam)):
# for p in range(13,14):
	num = 1
	folder = exam[p][1]
	os.mkdir('D:/examtopic/'+service+'_exam/'+folder)
	os.mkdir('D:/examtopic/'+service+'_exam/'+folder+'/Discussion')
	source = 'D:/examtopic/'+service+'_exam/'+folder+'/'
	while num <= int(exam[p][2]):
		driver = webdriver.Chrome('chromedriver',options=chrome_options)
		time.sleep(randint(5,7))
		try:
			url = 'https://www.examtopics.com/exams/'+com+'/'+exam[p][0]+'/view/'+str(num)+'/'
			driver.get('http://www.google.com/search?q='+url)
			time.sleep(randint(5,7))
			soup = BeautifulSoup(driver.page_source,'html.parser')
			if num == 1:
				url = '/'.join(url.split('/')[:-2])
				link = soup.find(href=re.compile(f'.*webcache.*{url}.*'))
				href = link.get('href')
				print(href)
			else:
				link = soup.find(href=re.compile(f'.*webcache.*{url}.*'))
				href = link.get('href')
				print(href)
			question,element = crawler_page()
			crawler_discussion()
		except:
			if num == 1:
				a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
				a.write('https://www.examtopics.com/exams/'+com+'/'+exam[p][0]+'/view/\n')
				a.close()			
			else:
				a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
				a.write('https://www.examtopics.com/exams/'+com+'/'+exam[p][0]+'/view/'+str(num)+'/\n')
				a.close()
			time.sleep(randint(60,90))
		driver.quit()
		num += 1