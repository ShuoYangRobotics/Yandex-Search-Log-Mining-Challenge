def checkMinMax(value,region,pos,s):
    if value < s.minMax[region][pos][0]:
        s.minMax[region][pos][0] = value
    if value > s.minMax[region][pos][1]:
        s.minMax[region][pos][1] = value
    return

def getAverage(s):
    for i,r in enumerate(s.region):
        for query in r:
            for url in r[query]:
                count = float(r[query][url][1])
                clickFreq = float(r[query][url][5]+1)
                #1 position 
                r[query][url][0] = round(r[query][url][0]/count,6)            
                checkMinMax(r[query][url][0],i,0,s)
                #2 count 
                r[query][url][1] = round(r[query][url][1]/s.queryCount[i][query],6)            
                checkMinMax(r[query][url][1],i,1,s)
                #3 isTop1
                r[query][url][2] = round(r[query][url][2]/count,6)
                checkMinMax(r[query][url][2],i,2,s)
                #4 is Top3
                r[query][url][3] = round(r[query][url][3]/count,6)
                checkMinMax(r[query][url][3],i,3,s)
                #5 is Top5
                r[query][url][4] = round(r[query][url][4]/count,6)
                checkMinMax(r[query][url][4],i,4,s)
                #6 clickFreq don't have to take average
                checkMinMax(r[query][url][5],i,5,s)
                #7 clickProb
                r[query][url][6] = round(r[query][url][6]/count,6)
                checkMinMax(r[query][url][6],i,6,s)
                #8 clickDevi
                r[query][url][7] += r[query][url][6]
                checkMinMax(r[query][url][7],i,7,s)
                #9 isClickAbove
                r[query][url][8] = round(r[query][url][8]/count,6)
                checkMinMax(r[query][url][8],i,8,s)
                #10 isClickBelow
                r[query][url][9] = round(r[query][url][9]/count,6)
                checkMinMax(r[query][url][9],i,9,s)
                #11 isNextClicked
                r[query][url][10] = round(r[query][url][10]/count,6)
                checkMinMax(r[query][url][10],i,10,s)
                #12 isPreviousClicked
                r[query][url][11] = round(r[query][url][11]/count,6)
                checkMinMax(r[query][url][11],i,11,s)
                #13 isFirstClicked
                r[query][url][12] = round(r[query][url][12]/clickFreq,6)
                checkMinMax(r[query][url][12],i,12,s)
                #14 isLastClicked
                r[query][url][13] = round(r[query][url][13]/clickFreq,6)
                checkMinMax(r[query][url][13],i,13,s)
                #15 dwellTimeBefore
                r[query][url][14] = \
                round(r[query][url][14]/(s.dwellCount[i][query][url][0]+1),6)
                checkMinMax(r[query][url][14],i,14,s)
                #16 dwellTimeAfter
                r[query][url][15] = \
                round(r[query][url][15]/(s.dwellCount[i][query][url][1]+1),6)
                checkMinMax(r[query][url][15],i,15,s)
                #17 clickTimeAfterQuery
                r[query][url][16] = round(r[query][url][16]/clickFreq,6)
                checkMinMax(r[query][url][16],i,16,s)
                #18 clickTimeInSession
                r[query][url][17] = round(r[query][url][17]/clickFreq,6)
                checkMinMax(r[query][url][17],i,17,s)
                #19 onlyOneClick
                try:
                    r[query][url][18] = \
                    round(r[query][url][18]/s.oneClickUrlAppear[i][query][url],6)
                except KeyError:
                    pass
                checkMinMax(r[query][url][18],i,18,s)

                #20 onlyOneClick2
                r[query][url][19] = round(r[query][url][19]/count,6)
                checkMinMax(r[query][url][19],i,19,s)
                #21 countURLClicked
                r[query][url][20] = s.urlClickedCount[i][url]
                checkMinMax(r[query][url][20],i,20,s)
    return s
            
def normalize(s):
    for i,r in enumerate(s.region):
        for query in r.keys():
            for url in r[query].keys():
                for j,value in enumerate(r[query][url]):
                    if j == len(r[query][url])-1:
                        continue
                    try:
                        value = (value - s.minMax[i][j][0])/(s.minMax[i][j][1] - s.minMax[i][j][0])
                    except ZeroDivisionError:
                        value = 0.5

                    s.region[i][query][url][j] = value
    return s
