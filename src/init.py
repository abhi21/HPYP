__author__ = 'abhi21'

#import numpy as num
import random

n = 2
modelDict = {}
keysDict ={}
totalIncrements = 0
global index
index = -1
characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

allContexts = []
allChars = []
allTables = []

def initializeList():
    freq = {'a':[0],'b':[0],'c':[0],'d':[0],'e':[0],'f':[0],'g':[0],'h':[0],'i':[0],'j':[0],'k':[0],'l':[0],'m':[0],'n':[0],'o':[0],'p':[0],'q':[0],'r':[0],'s':[0],'t':[0],'u':[0],'v':[0],'w':[0],'x':[0],'y':[0],'z':[0]}
    return freq;


def makeKey(k,n):
    if n-1==0:
        keysDict[k] = k
    else:
        keysDict[k] = k
        for item in characters:
            itemK = item + k
            makeKey(itemK, n-1)

def getSubStr(beginIndex, sliceWindow, word):
    return word[beginIndex: beginIndex + sliceWindow]



makeKey('',n)

for key in keysDict:
    modelDict[keysDict[key]] = initializeList()
    #print ('Key: ' + key + ' \t')
    #print(modelDict[keysDict[key]])


def updateFrequency(word, n):
    word = word.lower()
    wordLen = len(word)
    nTable = 0

    for i in range(0, wordLen):
        tempN = n
        psc = i

        while((psc >= 0) and (tempN - 1 >=0)):
            global index
            index = index + 1
            psc = psc-1
            tempN = tempN - 1
            context = word[psc + 1:i]
            #print('Context:' + context)
            char = word[i:i + 1]
            #print('Char: ' + char)
            modelDict[context][char][0] += 1
            allContexts.append(context)
            allChars.append(char)
            nTable = len(modelDict[context][char]) - 1
            tableNumber = random.randrange(0, nTable+1,1)
            if tableNumber in modelDict[context][char][1:nTable]:
                modelDict[context][char][tableNumber] += 1
            else:
                modelDict[context][char].append(1)
            allTables.append(tableNumber)


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

def assertInitialization():
    for key in keysDict:
        for char in characters:
            freq = modelDict[key][char][0]
            sumCustomers = sum(modelDict[key][char])-freq
            print('Freq: ' + str(freq) + 'Customers' + str(sumCustomers))


with open("data/dist_female_first.txt", "r") as f:
  for line in f:
    name = line.split()[0]
    updateFrequency(name,n)
  assertInitialization()

#print(totalIncrements)

#or key in keysDict:
#   print('\nKey: ' + key)
#   print(modelDict[key])






