__author__ = 'abhi21'
from math import floor

number = 0.05
list = [0.1, 0.1, 0.1, 0.1,0.1,0.1, 0.1,0.1,0.1, 0.1]

i = 0
j = len(list)

for k in range(0, len(list)):
        t = floor((i + j) / 2)
        sumTable = sum(list[0:t])
        if (sumTable <= number):
            i = t
        else:
            j=t
        if(j-i == 1):
            print(i)
            break

for j in range(2,3):
    print(j)