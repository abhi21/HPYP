__author__ = 'abhi21'

#import numpy as num
import random

n = 2
modelDict = {}
restaurantNames ={}
totalIncrements = 0
global index
index = -1

global loopC
loopC = 0
characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
totalTableStr = 'totalTables'
custCountStr = 'custCount'

allContexts = []
allChars = []
allTables = []
qu = .8
du = .2
quStr = 'qu'
duStr = 'du'


def initializeList():
    freq = {custCountStr: 0, totalTableStr:0, quStr: qu, duStr: du}
    for item in characters:
        freq[item] = [0]
    return freq

def makeKey(k,n):
    if n-1==0:
        restaurantNames[k] = k
    else:
        restaurantNames[k] = k
        for item in characters:
            itemK = item + k
            makeKey(itemK, n-1)

#Generating restaurantNames from n
makeKey('',n)

#Generating Main Dictionary
for restaurant in restaurantNames:
    modelDict[restaurantNames[restaurant]] = initializeList()

#Update frequency count, partitions
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
            modelDict[context][char][0] += 1               #Frequency update
            allContexts.append(context)
            allChars.append(char)
            nTable = len(modelDict[context][char])
            tableNumber = random.randrange(1, nTable)    #Range starts from 1, as first element is frequency count
            if tableNumber < nTable:
                modelDict[context][char][tableNumber] += 1
                #global loopC
                #loopC += 1
                #print(loopC)
            else:
                modelDict[context][char].append(1)
            allTables.append(tableNumber)

def assertInitialization():
    for key in restaurantNames:
        for char in characters:
            freq = modelDict[key][char][0]
            sumCustomers = sum(modelDict[key][char])-freq
            print('Freq: ' + str(freq) + 'Customers' + str(sumCustomers))

def wordProb(context, char):
    if(context == ''):
        return 1/26
    else:
        cuw = modelDict[context][char][0]
        qu = modelDict[context][quStr]
        du = modelDict[context][duStr]
        tuw = len(modelDict[context][char]) - 1
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


for restaurant in restaurantNames:
    for dish in modelDict[restaurant]:
        if dish != custCountStr and dish != totalTableStr:
            modelDict[restaurant][custCountStr] += modelDict[restaurant][dish][0]
            modelDict[restaurant][totalTableStr] += len(modelDict[restaurant][dish]) - 1

for restaurant in restaurantNames:
   print('\nKey: ' + restaurant)
   print('Cust '+str(modelDict[restaurant][custCountStr]) + "  TableCount: "+ str(modelDict[restaurant][totalTableStr]))
   #for k in modelDict[key]:
        #print(modelDict[key][k])

for restaurant in restaurantNames:
    print(restaurant)
