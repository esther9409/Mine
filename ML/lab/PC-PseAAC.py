import sys
import subprocess

input3 = open('C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\number_allele_specific_ml_change.txt','r')
input4 = open('C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\number_allele_specific_dl_change.txt','r')
input5 = open('C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\number_pan_allele.txt','r')

MHC_allele_specific_ml = []
MHC_allele_specific_dl = []
MHC_pan_allele = []

for MHC_a_ml in input3:
	MHC_a_ml_split = MHC_a_ml.split('\t')
	MHC_allele_specific_ml.append(MHC_a_ml_split[0])
for MHC_a_dl in input4:
	MHC_a_dl_split = MHC_a_dl.split('\t')
	MHC_allele_specific_dl.append(MHC_a_dl_split[0])
for MHC_p in input5:
	MHC_p_split = MHC_p.split('\t')
	MHC_pan_allele.append(MHC_p_split[0])

pse_py = r'C:\\Users\\NCBLAB\\Desktop\\Pse-in-One-2.0(mine)\pse.py'

# for num1 in range(0,len(MHC_allele_specific_ml)):
# 	a = MHC_allele_specific_ml[num1]+'_P_pse_in_one_input.txt'
# 	a = 'C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\ml\\pse_in_one_input\\' + a
# 	sys.dont_write_bytecode = True
# 	cmd = 'python ' + pse_py + ' ' + a + ' Protein PC-PseAAC -lamada 2 -w 0.05 -out ' + a + '_PC-PseAAC_out.txt'
# 	subprocess.call(cmd, shell=True)
# 	a = MHC_allele_specific_ml[num1]+'_N_pse_in_one_input.txt'
# 	a = 'C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\ml\\pse_in_one_input\\' + a
# 	sys.dont_write_bytecode = True
# 	cmd = 'python ' + pse_py + ' ' + a + ' Protein PC-PseAAC -lamada 2 -w 0.05 -out ' + a + '_PC-PseAAC_out.txt'
# 	subprocess.call(cmd, shell=True)

# for num1 in range(0,len(MHC_allele_specific_dl)):
# 	a = MHC_allele_specific_dl[num1]+'_P_pse_in_one_input.txt'
# 	a = 'C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\dl\\pse_in_one_input\\' + a
# 	sys.dont_write_bytecode = True
# 	cmd = 'python ' + pse_py + ' ' + a + ' Protein PC-PseAAC -lamada 2 -w 0.05 -out ' + a + '_PC-PseAAC_out.txt'
# 	subprocess.call(cmd, shell=True)
# 	a = MHC_allele_specific_dl[num1]+'_N_pse_in_one_input.txt'
# 	a = 'C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\dl\\pse_in_one_input\\' + a
# 	sys.dont_write_bytecode = True
# 	cmd = 'python ' + pse_py + ' ' + a + ' Protein PC-PseAAC -lamada 2 -w 0.05 -out ' + a + '_PC-PseAAC_out.txt'
# 	subprocess.call(cmd, shell=True)


a = 'C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\dl\\pse_in_one\\MHC_pan_allele_P_pse_in_one_input.txt'
sys.dont_write_bytecode = True
cmd = 'python ' + pse_py + ' ' + a + ' Protein PC-PseAAC -lamada 2 -w 0.05 -out ' + a + '_PC-PseAAC_out.txt'
subprocess.call(cmd, shell=True)
a = 'C:\\Users\\NCBLAB\\Desktop\\research\\20190422\\dl\\pse_in_one\\MHC_pan_allele_N_pse_in_one_input.txt'
sys.dont_write_bytecode = True
cmd = 'python ' + pse_py + ' ' + a + ' Protein PC-PseAAC -lamada 2 -w 0.05 -out ' + a + '_PC-PseAAC_out.txt'
subprocess.call(cmd, shell=True)

input3.close()
input4.close()
input5.close()