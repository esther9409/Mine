import requests
import urllib
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import gc
import re
import time

a = open('20190422\\number_allele_specific_ml.txt','r')
e = open('20190422\\number_allele_specific_dl.txt','r')

ml_allele = []
dl_allele = []
for every in a:
	every = every.split('\t')
	ml_allele.append(every[0])
	gc.collect()
a.close()
for every in e:
	every = every.split('\t')
	dl_allele.append(every[0])
	gc.collect()
e.close()

model = ['ANN 4.0','SMMPMBEC','SMM','PickPocket','netMHCcons','NetMHCpan BA 4.0']
headers = {
'User-Agent': 'Chrome/79.0.3945.79',
}
number = 0
r = requests.Session()
url = 'http://www.cbs.dtu.dk/cgi-bin/webface2.fcgi'
# for num in range(7,14):
# #	bb = '20190422\\dl\Testing\\normalization\\' + dl_allele[num] + '_Testing_normalization.txt'
# 	bb = '20190422\\dl\Testing\other_model\\ANN 4.0\\' + dl_allele[num] + '_Testing_ANN 4.0_wrong.txt'
# 	bb = bb.replace(':','_')
# 	bb = bb.replace('*','_')
# 	b = open(bb,'r')
# 	number_2 = 0
# 	for j in b:
# 		number_2 += 1
# 		if number_2 >= 0:
# 			number += 1
# 			jj = j.split('\t')
# 			cc = '20190422\\dl\Testing\other_model\\ANN 4.0\\' + dl_allele[num] + '_Testing_ANN 4.0_result.txt'
# 			cc = cc.replace(':','_')
# 			cc = cc.replace('*','_')
# 			c = open(cc,'a')
# 			dd = '20190422\\dl\Testing\other_model\\ANN 4.0\\' + dl_allele[num] + '_Testing_ANN 4.0_wrong_2.txt'
# 			dd = dd.replace(':','_')
# 			dd = dd.replace('*','_')
# 			d = open(dd,'a')
# 			print(dl_allele[num])
# 			print(number_2)
# 			if jj[1] == 'H2-Db' or jj[1] == 'H2-Kb':
# 				mhc = jj[1].replace('H2','H-2')
# 				form = {
# 				'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 				'inp': '1',
# 				'PEPPASTE': jj[2],
# 				'master': str(len(jj[2])),
# 				'slave0': mhc,
# 				'allele': mhc,
# 				'thrs': '0.5',
# 				'thrw': '2'
# 				}
# 			else:
# 				mhc = jj[1].replace(':','')
# 				mhc = mhc.replace('*','') 
# 				form = {
# 				'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 				'inp': '1',
# 				'PEPPASTE': jj[2],
# 				'master': str(len(jj[2])),
# 				'slave0': mhc,
# 				'allele': mhc,
# 				'thrs': '0.5',
# 				'thrw': '2'
# 				}
# 			r1 = r.post(url,data=form,headers=headers)
# 			print(r1.status_code)
# 			r2 = r1.text
# 			soup = BeautifulSoup(r2, 'html.parser')
# 			jobid = soup.title
# 			jobid = jobid.get_text().split(' ')
# 			print(jobid[-1])
# 			time.sleep(5)
# 			url_result = 'http://www.cbs.dtu.dk/cgi-bin/webface2.fcgi?jobid='+jobid[-1]+'&wait=20'
# 			r1 = r.get(url_result,headers=headers)
# 			print(r1.status_code)
# 			soup = BeautifulSoup(r1.text, 'html.parser')
# 			try:
# 				result = soup.find('pre')
# 				result = result.get_text().split('-----------------------------------------------------------------------------------')
# 				i = result[2].split(' ')
# 				temp = []
# 				for k in i:
# 					if k != '':
# 						temp.append(k)
# 				del temp[0]
# 				temp = '\t'.join(temp)
# 				temp = temp.strip('\n')
# 				print(temp)
# 				c.write(jj[0]+'\t'+temp+'\t'+str(len(jj[2]))+'\n')
# 			except:
# 				print('error')
# 				print('length '+str(len(jj[2])))
# 				d.write(jj[0])
# 				d.write('\t')
# 				d.write(jj[1])
# 				d.write('\t')
# 				d.write(jj[2])
# 				d.write('\t')
# 				d.write('error')
# 				d.write('\t'+str(len(jj[2])))
# 				d.write('\n')
# 			c.close()
# 			d.close()
# #			if number <= 20:
# #				time.sleep(3)
# #			else:
# #				time.sleep(60)
# #				number = 0
# 	b.close()
	
# for num in range(0,1):
# 	bb = '20190422\\ml\\Testing_3\\normalization\\' + ml_allele[num] + '_Testing_normalization.txt'
# 	bb = bb.replace(':','_')
# 	bb = bb.replace('*','_')
# 	b = open(bb,'r')
# 	number_2 = 0
# 	for j in b:
# 		number_2 += 1
# 		if number_2 >= 0:
# 			number += 1
# 			jj = j.split('\t')
# 			cc = '20190422\\ml\\Testing_3\\other_model\\ANN 4.0\\' + ml_allele[num] + '_Testing_ANN 4.0_result.txt'
# 			cc = cc.replace(':','_')
# 			cc = cc.replace('*','_')
# 			c = open(cc,'a')
# 			dd = '20190422\\ml\\Testing_3\\other_model\\ANN 4.0\\' + ml_allele[num] + '_Testing_ANN 4.0_wrong.txt'
# 			dd = dd.replace(':','_')
# 			dd = dd.replace('*','_')
# 			d = open(dd,'a')
# 			print(ml_allele[num])
# 			print(number_2)
# 			if jj[1] == 'H2-Kd':
# 				mhc = jj[1].replace('H2','H-2')
# 				form = {
# 				'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 				'inp': '1',
# 				'PEPPASTE': jj[2],
# 				'master': str(len(jj[2])),
# 				'slave0': mhc,
# 				'allele': mhc,
# 				'thrs': '0.5',
# 				'thrw': '2'
# 				}
# 			elif jj[1] == 'Mamu-A1*001:01' or jj[1] == 'Mamu-A1*011:01' or jj[1] == 'Mamu-B*017:04':
# 				if jj[1] == 'Mamu-A1*001:01':
# 					mhc = 'Mamu-A01'
# 				elif jj[1] == 'Mamu-A1*011:01':
# 					mhc = 'Mamu-A11'
# 				elif jj[1] == 'Mamu-B*017:04':
# 					mhc = 'Mamu-B17'
# 				form = {
# 				'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 				'inp': '1',
# 				'PEPPASTE': jj[2],
# 				'master': str(len(jj[2])),
# 				'slave0': mhc,
# 				'allele': mhc,
# 				'thrs': '0.5',
# 				'thrw': '2'
# 				}
# 			else:
# 				mhc = jj[1].replace(':','')
# 				mhc = mhc.replace('*','') 
# 				form = {
# 				'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 				'inp': '1',
# 				'PEPPASTE': jj[2],
# 				'master': str(len(jj[2])),
# 				'slave0': mhc,
# 				'allele': mhc,
# 				'thrs': '0.5',
# 				'thrw': '2'
# 				}
# 			r1 = r.post(url,data=form,headers=headers)
# 			print(r1.status_code)
# 			r2 = r1.text
# 			soup = BeautifulSoup(r2, 'html.parser')
# 			jobid = soup.title
# 			jobid = jobid.get_text().split(' ')
# 			print(jobid[-1])
# 			time.sleep(5)
# 			url_result = 'http://www.cbs.dtu.dk/cgi-bin/webface2.fcgi?jobid='+jobid[-1]+'&wait=20'
# 			r1 = r.get(url_result,headers=headers)
# 			print(r1.status_code)
# 			soup = BeautifulSoup(r1.text, 'html.parser')
# 			try:
# 				result = soup.find('pre')
# 				result = result.get_text().split('-----------------------------------------------------------------------------------')
# 				i = result[2].split(' ')
# 				temp = []
# 				for k in i:
# 					if k != '':
# 						temp.append(k)
# 				del temp[0]
# 				temp = '\t'.join(temp)
# 				temp = temp.strip('\n')
# 				print(temp)
# 				c.write(jj[0]+'\t'+temp+'\t'+str(len(jj[2]))+'\n')
# 			except:
# 				print('error')
# 				print('length '+str(len(jj[2])))
# 				d.write(jj[0])
# 				d.write('\t')
# 				d.write(jj[1])
# 				d.write('\t')
# 				d.write(jj[2])
# 				d.write('\t')
# 				d.write('error')
# 				d.write('\t'+str(len(jj[2])))
# 				d.write('\n')
# 			c.close()
# 			d.close()
# 			if number <= 20:
# 				time.sleep(3)
# 			else:
# 				time.sleep(60)
# 				number = 0
# 	b.close()

# bb = '20190422\\dl\Testing\\normalization\\MHC_pan_allele_Testing_normalization.txt'
# bb = bb.replace(':','_')
# bb = bb.replace('*','_')
# b = open(bb,'r')
# number_2 = 0
# for j in b:
# 	number_2 += 1
# 	if number_2 >= 380:
# 		number += 1
# 		jj = j.split('\t')
# 		catch = re.compile(r'BF.*')
# 		ans = catch.findall(jj[1])
# 		catch_2 = re.compile(r'BoLA.*')
# 		ans_2 = catch_2.findall(jj[1])
# 		catch_3 = re.compile(r'DLA.*')
# 		ans_3 = catch_3.findall(jj[1])
# 		catch_4 = re.compile(r'Eqca.*')
# 		ans_4 = catch_4.findall(jj[1])
# 		catch_5 = re.compile(r'H2.*')
# 		ans_5 = catch_5.findall(jj[1])
# 		catch_6 = re.compile(r'Mamu.*')
# 		ans_6 = catch_6.findall(jj[1])
# 		catch_7 = re.compile(r'Patr.*')
# 		ans_7 = catch_7.findall(jj[1])
# 		catch_8 = re.compile(r'SLA.*')
# 		ans_8 = catch_8.findall(jj[1])
# 		cc = '20190422\\dl\Testing\other_model\\ANN 4.0\\MHC_pan_allele_Testing_ANN 4.0_result.txt'
# 		cc = cc.replace(':','_')
# 		cc = cc.replace('*','_')
# 		c = open(cc,'a')
# 		dd = '20190422\\dl\Testing\other_model\\ANN 4.0\\MHC_pan_allele_Testing_ANN 4.0_wrong.txt'
# 		dd = dd.replace(':','_')
# 		dd = dd.replace('*','_')
# 		d = open(dd,'a')
# 		print(dl_allele[num])
# 		print(number_2)
# 		if ans:
# 			mhc = jj[1]
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif ans_2:
# 			mhc = jj[1]
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif jj[1] == 'Caja-E':
# 			mhc = jj[1]
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif ans_3:
# 			mhc = jj[1]
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif ans_4:
# 			mhc = jj[1]
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif jj[1] == 'FLA-E*01801':
# 			mhc = jj[1]
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif ans_5:
# 			mhc = jj[1].replace('H2','H-2')
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif ans_6:
# 			if jj[1] == 'Mamu-A1*002:01':
# 				mhc = 'Mamu-A02'
# 			elif jj[1] == 'Mamu-B*001:01':
# 				mhc = 'Mamu-B01'
# 			elif jj[1] == 'Mamu-B*003:01':
# 				mhc = 'Mamu-B03'
# 			elif jj[1] == 'Mamu-B*004:01':
# 				mhc = 'Mamu-B04'
# 			elif jj[1] == 'Mamu-B*065:02':
# 				mhc = 'Mamu-B65'
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif jj[1] == 'mouse CD1d':
# 			mhc = jj[1]
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif ans_7:
# 			mhc = jj[1].replace(':','')
# 			mhc = mhc.replace('*','') 
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif jj[1] == 'RT1-Aa':
# 			mhc = jj[1]
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		elif ans_8:
# 			mhc = jj[1].replace(':','')
# 			mhc = mhc.replace('*','') 
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		else:
# 			mhc = jj[1].replace(':','')
# 			mhc = mhc.replace('*','') 
# 			form = {
# 			'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
# 			'inp': '1',
# 			'PEPPASTE': jj[2],
# 			'master': str(len(jj[2])),
# 			'slave0': mhc,
# 			'allele': mhc,
# 			'thrs': '0.5',
# 			'thrw': '2'
# 			}
# 		r1 = r.post(url,data=form,headers=headers)
# 		print(r1.status_code)
# 		r2 = r1.text
# 		soup = BeautifulSoup(r2, 'html.parser')
# 		jobid = soup.title
# 		jobid = jobid.get_text().split(' ')
# 		print(jobid[-1])
# 		time.sleep(5)
# 		url_result = 'http://www.cbs.dtu.dk/cgi-bin/webface2.fcgi?jobid='+jobid[-1]+'&wait=20'
# 		r1 = r.get(url_result,headers=headers)
# 		print(r1.status_code)
# 		soup = BeautifulSoup(r1.text, 'html.parser')
# 		try:
# 			result = soup.find('pre')
# 			result = result.get_text().split('-----------------------------------------------------------------------------------')
# 			i = result[2].split(' ')
# 			temp = []
# 			for k in i:
# 				if k != '':
# 					temp.append(k)
# 			del temp[0]
# 			temp = '\t'.join(temp)
# 			temp = temp.strip('\n')
# 			print(temp)
# 			c.write(jj[0]+'\t'+temp+'\t'+str(len(jj[2]))+'\n')
# 		except:
# 			print('error')
# 			print('length '+str(len(jj[2])))
# 			d.write(jj[0])
# 			d.write('\t')
# 			d.write(jj[1])
# 			d.write('\t')
# 			d.write(jj[2])
# 			d.write('\t')
# 			d.write('error')
# 			d.write('\t'+str(len(jj[2])))
# 			d.write('\n')
# 		c.close()
# 		d.close()
# 		if number <= 20:
# 			time.sleep(3)
# 		else:
# 			time.sleep(60)
# 			number = 0
# b.close()

bb = '20190422\\case_study\\case_study.txt'
b = open(bb,'r')
number_2 = 0
for j in b:
	number_2 += 1
	if number_2 >= 0:
		number += 1
		jj = j.split('\t')
		cc = '20190422\\case_study\\case_study_ANN 4.0_result.txt'
		c = open(cc,'a')
		dd = '20190422\\case_study\\case_study_ANN 4.0_wrong.txt'
		d = open(dd,'a')
		print(jj[0])
		print(number_2)
		mhc = jj[0].replace(':','')
		mhc = mhc.replace('*','') 
		form = {
		'configfile': '/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
		'inp': '1',
		'PEPPASTE': jj[1],
		'master': str(len(jj[1])),
		'slave0': mhc,
		'allele': mhc,
		'thrs': '0.5',
		'thrw': '2'
		}
		r1 = r.post(url,data=form,headers=headers)
		print(r1.status_code)
		r2 = r1.text
		soup = BeautifulSoup(r2, 'html.parser')
		jobid = soup.title
		jobid = jobid.get_text().split(' ')
		print(jobid[-1])
		time.sleep(5)
		url_result = 'http://www.cbs.dtu.dk/cgi-bin/webface2.fcgi?jobid='+jobid[-1]+'&wait=20'
		r1 = r.get(url_result,headers=headers)
		print(r1.status_code)
		soup = BeautifulSoup(r1.text, 'html.parser')
		try:
			result = soup.find('pre')
			result = result.get_text().split('-----------------------------------------------------------------------------------')
			i = result[2].split(' ')
			temp = []
			for k in i:
				if k != '':
					temp.append(k)
			del temp[0]
			temp = '\t'.join(temp)
			temp = temp.strip('\n')
			print(temp)
			c.write(jj[2]+'\t'+temp+'\t'+str(len(jj[1]))+'\n')
		except:
			print('error')
			print('length '+str(len(jj[1])))
			d.write(jj[0])
			d.write('\t')
			d.write(jj[1])
			d.write('\t')
			d.write(jj[2])
			d.write('\t')
			d.write('error')
			d.write('\t'+str(len(jj[1])))
			d.write('\n')
		c.close()
		d.close()
#		if number <= 20:
#			time.sleep(3)
#		else:
#			time.sleep(60)
#			number = 0
b.close()