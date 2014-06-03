#!/usr/bin/python
import sys, getopt, os

# reads in a translation dictionary and converts that

inputDirectory = sys.argv[2]
outputDirectory = sys.argv[3]

conversionDict = {}
conversionDefinitionFile = open(sys.argv[1])
for line in conversionDefinitionFile:
    data = (line.strip('\n').strip()).split()
    conversionDict[data[0]] = data[1:]
conversionDefinitionFile.close()

corpusList = []
temp_filelist = os.listdir(sys.argv[2])
for filename in temp_filelist:
    if not (filename == ".DS_Store"):
        corpusList.append(filename)


os.mkdir(outputDirectory)
for corpus in corpusList:
    print "Translating corpus %s" % corpus
    inputFilehandle = open(inputDirectory + corpus)
    outputFilehandle = open(outputDirectory + "/" + corpus, "w")

    for line in inputFilehandle:
        token = line.strip('\n').strip()
        if token in conversionDict:
            currentOutput = conversionDict[token]
            for i in range(len(currentOutput)):
                outputFilehandle.write("%s\n" % currentOutput[i])
        else:
            outputFilehandle.write("%s\n" % token)
    inputFilehandle.close()