__author__ = 'abhi21'

#import numpy as num
import random
from math import floor

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
        freq[item] = [0,0]
    return freq

def initializeListSamplingTableCount():
    freq={}
    for item in characters:
        freq[item] = [0]
    return freq

#finds the index for the number for which sum exceeds the number
def findPos(list, number):
    i = 0;
    j = len(list)

    for k in range(0, len(list)):
        t = floor((i + j) / 2)
        sumTable = sum(list[0:t])
        if (sumTable <= number):
            i = t
        else:
            j=t
        if(j-i == 1):
           # print(i)
           return i

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
            tableNumber = random.randrange(2, nTable+1)    #tableNumber is the index of the list
            if tableNumber < nTable:
                modelDict[context][char][tableNumber] += 1
            else:
                modelDict[context][char].append(1)
                modelDict[context][char][1] += 1
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
            modelDict[restaurant][totalTableStr] += modelDict[restaurant][dish][1]

#Prints all details of seating arrangement
for restaurant in restaurantNames:
    print('\nrestaurant: ' + restaurant)
    print('Cust '+str(modelDict[restaurant][custCountStr]) + "  TableCount: "+ str(modelDict[restaurant][totalTableStr]))
    for dish in modelDict[restaurant]:
        if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr:
            print('\n\tdish: ' + dish)
            print('\tCust '+str(modelDict[restaurant][dish][0]) + "  TableCount: "+ str(modelDict[restaurant][dish][1]))

#Creates data structure to save table count for each dish in each restaurant for each iteration step
for restaurant in restaurantNames:
    samplingTableCount[restaurantNames[restaurant]] = initializeListSamplingTableCount()

for i in range(0,ITERATION_COUNT):
    charNo = -1
    for char in allChars:
        charNo += 1
        tempTableProb = []
        tempTableNo = allTables[charNo]
        context = allContexts[charNo]
        modelDict[context][char][tempTableNo] -= 1 # reduce by 1 number of customers sitting at that table
        #modelDict[context][char][0] -= 1 # reduce by 1 number of customers having that dish in that restaurant
        #modelDict[context][custCountStr] -= 1 #reduce by 1 number of customers in that restaurant

        if (modelDict[context][char][tempTableNo] == 0):
            modelDict[context][char][1] -= 1 #Reduce total number of tables serving that dish in that restaurant
            modelDict[context][totalTableStr] -= 1 #Reduce total number of tables in that restaurant

        qu = modelDict[context][quStr]
        du = modelDict[context][duStr]
        cu = modelDict[context][custCountStr] -1
        tu = modelDict[context][totalTableStr]

        for j in range(2, 2 + modelDict[context][char][1]):
            if(modelDict[context][char][j] > 0):
                cuw = modelDict[context][char][j]
                probTable = (cuw - du)/(cu + qu)
                tempTableProb.append(probTable)

        baseProb = (qu + (du * tu))/(qu + cu)
        probTableNew = baseProb * charProb(context[1:len(context)],char)
        tempTableProb.append(probTableNew)
        tempSum = sum(tempTableProb)
        for item in range(0,len(tempTableProb)):
            tempTableProb[item] = tempTableProb[item]/tempSum
        randNo = random.randrange(0, 100000)/100000
        posTable = findPos(tempTableProb,randNo)
        allTables[charNo] = posTable + 2
        lenTempProb = len(tempTableProb)

        counter = 0
        emptytableoccupied = False
        for j in range(2, 2 + modelDict[context][char][1]):
            if(modelDict[context][char][j] >= 1):
                if(counter == posTable):
                    modelDict[context][char][j] += 1
                    break
                counter += 1
            else:
                if(posTable == lenTempProb - 1):
                    modelDict[context][char][j] += 1
                    allTables[charNo] = j
                    emptytableoccupied = True
                    break
        if emptytableoccupied == False:
            modelDict[context][char].append(1)
            allTables[charNo] = 1+lenTempProb

        if (posTable == lenTempProb-1):
            modelDict[context][char][1] += 1 #Increase total number of tables serving that dish in that restaurant
            modelDict[context][totalTableStr] += 1 #Increase total number of tables in that restaurant


