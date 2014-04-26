__author__ = 'abhi21'

listOfSubStrs = []

def cutChars(beginIndex, sliceWindow, word):
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
print(len(inputWord))
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
