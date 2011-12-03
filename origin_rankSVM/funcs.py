import os
import string
from collections import defaultdict
def binary_search(x, a, lo=0, hi=None):
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        midval = a[mid]
        if midval < x:
            lo = mid+1
        elif midval > x: 
            hi = mid
        else:
            return mid
    return -1

"""
input:  one line of the raw log file
output: 
    pos 0           1   2       3       4       5
        sessionID   Q   region  time    queryID    urls
        sessionID   C   urlID   time    
"""
def parseLine(string):
    strlist = string.split('\n')[0].split('\t')
    
    time = strlist[1]
    sessionID = strlist[0]
    if strlist[2] == 'Q':
        urls = strlist[5:]
        queryID = strlist[3]
        region = strlist[4]
        return (sessionID, 'Q', region, time, queryID, urls)
    elif strlist[2] == 'C':
        urlID = strlist[3] 
        return (sessionID, 'C', urlID, time)

def extractTraining():
    qlist=[]
    dlist=[]
    f = open('../txt/Testq.txt','rb')
    for line in f:
        tmp = line.split('\t')
        q = tmp[0]
        qlist.append(int(q))
    f.close()
    qlist = sorted(list(set(qlist)))
    return qlist
        
def suitable(query,doclist,qlist):
    if binary_search(int(query),qlist)!=-1:
        return 1
    return 0
    
def getRaw():
    fileList = sorted(os.listdir('data/'))
    for i,item in enumerate(fileList):
        if item[0]!='x':
            fileList.pop(i)
    
    #qlist,dlist = extractTraining()
    qlist = extractTraining()

    count = 0
    MAX = 1000
    recording = 0
    while count < MAX:
        c = (count+1)/float(MAX)
        print "%6f%%"%(c*100)
        test = fileList[count]
        f = open('../data/'+test,'rb')
        y = open("../testRaw/"+test+"_extracted.txt",'wb')
        for line in f: 
            rst = parseLine(line)
            if rst[0] == 'Q':
                if suitable(rst[3],rst[4],qlist):
                    recording = 1 
                    y.write(line)
                else: 
                    recording = 0
            elif rst[0] == 'C':
                if recording == 1:
                    y.write(line)       
                else:
                    pass
        f.close()
        y.close()
        count+=1
