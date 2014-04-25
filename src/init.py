__author__ = 'abhi21'

n = 3
modelDict = {}
keysDict ={}
context = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def initializeList():
    freq = {'a':[0],'b':[0],'c':[0],'d':[0],'e':[0],'f':[0],'g':[0],'h':[0],'i':[0],'j':[0],'k':[0],'l':[0],'m':[0],'n':[0],'o':[0],'p':[0],'q':[0],'r':[0],'s':[0],'t':[0],'u':[0],'v':[0],'w':[0],'x':[0],'y':[0],'z':[0]}
    return freq;


def makeKey(k,n):
    if n-1==0:
        keysDict[k] = k
    else:
        keysDict[k] = k
        for item in context:
            itemK = item + k
            makeKey(itemK, n-1)

def getSubStr(beginIndex, sliceWindow, word):
    return word[beginIndex: beginIndex + sliceWindow]


def updateFrequency(word, n):
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
                else:
                    context = subStr[:lenSubStr-1]
                    char = subStr[lenSubStr -1:lenSubStr]
                    #print(char)
                    modelDict[context][char][0] += 1

makeKey('',n)

for key in keysDict:
    modelDict[keysDict[key]] = initializeList()
    #print ('Key: ' + key + ' \t')
    #print(modelDict[keysDict[key]])

updateFrequency('AbhiAb',n)

print(modelDict['']['a'][0])
print(modelDict['a']['b'][0])
print(modelDict['ab']['h'][0])
print(modelDict['']['b'][0])
print(modelDict['b']['h'][0])
print(modelDict['bh']['i'][0])
print(modelDict['']['h'][0])
print(modelDict['h']['i'][0])
print(modelDict['']['i'][0])

#modelDict['a']['a'][0] = modelDict['a']['a'][0] + 2
#print(modelDict['a']['a'][0])

file = open('train.txt', 'r').read()









