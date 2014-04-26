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