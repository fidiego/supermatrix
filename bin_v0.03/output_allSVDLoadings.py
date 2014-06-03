#!/usr/bin/python
import sys
from operator import itemgetter

infile = open(sys.argv[1])
outfile2 = open(sys.argv[2]+"_values.txt", "w")
outfile1 = open(sys.argv[2]+"_words.txt", "w")
outputN = int(sys.argv[3])

wordList = []
wordIndexDict = {}
dataMatrix = []

line = infile.readline()
infile.close()
data = (line.strip().strip('\n').strip()).split()
numCols = len(data) - 1
if outputN > numCols:
    outputN = numCols

print "Reading In SVD Data"
lineCounter = 0
infile = open(sys.argv[1])
for line in infile:
    data = (line.strip().strip('\n').strip()).split()
    wordList.append(data[0])
    wordIndexDict[data[0]] = lineCounter
    valueList = []
    for i in range(outputN):
        valueList.append([data[0],float(data[i+1])])
    lineCounter += 1
    dataMatrix.append(valueList)
infile.close()

print "Sorting Data"
outputMatrix1 = []
outputMatrix2 = []
for i in range(outputN):
    currentCol = [row[i] for row in dataMatrix]
    sortedColumn = sorted(currentCol,key=itemgetter(1))
    currentRow1 = []
    currentRow2 = []
    for j in range(lineCounter):
        currentRow1.append(sortedColumn[j][0])
        currentRow2.append(sortedColumn[j][1])
    outputMatrix1.append(currentRow1)
    outputMatrix2.append(currentRow2)
        
print "Outputting Data"
for i in range(outputN):
    outfile1.write("PC%s " % str(i+1))
outfile1.write("\n")

for i in range(lineCounter):
    for j in range(outputN):
        outfile1.write("%s " % outputMatrix1[j][i])
    outfile1.write("\n")
outfile1.close()

for i in range(outputN):
    outfile2.write("PC%s " % str(i+1))
outfile2.write("\n")

for i in range(lineCounter):
    for j in range(outputN):
        outfile2.write("%s " % outputMatrix2[j][i])
    outfile2.write("\n")
outfile2.close()

