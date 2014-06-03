import sys, os, time, operator, math
from operator import itemgetter
################################################################################################
################################################################################################
class corpus:
    ############################################################################################
    def __init__(self):
        self.rawCorpusFilename = 0                 
        self.rawDocumentDirectory = 0
        self.corpusDirectory = 0
        self.outputDirectory = 0
        self.orderTypesAlphabetically = 0
        self.orderTypesByFrequency = 0

        self.masterTypeList = []
        self.masterTypeDict = {}
        self.masterTypeIndexDict = {}
        
        self.masterTypeFreqDict = {}                # a dictionary with the frequency of all targets in the entire corpus, summed across documents
        self.typePerDocumentFreqDictList = []       # a list of dictionaries, one for each document, with the frequencies of all the types that occur in that document
        self.sortedTargetFreqList = []              # a list of tuples, containing each type and freq, summed across documents, sorted either by freq or alphabetically
        self.typeDocumentProportionDict = {}
        
        self.numTokens = 0
        self.numTypes = 0
        
        self.rawDocumentList = []
        self.rawDocumentDict = {}
        self.rawDocumentIndexDict = {}
        self.numDocuments = 0
        
        self.typesPerDocument = []
        self.tokensPerDocument = []
        self.typesPerDocumentDict = {}
        self.tokensPerDocumentDict = {}
        self.sortedDocumentTypeFreqList = []
        self.sortedDocumentTokenFreqList = []
        
    ############################################################################################
    def initializeNewCorpus(self, outputDirectory, freqOrder, alphaOrder):
        self.outputDirectory = outputDirectory
        self.freqOrder = freqOrder
        self.alphaOrder = alphaOrder
        
        if ((self.freqOrder == 0) and (self.alphaOrder)):
            self.freqOrder == 1
        
        try:
            os.mkdir(self.outputDirectory)
        except:
            print "Error: Couldn't create new corpus directory. Does it already exist?"
            sys.exit(0)
    
    ############################################################################################
    def initializeModifiedCorpus(self, corpusDirectory, outputDirectory, freqOrder, alphaOrder):
        self.corpusDirectory = corpusDirectory
        self.outputDirectory = corpusDirectory+outputDirectory
        self.freqOrder = freqOrder
        self.alphaOrder = alphaOrder
        
        if ((self.freqOrder == 0) and (self.alphaOrder)):
            self.freqOrder == 1
        
        try:
            os.mkdir(self.outputDirectory)
        except:
            print "Error: Couldn't create new corpus directory. Does it already exist?"
            sys.exit(0)
    
    ############################################################################################ 
    def getSeparateDocumentList(self, documentDirectory):
        self.rawDocumentDirectory = documentDirectory
    
        print "Getting document list from %s" % documentDirectory 
        try:
            directoryListing = os.listdir(documentDirectory)
        except:
            print "Error, invalid (or no) file directory was specified"
            sys.exit(0)
    
        for currentFilename in directoryListing:
            if not currentFilename == ".DS_Store":
                self.rawDocumentList.append(self.rawDocumentDirectory+currentFilename)
                self.rawDocumentDict[currentFilename] = self.numDocuments
                self.rawDocumentIndexDict[self.numDocuments] = currentFilename
                self.typePerDocumentFreqDictList.append({})
                self.numDocuments += 1
        print "Found %s documents" % (self.numDocuments)
    
    ############################################################################################ 
    def countAndMergeSeparateDocuments(self):
        print "Creating merged corpus file; counting token and type frequencies"
        
        mergedCorpusFilehandle = open(self.outputDirectory+"/corpus.txt", "w")
        
        for i in range(self.numDocuments):
            print "     %s" % self.rawDocumentList[i]
            currentCorpusFilehandle = open(self.rawDocumentList[i])
            currentTypeCount = 0
            currentTokenCount = 0
            for line in currentCorpusFilehandle:
                tokens = (line.strip().strip("\n").strip()).split()
                if len(tokens) > 0:
                    for token in tokens:
                        if len(token) > 0:                    
                            currentTokenCount += 1
                            self.numTokens += 1
                            mergedCorpusFilehandle.write("%s " % token)
                            
                            if token in self.masterTypeFreqDict:
                                self.masterTypeFreqDict[token] += 1
                            else:
                                self.masterTypeFreqDict[token] = 1
                                
                            if token in self.typePerDocumentFreqDictList[i]:
                                self.typePerDocumentFreqDictList[i][token] += 1
                            else:
                                self.typePerDocumentFreqDictList[i][token] = 1                
            mergedCorpusFilehandle.write("\n")
            currentCorpusFilehandle.close()
            self.tokensPerDocument.append(currentTokenCount)
            self.typesPerDocument.append(len(self.typePerDocumentFreqDictList[i]))
        mergedCorpusFilehandle.close()
        
        if self.freqOrder:
            print "Sorting Types by Frequency"
            self.sortedTargetFreqList = sorted(self.masterTypeFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
        elif self.alphaOrder:
            print "Sorting Types Alphabetically"
            self.sortedTargetFreqList = sorted(self.masterTypeFreqDict.iteritems(), key=operator.itemgetter(0), reverse=False)      
        
        for i in range(len(self.sortedTargetFreqList)):
            currentTarget = self.sortedTargetFreqList[i][0]
            self.masterTypeList.append(currentTarget)
            self.masterTypeDict[currentTarget] = i
            self.masterTypeIndexDict[i] = currentTarget
            numDocs = 0
            for j in range(self.numDocuments):
                currentDocumentFreqDict = self.typePerDocumentFreqDictList[j]
                if currentTarget in currentDocumentFreqDict:
                    if currentDocumentFreqDict[currentTarget] > 0:
                        numDocs += 1
            docProp = float(numDocs) / self.numDocuments
            self.typeDocumentProportionDict[currentTarget] = docProp
        self.numTypes = len(self.masterTypeDict)
        
    ############################################################################################ 
    def modifyCorpus(self, translateFile):
        print "Modifying corpus file; counting token and type frequencies"
    
        translateDict = {}
        translateFilehandle = open(translateFile)
        for line in translateFilehandle:
            data = (line.strip('\n').strip()).split()
            translateDict[data[0]] = data[1:]
        translateFilehandle.close()
        
        numCorpora = 0
        oldCorpusFilehandle = open(self.corpusDirectory+"corpus.txt")
        newCorpusFilehandle = open(self.outputDirectory+"/corpus.txt", "w")
        
        for line in oldCorpusFilehandle:
            currentTypeCount = 0
            currentTokenCount = 0
        
            tokenList = (line.strip('\n').strip()).split()
            for token in tokenList:
                if token in translateDict:
                    translatedTokens = translateDict[token]
                    for translatedToken in translatedTokens:
                        currentTokenCount += 1
                        self.numTokens += 1
                        newCorpusFilehandle.write("%s " % translatedToken)                        
                        if translatedToken in self.masterTypeFreqDict:
                            self.masterTypeFreqDict[translatedToken] += 1
                        else:
                            self.masterTypeFreqDict[translatedToken] = 1
                            
                        if translatedToken in self.typePerDocumentFreqDictList[i]:
                            self.typePerDocumentFreqDictList[i][translatedToken] += 1
                        else:
                            self.typePerDocumentFreqDictList[i][translatedToken] = 1  
                        
                else:
                    currentTokenCount += 1
                    self.numTokens += 1
                    if token in self.masterTypeFreqDict:
                        self.masterTypeFreqDict[token] += 1
                    else:
                        self.masterTypeFreqDict[token] = 1
                        
                    if token in self.typePerDocumentFreqDictList[i]:
                        self.typePerDocumentFreqDictList[i][token] += 1
                    else:
                        self.typePerDocumentFreqDictList[i][token] = 1  
                    
                    newCorpusFilehandle.write("%s " % token)
            newCorpusFilehandle.write("\n")
            
            self.tokensPerDocument.append(currentTokenCount)
            self.typesPerDocument.append(len(self.typePerDocumentFreqDictList[numCorpora]))
            numCorpora += 0
            
        oldCorpusFilehandle.close()
    
    ############################################################################################ 
    def convertCorpusToIndexes(self):
        outputFilehandle = open(self.outputDirectory+"/indexed_corpus.txt", "w")    
    
    ############################################################################################
    def outputCorpusInfo(self):
        outputFilehandle = open(self.outputDirectory+"/corpus_info.txt", "w")
        outputFilehandle.write("corpus_name: %s\n" % (self.outputDirectory))
        outputFilehandle.write("num_documents: %s\n" % (self.numDocuments))
        outputFilehandle.write("num_types: %s\n" % (self.numTypes))
        outputFilehandle.write("num_tokens: %s\n" % (self.numTokens))
        outputFilehandle.close()
    
    ############################################################################################ 
    def outputTargetInfo(self):
        outputFilehandle = open(self.outputDirectory+"/target_info.txt", "w")
        for i in range(self.numTypes):
            currentTarget = self.sortedTargetFreqList[i][0]
            currentFreq = self.sortedTargetFreqList[i][1]
            currentProp = self.typeDocumentProportionDict[currentTarget]
            outputFilehandle.write("%s %s %s %0.3f\n" % (currentTarget, i, currentFreq, currentProp))
        outputFilehandle.close()
        
    ############################################################################################ 
    def outputDocumentInfo(self):
        outputFilehandle = open(self.outputDirectory+"/document_info.txt", "w")
        for i in range(self.numDocuments):
            outputFilehandle.write("%s %s %s %s\n" % (self.rawDocumentList[i], i, self.typesPerDocument[i], self.tokensPerDocument[i]))
        outputFilehandle.close()    

    ############################################################################################
    def importCorpusInfo(self, corpusDirectory):
        print "Importing Corpus Information"
        self.corpusDirectory = corpusDirectory
        corpusInfoFilehandle = open(corpusDirectory+"corpus_info.txt")
        for line in corpusInfoFilehandle:
            data = (line.strip('\n').strip()).split()
            if data[0] == "num_documents:":
                self.numDocuments = int(data[1])
            if data[0] == "num_types:":
                self.numTypes = int(data[1])
            if data[0] == "num_tokens:":
                self.numTokens = int(data[1])            
        corpusInfoFilehandle.close()
    
    ############################################################################################
    def importTargetInfo(self):
        targetInfoFilehandle = open(self.corpusDirectory+"target_info.txt")
        for line in targetInfoFilehandle:
            data = (line.strip('\n').strip()).split()
            self.masterTypeList.append(data[0])
            self.masterTypeDict[data[0]] = int(data[1])
            self.masterTypeIndexDict[int(data[1])] = data[0]
            self.masterTypeFreqDict[data[0]] = int(data[2])
            self.typeDocumentProportionDict[data[0]] = float(data[3])
        targetInfoFilehandle.close()
        self.sortedTargetFreqList = sorted(self.masterTypeFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    ############################################################################################
    def importDocumentNames(self):
        documentInfoFilehandle = open(self.corpusDirectory+"document_info.txt")
        for line in documentInfoFilehandle:
            data = (line.strip('\n').strip()).split()
            self.rawDocumentList.append(data[0])
            self.rawDocumentDict[data[0]] = int(data[1])
            self.rawDocumentIndexDict[int(data[1])] = data[0]
        documentInfoFilehandle.close()
    ############################################################################################
    def importDocumentInfo(self):
    
        documentInfoFilehandle = open(self.corpusDirectory+"document_info.txt")
        for line in documentInfoFilehandle:
            data = (line.strip('\n').strip()).split()
            self.rawDocumentList.append(data[0])
            self.rawDocumentDict[data[0]] = int(data[1])
            self.rawDocumentIndexDict[int(data[1])] = data[0]
            self.typesPerDocument.append(int(data[2]))
            self.tokensPerDocument.append(int(data[3]))
            self.typesPerDocumentDict[data[0]] = int(data[2])
            self.tokensPerDocumentDict[data[0]] = int(data[3]) 
        documentInfoFilehandle.close()
        self.sortedDocumentTypeFreqList = sorted(self.typesPerDocumentDict.iteritems(), key=operator.itemgetter(1), reverse=True)
        self.sortedDocumentTokenFreqList = sorted(self.tokensPerDocumentDict.iteritems(), key=operator.itemgetter(1), reverse=True)
            
    ############################################################################################
    def outputTargetSubList(self, outputFilename, frequencyThreshold, numTargetsThreshold, docPropThreshold, includeListFilename, excludeListFilename):

        # create a stop list dictionary and add any targets in the stop list file if there is one
        excludeDict = {}
        if excludeListFilename:
            excludeListFilehandle = open(excludeListFilename)
            for line in excludeListFilehandle:
                targets = line.strip('\n').strip()
                excludeDict[targets] = 1
            excludeListFilehandle.close()
    
        # create a list and a dictionary of targets to include even if they do not meet the freq and docprop criteria
        includeList = []
        includeDict = {}
        includeCounter = 0
        inBothLists = 0
        inBothListsList = []
        zeroFreqs = 0
        zeroFreqList = []
        if includeListFilename:
            includeListFilehandle = open(includeListFilename)
            for line in includeListFilehandle:
                target = line.strip('\n').strip()
                currentOK = 1
                if target in excludeDict:
                    inBothLists += 1
                    inBothListsList.append(target)
                    currentOK = 0
                if not target in self.masterTypeFreqDict:
                    zeroFreqs += 1
                    zeroFreqList.append(target)
                    currentOK = 0
                if currentOK:
                    includeList.append(target)
                    includeDict[target] = includeCounter
                    includeCounter += 1
            includeListFilehandle.close()
            
            if zeroFreqs > 0:
                print
                print "Warning: The following %s targets were in the include list, but never occurred in the corpus. They will be removed from the include list." % zeroFreqs
                for currentTarget in zeroFreqList:
                    print "     %s" % currentTarget
            if inBothLists > 0:
                print
                print "Error: The following %s targets were in both the include and exclude lists. Please choose one or the other." % inBothLists
                for currentTarget in inBothListsList:
                    print "     %s" % currentTarget                
                sys.exit(0)
    
        # get the maximum number of targets
        if numTargetsThreshold:
            maxTargets = numTargetsThreshold
        else:
            maxTargets = self.numTypes
        
        # add corpus targets to the list until it is of size maxTargets
        done = 0
        docPropExcludeCount = 0
        freqExcludeCount = 0
        
        for i in range(len(self.sortedTargetFreqList)):
            if done:
                break
            if not self.sortedTargetFreqList[i][0] in includeDict:
                if not self.sortedTargetFreqList[i][0] in excludeDict:
                    if self.sortedTargetFreqList[i][1] >= frequencyThreshold:
                        if self.typeDocumentProportionDict[self.sortedTargetFreqList[i][0]] >= docPropThreshold:
                            includeList.append(self.sortedTargetFreqList[i][0])
                            includeDict[self.sortedTargetFreqList[i][0]] = includeCounter
                            includeCounter += 1
                            if includeCounter >= maxTargets:
                                done = 1
                        else:
                            docPropExcludeCount += 1
                    else:
                        freqExcludeCount += 1
        
        outputFilehandle = open(self.corpusDirectory+outputFilename, "w")
        for i in range(len(includeList)):
            outputFilehandle.write("%s\n" % includeList[i])
        outputFilehandle.close()
        
        print
        print "Final list was %s targets out of %s targets in the corpus" % (len(includeList), self.numTypes)
        print "     %s targets were excluded because they were on the exclude list" % len(excludeDict)
        print "     %s targets were excluded because they didn't meet the frequency threshold of %s occurrences" % (freqExcludeCount, frequencyThreshold)
        print "     %s targets were excluded because they didn't meet the document proportion threshold of existing in %f of the documents" % (docPropExcludeCount, docPropThreshold)

    ############################################################################################               
    def outputDocumentSubList(self, outputFilename, typeThreshold, tokenThreshold, numDocumentsThreshold, includeListFilename, excludeListFilename):
    
        # create a stop list dictionary and add any documents in the stop list file if there is one
        excludeDict = {}
        if excludeListFilename:
            excludeListFilehandle = open(excludeListFilename)
            for line in excludeListFilehandle:
                document = line.strip('\n').strip()
                excludeDict[document] = 1
            excludeListFilehandle.close()
    
        # create a list and a dictionary of documents to include even if they do not meet the freq and docprop criteria
        includeList = []
        includeDict = {}
        includeCounter = 0
        inBothLists = 0
        inBothListsList = []
        if includeListFilename:
            includeListFilehandle = open(includeListFilename)
            for line in includeListFilehandle:
                document = line.strip('\n').strip()
                currentOK = 1
                if document in excludeDict:
                    inBothLists += 1
                    inBothListsList.append(document)
                    currentOK = 0
                if not document in self.rawDocumentDict:
                    zeroFreqs += 1
                    zeroFreqList.append(document)
                    currentOK = 0
                if currentOK:
                    includeList.append(document)
                    includeDict[document] = (self.rawDocumentDict[document], includeCounter)
                    includeCounter += 1
            includeListFilehandle.close()
            
            if zeroFreqs > 0:
                print
                print "Warning: The following %s documents were in the include list, but never occurred in the corpus. They will be removed from the include list." % zeroFreqs
                for currentDocument in zeroFreqList:
                    print "     %s" % currentDocument
            if inBothLists > 0:
                print
                print "Error: The following %s documents were in both the include and exclude lists. Please choose one or the other." % inBothLists
                for currentDocument in inBothListsList:
                    print "     %s" % currentDocument                
                sys.exit(0)
                
        # get the maximum number of documents
        if numDocumentsThreshold:
            maxDocuments = numDocumentsThreshold
        else:
            maxDocuments = self.numDocuments
            
        # add documents to the list until it is of size maxDocuments 
        done = 0
        typeFreqExcludeCount = 0
        tokenFreqExcludeCount = 0
        
        for i in range(len(self.sortedDocumentTypeFreqList)):
            if done:
                break
            if not self.sortedDocumentTypeFreqList[i][0] in includeDict:
                if not self.sortedDocumentTypeFreqList[i][0] in excludeDict:
                    if self.sortedDocumentTypeFreqList[i][1] >= typeThreshold:
                        if self.tokensPerDocumentDict[self.sortedDocumentTypeFreqList[i][0]] >= tokenThreshold:
                
                            includeList.append(self.sortedDocumentTypeFreqList[i][0])
                            includeDict[self.sortedDocumentTypeFreqList[i][0]] = includeCounter
                            includeCounter += 1
                            if includeCounter >= maxDocuments:
                                done = 1
                        else:
                            tokenFreqExcludeCount += 1
                    else:
                        typeFreqExcludeCount += 1
        
        outputFilehandle = open(self.corpusDirectory+outputFilename, "w")
        for i in range(len(includeList)):
            outputFilehandle.write("%s\n" % includeList[i])
        outputFilehandle.close()
        
        print
        print "Final list was %s documents out of %s documents in the corpus" % (len(includeList), self.numDocuments)
        print "     %s documents were excluded because they were on the exclude list" % len(excludeDict)
        print "     %s documents were excluded because they didn't meet the type frequency threshold of %s occurrences" % (typeFreqExcludeCount, typeThreshold)
        print "     %s documents were excluded because they didn't meet the token frequency threshold of %s occurrences" % (tokenFreqExcludeCount, tokenThreshold)

############################################################################################
    def outputFreqs(self, outputFilename, includeListFilename, excludeListFilename, sortByFreq, partsPerMillion, logged):
        print "Outputting Frequency Information"
    
        # create a stop list dictionary and add any targets in the stop list file if there is one
        excludeDict = {}
        if excludeListFilename:
            excludeListFilehandle = open(excludeListFilename)
            for line in excludeListFilehandle:
                target = line.strip('\n').strip()
                excludeDict[target] = 1
            excludeListFilehandle.close()
    
        # create a list and a dictionary of targets to include even if they do not meet the freq and docprop criteria
        includeList = []
        includeDict = {}
        if includeListFilename:
            includeListFilehandle = open(includeListFilename)
            for line in includeListFilehandle:
                target = line.strip('\n').strip()
                includeDict[target] = 1
                includeList.append(target)
            includeListFilehandle.close()
        else:
            includeList = self.masterTypeList
            
        outputList = []
        for target in includeList:
            if not target in excludeDict:
                if target in self.masterTypeFreqDict:
                    freq = self.masterTypeFreqDict[target]
                else:
                    freq = 0
                if partsPerMillion:
                    freq = (float(freq) / self.numTokens) * 1000000
                if logged:
                    freq = math.log10(freq+1)
                outputList.append((target, freq))
                
        if sortByFreq:
            outputList = tuple(sorted(outputList, key=itemgetter(1), reverse=True))
            
        outputFilehandle = open(outputFilename, 'w')
        for targetTuple in outputList:
            outputFilehandle.write("%s %s\n" % (targetTuple[0], targetTuple[1]))
        outputFilehandle.close()
        
############################################################################################
    def outputDocDiversities(self, outputFilename, includeListFilename, excludeListFilename):
        print "Outputting Document Diversity Information"
    
        # create a stop list dictionary and add any targets in the stop list file if there is one
        excludeDict = {}
        if excludeListFilename:
            excludeListFilehandle = open(excludeListFilename)
            for line in excludeListFilehandle:
                target = line.strip('\n').strip()
                excludeDict[target] = 1
            excludeListFilehandle.close()
    
        # create a list and a dictionary of targets to include even if they do not meet the freq and docprop criteria
        includeList = []
        includeDict = {}
        if includeListFilename:
            includeListFilehandle = open(includeListFilename)
            for line in includeListFilehandle:
                target = line.strip('\n').strip()
                includeDict[target] = 1
                includeList.append(target)
            includeListFilehandle.close()
        else:
            includeList = self.masterTypeList
            
        outputList = []
        for target in includeList:
            if not target in excludeDict:
                if target in self.typeDocumentProportionDict:
                    docDiv = self.typeDocumentProportionDict[target]
                else:
                    docDiv = 0
                outputList.append((target, docDiv))
            
        outputFilehandle = open(outputFilename, 'w')
        for targetTuple in outputList:
            outputFilehandle.write("%s %s\n" % (targetTuple[0], targetTuple[1]))
        outputFilehandle.close()