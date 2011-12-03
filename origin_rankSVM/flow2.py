import time
import commands
import getFeatures2 
from rank2 import *
print '##################################'
print '#          Program start         #'
print '##################################'
print '-Stage 1- extract features..'
#trainStruct = getFeatures(1)

print '-Stage 2- processing features..'
#trainStruct = getAverage(trainStruct)
print '-Stage 3- normalizing features..'
#trainStruct = normalize(trainStruct)

#import json
#b = json.dumps(trainStruct.region)
#f = open("trainstruct_region.json",'wb')
#f.write(b)
#f.close()

print '-Stage 4- generating training set for SVMRank..'
#getFeatures2.svmRankGen(trainStruct.region)
#time.sleep(1)

print '-Stage 5- getting trained model parameters..'
#os.system('svm_rank_learn -c 20.0 clickThrough.dat model.dat')
#time.sleep(1)
f = open('model.dat','rb')
beta = f.readlines()[-1].split(" ")
beta = beta[1:len(beta)-1]
for i,item in enumerate(beta):
    beta[i] = float(item.split(":")[1])

intercept = 0
for i,item in enumerate(beta):
    beta[i] = float(item)
    print beta[i]

print '-Stage 6- get test set..'
test(intercept,beta)

print '-Stage 7- get final result..'
outGenerate()


