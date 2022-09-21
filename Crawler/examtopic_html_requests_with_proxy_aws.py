import requests
import time
from bs4 import BeautifulSoup
from random import randint
import os

pass_ip = [
'68.183.56.232',
'3.14.158.1'
]

def get_proxy_ip():
	driver = requests.get('https://www.us-proxy.org/',headers=headers)
	soup = BeautifulSoup(driver.text,'html.parser')
	table = soup.find('table',class_='table table-striped table-bordered')
	table_body = table.find('tbody')
	rows = table_body.find_all('tr')
	data = []
	for row in rows:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		data.append([cols[ele] for ele in range(0,len(cols)) if ele<2])
	proxies_fin = {}
	for ip in range(0,10):
		if data[ip][0] in pass_ip:
			continue
		proxies_temp = {'http':'http://'+data[ip][0]+':'+data[ip][1]}
		try:
			driver = requests.get('http://www.google.com/search?q=test',headers=headers,proxies=proxies_temp,verify=False,timeout=60)
			print(driver.status_code)
			if driver.status_code == 200:
				proxies_fin = {'http':'http://'+data[ip][0]+':'+data[ip][1]}
				print(proxies_fin)
				break
		except:
			print('wrong')
			continue
	if proxies_fin:
		return proxies_fin
	else:
		get_proxy_ip()

def crawler_page():
	# proxies = get_proxy_ip()
	driver = requests.get(href,headers=headers,proxies=proxies,verify=False)
	soup = BeautifulSoup(driver.text,'html.parser') 
	c = open('D:/examtopic/'+service+'_exam/'+folder+'/'+folder+'_page_'+str(num)+'.html','w', encoding="utf-8")
	c.write(soup.prettify())
	c.close()
	question_fin = soup.find_all('div',class_='card-header text-white bg-primary')
	for j in range(len(question_fin)):
		temp1 = question_fin[j].text.split('#')[-1]
		question_fin[j] ='T'+temp1.split('T')[-1].strip()+'_Question_'+temp1.split('T')[0].strip()
	element_fin = soup.find_all('a', class_='btn btn-secondary question-discussion-button d-print-none')
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
				proxies = get_proxy_ip()
				driver = requests.get('http://www.google.com/search?q=https://www.examtopics.com'+temp,headers=headers,proxies=proxies,verify=False)
				print(driver.status_code)
				if driver.status_code == 200:
					soup = BeautifulSoup(driver.text,'html.parser')
					fl = soup.find('a',class_='RBevQb')
					try:
						href_d = fl.get('href')
					except:
						fl = soup.find('a',class_='fl')
						href_d = fl.get('href')
					# proxies = get_proxy_ip()
					driver = requests.get(href_d,headers=headers,proxies=proxies,verify=False)
					soup = BeautifulSoup(driver.text,'html.parser') 
					b = open('D:/examtopic/'+service+'_exam/'+folder+'/Discussion/'+folder+'_'+str(question[qu_num])+'_discussion.html','w', encoding="utf-8")
					b.write(soup.prettify())
					b.close()
					print(str(num)+'\n'+exam[p][1]+'\n'+question[qu_num]+'\n'+temp+'\nFinish\n')
				else:
					a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
					a.write(question[qu_num]+'\thttps://www.examtopics.com/'+temp+'\n')
					a.close()
					print(str(num)+'\n'+exam[p][1]+'\n'+question[qu_num]+'\n'+temp+'\nError\n')
			except:
				a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
				a.write(question[qu_num]+'\thttps://www.examtopics.com/'+temp+'\n')
				a.close()
				print(str(num)+'\n'+exam[p][1]+'\n'+question[qu_num]+'\n'+temp+'\nError\n')
			# time.sleep(randint(60,90))
		qu_num += 1
	return True


com = 'amazon'
service = 'aws'
exam = []
local_path = 'D:/exam_information/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
a = open(local_path+service+'_exam_information_20220110.txt','r')
for k in a:
	k = k.strip().split('\t')
	temp = []
	for j in k:
		temp.append(j)
	exam.append(temp)
a.close()

os.mkdir('D:/examtopic/'+service+'_exam/')
for p in range(0,len(exam)):
# for p in range(2,3):
	num = 1
	folder = exam[p][1]
	os.mkdir('D:/examtopic/'+service+'_exam/'+folder)
	os.mkdir('D:/examtopic/'+service+'_exam/'+folder+'/Discussion')
	source = 'D:/examtopic/'+service+'_exam/'+folder+'/'
	while num <= int(exam[p][2]):
		try:
			url = 'http://www.google.com/search?q=https://www.examtopics.com/exams/'+com+'/'+exam[p][0]+'/view/'+str(num)+'/'
			proxies = get_proxy_ip()
			driver = requests.get(url,headers=headers,proxies=proxies,verify=False)
			print(driver.status_code)
			soup = BeautifulSoup(driver.text,'html.parser')
			fl = soup.find('a',class_='RBevQb')
			try:
				href = fl.get('href')
			except:
				fl = soup.find('a',class_='fl')
				href = fl.get('href')
			print(href)
			if num == 1:
				if (exam[p][0]+'/view/') in href and 'webcache' in href:
					question,element = crawler_page()
					crawler_discussion()
				else:
					a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
					a.write('https://www.examtopics.com/exams/'+com+'/'+exam[p][0]+'/view/'+str(num)+'/\n')
					a.close()
					# time.sleep(randint(60,90))
			else:
				if (exam[p][0]+'/view/'+str(num)+'/') in href and 'webcache' in href:
					question,element = crawler_page()
					crawler_discussion()
				else:
					a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
					a.write('https://www.examtopics.com/exams/'+com+'/'+exam[p][0]+'/view/'+str(num)+'/\n')
					a.close()
					# time.sleep(randint(60,90))
		except:
			a = open('D:/examtopic/'+service+'_exam/'+folder+'_error.txt','a')
			a.write('https://www.examtopics.com/exams/'+com+'/'+exam[p][0]+'/view/'+str(num)+'/\n')
			a.close()
			# time.sleep(randint(60,90))
		num += 1