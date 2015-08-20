import win32api,win32gui,win32con,win32com
import time
import os
import numpy as np
from xlrd import *
print 'Hi! Minecraft!'

# blockSet = {'minecraft:wool': [209, 209, 209],
# 			'minecraft:wool 1': [235, 129, 55],
# 			'minecraft:wool 2': [195, 81, 205],
# 			'minecraft:wool 3': [100, 137, 212],
# 			'minecraft:wool 4': [202, 188, 29],
# 			'minecraft:wool 5': [53, 174, 42],
# 			'minecraft:wool 6': [222, 145, 166],
# 			'minecraft:wool 7': [61, 61, 61],
# 			'minecraft:wool 8': [155, 162, 162],
# 			'minecraft:wool 9': [45, 135, 173],
# 			'minecraft:wool 10': [142, 66, 208],
# 			'minecraft:wool 11': [33, 43, 131],
# 			'minecraft:wool 12': [89, 53, 28],
# 			'minecraft:wool 13': [57, 78, 25],
# 			'minecraft:wool 14': [159, 43, 39],
# 			'minecraft:wool 15': [29, 25, 25],
# 			'minecraft:gold_block': [255, 255, 113],
# 			'minecraft:iron_block': [234, 234, 234],
# 			'minecraft:sandstone 2': [213, 205, 157],
# 			'minecraft:lapis_block': [33, 50, 152],
# 			'minecraft:stone 6': [129, 129, 136],
# 			'minecraft:stone 4': [133, 133, 135],
# 			'minecraft:stone 2': [160, 107, 88],
# 			'minecraft:stone': [116, 116, 116]
# 			}

blockSet = {'japanesecoloredwool:japanesecoloredwool_0_ 0': [253,243,243],
			'japanesecoloredwool:japanesecoloredwool_0_ 1': [252,238,241],
			'japanesecoloredwool:japanesecoloredwool_0_ 2': [232,222,228],
			'japanesecoloredwool:japanesecoloredwool_0_ 3': [227,209,215],
			'japanesecoloredwool:japanesecoloredwool_0_ 4': [245,190,187],
			'japanesecoloredwool:japanesecoloredwool_0_ 5': [244,176,169],
			'japanesecoloredwool:japanesecoloredwool_0_ 6': [244,176,152],
			'japanesecoloredwool:japanesecoloredwool_0_ 7': [238,170,146],
			'japanesecoloredwool:japanesecoloredwool_0_ 8': [241,159,160],
			'japanesecoloredwool:japanesecoloredwool_0_ 9': [239,143,140],
			'japanesecoloredwool:japanesecoloredwool_0_ 10': [237,129,123],
			'japanesecoloredwool:japanesecoloredwool_0_ 11': [239,144,152],
			'japanesecoloredwool:japanesecoloredwool_0_ 12': [243,178,193],
			'japanesecoloredwool:japanesecoloredwool_0_ 13': [237,186,202],
			'japanesecoloredwool:japanesecoloredwool_0_ 14': [231,210,198],
			'japanesecoloredwool:japanesecoloredwool_0_ 15': [231,210,208],
			'japanesecoloredwool:japanesecoloredwool_1_ 0': [229,204,226],
			'japanesecoloredwool:japanesecoloredwool_1_ 1': [228,170,189],
			'japanesecoloredwool:japanesecoloredwool_1_ 2': [228,150,177],
			'japanesecoloredwool:japanesecoloredwool_1_ 3': [224,151,179],
			'japanesecoloredwool:japanesecoloredwool_1_ 4': [227,170,154],
			'japanesecoloredwool:japanesecoloredwool_1_ 5': [223,157,134],
			'japanesecoloredwool:japanesecoloredwool_1_ 6': [213,143,143],
			'japanesecoloredwool:japanesecoloredwool_1_ 7': [211,171,172],
			'japanesecoloredwool:japanesecoloredwool_1_ 8': [200,116,133],
			'japanesecoloredwool:japanesecoloredwool_1_ 9': [190,152,159],
			'japanesecoloredwool:japanesecoloredwool_1_ 10': [183,135,131],
			'japanesecoloredwool:japanesecoloredwool_1_ 11': [179,137,117],
			'japanesecoloredwool:japanesecoloredwool_1_ 12': [167,104,100],
			'japanesecoloredwool:japanesecoloredwool_1_ 13': [161,86,103],
			'japanesecoloredwool:japanesecoloredwool_1_ 14': [235,108,112],
			'japanesecoloredwool:japanesecoloredwool_1_ 15': [234,109,164],
			'japanesecoloredwool:japanesecoloredwool_2_ 0': [232,81,148],
			'japanesecoloredwool:japanesecoloredwool_2_ 1': [230,95,157],
			'japanesecoloredwool:japanesecoloredwool_2_ 2': [207,86,106],
			'japanesecoloredwool:japanesecoloredwool_2_ 3': [199,80,120],
			'japanesecoloredwool:japanesecoloredwool_2_ 4': [232,83,106],
			'japanesecoloredwool:japanesecoloredwool_2_ 5': [232,83,99],
			'japanesecoloredwool:japanesecoloredwool_2_ 6': [199,84,83],
			'japanesecoloredwool:japanesecoloredwool_2_ 7': [196,60,66],
			'japanesecoloredwool:japanesecoloredwool_2_ 8': [231,56,40],
			'japanesecoloredwool:japanesecoloredwool_2_ 9': [229,0,50],
			'japanesecoloredwool:japanesecoloredwool_2_ 10': [225,3,26],
			'japanesecoloredwool:japanesecoloredwool_2_ 11': [214,0,57],
			'japanesecoloredwool:japanesecoloredwool_2_ 12': [200,22,29],
			'japanesecoloredwool:japanesecoloredwool_2_ 13': [210,55,27],
			'japanesecoloredwool:japanesecoloredwool_2_ 14': [205,81,65],
			'japanesecoloredwool:japanesecoloredwool_2_ 15': [216,50,62],
			'japanesecoloredwool:japanesecoloredwool_3_ 0': [184,63,70],
			'japanesecoloredwool:japanesecoloredwool_3_ 1': [185,37,53],
			'japanesecoloredwool:japanesecoloredwool_3_ 2': [182,39,45],
			'japanesecoloredwool:japanesecoloredwool_3_ 3': [166,55,53],
			'japanesecoloredwool:japanesecoloredwool_3_ 4': [157,60,62],
			'japanesecoloredwool:japanesecoloredwool_3_ 5': [161,31,64],
			'japanesecoloredwool:japanesecoloredwool_3_ 6': [247,243,229],
			'japanesecoloredwool:japanesecoloredwool_3_ 7': [236,227,204],
			'japanesecoloredwool:japanesecoloredwool_3_ 8': [232,227,211],
			'japanesecoloredwool:japanesecoloredwool_3_ 9': [234,224,168],
			'japanesecoloredwool:japanesecoloredwool_3_ 10': [241,241,175],
			'japanesecoloredwool:japanesecoloredwool_3_ 11': [227,219,137],
			'japanesecoloredwool:japanesecoloredwool_3_ 12': [247,228,139],
			'japanesecoloredwool:japanesecoloredwool_3_ 13': [220,186,152],
			'japanesecoloredwool:japanesecoloredwool_3_ 14': [214,168,139],
			'japanesecoloredwool:japanesecoloredwool_3_ 15': [241,200,171],
			'japanesecoloredwool:japanesecoloredwool_4_ 0': [254,240,206],
			'japanesecoloredwool:japanesecoloredwool_4_ 1': [252,221,164],
			'japanesecoloredwool:japanesecoloredwool_4_ 2': [251,225,195],
			'japanesecoloredwool:japanesecoloredwool_4_ 3': [252,231,207],
			'japanesecoloredwool:japanesecoloredwool_4_ 4': [248,199,154],
			'japanesecoloredwool:japanesecoloredwool_4_ 5': [246,188,142],
			'japanesecoloredwool:japanesecoloredwool_4_ 6': [245,183,147],
			'japanesecoloredwool:japanesecoloredwool_4_ 7': [243,220,164],
			'japanesecoloredwool:japanesecoloredwool_4_ 8': [240,190,152],
			'japanesecoloredwool:japanesecoloredwool_4_ 9': [238,204,153],
			'japanesecoloredwool:japanesecoloredwool_4_ 10': [239,206,159],
			'japanesecoloredwool:japanesecoloredwool_4_ 11': [236,210,160],
			'japanesecoloredwool:japanesecoloredwool_4_ 12': [223,194,139],
			'japanesecoloredwool:japanesecoloredwool_4_ 13': [242,190,135],
			'japanesecoloredwool:japanesecoloredwool_4_ 14': [246,184,118],
			'japanesecoloredwool:japanesecoloredwool_4_ 15': [240,143,113],
			'japanesecoloredwool:japanesecoloredwool_5_ 0': [237,130,110],
			'japanesecoloredwool:japanesecoloredwool_5_ 1': [234,145,101],
			'japanesecoloredwool:japanesecoloredwool_5_ 2': [223,128,93],
			'japanesecoloredwool:japanesecoloredwool_5_ 3': [222,112,98],
			'japanesecoloredwool:japanesecoloredwool_5_ 4': [212,123,106],
			'japanesecoloredwool:japanesecoloredwool_5_ 5': [207,129,107],
			'japanesecoloredwool:japanesecoloredwool_5_ 6': [201,129,104],
			'japanesecoloredwool:japanesecoloredwool_5_ 7': [186,84,71],
			'japanesecoloredwool:japanesecoloredwool_5_ 8': [170,104,82],
			'japanesecoloredwool:japanesecoloredwool_5_ 9': [149,80,76],
			'japanesecoloredwool:japanesecoloredwool_5_ 10': [140,99,72],
			'japanesecoloredwool:japanesecoloredwool_5_ 11': [221,175,103],
			'japanesecoloredwool:japanesecoloredwool_5_ 12': [190,120,77],
			'japanesecoloredwool:japanesecoloredwool_5_ 13': [187,117,59],
			'japanesecoloredwool:japanesecoloredwool_5_ 14': [184,139,69],
			'japanesecoloredwool:japanesecoloredwool_5_ 15': [182,154,90],
			'japanesecoloredwool:japanesecoloredwool_6_ 0': [182,122,86],
			'japanesecoloredwool:japanesecoloredwool_6_ 1': [181,140,75],
			'japanesecoloredwool:japanesecoloredwool_6_ 2': [172,124,75],
			'japanesecoloredwool:japanesecoloredwool_6_ 3': [173,123,78],
			'japanesecoloredwool:japanesecoloredwool_6_ 4': [172,125,77],
			'japanesecoloredwool:japanesecoloredwool_6_ 5': [173,123,87],
			'japanesecoloredwool:japanesecoloredwool_6_ 6': [167,110,75],
			'japanesecoloredwool:japanesecoloredwool_6_ 7': [147,97,66],
			'japanesecoloredwool:japanesecoloredwool_6_ 8': [144,114,70],
			'japanesecoloredwool:japanesecoloredwool_6_ 9': [148,110,40],
			'japanesecoloredwool:japanesecoloredwool_6_ 10': [138,111,65],
			'japanesecoloredwool:japanesecoloredwool_6_ 11': [122,107,61],
			'japanesecoloredwool:japanesecoloredwool_6_ 12': [215,162,114],
			'japanesecoloredwool:japanesecoloredwool_6_ 13': [204,139,91],
			'japanesecoloredwool:japanesecoloredwool_6_ 14': [204,93,59],
			'japanesecoloredwool:japanesecoloredwool_6_ 15': [202,130,70],
			'japanesecoloredwool:japanesecoloredwool_7_ 0': [194,119,83],
			'japanesecoloredwool:japanesecoloredwool_7_ 1': [194,134,66],
			'japanesecoloredwool:japanesecoloredwool_7_ 2': [194,144,66],
			'japanesecoloredwool:japanesecoloredwool_7_ 3': [190,119,57],
			'japanesecoloredwool:japanesecoloredwool_7_ 4': [186,84,52],
			'japanesecoloredwool:japanesecoloredwool_7_ 5': [186,84,31],
			'japanesecoloredwool:japanesecoloredwool_7_ 6': [180,81,50],
			'japanesecoloredwool:japanesecoloredwool_7_ 7': [169,78,54],
			'japanesecoloredwool:japanesecoloredwool_7_ 8': [157,85,57],
			'japanesecoloredwool:japanesecoloredwool_7_ 9': [153,72,62],
			'japanesecoloredwool:japanesecoloredwool_7_ 10': [151,97,59],
			'japanesecoloredwool:japanesecoloredwool_7_ 11': [149,79,65],
			'japanesecoloredwool:japanesecoloredwool_7_ 12': [149,79,53],
			'japanesecoloredwool:japanesecoloredwool_7_ 13': [148,71,62],
			'japanesecoloredwool:japanesecoloredwool_7_ 14': [148,77,41],
			'japanesecoloredwool:japanesecoloredwool_7_ 15': [142,45,19],
			'japanesecoloredwool:japanesecoloredwool_8_ 0': [137,50,24],
			'japanesecoloredwool:japanesecoloredwool_8_ 1': [137,58,0],
			'japanesecoloredwool:japanesecoloredwool_8_ 2': [132,45,24],
			'japanesecoloredwool:japanesecoloredwool_8_ 3': [122,70,64],
			'japanesecoloredwool:japanesecoloredwool_8_ 4': [118,59,47],
			'japanesecoloredwool:japanesecoloredwool_8_ 5': [119,59,28],
			'japanesecoloredwool:japanesecoloredwool_8_ 6': [117,46,6],
			'japanesecoloredwool:japanesecoloredwool_8_ 7': [116,32,0],
			'japanesecoloredwool:japanesecoloredwool_8_ 8': [107,52,35],
			'japanesecoloredwool:japanesecoloredwool_8_ 9': [103,62,53],
			'japanesecoloredwool:japanesecoloredwool_8_ 10': [101,63,49],
			'japanesecoloredwool:japanesecoloredwool_8_ 11': [108,59,49],
			'japanesecoloredwool:japanesecoloredwool_8_ 12': [87,55,33],
			'japanesecoloredwool:japanesecoloredwool_8_ 13': [107,43,46],
			'japanesecoloredwool:japanesecoloredwool_8_ 14': [247,183,97],
			'japanesecoloredwool:japanesecoloredwool_8_ 15': [245,172,72],
			'japanesecoloredwool:japanesecoloredwool_9_ 0': [242,151,0],
			'japanesecoloredwool:japanesecoloredwool_9_ 1': [239,130,0],
			'japanesecoloredwool:japanesecoloredwool_9_ 2': [235,108,80],
			'japanesecoloredwool:japanesecoloredwool_9_ 3': [237,120,71],
			'japanesecoloredwool:japanesecoloredwool_9_ 4': [236,108,60],
			'japanesecoloredwool:japanesecoloredwool_9_ 5': [235,103,0],
			'japanesecoloredwool:japanesecoloredwool_9_ 6': [237,119,0],
			'japanesecoloredwool:japanesecoloredwool_9_ 7': [234,97,55],
			'japanesecoloredwool:japanesecoloredwool_9_ 8': [233,84,5],
			'japanesecoloredwool:japanesecoloredwool_9_ 9': [234,96,0],
			'japanesecoloredwool:japanesecoloredwool_9_ 10': [227,157,96],
			'japanesecoloredwool:japanesecoloredwool_9_ 11': [227,93,49],
			'japanesecoloredwool:japanesecoloredwool_9_ 12': [224,122,51],
			'japanesecoloredwool:japanesecoloredwool_9_ 13': [220,121,85],
			'japanesecoloredwool:japanesecoloredwool_9_ 14': [218,131,72],
			'japanesecoloredwool:japanesecoloredwool_9_ 15': [213,105,52],
			'japanesecoloredwool:japanesecoloredwool_10_ 0': [254,216,0],
			'japanesecoloredwool:japanesecoloredwool_10_ 1': [254,233,0],
			'japanesecoloredwool:japanesecoloredwool_10_ 2': [254,235,70],
			'japanesecoloredwool:japanesecoloredwool_10_ 3': [253,241,98],
			'japanesecoloredwool:japanesecoloredwool_10_ 4': [251,212,116],
			'japanesecoloredwool:japanesecoloredwool_10_ 5': [250,209,106],
			'japanesecoloredwool:japanesecoloredwool_10_ 6': [244,228,106],
			'japanesecoloredwool:japanesecoloredwool_10_ 7': [237,194,97],
			'japanesecoloredwool:japanesecoloredwool_10_ 8': [234,215,65],
			'japanesecoloredwool:japanesecoloredwool_10_ 9': [254,218,78],
			'japanesecoloredwool:japanesecoloredwool_10_ 10': [250,201,76],
			'japanesecoloredwool:japanesecoloredwool_10_ 11': [251,199,0],
			'japanesecoloredwool:japanesecoloredwool_10_ 12': [247,180,0],
			'japanesecoloredwool:japanesecoloredwool_10_ 13': [249,190,19],
			'japanesecoloredwool:japanesecoloredwool_10_ 14': [246,192,19],
			'japanesecoloredwool:japanesecoloredwool_10_ 15': [229,179,33],
			'japanesecoloredwool:japanesecoloredwool_11_ 0': [216,165,45],
			'japanesecoloredwool:japanesecoloredwool_11_ 1': [210,161,66],
			'japanesecoloredwool:japanesecoloredwool_11_ 2': [199,152,49],
			'japanesecoloredwool:japanesecoloredwool_11_ 3': [207,174,75],
			'japanesecoloredwool:japanesecoloredwool_11_ 4': [138,149,140],
			'japanesecoloredwool:japanesecoloredwool_11_ 5': [109,120,84],
			'japanesecoloredwool:japanesecoloredwool_11_ 6': [117,123,106],
			'japanesecoloredwool:japanesecoloredwool_11_ 7': [135,141,125],
			'japanesecoloredwool:japanesecoloredwool_11_ 8': [89,83,74],
			'japanesecoloredwool:japanesecoloredwool_11_ 9': [85,85,74],
			'japanesecoloredwool:japanesecoloredwool_11_ 10': [84,85,70],
			'japanesecoloredwool:japanesecoloredwool_11_ 11': [72,73,64],
			'japanesecoloredwool:japanesecoloredwool_11_ 12': [106,110,88],
			'japanesecoloredwool:japanesecoloredwool_11_ 13': [70,74,65],
			'japanesecoloredwool:japanesecoloredwool_11_ 14': [47,50,45],
			'japanesecoloredwool:japanesecoloredwool_11_ 15': [90,98,85],
			'japanesecoloredwool:japanesecoloredwool_12_ 0': [113,97,79],
			'japanesecoloredwool:japanesecoloredwool_12_ 1': [156,136,107],
			'japanesecoloredwool:japanesecoloredwool_12_ 2': [147,131,105],
			'japanesecoloredwool:japanesecoloredwool_12_ 3': [136,119,87],
			'japanesecoloredwool:japanesecoloredwool_12_ 4': [112,97,69],
			'japanesecoloredwool:japanesecoloredwool_12_ 5': [202,184,147],
			'japanesecoloredwool:japanesecoloredwool_12_ 6': [213,197,174],
			'japanesecoloredwool:japanesecoloredwool_12_ 7': [190,163,110],
			'japanesecoloredwool:japanesecoloredwool_12_ 8': [157,147,119],
			'japanesecoloredwool:japanesecoloredwool_12_ 9': [164,148,99],
			'japanesecoloredwool:japanesecoloredwool_12_ 10': [112,91,30],
			'japanesecoloredwool:japanesecoloredwool_12_ 11': [198,178,111],
			'japanesecoloredwool:japanesecoloredwool_12_ 12': [219,210,177],
			'japanesecoloredwool:japanesecoloredwool_12_ 13': [160,146,96],
			'japanesecoloredwool:japanesecoloredwool_12_ 14': [142,133,102],
			'japanesecoloredwool:japanesecoloredwool_12_ 15': [135,120,55],
			'japanesecoloredwool:japanesecoloredwool_13_ 0': [105,92,32],
			'japanesecoloredwool:japanesecoloredwool_13_ 1': [144,134,83],
			'japanesecoloredwool:japanesecoloredwool_13_ 2': [165,147,36],
			'japanesecoloredwool:japanesecoloredwool_13_ 3': [172,161,79],
			'japanesecoloredwool:japanesecoloredwool_13_ 4': [146,138,74],
			'japanesecoloredwool:japanesecoloredwool_13_ 5': [139,135,96],
			'japanesecoloredwool:japanesecoloredwool_13_ 6': [160,163,108],
			'japanesecoloredwool:japanesecoloredwool_13_ 7': [113,108,63],
			'japanesecoloredwool:japanesecoloredwool_13_ 8': [145,139,53],
			'japanesecoloredwool:japanesecoloredwool_13_ 9': [219,202,23],
			'japanesecoloredwool:japanesecoloredwool_13_ 10': [214,206,57],
			'japanesecoloredwool:japanesecoloredwool_13_ 11': [196,196,105],
			'japanesecoloredwool:japanesecoloredwool_13_ 12': [194,215,36],
			'japanesecoloredwool:japanesecoloredwool_13_ 13': [183,209,0],
			'japanesecoloredwool:japanesecoloredwool_13_ 14': [223,234,174],
			'japanesecoloredwool:japanesecoloredwool_13_ 15': [215,229,151],
			'japanesecoloredwool:japanesecoloredwool_14_ 0': [198,219,103],
			'japanesecoloredwool:japanesecoloredwool_14_ 1': [152,170,77],
			'japanesecoloredwool:japanesecoloredwool_14_ 2': [122,140,65],
			'japanesecoloredwool:japanesecoloredwool_14_ 3': [104,129,26],
			'japanesecoloredwool:japanesecoloredwool_14_ 4': [169,206,82],
			'japanesecoloredwool:japanesecoloredwool_14_ 5': [175,201,112],
			'japanesecoloredwool:japanesecoloredwool_14_ 6': [184,207,138],
			'japanesecoloredwool:japanesecoloredwool_14_ 7': [130,154,91],
			'japanesecoloredwool:japanesecoloredwool_14_ 8': [202,223,170],
			'japanesecoloredwool:japanesecoloredwool_14_ 9': [129,173,69],
			'japanesecoloredwool:japanesecoloredwool_14_ 10': [167,200,127],
			'japanesecoloredwool:japanesecoloredwool_14_ 11': [154,167,140],
			'japanesecoloredwool:japanesecoloredwool_14_ 12': [199,212,186],
			'japanesecoloredwool:japanesecoloredwool_14_ 13': [192,215,171],
			'japanesecoloredwool:japanesecoloredwool_14_ 14': [167,190,146],
			'japanesecoloredwool:japanesecoloredwool_14_ 15': [117,144,99],
			'japanesecoloredwool:japanesecoloredwool_15_ 0': [213,232,201],
			'japanesecoloredwool:japanesecoloredwool_15_ 1': [146,201,117],
			'japanesecoloredwool:japanesecoloredwool_15_ 2': [146,183,128],
			'japanesecoloredwool:japanesecoloredwool_15_ 3': [185,219,172],
			'japanesecoloredwool:japanesecoloredwool_15_ 4': [150,166,144],
			'japanesecoloredwool:japanesecoloredwool_15_ 5': [151,216,141],
			'japanesecoloredwool:japanesecoloredwool_15_ 6': [135,202,126],
			'japanesecoloredwool:japanesecoloredwool_15_ 7': [104,175,117],
			'japanesecoloredwool:japanesecoloredwool_15_ 8': [106,122,109],
			'japanesecoloredwool:japanesecoloredwool_15_ 9': [189,209,194],
			'japanesecoloredwool:japanesecoloredwool_15_ 10': [146,181,155],
			'japanesecoloredwool:japanesecoloredwool_15_ 11': [165,199,177],
			'japanesecoloredwool:japanesecoloredwool_15_ 12': [70,135,93],
			'japanesecoloredwool:japanesecoloredwool_15_ 13': [48,102,68],
			'japanesecoloredwool:japanesecoloredwool_15_ 14': [98,184,135],
			'japanesecoloredwool:japanesecoloredwool_15_ 15': [61,178,111],
			'japanesecoloredwool:japanesecoloredwool_16_ 0': [0,122,66],
			'japanesecoloredwool:japanesecoloredwool_16_ 1': [189,210,201],
			'japanesecoloredwool:japanesecoloredwool_16_ 2': [138,173,161],
			'japanesecoloredwool:japanesecoloredwool_16_ 3': [125,189,164],
			'japanesecoloredwool:japanesecoloredwool_16_ 4': [125,189,170],
			'japanesecoloredwool:japanesecoloredwool_16_ 5': [1,134,95],
			'japanesecoloredwool:japanesecoloredwool_16_ 6': [58,120,95],
			'japanesecoloredwool:japanesecoloredwool_16_ 7': [46,92,79],
			'japanesecoloredwool:japanesecoloredwool_16_ 8': [57,90,81],
			'japanesecoloredwool:japanesecoloredwool_16_ 9': [70,88,79],
			'japanesecoloredwool:japanesecoloredwool_16_ 10': [0,84,45],
			'japanesecoloredwool:japanesecoloredwool_16_ 11': [0,81,66],
			'japanesecoloredwool:japanesecoloredwool_16_ 12': [0,109,83],
			'japanesecoloredwool:japanesecoloredwool_16_ 13': [0,162,128],
			'japanesecoloredwool:japanesecoloredwool_16_ 14': [55,179,138],
			'japanesecoloredwool:japanesecoloredwool_16_ 15': [0,163,150],
			'japanesecoloredwool:japanesecoloredwool_17_ 0': [127,170,168],
			'japanesecoloredwool:japanesecoloredwool_17_ 1': [91,145,144],
			'japanesecoloredwool:japanesecoloredwool_17_ 2': [70,130,131],
			'japanesecoloredwool:japanesecoloredwool_17_ 3': [66,102,106],
			'japanesecoloredwool:japanesecoloredwool_17_ 4': [127,151,154],
			'japanesecoloredwool:japanesecoloredwool_17_ 5': [43,78,83],
			'japanesecoloredwool:japanesecoloredwool_17_ 6': [30,48,51],
			'japanesecoloredwool:japanesecoloredwool_17_ 7': [70,87,91],
			'japanesecoloredwool:japanesecoloredwool_17_ 8': [81,87,88],
			'japanesecoloredwool:japanesecoloredwool_17_ 9': [107,131,140],
			'japanesecoloredwool:japanesecoloredwool_17_ 10': [82,113,124],
			'japanesecoloredwool:japanesecoloredwool_17_ 11': [90,125,144],
			'japanesecoloredwool:japanesecoloredwool_17_ 12': [65,100,120],
			'japanesecoloredwool:japanesecoloredwool_17_ 13': [75,99,114],
			'japanesecoloredwool:japanesecoloredwool_17_ 14': [68,86,100],
			'japanesecoloredwool:japanesecoloredwool_17_ 15': [67,96,122],
			'japanesecoloredwool:japanesecoloredwool_18_ 0': [56,62,75],
			'japanesecoloredwool:japanesecoloredwool_18_ 1': [56,61,78],
			'japanesecoloredwool:japanesecoloredwool_18_ 2': [31,54,67],
			'japanesecoloredwool:japanesecoloredwool_18_ 3': [76,75,96],
			'japanesecoloredwool:japanesecoloredwool_18_ 4': [233,243,251],
			'japanesecoloredwool:japanesecoloredwool_18_ 5': [233,236,246],
			'japanesecoloredwool:japanesecoloredwool_18_ 6': [231,235,238],
			'japanesecoloredwool:japanesecoloredwool_18_ 7': [234,245,246],
			'japanesecoloredwool:japanesecoloredwool_18_ 8': [191,227,232],
			'japanesecoloredwool:japanesecoloredwool_18_ 9': [187,225,231],
			'japanesecoloredwool:japanesecoloredwool_18_ 10': [161,214,220],
			'japanesecoloredwool:japanesecoloredwool_18_ 11': [170,205,215],
			'japanesecoloredwool:japanesecoloredwool_18_ 12': [159,215,238],
			'japanesecoloredwool:japanesecoloredwool_18_ 13': [136,194,234],
			'japanesecoloredwool:japanesecoloredwool_18_ 14': [131,161,211],
			'japanesecoloredwool:japanesecoloredwool_18_ 15': [130,203,209],
			'japanesecoloredwool:japanesecoloredwool_19_ 0': [131,184,202],
			'japanesecoloredwool:japanesecoloredwool_19_ 1': [104,137,170],
			'japanesecoloredwool:japanesecoloredwool_19_ 2': [0,135,152],
			'japanesecoloredwool:japanesecoloredwool_19_ 3': [0,162,174],
			'japanesecoloredwool:japanesecoloredwool_19_ 4': [41,130,161],
			'japanesecoloredwool:japanesecoloredwool_19_ 5': [88,184,197],
			'japanesecoloredwool:japanesecoloredwool_19_ 6': [43,168,224],
			'japanesecoloredwool:japanesecoloredwool_19_ 7': [55,160,218],
			'japanesecoloredwool:japanesecoloredwool_19_ 8': [0,148,216],
			'japanesecoloredwool:japanesecoloredwool_19_ 9': [0,147,199],
			'japanesecoloredwool:japanesecoloredwool_19_ 10': [38,145,194],
			'japanesecoloredwool:japanesecoloredwool_19_ 11': [0,122,186],
			'japanesecoloredwool:japanesecoloredwool_19_ 12': [81,128,191],
			'japanesecoloredwool:japanesecoloredwool_19_ 13': [61,97,172],
			'japanesecoloredwool:japanesecoloredwool_19_ 14': [29,79,161],
			'japanesecoloredwool:japanesecoloredwool_19_ 15': [79,125,163],
			'japanesecoloredwool:japanesecoloredwool_20_ 0': [24,67,141],
			'japanesecoloredwool:japanesecoloredwool_20_ 1': [21,73,131],
			'japanesecoloredwool:japanesecoloredwool_20_ 2': [21,93,130],
			'japanesecoloredwool:japanesecoloredwool_20_ 3': [38,73,119],
			'japanesecoloredwool:japanesecoloredwool_20_ 4': [41,63,114],
			'japanesecoloredwool:japanesecoloredwool_20_ 5': [33,57,111],
			'japanesecoloredwool:japanesecoloredwool_20_ 6': [24,46,95],
			'japanesecoloredwool:japanesecoloredwool_20_ 7': [27,47,91],
			'japanesecoloredwool:japanesecoloredwool_20_ 8': [14,34,79],
			'japanesecoloredwool:japanesecoloredwool_20_ 9': [22,23,74],
			'japanesecoloredwool:japanesecoloredwool_20_ 10': [12,0,20],
			'japanesecoloredwool:japanesecoloredwool_20_ 11': [186,199,229],
			'japanesecoloredwool:japanesecoloredwool_20_ 12': [186,187,221],
			'japanesecoloredwool:japanesecoloredwool_20_ 13': [131,144,194],
			'japanesecoloredwool:japanesecoloredwool_20_ 14': [76,89,174],
			'japanesecoloredwool:japanesecoloredwool_20_ 15': [73,71,141],
			'japanesecoloredwool:japanesecoloredwool_21_ 0': [76,66,151],
			'japanesecoloredwool:japanesecoloredwool_21_ 1': [85,83,161],
			'japanesecoloredwool:japanesecoloredwool_21_ 2': [111,107,169],
			'japanesecoloredwool:japanesecoloredwool_21_ 3': [103,104,154],
			'japanesecoloredwool:japanesecoloredwool_21_ 4': [133,122,168],
			'japanesecoloredwool:japanesecoloredwool_21_ 5': [218,207,229],
			'japanesecoloredwool:japanesecoloredwool_21_ 6': [164,153,201],
			'japanesecoloredwool:japanesecoloredwool_21_ 7': [111,87,162],
			'japanesecoloredwool:japanesecoloredwool_21_ 8': [102,68,151],
			'japanesecoloredwool:japanesecoloredwool_21_ 9': [102,64,149],
			'japanesecoloredwool:japanesecoloredwool_21_ 10': [143,120,172],
			'japanesecoloredwool:japanesecoloredwool_21_ 11': [115,82,152],
			'japanesecoloredwool:japanesecoloredwool_21_ 12': [100,48,141],
			'japanesecoloredwool:japanesecoloredwool_21_ 13': [81,46,95],
			'japanesecoloredwool:japanesecoloredwool_21_ 14': [72,54,88],
			'japanesecoloredwool:japanesecoloredwool_21_ 15': [45,40,47],
			'japanesecoloredwool:japanesecoloredwool_22_ 0': [135,71,151],
			'japanesecoloredwool:japanesecoloredwool_22_ 1': [191,161,198],
			'japanesecoloredwool:japanesecoloredwool_22_ 2': [69,13,67],
			'japanesecoloredwool:japanesecoloredwool_22_ 3': [115,49,91],
			'japanesecoloredwool:japanesecoloredwool_22_ 4': [84,40,90],
			'japanesecoloredwool:japanesecoloredwool_22_ 5': [136,90,137],
			'japanesecoloredwool:japanesecoloredwool_22_ 6': [129,71,127],
			'japanesecoloredwool:japanesecoloredwool_22_ 7': [144,91,138],
			'japanesecoloredwool:japanesecoloredwool_22_ 8': [156,90,138],
			'japanesecoloredwool:japanesecoloredwool_22_ 9': [121,64,112],
			'japanesecoloredwool:japanesecoloredwool_22_ 10': [187,99,163],
			'japanesecoloredwool:japanesecoloredwool_22_ 11': [179,75,150],
			'japanesecoloredwool:japanesecoloredwool_22_ 12': [169,75,142],
			'japanesecoloredwool:japanesecoloredwool_22_ 13': [203,125,176],
			'japanesecoloredwool:japanesecoloredwool_22_ 14': [203,165,190],
			'japanesecoloredwool:japanesecoloredwool_22_ 15': [195,162,190],
			'japanesecoloredwool:japanesecoloredwool_23_ 0': [230,230,234],
			'japanesecoloredwool:japanesecoloredwool_23_ 1': [219,213,216],
			'japanesecoloredwool:japanesecoloredwool_23_ 2': [210,206,216],
			'japanesecoloredwool:japanesecoloredwool_23_ 3': [210,203,213],
			'japanesecoloredwool:japanesecoloredwool_23_ 4': [199,193,197],
			'japanesecoloredwool:japanesecoloredwool_23_ 5': [165,164,195],
			'japanesecoloredwool:japanesecoloredwool_23_ 6': [100,93,115],
			'japanesecoloredwool:japanesecoloredwool_23_ 7': [167,156,171],
			'japanesecoloredwool:japanesecoloredwool_23_ 8': [150,143,163],
			'japanesecoloredwool:japanesecoloredwool_23_ 9': [157,138,141],
			'japanesecoloredwool:japanesecoloredwool_23_ 10': [148,132,155],
			'japanesecoloredwool:japanesecoloredwool_23_ 11': [148,147,153],
			'japanesecoloredwool:japanesecoloredwool_23_ 12': [112,103,107],
			'japanesecoloredwool:japanesecoloredwool_23_ 13': [111,90,102],
			'japanesecoloredwool:japanesecoloredwool_23_ 14': [98,72,79],
			'japanesecoloredwool:japanesecoloredwool_23_ 15': [94,64,74],
			'japanesecoloredwool:japanesecoloredwool_24_ 0': [78,68,91],
			'japanesecoloredwool:japanesecoloredwool_24_ 1': [89,82,88],
			'japanesecoloredwool:japanesecoloredwool_24_ 2': [88,65,84],
			'japanesecoloredwool:japanesecoloredwool_24_ 3': [81,70,71],
			'japanesecoloredwool:japanesecoloredwool_24_ 4': [80,54,66],
			'japanesecoloredwool:japanesecoloredwool_24_ 5': [229,233,226],
			'japanesecoloredwool:japanesecoloredwool_24_ 6': [211,219,213],
			'japanesecoloredwool:japanesecoloredwool_24_ 7': [211,219,217],
			'japanesecoloredwool:japanesecoloredwool_24_ 8': [210,202,197],
			'japanesecoloredwool:japanesecoloredwool_24_ 9': [199,193,189],
			'japanesecoloredwool:japanesecoloredwool_24_ 10': [178,172,159],
			'japanesecoloredwool:japanesecoloredwool_24_ 11': [168,157,146],
			'japanesecoloredwool:japanesecoloredwool_24_ 12': [164,142,133],
			'japanesecoloredwool:japanesecoloredwool_24_ 13': [145,128,119],
			'japanesecoloredwool:japanesecoloredwool_24_ 14': [135,126,121],
			'japanesecoloredwool:japanesecoloredwool_24_ 15': [179,133,106],
			'japanesecoloredwool:japanesecoloredwool_25_ 0': [177,139,109],
			'japanesecoloredwool:japanesecoloredwool_25_ 1': [160,108,92],
			'japanesecoloredwool:japanesecoloredwool_25_ 2': [158,110,84],
			'japanesecoloredwool:japanesecoloredwool_25_ 3': [139,99,79],
			'japanesecoloredwool:japanesecoloredwool_25_ 4': [132,103,88],
			'japanesecoloredwool:japanesecoloredwool_25_ 5': [117,91,70],
			'japanesecoloredwool:japanesecoloredwool_25_ 6': [110,80,75],
			'japanesecoloredwool:japanesecoloredwool_25_ 7': [110,74,61],
			'japanesecoloredwool:japanesecoloredwool_25_ 8': [83,73,70],
			'japanesecoloredwool:japanesecoloredwool_25_ 9': [83,62,49],
			'japanesecoloredwool:japanesecoloredwool_25_ 10': [84,70,55],
			'japanesecoloredwool:japanesecoloredwool_25_ 11': [66,60,59],
			'japanesecoloredwool:japanesecoloredwool_25_ 12': [66,46,46],
			'japanesecoloredwool:japanesecoloredwool_25_ 13': [62,48,42],
			'japanesecoloredwool:japanesecoloredwool_25_ 14': [47,39,50],
			'japanesecoloredwool:japanesecoloredwool_25_ 15': [254,254,254],
			'japanesecoloredwool:japanesecoloredwool_26_ 0': [254,254,251],
			'japanesecoloredwool:japanesecoloredwool_26_ 1': [246,251,253],
			'japanesecoloredwool:japanesecoloredwool_26_ 2': [247,250,247],
			'japanesecoloredwool:japanesecoloredwool_26_ 3': [250,249,244],
			'japanesecoloredwool:japanesecoloredwool_26_ 4': [242,242,242],
			'japanesecoloredwool:japanesecoloredwool_26_ 5': [242,242,241],
			'japanesecoloredwool:japanesecoloredwool_26_ 6': [233,228,226],
			'japanesecoloredwool:japanesecoloredwool_26_ 7': [228,227,229],
			'japanesecoloredwool:japanesecoloredwool_26_ 8': [219,220,220],
			'japanesecoloredwool:japanesecoloredwool_26_ 9': [220,219,213],
			'japanesecoloredwool:japanesecoloredwool_26_ 10': [191,197,200],
			'japanesecoloredwool:japanesecoloredwool_26_ 11': [174,174,175],
			'japanesecoloredwool:japanesecoloredwool_26_ 12': [172,172,172],
			'japanesecoloredwool:japanesecoloredwool_26_ 13': [162,162,161],
			'japanesecoloredwool:japanesecoloredwool_26_ 14': [157,160,162],
			'japanesecoloredwool:japanesecoloredwool_26_ 15': [158,159,159],
			'japanesecoloredwool:japanesecoloredwool_27_ 0': [147,147,148],
			'japanesecoloredwool:japanesecoloredwool_27_ 1': [135,127,131],
			'japanesecoloredwool:japanesecoloredwool_27_ 2': [124,124,124],
			'japanesecoloredwool:japanesecoloredwool_27_ 3': [122,123,124],
			'japanesecoloredwool:japanesecoloredwool_27_ 4': [110,109,109],
			'japanesecoloredwool:japanesecoloredwool_27_ 5': [88,87,86],
			'japanesecoloredwool:japanesecoloredwool_27_ 6': [88,83,84],
			'japanesecoloredwool:japanesecoloredwool_27_ 7': [81,77,76],
			'japanesecoloredwool:japanesecoloredwool_27_ 8': [70,73,76],
			'japanesecoloredwool:japanesecoloredwool_27_ 9': [55,59,59],
			'japanesecoloredwool:japanesecoloredwool_27_ 10': [42,42,42],
			'japanesecoloredwool:japanesecoloredwool_27_ 11': [23,5,19],
			'japanesecoloredwool:japanesecoloredwool_27_ 12': [39,25,19],
			'japanesecoloredwool:japanesecoloredwool_27_ 13': [0,10,0],
			'japanesecoloredwool:japanesecoloredwool_27_ 14': [36,12,0],
			'japanesecoloredwool:japanesecoloredwool_27_ 15': [35,25,7],
			'japanesecoloredwool:japanesecoloredwool_28_ 0': [21,21,13]
			}

def sendMessage(hwnd, message):
	for tmp_char in message:
		tmp2_char = tmp_char.upper()
		if (tmp2_char >= '0' and tmp2_char <= '9') or (tmp2_char >= 'A' and tmp2_char <= 'Z') or tmp2_char == ' ':		
			win32api.keybd_event(ord(tmp2_char), 0, 0, 0)
			win32api.keybd_event(ord(tmp2_char), 0, win32con.KEYEVENTF_KEYUP, 0)
		elif tmp2_char == ':':
			# key: 'shift' 0x10
			win32api.keybd_event(0x10, 0, 0, 0)			
			# key: ':' 0xba 
			win32api.keybd_event(0xba, 0, 0, 0)
			win32api.keybd_event(0xba, 0, win32con.KEYEVENTF_KEYUP, 0)
			win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)
		elif tmp2_char == '_':
			# key: 'shift' 0x10
			win32api.keybd_event(0x10, 0, 0, 0)			
			# key: '_' 0xbd 
			win32api.keybd_event(0xbd, 0, 0, 0)
			win32api.keybd_event(0xbd, 0, win32con.KEYEVENTF_KEYUP, 0)
			win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)
		else:
			print 'Error! ' + tmp2_char + ' not in the database!'				
		time.sleep(0.001)
	# key: enter		
	time.sleep(0.1)
	win32api.keybd_event(13, 0, 0, 0)
	win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
	time.sleep(0.15)
	# key: '/' 0x6c 
	win32api.keybd_event(0xbf, 0, 0, 0)
	win32api.keybd_event(0xbf, 0, win32con.KEYEVENTF_KEYUP, 0)
	time.sleep(0.15)	

def setBlock(hwnd, x, y, z, block, location = []):
	if location	!= []:
		if max([np.abs(x-location[0]), np.abs(y-location[1]), np.abs(z-location[2])]) > 100:
			tpPosition(hwnd, x+1, y+1, z+1)
	else:
		tpPosition(hwnd, x+1, y+1, z+1)	
	tmp_coordinate = str(x) + ' ' + str(y) + ' ' + str(z)
	tmp_command = 'setblock ' + tmp_coordinate + ' ' + block
	print tmp_command
	sendMessage(hwnd, tmp_command)
	return [x+1, y+1, z+1]

def tpPosition(hwnd, x, y, z):
	tmp_coordinate = str(x) + ' ' + str(y) + ' ' + str(z)
	tmp_command = 'tp ' + tmp_coordinate
	print tmp_command
	sendMessage(hwnd, tmp_command)

def getBlock(color):
	tmp_color = np.array(color)
	tmp_num = 200000
	targetBlock = ''
	tmp2_num = 0
	for tmp_block in blockSet.keys():
		tmp2_num = np.sum((tmp_color - np.array(blockSet[tmp_block]))**2)
		if tmp2_num < tmp_num:
			tmp_num = tmp2_num
			targetBlock = tmp_block
	return targetBlock

#######################################
# world-creating program start
#######################################
# variables
tmp_hwnd = win32gui.FindWindow(None, 'Minecraft 1.7.10')
# tmp_hwnd=0x00170B72
# tmp_hwnd=0x0005022e
# tmp_hwnd=0x0005022e
color = [116, 116, 116]
block = getBlock(color)
location = [4000, 4, 3000]

# ##########################################
# # drawing using rbg.xlsx
# # this is used to draw 2D images
# ##########################################
# # reading data
# wb = open_workbook('rgb.xlsx')
# sh_r = wb.sheet_by_name('r')
# sh_g = wb.sheet_by_name('g')
# sh_b = wb.sheet_by_name('b')

# num_rows = sh_r.nrows
# num_cols = sh_r.ncols
# r_matrix = []
# for i in xrange(num_rows):
# 	tmp_line = []
# 	for j in xrange(num_cols):
# 		tmp_line.append(sh_r.cell_value(i, j))
# 	r_matrix.append(tmp_line)

# num_rows = sh_g.nrows
# num_cols = sh_g.ncols
# g_matrix = []
# for i in xrange(num_rows):
# 	tmp_line = []
# 	for j in xrange(num_cols):
# 		tmp_line.append(sh_g.cell_value(i, j))
# 	g_matrix.append(tmp_line)

# num_rows = sh_b.nrows
# num_cols = sh_b.ncols
# b_matrix = []
# for i in xrange(num_rows):
# 	tmp_line = []
# 	for j in xrange(num_cols):
# 		tmp_line.append(sh_b.cell_value(i, j))
# 	b_matrix.append(tmp_line)


# # drawing
# if tmp_hwnd:
# 	print 'tmp_hwnd', tmp_hwnd
# 	win32gui.ShowWindow(tmp_hwnd, 1)
# 	win32gui.SetForegroundWindow(tmp_hwnd)
# 	print 'window text', win32gui.GetWindowText(tmp_hwnd)
# 	print 'window class', win32gui.GetClassName(tmp_hwnd)
# 	time.sleep(1)

# 	tpPosition(tmp_hwnd, location[0], location[1], location[2])
# 	time.sleep(1)

# 	for i in xrange(num_rows):
# 		for j in xrange(num_cols):
# 			tmp_color = [r_matrix[i][j], g_matrix[i][j], b_matrix[i][j]]
# 			if color != tmp_color:
# 				color = tmp_color
# 				block = getBlock(color)
# 			location = setBlock(tmp_hwnd, 3500, 6+num_rows-i, 3500+j, block, location)

##########################################
# drawing using xyzColor.xlsx
# this is used to draw 3D images
##########################################
# reading data
wb = open_workbook('xyzColor.xlsx')
sh = wb.sheet_by_name('xyzColor')

num_rows = sh.nrows
num_cols = sh.ncols
xyzColor = []
tmp_xyzColor = []
for i in xrange(num_rows):
	tmp_xyzColor = []
	for j in xrange(num_cols):
		tmp_xyzColor.append(int(sh.cell_value(i, j)))
	xyzColor.append(tmp_xyzColor)

# drawing
if tmp_hwnd:
	print 'tmp_hwnd', tmp_hwnd
	win32gui.ShowWindow(tmp_hwnd, 1)
	win32gui.SetForegroundWindow(tmp_hwnd)
	print 'window text', win32gui.GetWindowText(tmp_hwnd)
	print 'window class', win32gui.GetClassName(tmp_hwnd)
	time.sleep(1)

	tpPosition(tmp_hwnd, location[0], location[1], location[2])
	time.sleep(1)

	for tmp_xyzColor in xyzColor:
		tmp_color = tmp_xyzColor[3:]
		if color != tmp_color:
			color = tmp_color
			block = getBlock(color)
		location = setBlock(tmp_hwnd, tmp_xyzColor[0], tmp_xyzColor[1], tmp_xyzColor[2], block, location)
