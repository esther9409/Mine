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
model_num = {
'ANN 4.0':'4',
'SMMPMBEC':'5',
'SMM':'6',
'PickPocket':'9',
'netMHCcons':'10',
'NetMHCpan BA 4.0':'34'
}
headers = {
'User-Agent': 'Chrome/78.0.3904.108',
'Accept-Encoding': 'gzip, deflate',
}
number = 0
r = requests.Session()
url = 'http://tools.iedb.org/mhci/'
url_result = 'http://tools.iedb.org/mhci/result/'
url_result_2 = 'http://tools.iedb.org/mhci/result_in_csv/'
for num in range(18,28):
	for num_2 in range(2,3):
		bb = '20190422\\ml\Testing_3\other_model\\' + model[num_2]+ '\\' + ml_allele[num] + '_Testing_' + model[num_2] + '_wrong.txt'
		bb = bb.replace(':','_')
		bb = bb.replace('*','_')
		b = open(bb,'r')
		number_2 = 0
		for j in b:
			number += 1
			number_2 += 1
			jj = j.split('\t')
			cc = '20190422\\ml\Testing_3\other_model\\' + model[num_2]+ '\\' + ml_allele[num] + '_Testing_' + model[num_2] + '_result.txt'
			cc = cc.replace(':','_')
			cc = cc.replace('*','_')
			c = open(cc,'a')
			dd = '20190422\\ml\Testing_3\other_model\\' + model[num_2]+ '\\' + ml_allele[num] + '_Testing_' + model[num_2] + '_wrong_2.txt'
			dd = dd.replace(':','_')
			dd = dd.replace('*','_')
			d = open(dd,'a')
			print(ml_allele[num])
			print(model[num_2]+' '+model_num[model[num_2]])
			print(number_2)
			r1 = r.get(url,headers=headers)
			r2 = r1.cookies['csrftoken']
			if jj[1] == 'H2-Kd':
				mhc = jj[1].replace('H2','H-2')
				form = {
				'csrfmiddlewaretoken':r2,
				'source':'html',
				'pred_tool':'mhci',
				'version':'20130222',
				'sequence_text': jj[2],
				'method': model_num[model[num_2]],
				'species_list':'mouse',
				'freq':'freq',
				'allele':mhc,
				'length': str(len(jj[2])),
				'species':'mouse',
				'sort_output':'MHC_IC50',
				'output_format':'xhtml',
				'submit':'Submit'
				}
			elif jj[1] == 'Mamu-A1*001:01' or jj[1] == 'Mamu-A1*011:01' or jj[1] == 'Mamu-B*017:04':
				mhc = jj[1].replace(':','')
				form = {
				'csrfmiddlewaretoken':r2,
				'source':'html',
				'pred_tool':'mhci',
				'version':'20130222',
				'sequence_text': jj[2],
				'method': model_num[model[num_2]],
				'species_list':'macaque',
				'freq':'freq',
				'allele':mhc,
				'length':str(len(jj[2])),
				'species':'macaque',
				'sort_output':'MHC_IC50',
				'output_format':'xhtml',
				'submit':'Submit'
				}
			else:
				mhc = jj[1]
				form = {
				'csrfmiddlewaretoken':r2,
				'source':'html',
				'pred_tool':'mhci',
				'version':'20130222',
				'sequence_text': jj[2],
				'method': model_num[model[num_2]],
				'species_list':'human',
				'freq':'freq',
				'allele':mhc,
				'length':str(len(jj[2])),
				'species':'human',
				'sort_output':'MHC_IC50',
				'output_format':'xhtml',
				'submit':'Submit'
				}
			r1 = r.post(url,data=form,headers=headers)
			print(r1.status_code)
			r1 = r.get(url_result,headers=headers)
			print(r1.status_code)
			if r1.status_code == 200:
				r3 = r1.text
				soup = BeautifulSoup(r3, 'html.parser')
				result = soup.find(id='result_table')
				table = result.find('tr',class_='odd_row')
				output = []
				output.append(jj[0])
				for i in table.find_all('td'):
					output.append(i.get_text().strip('\n'))
				if output[1] == mhc and output[6] == jj[2]:
					output =	' '.join(output)
					c.write(output+'\n')
				else:
					print('form wrong')
					print('length '+str(len(jj[2])))
					d.write(jj[0])
					d.write('\t')
					d.write(jj[1])
					d.write('\t')
					d.write(jj[2])
					d.write('\t')
					d.write('form wrong')
					d.write('\t'+str(len(jj[2])))
					d.write('\n')
			else:
				print('form wrong')
				print('length '+str(len(jj[2])))
				d.write(jj[0])
				d.write('\t')
				d.write(jj[1])
				d.write('\t')
				d.write(jj[2])
				d.write('\t')
				d.write('form wrong')
				d.write('\t'+str(len(jj[2])))
				d.write('\n')
			c.close()
			d.close()
			if number <= 20:
				time.sleep(5)
			else:
				time.sleep(60)
				number = 0
		b.close()

'''for num in range(0,18):
	for num_2 in range(0,1):
		bb = '20190422\\dl\Testing\Testing\\normalization\\' + dl_allele[num] + '_Testing_normalization.txt'
		bb = bb.replace(':','_')
		bb = bb.replace('*','_')
		b = open(bb,'r')
		number_2 = 0
		for j in b:
			number += 1
			number_2 += 1
			jj = j.split('\t')
			cc = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\' + dl_allele[num] + '_Testing_' + model[num_2] + '_result_2.txt'
			cc = cc.replace(':','_')
			cc = cc.replace('*','_')
			c = open(cc,'a')
			dd = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\' + dl_allele[num] + '_Testing_' + model[num_2] + '_wrong.txt'
			dd = dd.replace(':','_')
			dd = dd.replace('*','_')
			d = open(dd,'a')
			print(dl_allele[num])
			print(model[num_2]+' '+model_num[model[num_2]])
			print(number_2)
			r1 = r.get(url,headers=headers)
			r2 = r1.cookies['csrftoken']
			if jj[1] == 'H2-Db' or jj[1] == 'H2-Kb':
				mhc = jj[1].replace('H2','H-2')
				form = {
				'csrfmiddlewaretoken':r2,
				'source':'html',
				'pred_tool':'mhci',
				'version':'20130222',
				'sequence_text': jj[2],
				'method': model_num[model[num_2]],
				'species_list':'mouse',
				'freq':'freq',
				'allele':mhc,
				'length': str(len(jj[2])),
				'species':'mouse',
				'sort_output':'MHC_IC50',
				'output_format':'xhtml',
				'submit':'Submit'
				}
			else:
				mhc = jj[1]
				form = {
				'csrfmiddlewaretoken':r2,
				'source':'html',
				'pred_tool':'mhci',
				'version':'20130222',
				'sequence_text': jj[2],
				'method': model_num[model[num_2]],
				'species_list':'human',
				'freq':'freq',
				'allele':mhc,
				'length':str(len(jj[2])),
				'species':'human',
				'sort_output':'MHC_IC50',
				'output_format':'xhtml',
				'submit':'Submit'
				}
			r1 = r.post(url,data=form,headers=headers)
			print(r1.status_code)
			r1 = r.get(url_result,headers=headers)
			print(r1.status_code)
			if r1.status_code == 200:
				r3 = r1.text
				soup = BeautifulSoup(r3, 'html.parser')
				result = soup.find(id='result_table')
				table = result.find('tr',class_='odd_row')
				output = []
				output.append(jj[0])
				for i in table.find_all('td'):
					output.append(i.get_text().strip('\n'))
				if output[1] == mhc and output[6] == jj[2]:
					output = ' '.join(output)
					c.write(output+'\n')
				else:
					print('form wrong')
					print('length '+str(len(jj[2])))
					d.write(jj[0])
					d.write('\t')
					d.write(jj[1])
					d.write('\t')
					d.write(jj[2])
					d.write('\t')
					d.write('form wrong')
					d.write('\t'+str(len(jj[2])))
					d.write('\n')
			else:
				print('form wrong')
				print('length '+str(len(jj[2])))
				d.write(jj[0])
				d.write('\t')
				d.write(jj[1])
				d.write('\t')
				d.write(jj[2])
				d.write('\t')
				d.write('form wrong')
				d.write('\t'+str(len(jj[2])))
				d.write('\n')
			c.close()
			d.close()
			if number <= 20:
				time.sleep(3)
			else:
				time.sleep(60)
				number = 0
		b.close()'''

'''for num in range(0,18):
	for num_2 in range(0,1):
		bb = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\' + dl_allele[num] + '_Testing_' + model[num_2] + '_wrong_3.txt'
		bb = bb.replace(':','_')
		bb = bb.replace('*','_')
		b = open(bb,'r')
		number_2 = 0
		for j in b:
			number += 1
			number_2 += 1
			jj = j.split('\t')
			cc = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\' + dl_allele[num] + '_Testing_' + model[num_2] + '_result_2.txt'
			cc = cc.replace(':','_')
			cc = cc.replace('*','_')
			c = open(cc,'a')
			dd = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\' + dl_allele[num] + '_Testing_' + model[num_2] + '_wrong_4.txt'
			dd = dd.replace(':','_')
			dd = dd.replace('*','_')
			d = open(dd,'a')
			print(dl_allele[num])
			print(model[num_2]+' '+model_num[model[num_2]])
			print(number_2)
			r1 = r.get(url,headers=headers)
			r2 = r1.cookies['csrftoken']
			if jj[1] == 'H2-Db' or jj[1] == 'H2-Kb':
				mhc = jj[1].replace('H2','H-2')
				form = {
				'csrfmiddlewaretoken':r2,
				'source':'html',
				'pred_tool':'mhci',
				'version':'20130222',
				'sequence_text': jj[2],
				'method': model_num[model[num_2]],
				'species_list':'mouse',
				'freq':'freq',
				'allele':mhc,
				'length': str(len(jj[2])),
				'species':'mouse',
				'sort_output':'MHC_IC50',
				'output_format':'xhtml',
				'submit':'Submit'
				}
			else:
				mhc = jj[1]
				form = {
				'csrfmiddlewaretoken':r2,
				'source':'html',
				'pred_tool':'mhci',
				'version':'20130222',
				'sequence_text': jj[2],
				'method': model_num[model[num_2]],
				'species_list':'human',
				'freq':'freq',
				'allele':mhc,
				'length':str(len(jj[2])),
				'species':'human',
				'sort_output':'MHC_IC50',
				'output_format':'xhtml',
				'submit':'Submit'
				}
			r1 = r.post(url,data=form,headers=headers)
			print(r1.status_code)
			r1 = r.get(url_result,headers=headers)
			print(r1.status_code)
			if r1.status_code == 200:
				r3 = r1.text
				soup = BeautifulSoup(r3, 'html.parser')
				result = soup.find(id='result_table')
				table = result.find('tr',class_='odd_row')
				output = []
				output.append(jj[0])
				for i in table.find_all('td'):
					output.append(i.get_text().strip('\n'))
				if output[1] == mhc and output[6] == jj[2]:
					output =	' '.join(output)
					c.write(output+'\n')
				else:
					print('form wrong')
					print('length '+str(len(jj[2])))
					d.write(jj[0])
					d.write('\t')
					d.write(jj[1])
					d.write('\t')
					d.write(jj[2])
					d.write('\t')
					d.write('form wrong')
					d.write('\t'+str(len(jj[2])))
					d.write('\n')
			else:
				print('form wrong')
				print('length '+str(len(jj[2])))
				d.write(jj[0])
				d.write('\t')
				d.write(jj[1])
				d.write('\t')
				d.write(jj[2])
				d.write('\t')
				d.write('form wrong')
				d.write('\t'+str(len(jj[2])))
				d.write('\n')
			c.close()
			d.close()
			if number <= 20:
				time.sleep(3)
			else:
				time.sleep(60)
				number = 0
		b.close()'''

'''number_2 = 0
bb = '20190422\\dl\Testing\\normalization\\MHC_pan_allele_Testing_normalization.txt'
bb = bb.replace(':','_')
bb = bb.replace('*','_')
b = open(bb,'r')
if number_2 >= 0:
	for j in b:
		number += 1
		number_2 += 1
		jj = j.split('\t')
		catch = re.compile(r'BF.*')
		ans = catch.findall(jj[1])
		catch_2 = re.compile(r'BoLA.*')
		ans_2 = catch_2.findall(jj[1])
		catch_3 = re.compile(r'DLA.*')
		ans_3 = catch_3.findall(jj[1])
		catch_4 = re.compile(r'Eqca.*')
		ans_4 = catch_4.findall(jj[1])
		catch_5 = re.compile(r'H2.*')
		ans_5 = catch_5.findall(jj[1])
		catch_6 = re.compile(r'Mamu.*')
		ans_6 = catch_6.findall(jj[1])
		catch_7 = re.compile(r'Patr.*')
		ans_7 = catch_7.findall(jj[1])
		catch_8 = re.compile(r'SLA.*')
		ans_8 = catch_8.findall(jj[1])
		cc = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\' + dl_allele[num] + '_Testing_' + model[num_2] + '_result_2.txt'
		cc = cc.replace(':','_')
		cc = cc.replace('*','_')
		c = open(cc,'a')
		dd = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\' + dl_allele[num] + '_Testing_' + model[num_2] + '_wrong_4.txt'
		dd = dd.replace(':','_')
		dd = dd.replace('*','_')
		d = open(dd,'a')
		print(dl_allele[num])
		print(model[num_2]+' '+model_num[model[num_2]])
		print(number_2)
		r1 = r.get(url,headers=headers)
		r2 = r1.cookies['csrftoken']
		if ans:
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'chicken'
			form['species'] = 'chicken'
		elif ans_2:
			mhc = jj[1].replace('*',':')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'cow'
			form['species'] = 'cow'
		elif jj[1] == 'Caja-E':
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'marmoset'
			form['species'] = 'marmoset'
		elif ans_3:
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'dog'
			form['species'] = 'dog'
		elif ans_4:
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'horse'
			form['species'] = 'horse'
		elif jj[1] == 'FLA-E*01801':
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'cat'
			form['species'] = 'cat'
		elif ans_5:
			mhc = jj[1].replace('H2','H-2')
			mhc = mhc.replace('H-2-Q1','H-2-Qa1')
			mhc = mhc.replace('H-2-Q2','H-2-Qa2')
			mhc = mhc.replace('H-2-Q9','H-2-Qa9')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'mouse'
			form['species'] = 'mouse'
		elif ans_6:
			mhc = jj[1].replace('*',':')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'macaque'
			form['species'] = 'macaque'
		elif jj[1] == 'mouse CD1d':
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'mouse'
			form['species'] = 'mouse'
		elif ans_7:
			mhc = jj[1].replace('*',':')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'chimpanzee'
			form['species'] = 'chimpanzee'
		elif jj[1] == 'RT1-Aa':
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'rat'
			form['species'] = 'rat'
		elif ans_8:
			mhc = jj[1].replace('*',':')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'pig'
			form['species'] = 'pig'
		else:
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'human',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'human',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
		r1 = r.post(url,data=form,headers=headers)
		print(r1.status_code)
		r1 = r.get(url_result,headers=headers)
		print(r1.status_code)
		if r1.status_code == 200:
			r3 = r1.text
			soup = BeautifulSoup(r3, 'html.parser')
			result = soup.find(id='result_table')
			table = result.find('tr',class_='odd_row')
			output = []
			output.append(jj[0])
			for i in table.find_all('td'):
				output.append(i.get_text().strip('\n'))
			if output[1] == mhc and output[6] == jj[2]:
				output =	' '.join(output)
				c.write(output+'\n')
			else:
				print('form wrong')
				print('length '+str(len(jj[2])))
				d.write(jj[0])
				d.write('\t')
				d.write(jj[1])
				d.write('\t')
				d.write(jj[2])
				d.write('\t')
				d.write('form wrong')
				d.write('\t'+str(len(jj[2])))
				d.write('\n')
		else:
			print('form wrong')
			print('length '+str(len(jj[2])))
			d.write(jj[0])
			d.write('\t')
			d.write(jj[1])
			d.write('\t')
			d.write(jj[2])
			d.write('\t')
			d.write('form wrong')
			d.write('\t'+str(len(jj[2])))
			d.write('\n')
		c.close()
		d.close()
		if number <= 20:
			time.sleep(3)
		else:
			time.sleep(60)
			number = 0
	b.close()'''

'''number_2 = 0
bb = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\MHC_pan_allele_Testing_' + model[num_2] + '_wrong.txt'
bb = bb.replace(':','_')
bb = bb.replace('*','_')
b = open(bb,'r')
if number_2 >= 0:
	for j in b:
		number += 1
		number_2 += 1
		jj = j.split('\t')
		catch = re.compile(r'BF.*')
		ans = catch.findall(jj[1])
		catch_2 = re.compile(r'BoLA.*')
		ans_2 = catch_2.findall(jj[1])
		catch_3 = re.compile(r'DLA.*')
		ans_3 = catch_3.findall(jj[1])
		catch_4 = re.compile(r'Eqca.*')
		ans_4 = catch_4.findall(jj[1])
		catch_5 = re.compile(r'H2.*')
		ans_5 = catch_5.findall(jj[1])
		catch_6 = re.compile(r'Mamu.*')
		ans_6 = catch_6.findall(jj[1])
		catch_7 = re.compile(r'Patr.*')
		ans_7 = catch_7.findall(jj[1])
		catch_8 = re.compile(r'SLA.*')
		ans_8 = catch_8.findall(jj[1])
		cc = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\' + dl_allele[num] + '_Testing_' + model[num_2] + '_result_2.txt'
		cc = cc.replace(':','_')
		cc = cc.replace('*','_')
		c = open(cc,'a')
		dd = '20190422\\dl\Testing\other_model\\' + model[num_2]+ '\\' + dl_allele[num] + '_Testing_' + model[num_2] + '_wrong_2.txt'
		dd = dd.replace(':','_')
		dd = dd.replace('*','_')
		d = open(dd,'a')
		print(dl_allele[num])
		print(model[num_2]+' '+model_num[model[num_2]])
		print(number_2)
		r1 = r.get(url,headers=headers)
		r2 = r1.cookies['csrftoken']
		if ans:
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'chicken'
			form['species'] = 'chicken'
		elif ans_2:
			mhc = jj[1].replace('*',':')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'cow'
			form['species'] = 'cow'
		elif jj[1] == 'Caja-E':
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'marmoset'
			form['species'] = 'marmoset'
		elif ans_3:
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'dog'
			form['species'] = 'dog'
		elif ans_4:
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'horse'
			form['species'] = 'horse'
		elif jj[1] == 'FLA-E*01801':
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'cat'
			form['species'] = 'cat'
		elif ans_5:
			mhc = jj[1].replace('H2','H-2')
			mhc = mhc.replace('H-2-Q1','H-2-Qa1')
			mhc = mhc.replace('H-2-Q2','H-2-Qa2')
			mhc = mhc.replace('H-2-Q9','H-2-Qa9')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'mouse'
			form['species'] = 'mouse'
		elif ans_6:
			mhc = jj[1].replace('*',':')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'macaque'
			form['species'] = 'macaque'
		elif jj[1] == 'mouse CD1d':
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'mouse'
			form['species'] = 'mouse'
		elif ans_7:
			mhc = jj[1].replace('*',':')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'chimpanzee'
			form['species'] = 'chimpanzee'
		elif jj[1] == 'RT1-Aa':
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'rat'
			form['species'] = 'rat'
		elif ans_8:
			mhc = jj[1].replace('*',':')
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
			form['species_list'] = 'pig'
			form['species'] = 'pig'
		else:
			mhc = jj[1]
			form = {
			'csrfmiddlewaretoken':r2,
			'source':'html',
			'pred_tool':'mhci',
			'version':'20130222',
			'sequence_text': jj[2],
			'method': model_num[model[num_2]],
			'species_list':'human',
			'freq':'freq',
			'allele':mhc,
			'length':str(len(jj[2])),
			'species':'human',
			'sort_output':'MHC_IC50',
			'output_format':'xhtml',
			'submit':'Submit'
			}
		r1 = r.post(url,data=form,headers=headers)
		print(r1.status_code)
		r1 = r.get(url_result,headers=headers)
		print(r1.status_code)
		if r1.status_code == 200:
			r3 = r1.text
			soup = BeautifulSoup(r3, 'html.parser')
			result = soup.find(id='result_table')
			table = result.find('tr',class_='odd_row')
			output = []
			output.append(jj[0])
			for i in table.find_all('td'):
				output.append(i.get_text().strip('\n'))
			if output[1] == mhc and output[6] == jj[2]:
				output =	' '.join(output)
				c.write(output+'\n')
			else:
				print('form wrong')
				print('length '+str(len(jj[2])))
				d.write(jj[0])
				d.write('\t')
				d.write(jj[1])
				d.write('\t')
				d.write(jj[2])
				d.write('\t')
				d.write('form wrong')
				d.write('\t'+str(len(jj[2])))
				d.write('\n')
		else:
			print('form wrong')
			print('length '+str(len(jj[2])))
			d.write(jj[0])
			d.write('\t')
			d.write(jj[1])
			d.write('\t')
			d.write(jj[2])
			d.write('\t')
			d.write('form wrong')
			d.write('\t'+str(len(jj[2])))
			d.write('\n')
		c.close()
		d.close()
		if number <= 20:
			time.sleep(3)
		else:
			time.sleep(60)
			number = 0
	b.close()'''