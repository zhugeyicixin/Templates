# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from xlutils.copy import copy
from re import *
import re
import os
import shutil


#input
files='''C10H20_6_19_1_opt_PM6
C10H20_10_00_1_opt_PM6
C10H20_10_30_1_opt_PM6
C10H20_11_24_1_opt_PM6
C10H20_12_34_1_opt_PM6
C10H20_19_13_1_opt_PM6
C10H20_20_02_1_opt_PM6
C10H20_20_15_1_opt_PM6
C10H20_20_39_1_opt_PM6
C10H20_22_33_1_opt_PM6
C10H20_22_39_1_opt_PM6
C10H20_25_25_1_opt_PM6
C10H20_28_28_1_opt_PM6
C10H20_31_39_1_opt_PM6
C10H20_32_45_1_opt_PM6
C10H20_35_20_1_opt_PM6
C10H20_37_06_1_opt_PM6
C10H20_38_12_1_opt_PM6
C10H20_39_04_1_opt_PM6
C10H20_43_06_1_opt_PM6
C10H20_46_05_1_opt_PM6
C10H20_46_16_1_opt_PM6
C10H20_47_09_1_opt_PM6
C10H20_49_06_1_opt_PM6
C10H20_49_28_1_opt_PM6
C10H20_51_43_1_opt_PM6
C10H20_54_20_1_opt_PM6
C10H20_57_38_1_opt_PM6
C10H20_59_19_1_opt_PM6
C10H20_60_29_1_opt_PM6
C10H20_62_22_1_opt_PM6
C10H20_62_31_1_opt_PM6
C10H20_64_18_1_opt_PM6
C10H20_69_01_1_opt_PM6
C10H20_70_20_1_opt_PM6
C10H20_71_29_1_opt_PM6
C10H20_78_03_1_opt_PM6
C10H20_84_02_1_opt_PM6
C10H20_84_13_1_opt_PM6
C10H20_93_01_1_opt_PM6
C10H20_95_10_1_opt_PM6
C10H20_128_13_1_opt_PM6
C10H20_128_27_1_opt_PM6
C10H20_135_14_1_opt_PM6
C10H20_137_04_1_opt_PM6
C10H20_142_21_1_opt_PM6
C10H20_145_07_1_opt_PM6
C10H20_146_17_1_opt_PM6
C10H20_153_24_1_opt_PM6
C10H20_156_08_1_opt_PM6
C10H20_156_19_1_opt_PM6
C10H20_171_43_1_opt_PM6
C10H20_172_19_1_opt_PM6
C10H20_175_16_1_opt_PM6
C10H20_176_05_1_opt_PM6
C10H20_176_45_1_opt_PM6
C10H20_177_34_1_opt_PM6
C10H20_182_02_1_opt_PM6
C10H20_182_42_1_opt_PM6
C10H20_189_38_1_opt_PM6
C10H20_192_05_1_opt_PM6
C10H20_192_47_1_opt_PM6
C10H20_193_27_1_opt_PM6
C10H20_202_35_1_opt_PM6
C10H20_208_22_1_opt_PM6
C10H20_209_27_1_opt_PM6
C10H20_215_19_1_opt_PM6
C10H20_218_18_1_opt_PM6
C10H20_218_22_1_opt_PM6
C10H20_218_28_1_opt_PM6
C10H20_219_09_1_opt_PM6
C10H20_230_17_1_opt_PM6
C10H20_231_01_1_opt_PM6
C10H20_232_01_1_opt_PM6
C10H20_232_04_1_opt_PM6
C10H20_236_11_1_opt_PM6
C10H20_239_08_1_opt_PM6
C10H20_242_18_1_opt_PM6
C10H20_242_20_1_opt_PM6
C10H20_247_21_1_opt_PM6
C10H20_249_19_1_opt_PM6
C10H20_250_08_1_opt_PM6
C10H20_250_24_1_opt_PM6
C10H20_252_05_1_opt_PM6
C10H20_255_06_1_opt_PM6
C10H20_255_09_1_opt_PM6
C10H20_255_13_1_opt_PM6
C10H20_266_01_1_opt_PM6
C10H20_282_10_1_opt_PM6
C10H20_284_05_1_opt_PM6
C10H20_292_15_1_opt_PM6
C10H20_322_03_1_opt_PM6
C10H20_328_05_1_opt_PM6
C10H20_329_00_1_opt_PM6
C10H20_338_11_1_opt_PM6
C10H20_339_01_1_opt_PM6
C10H20_354_08_1_opt_PM6
C10H20_362_06_1_opt_PM6
C10H20_365_04_1_opt_PM6
C10H20_365_14_1_opt_PM6
C10H20_368_07_1_opt_PM6
C10H20_369_13_1_opt_PM6
C10H20_370_13_1_opt_PM6
C10H20_376_06_1_opt_PM6
C10H20_379_05_1_opt_PM6
C10H20_385_01_1_opt_PM6
C10H20_385_02_1_opt_PM6
C10H20_388_05_1_opt_PM6
C10H20_408_19_1_opt_PM6
C10H20_420_01_1_opt_PM6
C10H20_436_02_1_opt_PM6
C10H20_443_16_1_opt_PM6
C10H20_444_00_1_opt_PM6
C10H20_463_04_1_opt_PM6
C10H20_463_12_1_opt_PM6
C10H20_467_00_1_opt_PM6
C10H20_470_01_1_opt_PM6
C10H20_470_17_1_opt_PM6
C10H20_474_04_1_opt_PM6
C10H20_476_04_1_opt_PM6
C10H20_478_02_1_opt_PM6
C10H20_480_06_1_opt_PM6
C10H20_485_01_1_opt_PM6
C10H20_485_12_1_opt_PM6
C10H20_487_14_1_opt_PM6
C10H20_489_00_1_opt_PM6
C10H20_489_03_1_opt_PM6
C9H18_352_01_1_opt_PM6
C9H18_433_00_1_opt_PM6
C9H18_476_08_1_opt_PM6
'''


files=files.split()
for (index, tmp_file) in enumerate(files):
	files[index] = tmp_file[0:-3]+'B3L'
print len(files)


if os.path.exists('toBeSubmit'):
	shutil.rmtree('toBeSubmit')
os.mkdir('toBeSubmit')

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if os.path.isfile(tmp_file):
		continue
	if tmp_file in files:
		print tmp_file
		shutil.copytree(tmp_file,os.path.join('toBeSubmit', tmp_file))

print 'hindered rotation scripts generated successfully!'

# THE END




