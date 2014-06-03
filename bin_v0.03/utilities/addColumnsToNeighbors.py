import sys, os
import numpy as np

indexList = []
indexDict = {}
f = open(sys.argv[1])
for line in f:
    data = (line.strip().strip('\n').strip()).split()
    indexList.append(data[1])
    indexDict[data[1]] = data[0]
f.close()
numWords = len(indexList)

print "Importing Sims"
f = open(sys.argv[2])
simMatrix = np.zeros([numWords, numWords],float)
for line in f:
    data = (line.strip().strip('\n').strip()).split()
    currentTargetIndex = int(data[0])
    currentTarget = indexList[currentTargetIndex]
    currentSimList = data[1:]
    
    for currentSimPair in currentSimList:
        pair = currentSimPair.split(':')
        currentComparisonIndex = int(pair[0])
        currentComparison = indexList[currentComparisonIndex]
        currentSim = float(pair[1])
        simMatrix[currentTargetIndex, currentComparisonIndex] = currentSim
f.close()

print "Converting Files"
input_directory = sys.argv[3]
output_directory = sys.argv[4]
directoryListing = os.listdir(input_directory)
for currentFilename in directoryListing:
    if not currentFilename == ".DS_Store":
        outputList = []
        f1 = open(input_directory+currentFilename)
        for line in f1:
            foundIt = 0
            data = (line.strip().strip('\n').strip()).split()
            if ((data[0] in indexDict) and (data[1] in indexDict)):
                currentSim = simMatrix[indexDict[data[0]], indexDict[data[1]]]
            else:
                currentSim = -1
            data.append(currentSim)
            outputList.append(data)
        f1.close()
        f2 = open(output_directory+currentFilename, "w")
        for item in outputList:
            f2.write("%s %s %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f\n" % (item[0], item[1], float(item[2]), float(item[3]), float(item[4]), float(item[5]), float(item[6]), float(item[7]), float(item[8])))
        f2.close()