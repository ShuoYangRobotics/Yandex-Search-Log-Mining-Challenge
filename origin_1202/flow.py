import time
import commands
from getFeatures import *
from featureProcess import getAverage
from featureProcess import normalize
from rank import *
print '##################################'
print '#          Program start         #'
print '##################################'
print '-Stage 1- extract features..'
trainStruct = getFeatures(1)
print '-Stage 2- processing features..'
trainStruct = getAverage(trainStruct)
print '-Stage 3- normalizing features..'
trainStruct = normalize(trainStruct)

print '-Stage 4- generating training set for Weka..'
arffGen(trainStruct.region)
time.sleep(1)

print '-Stage 5- getting trained model parameters..'
beta = commands.getoutput("java WekaTester trainClickThrough.arff").split('\n')
intercept = float(beta[0])
beta = beta[1:len(beta)-1]
for i,item in enumerate(beta):
    beta[i] = float(item)
    print beta[i]

print '-Stage 6- get test set..'
test(intercept,beta)

print '-Stage 7- get final result..'
outGenerate()

