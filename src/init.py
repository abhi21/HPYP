__author__ = 'abhi21'

#import numpy as num
import random

n = 2
modelDict = {}
restaurantNames ={}
totalIncrements = 0
global index
index = -1
characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
totalTableStr = 'totalTables'

allContexts = []
allChars = []
allTables = []
qu = 10
du = 1

custCountStr = 'custCount'


def initializeList():
    freq = {custCountStr: 0, totalTableStr:0, 'a':[0,qu,du],'b':[0,qu,du],'c':[0,qu,du],'d':[0,qu,du],'e':[0,qu,du],'f':[0,qu,du],'g':[0,qu,du],'h':[0,qu,du],'i':[0,qu,du],'j':[0,qu,du],'k':[0,qu,du],'l':[0,qu,du],'m':[0,qu,du],'n':[0,qu,du],'o':[0,qu,du],'p':[0,qu,du],'q':[0,qu,du],'r':[0,qu,du],'s':[0,qu,du],'t':[0,qu,du],'u':[0,qu,du],'v':[0,qu,du],'w':[0,qu,du],'x':[0,qu,du],'y':[0,qu,du],'z':[0,qu,du]}
    return freq;


def makeKey(k,n):
    if n-1==0:
        restaurantNames[k] = k
    else:
        restaurantNames[k] = k
        for item in characters:
            itemK = item + k
            makeKey(itemK, n-1)

def getSubStr(beginIndex, sliceWindow, word):
    return word[beginIndex: beginIndex + sliceWindow]



makeKey('',n)

for key in restaurantNames:
    modelDict[restaurantNames[key]] = initializeList()
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
            nTable = len(modelDict[context][char]) - 3
            tableNumber = random.randrange(0, nTable+1,1)
            if tableNumber in modelDict[context][char][3:nTable]:
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

def assertInitialization():
    for key in restaurantNames:
        for char in characters:
            freq = modelDict[key][char][0]
            sumCustomers = sum(modelDict[key][char])-freq-qu-du
            print('Freq: ' + str(freq) + 'Customers' + str(sumCustomers))

def wordProb(context, char):
    if(context == ''):
        return 1/26
    else:
        cuw = modelDict[context][char][0]
        qu = modelDict[context][char][1]
        du = modelDict[context][char][2]
        tuw = len(modelDict[context][char]) - 3
        cu = modelDict[context][custCountStr]
        tu = modelDict[context][totalTableStr]
        selfProb = (cuw - (du*tuw))/(qu + cu)
        baseProb = (qu + (du*tu))/(qu+cu)
        context = context[1:len(context)]
        return selfProb + (baseProb*wordProb(context,char))


with open("data/dist_female_first.txt", "r") as f:
  for line in f:
    name = line.split()[0]
    updateFrequency(name,n)
  assertInitialization()

#print(totalIncrements)

#or key in keysDict:
#   print('\nKey: ' + key)
#   print(modelDict[key])

for key in restaurantNames:
    for dish in modelDict[key]:
        if dish != custCountStr and dish != totalTableStr:
            modelDict[key][custCountStr] += modelDict[key][dish][0]
            modelDict[key][totalTableStr] += len(modelDict[key][dish]) - 3

for key in restaurantNames:
   print('\nKey: ' + key)
   print('Cust '+str(modelDict[key][custCountStr]) + "  TableCount: "+ str(modelDict[key][totalTableStr]))



