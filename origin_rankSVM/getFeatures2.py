import os
from collections import defaultdict
class param:
    def __init__(self):
        region =[]
        dwellCount =[]
        urlClickedCount = []
        queryCount = []
        oneClickUrlAppear = []
        minMax = []
        for i in range(0,4):
            self.region.append(defaultdict(dict)) 
            self.dwellCount.append(defaultdict(dict)) 
            self.urlClickedCount.append(defaultdict(float))
            self.queryCount.append(defaultdict(float))
            self.oneClickUrlAppear.append(defaultdict(dict))
            self.minMax.append([])
            for j in range(0,21):
                self.minMax[i].append([9999,-9999])
    grossClick = 0L
    posClick = [0L,0L,0L,0L,0L,0L,0L,0L,0L,0L]
    region =[]
    dwellCount =[]
    urlClickedCount = []
    queryCount = []
    oneClickUrlAppear = []
    minMax = []

def parsePrevSession(session,data,ecp,struct,switch):
    session = session[1:]
    for i,item in enumerate(session):
        if i == 0:
            if len(session) ==1:
                parseQCList(item,data,ecp,struct,switch,
                    None,None)
            else:
                parseQCList(item,data,ecp,struct,switch,
                    None,session[1][0])

        elif i == len(session)-1:
            if len(session) ==1:
                parseQCList(item,data,ecp,struct,switch,
                    None,None)
            else:
                parseQCList(item,data,ecp,struct,switch,
                    session[i-1][-1],None)
        else:
            parseQCList(item,data,ecp,struct,switch,
                session[i-1][-1],session[i+1][0])

def parseQCList(QCList,data,ecp,struct,switch,itemBefore,itemAfter):
    #print QCList
    if QCList == []:
        return
    region = int(QCList[0][1])
    query = QCList[0][3]
    queryTime = int(QCList[0][2])
    clickActions = QCList[1:]
    totalClick = len(clickActions)
    struct.queryCount[region][query] +=1

    for i,url in enumerate(QCList[0][4]):
        #position
        position = -(i+1)

        #isTop1,3,5
        isTop1 = 0
        isTop3 = 0
        isTop5 = 0
        if i == 0:
            isTop1 = 1
            isTop3 = 1
            isTop5 = 1
        elif i < 3:
            isTop3 = 1
            isTop5 = 1
        elif i < 5:
            isTop5 = 1

        #Above,Below,Next,Previous        
        AboveList = QCList[0][4][:i]
        BelowList = QCList[0][4][i+1:]
        if i != 9:
            Next = QCList[0][4][i+1]
        else:
            Next = None
        if i != 0:
            Previous = QCList[0][4][i-1]
        else:
            Previous = None

        #clickFreq, get features about clicks, by default they are all 0
        isClickAbove = 0 
        isClickBelow = 0
        isPreviousClicked = 0
        isNextClicked= 0        
        isFirstClicked = 0
        isLastClicked = 0
        onlyOneClick = 0
        clickFreq = 0

        #time related features
        dwellTimeBefore = 0
        dwellTimeAfter = 0
        clickTimeAfterQuery = 0 
        clickTimeInSession = 0 

        if switch == 1:
            try:
                touch = struct.region[region][query][url][1]
            except KeyError:
                #label
                if getLabels(str(region),str(query),str(url),data):
                    label = "+"
                else:
                    label = "-"
                struct.region[region][query][url] = \
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,label]
                struct.dwellCount[region][query][url]=[0,0]
        else:
            try:
                touch = struct.region[region][query][url][1]
            except KeyError:
                struct.region[region][query][url] = \
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                struct.dwellCount[region][query][url]=[0,0]
                struct.oneClickUrlAppear[region][query][url] = 1.0

        if totalClick != 0:
            for j,action in enumerate(clickActions):
                if action[1] == url:
                    if j == 0:
                        isFirstClicked = 1

                        if totalClick == 1:
                            for u in QCList[0][4]:
                                if query in struct.oneClickUrlAppear[region]:
                                    if u in struct.oneClickUrlAppear[region][query]:
                                        struct.oneClickUrlAppear[region][query][u]+=1
                                    else:
                                        struct.oneClickUrlAppear[region][query][u] = 1
                                else:
                                    struct.oneClickUrlAppear[region][query] = {}
                                    struct.oneClickUrlAppear[region][query][u] = 1
                            onlyOneClick = 1
                        if itemBefore != None:
                            struct.dwellCount[region][query][url][0] += 1
                            dwellTimeBefore = int(action[2]) - \
                            int(itemBefore[2])
                        else:
                            dwellTimeBefore = -1
                        if totalClick ==1:
                            pass
                        else:
                            struct.dwellCount[region][query][url][1] += 1
                            dwellTimeAfter = int(clickActions[j+1][2]) - \
                            int(action[2])

                    elif j == totalClick-1:
                        isLastClicked = 1
                        if itemAfter != None:
                            struct.dwellCount[region][query][url][1] += 1
                            dwellTimeAfter = int(itemAfter[2]) - \
                            int(action[2])
                        else:
                            dwellTimeAfter = -1
                        if totalClick ==1:
                            pass
                        else:
                            struct.dwellCount[region][query][url][0] += 1
                            dwellTimeBefore = int(action[2]) -\
                            int(clickActions[j-1][2])
                    else:
                        struct.dwellCount[region][query][url][0] += 1
                        dwellTimeBefore = int(action[2]) - \
                        int(clickActions[j-1][2])
                        struct.dwellCount[region][query][url][1] += 1
                        dwellTimeAfter = int(clickActions[j+1][2]) - \
                        int(action[2])

                    clickFreq+=1
                    clickTimeInSession = int(action[2]) 
                    clickTimeAfterQuery = clickTimeInSession - queryTime 
           
                elif action[1] in AboveList:
                    isClickAbove = 1
                    if action[1] == Previous:
                        isPreviousClicked = 1
                elif action[1] in BelowList:
                    isClickBelow = 1
                    if action[1] == Next:
                        isNextClicked = 1

        #1 position 
        struct.region[region][query][url][0] += position
        #2 count 
        struct.region[region][query][url][1] += 1
        #3 isTop1 
        struct.region[region][query][url][2] += isTop1
         #4 isTop3
        struct.region[region][query][url][3] += isTop3
        #5 isTop5 
        struct.region[region][query][url][4] += isTop5
        #6 clickFreq 
        struct.region[region][query][url][5] += clickFreq
        #7 clickProb 
        struct.region[region][query][url][6] += clickFreq 
        #8 clickDevi 
        struct.region[region][query][url][7] = -ecp[i] 
        #9 isClickAbove 
        struct.region[region][query][url][8] += isClickAbove
        #10 isClickBelow
        struct.region[region][query][url][9] += isClickBelow 
        #11 isPreviousClicked
        struct.region[region][query][url][10] += isPreviousClicked
        #12 isNextClicked 
        struct.region[region][query][url][11] += isNextClicked
        #13 isFirstClicked 
        struct.region[region][query][url][12] += isFirstClicked
        #14 isLastClicked 
        struct.region[region][query][url][13] += isLastClicked
        #15 dwellTimeBefore
        if dwellTimeBefore != -1:
            struct.region[region][query][url][14] += dwellTimeBefore 
        #16 dwellTimeAfter
        if dwellTimeAfter != -1:
            struct.region[region][query][url][15] += dwellTimeAfter
        #17 clickTimeAfterQuery
        struct.region[region][query][url][16] += clickTimeAfterQuery
        #18 clickTimeInSession
        struct.region[region][query][url][17] += clickTimeInSession
        #19 onlyOneClick 
        struct.region[region][query][url][18] += onlyOneClick
        #20 onlyOneClick2 
        struct.region[region][query][url][19] += onlyOneClick
        #21 countUrlClicked
        struct.urlClickedCount[region][url] += clickFreq

        #print str(position)+",",
        #print str(currCount)+",",
        #print str(isTop1)+",",
        #print str(isTop3)+",",
        #print str(isTop5)+",",
        #print str(clickFreq)+",",
        #print str(clickFreq)+",",
        #print str(-ecp[i])+",",
        #print str(isClickAbove)+",",
        #print str(isClickBelow)+",",
        #print str(isPreviousClicked)+",",
        #print str(isNextClicked)+",",
        #print str(isFirstClicked)+",",
        #print str(isLastClicked)+",",
        #print str(dwellTimeBefore)+",",
        #print str(dwellTimeAfter)+",",
        #print str(clickTimeAfterQuery)+",",
        #print str(clickTimeInSession)+",",
        #print str(onlyOneClick)+",",
        #print str(onlyOneClick)

def parseTrain():
    data = defaultdict(dict)
    f = open('../txt/Trainq.txt','rb')
    a = f.readlines()
    for line in a:
        tmp = line.split('\n')[0].split('\t')
        region = str(tmp[1])
        data[region] = defaultdict(list)
    for line in a:
        tmp = line.split('\n')[0].split('\t')
        query = tmp[0]
        region = tmp[1]
        url = tmp[2]
        label = tmp[3]
        data[region][query].append((url,label))
    
    return data


def getLabels(region,query,url,data):
    tmp = data[region][query]
    for item in tmp:
        if int(url) == int(item[0]):
            return int(item[1])
    return 0

def getEcp():
    a = open('../txt/ecp_1000.txt','rb')
    b = a.readlines()
    c = [] 
    for item in b:
        c.append(float(item.split('\n')[0]))
    return c

def saveEcp(newEcp):
    a = open('../txt/ecp.txt','wb')
    for item in newEcp:
        a.write(str(item))
        a.write('\n')

'''
input: 
        if switch is 1, this extract trainRaw
        if switch is 0, this extract testRaw
'''
def getFeatures(switch):
    if switch == 1:
        path = '../trainRaw/'
    elif switch == 0:
        path = '../testRaw/'
    else:
        print 'Error: please indicate your action type'
        return

    from funcs import parseLine
    import os
    fileList = sorted(os.listdir(path))
    for i,item in enumerate(fileList):
        if item[0]!='x':
            fileList.pop(i)
    data = parseTrain()
    ecp = getEcp()
    struct = param()
    
    count = 0
    MAX = 1000
    #MAX = 2

    import time
    t0 = time.mktime(time.localtime())
    print "start\t\ttime:\t0.0"
    session = []
    subsession = []
    recording = -1
    while count < MAX:
        c = (count+1)/float(MAX)
        name = fileList[count]
        f = open(path+name,'rb')
        #a = f.readlines()
        #for line in a[1000:1050]: 
        for line in f: 
            rst = parseLine(line)
            sessionID = int(rst[0])

            if rst[1] == 'Q':
                if subsession != []:
                    session.append(subsession)
                subsession = []
                subsession.append(rst[1:]) 
            elif rst[1] == 'C':
                subsession.append(rst[1:]) 
            if sessionID != recording:
                recording = sessionID
                if (session !=[]):
                    parsePrevSession(session,data,ecp,struct,switch)
                session = []
                session.append(sessionID)

        f.close()
        count+=1
        t1 = time.mktime(time.localtime())
        print "%.2f%%\t\ttime:\t%.2f"%(c*100,float(t1-t0))

    return struct

def arffGen(regionList):
    file = open("trainClickThrough.arff",'w')
    file.write("@relation ClickThrough\n")
    file.write("\n") 
    file.write("@attribute position numeric\n")
    file.write("@attribute count numeric\n")
    file.write("@attribute isTop1 numeric\n")
    file.write("@attribute isTop3 numeric\n")
    file.write("@attribute isTop5 numeric\n")
    file.write("@attribute clickFreq numeric\n")
    file.write("@attribute clickProb numeric\n")
    file.write("@attribute clickDevi numeric\n")
    file.write("@attribute clickAbove numeric\n")
    file.write("@attribute clickBelow numeric\n")
    file.write("@attribute isPreviousClicked numeric\n")
    file.write("@attribute isNextClicked numeric\n")
    file.write("@attribute isFirstClicked numeric\n")
    file.write("@attribute isLastClicked numeric\n")
    file.write("@attribute dwellTimeBefore numeric\n")
    file.write("@attribute dwellTimeAfter numeric\n")
    file.write("@attribute clickTimeAfterQuery numeric\n")
    file.write("@attribute clickTimeInSession numeric\n")
    file.write("@attribute onlyOneClick numeric\n")
    file.write("@attribute onlyOneClick2 numeric\n")
    file.write("@attribute countURLClicked numeric\n")
    file.write("@attribute Class {+,-}\n")
    file.write("\n") 
    file.write("@data\n")
    for r in regionList:
        for query in r:
            for url in r[query]:
                out = ""
                for i in range(len(r[query][url])):
                    out = out + str(r[query][url][i])
                    if i != len(r[query][url]) -1:
                        out = out + ","
                file.write(out + "\n")

def svmRankGen(region):
    sortedKeyList = []
    for i in range(len(region)):
        sortedKeyList.append([])
        sortedKeyList[i] = region[i].keys()
        for j in range(len(sortedKeyList[i])):
            sortedKeyList[i][j] = int(sortedKeyList[i][j])
        sortedKeyList[i].sort()
        for j in range(len(sortedKeyList[i])):
            sortedKeyList[i][j] = str(sortedKeyList[i][j])

    file = open("clickThrough.dat",'w')
    count = 1
    for i,r in enumerate(region):
        for key in sortedKeyList[i]:
            #print count
            file.write( "#region " + str(i) + " query " + str(key) + "\n")
            for url in r[key]:
                out = ""
                if r[key][url][len(r[key][url])-1] == '+':
                    out += "1 "
                else:
                    out += "0 "
                out = out + "qid:" + str(count) + " "                 
                for j in range(len(r[key][url])-1):
                    out = out + str(j+1) +":"+str(r[key][url][j]) + " "
                out = out + "#url:" + str(url) +"\n"
                file.write(out)
            count = count + 1
