__author__ = 'abhi21'

def getSubStr(beginIndex, sliceWindow, word):
    return word[beginIndex: beginIndex + sliceWindow]


def updateFrequency(word, n):
    lenWord = len(word)
    for i in range(0, lenWord):
        for sliceWindow in range(1,n):
            noOfRemChars = len(word[i:])
            if (noOfRemChars >= sliceWindow):
                subStr = getSubStr(i, sliceWindow, word)
                context = subStr[i:sliceWindow-1]
                char = subStr[sliceWindow]