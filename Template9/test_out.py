import sys
import subprocess
import time
import THERMcalc

fileName = 'comb2'

cmd = ['therm.exe']
p = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print p.poll()
THERMcalc.start(p)
p.stdin.write('8\n' + fileName + '\n' + fileName + '\n1\n')
print 'input:\t8\\n' + fileName + '\\n' + fileName + '\\n1\\n'
# p.stdin.write('\n')
# print 'input:\t\\n'
print 'output:'
THERMcalc.readOut(p,6)

THERMcalc.kill(p)
print 'ThermFit end successfully!'


# print ("Hello")
# # sys.stdout.flush()
# content=raw_input("input1:")
# print content
# # sys.stdout.flush()
# content=raw_input("input2:")
# print content
# # sys.stdout.flush()
# for i in range(0,10):
# 	time.sleep(0.1)
# content=raw_input("input3:")
# print content
# # sys.stdout.flush()
# print ("World")
# # sys.stdout.flush()