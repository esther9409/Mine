import os
from os import listdir
from natsort import natsorted

path = os.path.abspath(os.getcwd())
exam = listdir(path)
for i in range(1,len(exam)):
	discussion = listdir(path+'\\'+exam[i]+'\\Discussion')
	discussion = natsorted(discussion)
	for k in range(0,len(discussion)):
		temp = ''
		num = 0
		a = open(path+'\\'+exam[i]+'\\Discussion\\'+discussion[k],'r',encoding="utf-8")
		if k == 0:
			button = '     <div class="page-navigation-bar">\n      <div class="col-12">\n         <a class="btn btn-success pull-right" href="'+path+'\\'+exam[i]+'\\Discussion\\'+discussion[k+1]+'">\n          Next Questions\n         </a>\n      </div>\n     </div>\n'

		elif k == len(discussion)-1:
			button = '     <div class="page-navigation-bar">\n      <div class="col-12">\n         <a class="btn btn-success" href="'+path+'\\'+exam[i]+'\\Discussion\\'+discussion[k-1]+'">\n          Previous Questions\n         </a>\n      </div>\n     </div>\n'
		else:
			button = '     <div class="page-navigation-bar">\n      <div class="col-12">\n         <a class="btn btn-success" href="'+path+'\\'+exam[i]+'\\Discussion\\'+discussion[k-1]+'">\n          Previous Questions\n         </a>\n         <a class="btn btn-success pull-right" href="'+path+'\\'+exam[i]+'\\Discussion\\'+discussion[k+1]+'">\n          Next Questions\n         </a>\n      </div>\n     </div>\n'
		for line in a:
			if num > 2:
				temp += button
				num = 0
			if 1 <= num <=2:
				temp += line
				num += 1
			if num == 0:
				if '<!-- Discussion end -->' in line:
					temp += line
					num += 1
				else:
					temp += line
		a.close()
		b = open(path+'\\'+exam[i]+'\\Discussion\\'+discussion[k],'w',encoding="utf-8")
		b.write(temp)
		b.close()
	print(exam[i]+'\nFinish\n')
input('Please enter any key to exit...')