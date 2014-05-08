__author__ = 'abhi21'

p = testPerplexity()
print(p)
print("-----------------Before Gibbs--------------------")
print('Total Cust '+str(modelDict['a'][custCountStr]) + "  Total TableCount: "+ str(modelDict['a'][totalTableStr]))

for i in range(0,ITERATION_COUNT):
    print("==============> Iteration: "+ str(i))
    charNo = -1
    for char in allChars:
        tableEmptied = False
        charNo += 1
        tempTableProb = []
        tempTableNo = allTables[charNo]
        context = allContexts[charNo]
        modelDict[context][char][tempTableNo] -= 1 # reduce by 1 number of customers sitting at that table

        if (modelDict[context][char][tempTableNo] == 0):
            modelDict[context][char][1] -= 1 #Reduce total number of tables serving that dish in that restaurant
            modelDict[context][totalTableStr] -= 1 #Reduce total number of tables in that restaurant
            tableEmptied = True

        qu = modelDict[context][quStr]
        du = modelDict[context][duStr]
        cu = modelDict[context][custCountStr] -1
        tu = modelDict[context][totalTableStr]

        for j in range(2, 2 + modelDict[context][char][1]):
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
            if (tableEmptied == True):
                modelDict[context][char][allTables[charNo]] += 1
            else:
                modelDict[context][char].append(1)
                allTables[charNo] = 2 + posTable
        else:
            counter = 0
            for j in range(2, 2 + modelDict[context][char][1]):
                if(modelDict[context][char][j] > 0):
                    if(counter == posTable):
                        modelDict[context][char][j] += 1
                        allTables[charNo] = j
                        break
                    counter += 1
    p= testPerplexity()
    print(p)

    #print("-----------------After Each Gibbs Iteration--------------------")
    #print('Total Cust '+str(modelDict['a'][custCountStr]) + "  Total TableCount: "+ str(modelDict['a'][totalTableStr]))

    #At the end of each iteration storing no of tables for each dish in each restaurant
    for restaurant in restaurantNames:
        for dish in restaurant:
            if dish != custCountStr and dish != totalTableStr and dish != quStr and dish != duStr:
                samplingTableCount[restaurant][dish].append(modelDict[restaurant][dish][1])






