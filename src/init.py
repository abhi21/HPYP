__author__ = 'abhi21'

#import numpy as num
import random

n = 2
modelDict = {}
samplingTableCount ={}
restaurantNames ={}
totalIncrements = 0
global index
index = -1

global ITERATION_COUNT
ITERATION_COUNT = 1


global loopC
loopC = 0
characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
totalTableStr = 'totalTables'
custCountStr = 'custCount'
qu = .8
du = .2
quStr = 'qu'
duStr = 'du'

allContexts = []
allChars = []
allTables = []


def initializeList():
    freq = {custCountStr: 0, totalTableStr:0, quStr: qu, duStr: du}
    for item in characters:
        freq[item] = [0]
    return freq

def initializeListSamplingTableCount():
    freq={}
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

#Updates frequency count, and initializes table assignment
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
            tableNumber = random.randrange(1, nTable+1)    #Range starts from 1, as first element is frequency count
            if tableNumber < nTable:
                modelDict[context][char][tableNumber] += 1
            else:
                modelDict[context][char].append(1)
            allTables.append(tableNumber)

#Calculates probability of a character in a given context
def charProb(context, char):
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
        return selfProb + (baseProb*charProb(context,char))

#Creates restaurantNames for a given context length
makeKey('',n)

#Creates Main Dictionary
for restaurant in restaurantNames:
    modelDict[restaurantNames[restaurant]] = initializeList()

#Reads Training File
fileName = "data/dist_female_first.txt"
file = open(fileName, "r")
with file as f:
  for line in f:
    name = line.split()[0]
    updateFrequency(name,n)  #Updates frequency count, and initializes table assignment

file.close()

#Generates custCount and totalTable
for restaurant in restaurantNames:
    for dish in modelDict[restaurant]:
        if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr:
            modelDict[restaurant][custCountStr] += modelDict[restaurant][dish][0]
            modelDict[restaurant][totalTableStr] += len(modelDict[restaurant][dish]) - 1

#Prints all details of seating arrangement
for restaurant in restaurantNames:
    print('\nrestaurant: ' + restaurant)
    print('Cust '+str(modelDict[restaurant][custCountStr]) + "  TableCount: "+ str(modelDict[restaurant][totalTableStr]))
    for dish in modelDict[restaurant]:
        if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr:
            print('\n\tdish: ' + dish)
            print('\tCust '+str(modelDict[restaurant][dish][0]) + "  TableCount: "+ str(len(modelDict[restaurant][dish])-1))

#Creates data structure to save table count for each dish in each restaurant for each iteration step
for restaurant in restaurantNames:
    samplingTableCount[restaurantNames[restaurant]] = initializeListSamplingTableCount()


#for i in range(0,ITERATION_COUNT):
#    for char in allChars:
