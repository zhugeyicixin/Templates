import chem
import copy

class A:
    A1=[]
    A2='this is A2'

class B:
    B1 = []
    B2 = 'this is B2'

instance_A = A()
instance_B = B()
instance_A.A1.append(instance_B)
instance_B.B1.append(instance_A)
print instance_A.A2
print instance_A.A1[0].B1[0].A1[0].B1[0].A1[0].B1[0].A1[0].B1[0].A2
instance_C = copy.deepcopy(instance_A)
print instance_C.A1[0].B2
instance_D = copy.deepcopy(instance_B)
print instance_D.B1[0].A2

# a=[234.23423]
# print [str(x) for x in a]

reactionSystem1 = chem.reactionSystem()
reactionSystem1.setFreqScale(0.95)

print chem.reactionSystem.freqScaleFactor
# chem.reactionSystem.setFreqScale(0.97)
print chem.reactionSystem.freqScaleFactor

reactionSystem2 = chem.reactionSystem()
reactionSystem2.setFreqScale(0.93)

print reactionSystem1.freqScaleFactor
print reactionSystem2.freqScaleFactor

a={'asg':'adga','dhh':'ahag'}
print a.keys()

