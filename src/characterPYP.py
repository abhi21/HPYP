__author__ = 'abhi21'

#import numpy as num
import random
import numpy
from math import log2
from math import floor

n = 2
modelDict = {}
samplingTableCount ={}
restaurantNames ={}
totalIncrements = 0

global ITERATION_COUNT
ITERATION_COUNT = 100

characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
totalTableStr = 'totalTables'
custCountStr = 'custCount'
qu = 0.2
du = 0.2
quStr = 'qu'
duStr = 'du'

param = [1,1,1,1]
paramStr = 'param'

allContexts = []
allChars = []
allTables = []

#UnigramDict
uniDict = {}
for item in characters:
    uniDict[item] = 0

def initializeList():
    freq = {custCountStr: 0, totalTableStr:0, quStr: qu, duStr: du, paramStr: param}
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
    if (n-1==0):
        if (k != ''):
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
        #Increment freq for unigram
        uniDict[word[i]] += 1

        while((psc >= 0) and (tempN - 1 >=0)):
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
            tableNumber = random.randrange(2, 1+nTable)    #tableNumber is the index of the list, 3 = ntable +1
            if tableNumber < nTable:
                modelDict[context][char][tableNumber] += 1
            else:
                modelDict[context][char].append(1)
                modelDict[context][char][1] += 1
            allTables.append(tableNumber)

#Calculates probability of a character in a given context
def charProb(context, char):
    if(context == ''):
        return uniDict[char]
        #return 1/26
    else:
        cuw = modelDict[context][char][0]
        qu = modelDict[context][quStr]
        du = modelDict[context][duStr]
        tuw = modelDict[context][char][1]
        cu = modelDict[context][custCountStr]
        tu = modelDict[context][totalTableStr]
        selfProb = (cuw - (du*tuw))/(qu + cu)
        baseProb = (qu + (du*tu))/(qu+cu)
        context = context[1:len(context)]
        return selfProb + (baseProb*charProb(context,char))

def calcEntropy(word, n):
    word = word.lower()
    wordLen = len(word)

    entropy = 0
    for i in range(0, wordLen):
        contextlength = min(i,n)
        context = word[i+1-contextlength:i]
        char = word[i:i + 1]
        entropy += log2(charProb(context,char))
    return entropy

def testPerplexity():
    global entropy, nChars, f, line, name, perplexity
    testFile = readTestFile()
    entropy = 0
    nChars = 0
    with testFile as f:
        for line in f:
            name = line.split()[0]
            nChars += len(name)
            entropy += calcEntropy(name, n)
    perplexity = pow(2, (-entropy / nChars))
    testFile.close()
    return perplexity

def trainPerplexity():
    global entropy, nChars, f, line, name, perplexity
    testFile = readTrainFile()
    entropy = 0
    nChars = 0
    with testFile as f:
        for line in f:
            name = line.split()[0]
            nChars += len(name)
            entropy += calcEntropy(name, n)
    perplexity = pow(2, (-entropy / nChars))
    testFile.close()
    return perplexity

def calcEntropyUnigram(word):
    word = word.lower()
    wordLen = len(word)

    entropy = 0
    for i in range(0, wordLen):
        char = word[i]
        entropy += log2(uniDict[char])
    return entropy


def readTestFile():
    testFile = open("data/dist_male_first.txt", "r")
    return testFile

def readTrainFile():
    testFile = open("data/dist_female_first.txt", "r")
    return testFile


def testPerplexityUnigram():
    global entropy, nChars, f, line, name, perplexity
    testFile = readTestFile()
    entropy = 0
    nChars = 0
    with testFile as f:
        for line in f:
            name = line.split()[0]
            nChars += len(name)
            entropy += calcEntropyUnigram(name)
    perplexity = pow(2, (-entropy / nChars))
    testFile.close()
    return perplexity

def parametersampler():
    for restaurant in restaurantNames:
        qu = modelDict[restaurant][quStr]
        du = modelDict[restaurant][duStr]
        cu = modelDict[restaurant][custCountStr]
        tu = modelDict[restaurant][totalTableStr]
        xu = 0
        if (tu >= 2):
            xu = log2(random.betavariate(qu + 1,cu-1))
        yubeta = 0
        yugamma = 0
        if(tu>=2):
            for p in range(1,tu):
                yui = 0
                uni = random.randrange(0,1000)/1000
                probBernoulli = (qu/(qu + du*p))
                if (uni<probBernoulli):
                    yui = 1
                yubeta = yubeta + (1 - yui)
                yugamma = yugamma + yui
        zuw = 0;
        for dish in modelDict[restaurant]:
            if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr and dish != paramStr:
                for t in range(2,len(modelDict[restaurant][dish])):
                    if modelDict[restaurant][dish][t] >= 2:
                        for tw in range(1,modelDict[restaurant][dish][t]):
                            zuwk = 0
                            uni = random.randrange(0,1000)/1000
                            probBernoulli = (tw-1)/(tw -du)
                            if(uni<probBernoulli):
                                zuwk = 1
                            zuw = zuw + (1-zuwk)
    am = modelDict[restaurant][paramStr][0] + yubeta
    bm = modelDict[restaurant][paramStr][1] + zuw
    alpham = modelDict[restaurant][paramStr][2] + yugamma
    betam = modelDict[restaurant][paramStr][3] - xu
    modelDict[restaurant][quStr] = random.gammavariate(alpham,betam)
    modelDict[restaurant][duStr] = random.betavariate(am,bm)


#Creates restaurantNames for a given context length
makeKey('',n)

#Creates Main Dictionary
for restaurant in restaurantNames:
    modelDict[restaurantNames[restaurant]] = initializeList()

#Creates data structure to save table count for each dish in each restaurant for each iteration step
for restaurant in restaurantNames:
    samplingTableCount[restaurantNames[restaurant]] = initializeListSamplingTableCount()

#Reads Training File
file = readTrainFile()
with file as f:
  for line in f:
    name = line.split()[0]
    updateFrequency(name,n)  #Updates frequency count, and initializes table assignment

file.close()

#calculate sum for unigram
sumUnigram = 0
for key in uniDict:
    sumUnigram += uniDict[key]
#Calculate probability
for key in uniDict:
    uniDict[key] = uniDict[key]/sumUnigram


#Generates custCount and totalTable
for restaurant in restaurantNames:
    am = modelDict[restaurant][paramStr][0]
    bm = modelDict[restaurant][paramStr][1]
    alpham = modelDict[restaurant][paramStr][2]
    betam = modelDict[restaurant][paramStr][3]
    modelDict[restaurant][quStr] = random.gammavariate(alpham,betam)
    modelDict[restaurant][duStr] = random.betavariate(am,bm)
    for dish in modelDict[restaurant]:
        if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr and dish != paramStr:
            modelDict[restaurant][custCountStr] += modelDict[restaurant][dish][0]
            modelDict[restaurant][totalTableStr] += modelDict[restaurant][dish][1]

#Prints all details of seating arrangement
#for restaurant in restaurantNames:
#    print('\nrestaurant: ' + restaurant)
#    print('Cust '+str(modelDict[restaurant][custCountStr]) + "  TableCount: "+ str(modelDict[restaurant][totalTableStr]))
#    for dish in modelDict[restaurant]:
#        if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr  and dish != paramStr:
#            print('\n\tdish: ' + dish)
#            print('\tCust '+str(modelDict[restaurant][dish][0]) + "  TableCount: "+ str(modelDict[restaurant][dish][1]))

def verifytable():
    for restaurant in restaurantNames:
        for dish in modelDict[restaurant]:
            if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr and dish != paramStr:
                ntables = modelDict[restaurant][dish][1]
                ntablespart = 0
                for i in range(2,len(modelDict[restaurant][dish])):
                    if(modelDict[restaurant][dish][i] > 0):
                        ntablespart += 1
                if ntables != ntablespart:
                    print('\nNumber of Tables: ' + str(ntables) + "   Number of tables as per partitions " + str(ntablespart))
                ncust = modelDict[restaurant][dish][0]
                ncustpart = sum(modelDict[restaurant][dish]) - modelDict[restaurant][dish][0] -modelDict[restaurant][dish][1]
                if ncust != ncustpart:
                    print('Total Customers: ' + str(ncust) + "   Number of customers as per partitions " + str(ncustpart))

p = testPerplexityUnigram()
print('UnigramP: '+str(p))

p = testPerplexity()
print(p)
print("-----------------Before Gibbs--------------------")
print('Total Cust '+str(modelDict['a'][custCountStr]) + "  Total TableCount: "+ str(modelDict['a'][totalTableStr]))

for i in range(0,ITERATION_COUNT):
    print("==============> Iteration: "+ str(i))
    charNo = -1
    for char in allChars:
        charNo += 1
        tempTableProb = []
        tempTableNo = allTables[charNo]
        context = allContexts[charNo]
        modelDict[context][char][tempTableNo] -= 1 # reduce by 1 number of customers sitting at that table

        if (modelDict[context][char][tempTableNo] == 0):
            modelDict[context][char][1] -= 1 #Reduce total number of tables serving that dish in that restaurant
            modelDict[context][totalTableStr] -= 1 #Reduce total number of tables in that restaurant

        qu = modelDict[context][quStr]
        du = modelDict[context][duStr]
        cu = modelDict[context][custCountStr] -1
        tu = modelDict[context][totalTableStr]

        for j in range(2, len(modelDict[context][char])):
            if(modelDict[context][char][j] > 0): #non empty tables
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
        lenTempProb = len(tempTableProb)

        if (posTable == (lenTempProb - 1)):
            modelDict[context][char][1] += 1 #Increase total number of tables serving that dish in that restaurant
            modelDict[context][totalTableStr] += 1 #Increase total number of tables in that restaurant

        occupiedemptytable = 0
        counter = 0
        for j in range(2, len(modelDict[context][char])):
            if(modelDict[context][char][j] > 0):
                if(counter == posTable):
                    modelDict[context][char][j] += 1
                    allTables[charNo] = j
                    break
                counter += 1
            else:
                if(posTable == (lenTempProb - 1)):
                    modelDict[context][char][j] += 1
                    allTables[charNo] = j
                    occupiedemptytable = 1
                    break
        if((posTable == lenTempProb - 1) and (occupiedemptytable == 0)):
            modelDict[context][char].append(1)
            allTables[charNo] = len(modelDict[context][char]) -1

    # Call Hyper-parameter Sampler
    parametersampler()

    if i in range(1,ITERATION_COUNT,1):
        p= testPerplexity()
        print(p)
        #verifytable()
    print("-----------------After Each Gibbs Iteration--------------------")
    print('Total Cust '+str(modelDict['a'][custCountStr]) + "  Total TableCount: "+ str(modelDict['a'][totalTableStr]))

#At the end of each iteration storing no of tables for each dish in each restaurant
for restaurant in restaurantNames:
    for dish in restaurant:
        if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr  and dish != paramStr:
            samplingTableCount[restaurant][dish].append(modelDict[restaurant][dish][1])

#After Gibbs sampling update the no of tables for each dish in each restaurant by averaging the counts
for restaurant in restaurantNames:
    for dish in restaurant:
        if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr:
            modelDict[restaurant][dish][1] = floor(numpy.mean(samplingTableCount[restaurant][dish]))

trainP = trainPerplexity()
print("Train Perplexity " + str(trainP))

p= testPerplexity()
print("Test Perplexity " + str(p))





