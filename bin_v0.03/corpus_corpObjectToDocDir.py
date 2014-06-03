import sys, os

corpusFile = open(sys.argv[1])
documentListFile = open(sys.argv[2])
outputDirectory = sys.argv[3]
os.mkdir(outputDirectory)

documentList = []
for line in documentListFile:
    data = (line.strip().strip('\n').strip()).split()
    documentTitle = data[0]
    documentName = documentTitle.split('/')
    documentList.append(documentName[-1])
documentListFile.close()

documentCounter = 0
for line in corpusFile:
    document = (line.strip().strip('\n').strip()).split()
    documentTitle = documentList[documentCounter]
    documentFilehandle = open(outputDirectory + "/" + documentTitle, "w")
    for token in document:
        documentFilehandle.write("%s\n" % token)
    documentFilehandle.close()
    documentCounter += 1
    