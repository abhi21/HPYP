__author__ = 'abhi21'

listOfSubStrs = []

def cutChars(beginIndex, sliceWindow, word):
    return word[beginIndex: beginIndex + sliceWindow]

def getSubStr(beginIndex, sliceWindow, word):
    return word[beginIndex: beginIndex + sliceWindow]

def generateNgrams(word, n):
    lenWord = len(word)
    for i in range(0, lenWord):
        for sliceWindow in range(1,n):
            noOfRemChars = len(word[i:])
            if (noOfRemChars >= sliceWindow):
                listOfSubStrs.append(cutChars(i, sliceWindow, word))
    print(listOfSubStrs)

inputWord = 'Hello!!'
#print(len(inputWord))
generateNgrams(inputWord,3)


def updateFrequencyOld(word, n, totalIncrements):
    word = word.lower()
    lenWord = len(word)
    for i in range(0, lenWord):
        for sliceWindow in range(1,n):
            noOfRemChars = len(word[i:])
            if (noOfRemChars >= sliceWindow):
                subStr = getSubStr(i, sliceWindow, word)
                lenSubStr = len(subStr)
                if lenSubStr == 1:
                    modelDict[''][subStr][0] += 1
                    totalIncrements +=1
                else:
                    context = subStr[:lenSubStr-1]
                    char = subStr[lenSubStr -1:lenSubStr]
                    #print(char)
                    modelDict[context][char][0] += 1
                    totalIncrements +=1


#Checks
sumForNull = modelDict['']['custCount']
sumForAll = 0
for key in keysDict:
    sumForAll += modelDict[key]['custCount']
sumForAll -= sumForNull

print(sumForNull)
print(sumForAll)



#updateFrequency('AbhiAb',n)

#print(modelDict['']['a'][0])
#print(modelDict['a']['b'][0])
#print(modelDict['ab']['h'][0])
#print(modelDict['']['b'][0])
#print(modelDict['b']['h'][0])
#print(modelDict['bh']['i'][0])
#print(modelDict['']['h'][0])
#print(modelDict['h']['i'][0])
#print(modelDict['']['i'][0])

#modelDict['a']['a'][0] = modelDict['a']['a'][0] + 2
#print(modelDict['a']['a'][0])
#
#for key in keysDict:
#    print('\nKey: ' + key)
#    #print(modelDict[key])


###########################################################Partition


def initializeTables(word):
    word = word.lower()
    wordLen = len(word)

    for i in range(0, wordLen):
        tempN = n
        psc = i
        while((psc >= 0) and (tempN - 1 >=0)):
            psc = psc-1
            tempN = tempN - 1
            context = word[psc + 1:i]
            #print('Context:' + context)
            char = word[i:i + 1]
            #print('Char: ' + char)
            modelDict[context][char][0] += 1
