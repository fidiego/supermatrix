import sys

targetListFile = open(sys.argv[1])
svdLoadingsFile = open(sys.argv[2])
outfileName = open(sys.argv[3], "w")
n = int(sys.argv[4])

targetList = []
targetIndexDict = {}
i = 0
for line in targetListFile:
    word = line.strip().strip('\n').strip()
    targetList.append(word)
    targetIndexDict[word] = i
    i += 1
targetListFile.close()

print "Reading In SVD Data"
svdDict = {}
for line in svdLoadingsFile:
    data = (line.strip().strip('\n').strip()).split()
    word = data[0]
    singVals = data[1:n+2]
    svdDict[word] = singVals
svdLoadingsFile.close()

for i in range(len(targetList)):
    word = targetList[i]
    outfileName.write("%s" % word)
    if word in svdDict:
        singVals = svdDict[word]
        for j in range(n):
            outfileName.write(" %s" % singVals[j])
    outfileName.write("\n")
outfileName.close()
        

