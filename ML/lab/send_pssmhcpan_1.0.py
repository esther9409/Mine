import sys
import os
from subprocess import *
from os import listdir

files = listdir('20190422/case_study/fasta/PSSMHCpan_random/')
output = open('20190422\\case_study\\pssmhcpan_random_input.txt','a')

for t in range(len(files)):
	file_name = files[t].split('.f')
	file_name = file_name[0].split('_len_')
	file_length = file_name[1]
	file_name = file_name[0]
	output.write('perl PSSMHCpan-1.0.pl C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\case_study\\fasta\\PSSMHCpan_random\\'+files[t]+' '+file_length+' '+file_name+' C:\\Users\\NCBLAB\\Desktop\\PSSMHCpan-1.0\\database\\PSSM\\pssm_file.list > C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\case_study\\PSSMHCpan\\random\\'+file_name+'_'+file_length+'_result.txt\n')
#	cmd = 'perl C:\\Users\\NCBLAB\\Desktop\\PSSMHCpan-1.0\\PSSMHCpan-1.0.pl 20190422\\case_study\\fasta\\'+files[t]+' '+file_length+' '+file_name+' C:\\Users\\NCBLAB\\Desktop\\PSSMHCpan-1.0\\database\\PSSM\\pssm_file.list > 20190422\\case_study\\PSSMHCpan\\'+file_name+'_'+file_length+'_result.txt'
#	Popen(cmd, shell = True, stdout = PIPE).communicate()
output.close()