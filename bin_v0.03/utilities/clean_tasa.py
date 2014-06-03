#/usr/bin/python
import sys, os, nltk

inputDirectory = sys.argv[1]
outputDirectory = sys.argv[2]
masterOutputFile = open("tasaALL.txt", "w")

conversionDict = {}
conversionDict['.'] = "PERIOD"
conversionDict[','] = "COMMA"
conversionDict['!'] = "EXCLAMATION"
conversionDict['?'] = "QUESTION"
conversionDict[':'] = "COLON"
conversionDict[';'] = "SEMICOLON"
conversionDict['"'] = "DQUOTE"
conversionDict['('] = "OPAREN"
conversionDict[')'] = "CPAREN"
conversionDict['['] = "OBRACKET"
conversionDict[']'] = "CBRACKET"
conversionDict['{'] = "OSBRACKET"
conversionDict['}'] = "CSBRACKET"

os.mkdir(outputDirectory)
corpusList = []
temp_filelist = os.listdir(inputDirectory)
for filename in temp_filelist:
    if not (filename == ".DS_Store"):
        corpusList.append(filename)
     
for corpus in corpusList:
    print "Translating corpus %s" % corpus
    inputFilehandle = open(inputDirectory + corpus)
    outputFilehandle = open(outputDirectory + "/" + corpus, "w")

    for line in inputFilehandle:
        token = line.strip().strip('\n').strip()
        done = 0
        beginningOutputList = []
        while not done:
            if len(token) == 0:
                done = 1
            elif token[0] in conversionDict:
                beginningOutputList.append(conversionDict[token[0]])
                token = token[1:]
            else:
                done = 1

        done = 0
        endingOutputList = []
        while not done:
            if len(token) == 0:
                done = 1
            elif token[-1] in conversionDict:
                endingOutputList.insert(0, conversionDict[token[-1]])
                token = token[:-1]
            else:
                done = 1
        
        for item in beginningOutputList:
            outputFilehandle.write("%s\n" % item)
            masterOutputFile.write("%s\n" % item)
        if len(token) > 0:
            outputFilehandle.write("%s\n" % token)
            masterOutputFile.write("%s\n" % token)
        for item in endingOutputList:
            outputFilehandle.write("%s\n" % item)
            masterOutputFile.write("%s\n" % item)        
        
    inputFilehandle.close()
    outputFilehandle.close()
masterOutputFile.close()