import os
from ordereddict import OrderedDict
from getRegionFeatures import *
import datetime

def dot_product(a, b):
    return reduce(lambda sum, p: sum + p[0]*p[1], zip(a,b), 0)
    
def outGenerate():
    rst = defaultdict(list)

    outF = open('../txt/finalResult'+ \
    datetime.datetime.now().strftime("%d-%b-%Y-%I-%M")+'.txt','wb')

    g = open('../txt/result.txt','rb')
    for line in g:
        try:
            tmp = line.split('\n')[0].split(" ")
            key = tmp[0]+" "+tmp[1]
        except IndexError:
            print tmp 
        rst[key]=tmp[2:]
    g.close()

    f = open('../txt/Testq.txt','rb')
    for line in f:
        tmp = line.split('\n')[0].split("\t")
        key = tmp[0]+" "+tmp[1]
        out = tmp[0]+'\t'+tmp[1]
        for i in range (0,len(rst[key])):
            out +='\t'+rst[key][i]
        outF.write(out)
        outF.write('\n')
    f.close()

def test(intercept, featureWeight):
    testFeatures = getFeatures(0)
    region = testFeatures.region
    score = []
    for i in range(len(region)):
        score.append({})
    fOut = open("../txt/result.txt",'w')
    for i in range(len(region)):
        for query in region[i]:
            score[i][query] = {}
            for url in region[i][query]:
                score[i][query][url] = \
                dot_product(region[i][query][url],featureWeight) + intercept
            url_sorted_by_value = OrderedDict(sorted(score[i][query].items(), key=lambda x: x[1]))
            url_sorted_by_value_r = list(reversed(url_sorted_by_value))
            out = str(query) + " " + str(i) + " "
            for u in url_sorted_by_value_r:
                out = out + str(u) + " "
            out = out+ "\n"
            fOut.write(out)
