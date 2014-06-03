import sys, os, shutil, time, datetime, operator
import scipy
from operator import itemgetter, attrgetter
import sm_libs.normalizations as norm
import sm_libs.simMatrix as simMatrix
################################################################################################
################################################################################################
class tdMatrix:
    ############################################################################################
    def __init__(self):
        self.corpusDirectory = 0            # the path of the corpus directory
        self.matrixDirectory = 0            # the name of the matrix, the folder it is in

        self.targetList = []                # a list of all the targets
        self.targetCorpusDict = {}          # a dictionary indexed by the target string, pointing to its index number in the original corpus
        self.targetCorpusIndexDict = {}     # a dictionary indexed by the index number in the original corpus, pointing to the target string
        self.targetMatrixDict = {}          # a dictionary indexed by the target string, pointing to its index number in the original corpus
        self.targetMatrixIndexDict = {}     # a dictionary indexed by the index number in the original corpus, pointing to the target string
        self.numTargets = 0                 # the number of target words
        self.targetFreqs = []               # a list of dictionaries, with the frequency of each target in each document, summed across documents
        self.targetSumFreqs = []            # a list containing the frequency of each target, summed across documents
        
        self.documentList = []              # a list of all the document labels
        self.documentCorpusDict = {}        # a dictionary of docnames pointing to the original index numbers in the corpus
        self.documentMatrixDict = {}        # a dictionary of original corpus indexes pointing to doc names
        self.documentCorpusIndexDict = {}   # a dictionary of docnames pointing to matrix index numbers (e.g. included docs only)
        self.documentMatrixIndexDict = {}   # a dictionary of matrix indexes pointing to doc names
        self.numDocuments = 0               # the number of documents
        self.documentSizes = []             # a list of the number of tokens in each file
        self.documentSums = []              # a list of the number of counted tokens in each file
    
    ############################################################################################
    def initializeMatrix(self, corpusDirectory, matrixDirectory):
        self.ST = (datetime.datetime.now()).timetuple()
        
        self.corpusDirectory = corpusDirectory
        self.matrixDirectory = matrixDirectory
    
        if os.path.isdir(self.corpusDirectory+self.matrixDirectory):
        
            print
            print "         Warning: The matrix directory %s already exists in the %s corpus directory." % (self.matrixDirectory, self.corpusDirectory)
            userInput = raw_input("         Do you want to erase and overwrite this directory? (y/n) -->")
            print
            if ((userInput == "y") or (userInput == "Y")):
                shutil.rmtree(self.corpusDirectory+self.matrixDirectory)
            else:
                sys.exit(0)

        os.mkdir(self.corpusDirectory+self.matrixDirectory)
        
    ############################################################################################
    def getTargetList(self, targetListFilename):
    
        if targetListFilename:
            targetListFilehandle = open(targetListFilename)
        else:
            targetListFilehandle = open(self.corpusDirectory+"target_info.txt")
    
        for line in targetListFilehandle:
            data = (line.strip("\n").strip()).split()
            if len(data) > 0:
                newTarget = data[0]
                
                if len(newTarget) > 0:
                    if not newTarget in self.targetMatrixDict:
                        self.targetList.append(newTarget)
                        self.targetMatrixDict[newTarget] = self.numTargets
                        self.targetMatrixIndexDict[self.numTargets] = newTarget
                        self.numTargets += 1
        targetListFilehandle.close()
        
        self.targetSumFreqs = [0]*self.numTargets
        
    ############################################################################################
    def getDocumentList(self, documentListFilename):
    
        if documentListFilename:
            includeDict = {}

            documentListFilehandle = open(documentListFilename)
            for line in documentListFilehandle:
                
                data = (line.strip("\n").strip()).split()
                if len(data) > 0:
                    newDocument = data[0]
                    if not newDocument in includeDict:
                        includeDict[newDocument] = 1
            documentListFilehandle.close()
            
            documentListFilehandle = open(self.corpusDirectory+"document_info.txt")
            for line in documentListFilehandle:
                data = (line.strip("\n").strip()).split()
                if len(data) > 1:
                    newDocument = data[0]
                    newIndex = int(data[1])
                    if newDocument in includeDict:                    
                        if not newDocument in self.documentCorpusDict:
                        
                            self.documentList.append(newDocument)
                            self.documentCorpusDict[newDocument] = newIndex
                            self.documentMatrixDict[newDocument] = self.numDocuments
                            self.documentCorpusIndexDict[newIndex] = newDocument
                            self.documentMatrixIndexDict[self.numDocuments] = newDocument
                            self.numDocuments += 1
            documentListFilehandle.close()
            
        else:
            documentListFilehandle = open(self.corpusDirectory+"document_info.txt")
            for line in documentListFilehandle:
                data = (line.strip("\n").strip()).split()
                if len(data) > 1:
                    newDocument = data[0]
                    newIndex = int(data[1])
                    if not newDocument in self.documentCorpusDict:
                    
                        self.documentList.append(newDocument)
                        self.documentCorpusDict[newDocument] = newIndex
                        self.documentMatrixDict[newDocument] = self.numDocuments
                        self.documentCorpusIndexDict[newIndex] = newDocument
                        self.documentMatrixIndexDict[self.numDocuments] = newDocument
                        self.numDocuments += 1
            documentListFilehandle.close()
        
        self.documentSizes = [0]*self.numDocuments
        self.documentSums = [0]*self.numDocuments

    ############################################################################################
    def processCorpus(self):

        linecounter = 0
        documentIndex = 0
        corpusFilehandle = open(self.corpusDirectory+"corpus.txt")
        for line in corpusFilehandle:
            
            
            if linecounter in self.documentCorpusIndexDict:
                startTime = time.time()
                currentTotalTokens = 0
                currentCountedTokens = 0
                currentFreqDict = {}
                
                data = (line.strip('\n').strip()).split()
                
                for token in data:
                    currentTotalTokens += 1
                    if token in self.targetMatrixDict:
                        currentCountedTokens += 1
                        self.targetSumFreqs[self.targetMatrixDict[token]] += 1
                        if token in currentFreqDict:
                            currentFreqDict[token] += 1
                        else:
                            currentFreqDict[token] = 1
                
                self.targetFreqs.append(currentFreqDict)
                self.documentSizes[documentIndex] = currentTotalTokens
                self.documentSums[documentIndex] = currentCountedTokens
                
                took = time.time() - startTime
                print "         Finished Document %s. Counted %s of %s Tokens (%6.4f sec.)" % (self.documentList[documentIndex], currentCountedTokens, currentTotalTokens, took)
                documentIndex += 1
            linecounter += 1
    
        corpusFilehandle.close()
        
    ############################################################################################
    def outputDocumentInfo(self):
        infoFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/document_info.txt", "w")
        for documentCounter in range(self.numDocuments):
            infoFilehandle.write("%s %s %s %s %s\n" % (documentCounter, self.documentList[documentCounter], self.documentSizes[documentCounter], self.documentSums[documentCounter], self.documentCorpusDict[self.documentMatrixIndexDict[documentCounter]]))
        infoFilehandle.close()
        
    ############################################################################################
    def outputTargetInfo(self):
        targetInfoFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/target_info.txt", "w")
        for i in range(self.numTargets):
            targetInfoFilehandle.write("%s %s %s\n" % (self.targetMatrixDict[self.targetList[i]], self.targetList[i], self.targetSumFreqs[i]))    
        targetInfoFilehandle.close()

    ############################################################################################
    def outputTargetDocumentCountMatrix(self):
        print "Outputting Target x Document Frequency Matrix"
        matrixFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/targetXdocument_counts.txt", "w")
        for documentCounter in range(self.numDocuments):
            matrixFilehandle.write("%s " % documentCounter)
            for targetCounter in range(self.numTargets):
                if self.targetMatrixIndexDict[targetCounter] in self.targetFreqs[documentCounter]:
                    matrixFilehandle.write(" %s:%s" % (targetCounter, self.targetFreqs[documentCounter][self.targetMatrixIndexDict[targetCounter]]))
            matrixFilehandle.write("\n")
        matrixFilehandle.close()

    ############################################################################################
    def outputMatrixInfo(self):
        summaryFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/matrix_summary.txt", "w")
        summaryFilehandle.write("num_documents: %s\n" % self.numDocuments)
        summaryFilehandle.write("num_targets: %s\n" % self.numTargets)
        summaryFilehandle.write("datetime_started: %s-%s-%s_%s:%s:%s\n" % (self.ST[0],self.ST[1],self.ST[2],self.ST[3],self.ST[4],self.ST[5]))
        DT = (datetime.datetime.now()).timetuple()
        summaryFilehandle.write("datetime_finished: %s-%s-%s_%s:%s:%s\n" % (DT[0],DT[1],DT[2],DT[3],DT[4],DT[5]))
        summaryFilehandle.close()

    ############################################################################################
    def importMatrixInfo(self, matrixDirectory):
        self.matrixDirectory = matrixDirectory
        matrixInfoFilehandle = open(self.matrixDirectory+"matrix_summary.txt")
        for line in matrixInfoFilehandle:
            data = (line.strip('\n').strip()).split()
            if data[0] == "datetime_started:":
                self.datetimeStarted = data[1]
            elif data[0] == "datetime_finished:":
                self.datetimeFinished = data[1]            
        matrixInfoFilehandle.close()
        
    ############################################################################################    
    def importDocumentInfo(self, documentInclusionFile, documentExclusionFile):
        
        # if there is an exclusion list, add those items to a dictionary
        excludeDict = {}
        if documentExclusionFile:
            documentExclusionFilehandle = open(documentExclusionFile)
            for line in documentExclusionFilehandle:
                document = line.strip('\n').strip()
                excludeDict[document] = 1
            documentExclusionFilehandle.close()    
        
        try:
            documentFilehandle = open(self.matrixDirectory + "/document_info.txt")
        except:
            documentFilehandle = open(self.matrixDirectory + "document_info.txt")
        
        self.subDocumentList = []
        self.subDocumentDict = {}
        self.subDocumentIndexDict = {}
        
        # if the user specified that only a subset of documents are to be used
        # then add only those items to the matrix, excluding any in the exclude dict
        if documentInclusionFile:
            # read in that subset from the file
            includeDict = {}
            documentInclusionFilehandle = open(documentInclusionFile)
            for line in documentInclusionFilehandle:
                word = line.strip('\n').strip()
                includeDict[word] = 1
            documentInclusionFilehandle.close()
            
            # then read in the master list of documents but only keep the ones that were in the sublist
            documentCounter = 0
            lineCounter = 1
            for line in documentFilehandle:
                data = (line.strip('\n').strip()).split()
                if data[1] in includeDict:
                    if not data[1] in excludeDict:
                        self.documentList.append(data[1])
                        self.documentSizes.append(int(data[2]))
                        self.documentMatrixDict[data[1]] = int(data[0])
                        self.documentMatrixIndexDict[int(data[0])] = data[1]
                        self.subDocumentList.append(data[1])
                        self.subDocumentDict[data[1]] = documentCounter
                        self.subDocumentIndexDict[documentCounter] = data[1]
                        documentCounter += 1
                lineCounter += 1

        else:
            # otherwise, just read in the master list, excluding any in the exclude dict
            lineCounter = 1
            documentCounter = 0
            for line in documentFilehandle:
                data = (line.strip('\n').strip()).split()
                if not data[1] in excludeDict:
                    self.documentList.append(data[1])
                    self.documentSizes.append(int(data[2]))
                    self.documentMatrixDict[data[1]] = int(data[0])
                    self.documentMatrixIndexDict[int(data[0])] = data[1]
                    self.subDocumentList.append(data[1])
                    self.subDocumentDict[data[1]] = documentCounter
                    self.subDocumentIndexDict[documentCounter] = data[1]
                    documentCounter += 1
                lineCounter += 1
                
        documentFilehandle.close()
        self.numDocuments = lineCounter - 1
        self.numSubDocuments = len(self.subDocumentDict)
        
    ###########################################################################################
    def importTargetInfo(self, targetInclusionFile, targetExclusionFile):
    
        # if there is an exclusion list, add those items to a dictionary
        excludeDict = {}
        if targetExclusionFile:
            targetExclusionFilehandle = open(targetExclusionFile)
            for line in targetExclusionFilehandle:
                target = line.strip('\n').strip()
                excludeDict[target] = 1
            targetExclusionFilehandle.close()    
        
        targetFilehandle = open(self.matrixDirectory + "/target_info.txt")
        self.subTargetList = []
        self.subTargetDict = {}
        self.subTargetIndexDict = {}
        
        # if the user specified that only a subset of documents are to be used
        # then add only those items to the matrix, excluding any in the exclude dict
        if targetInclusionFile:
            # read in that subset from the file
            includeDict = {}
            targetInclusionFilehandle = open(targetInclusionFile)
            for line in targetInclusionFilehandle:
                target = line.strip('\n').strip()
                includeDict[target] = 1
            targetInclusionFilehandle.close()
            
            # then read in the master list of documents but only keep the ones that were in the sublist
            targetCounter = 0
            lineCounter = 1
            for line in targetFilehandle:
                data = (line.strip('\n').strip()).split()
                if data[1] in includeDict:
                    if not data[1] in excludeDict:
                        self.targetList.append(data[1])
                        self.targetFreqs.append(int(data[2]))
                        self.targetMatrixDict[data[1]] = int(data[0])
                        self.targetMatrixIndexDict[int(data[0])] = data[1]
                        self.subTargetList.append(data[1])
                        self.subTargetDict[data[1]] = targetCounter
                        self.subTargetIndexDict[targetCounter] = data[1]
                        targetCounter += 1
                lineCounter += 1

        else:
            # otherwise, just read in the master list, excluding any in the exclude dict
            lineCounter = 1
            targetCounter = 0
            for line in targetFilehandle:
                data = (line.strip('\n').strip()).split()
                if not data[1] in excludeDict:
                    self.targetList.append(data[1])
                    self.targetFreqs.append(int(data[2]))
                    self.targetMatrixDict[data[1]] = int(data[0])
                    self.targetMatrixIndexDict[int(data[0])] = data[1]
                    self.subTargetList.append(data[1])
                    self.subTargetDict[data[1]] = targetCounter
                    self.subTargetIndexDict[targetCounter] = data[1]
                    targetCounter += 1
                lineCounter += 1
                
        targetFilehandle.close()
        self.numTargets = lineCounter - 1
        self.numSubTargets = len(self.subTargetDict)
             
    ############################################################################################
    def importTargetDocumentMatrix(self):
        print "...Importing target-document count matrix"
        self.subTargetFreqs = scipy.zeros([self.numSubTargets, self.numSubDocuments], float)

        targetFilehandle = open(self.matrixDirectory + "targetXdocument_counts.txt")
        lineCounter = 1
        for line in targetFilehandle:
            data = (line.strip('\n').strip()).split()
            if int(data[0]) in self.documentMatrixIndexDict:
                for i in range(len(data[1:])):
                    currentPair = data[i+1].split(":")
                    if int(currentPair[0]) in self.targetMatrixIndexDict:
                        self.subTargetFreqs[self.subTargetDict[self.targetMatrixIndexDict[int(currentPair[0])]], self.subDocumentDict[self.documentMatrixIndexDict[int(data[0])]]] = int(currentPair[1])
            lineCounter += 1
        targetFilehandle.close()
        
        wereThereZeros = 0
        self.targetSums = self.subTargetFreqs.sum(1)
        for i in range(self.numSubTargets):
            if self.targetSums[i] == 0:
                print
                print "         Warning! Target %s has a frequency of zero for this set of documents" % (self.subTargetIndexDict[i])
                wereThereZeros += 1
        if wereThereZeros:
            response = raw_input("          There were %s targets with frequencies of zero. Are you sure you want to continue? (y/n)" % wereThereZeros)
            print
            if ((response == "N") or (response == "n")):
                sys.exit(0)

        self.documentSums = self.subTargetFreqs.sum(0)
        for j in range(self.numSubDocuments):
            if self.documentSums[j] == 0:
                print
                print "          Warning! Document %s has zero targets for this set of targets" % (self.subDocumentIndexDict[j])
                wereThereZeros += 1
        if wereThereZeros:
            response = raw_input("          There were %s documents with target counts of zero. Are you sure you want to continue? (y/n)" % wereThereZeros)
            print
            if ((response == "N") or (response == "n")):
                sys.exit()
    
    ############################################################################################   
    def normalizeTargetDocumentMatrix(self, normalizationMethod):
        self.normalizationMethod = normalizationMethod

        if self.normalizationMethod == 0:
            self.normalizedTargetDocumentMatrix = self.subTargetFreqs
        elif self.normalizationMethod == 1:
            self.normalizedTargetDocumentMatrix = norm.rowProbabilityNormalization(self.subTargetFreqs)
        elif self.normalizationMethod == 2:
            self.normalizedTargetDocumentMatrix = norm.columnProbabilityNormalization(self.subTargetFreqs)
        elif self.normalizationMethod == 3:
            self.normalizedTargetDocumentMatrix = norm.lengthRowNormalization(self.subTargetFreqs)
        elif self.normalizationMethod == 4:
            self.normalizedTargetDocumentMatrix = norm.zscoreRowsNormalization(self.subTargetFreqs)
        elif self.normalizationMethod == 5:
            self.normalizedTargetDocumentMatrix = norm.zscoreColumnsNormalization(self.subTargetFreqs)
        elif self.normalizationMethod == 11:
            self.normalizedTargetDocumentMatrix = norm.logRowEntropyNormalization(self.subTargetFreqs)
        elif self.normalizationMethod == 12:
            self.normalizedTargetDocumentMatrix = norm.pmiNormalization(self.subTargetFreqs)
        elif self.normalizationMethod == 13:
            self.normalizedTargetDocumentMatrix = norm.positivePmiNormalization(self.subTargetFreqs)
        elif self.normalizationMethod == 14:
            self.normalizedTargetDocumentMatrix = norm.coalsCorrelationNormalization(self.subTargetFreqs)
        elif self.normalizationMethod == 14:
            self.normalizedTargetDocumentMatrix = norm.integerizeNormalization(self.subTargetFreqs)
    
    ############################################################################################   
    def calculateAllSimilarities(self, similarityMetric):
    
        self.similarityMetric = similarityMetric
        
        self.outputFilename = "tdSimilarities_N%s_M%s.txt" % (self.normalizationMethod, self.similarityMetric)
        normTypeName = norm.getNormMethodName(self.normalizationMethod)

        self.the_simMatrix = simMatrix.simMatrix()
        simMetricName = self.the_simMatrix.getSimMetricName(self.similarityMetric)
        updateString = "%s %s %s\n" % (self.outputFilename, normTypeName, simMetricName)
        
        self.the_simMatrix.assignTargetInfo(self.subTargetList, self.subTargetDict, self.subTargetIndexDict)
        self.the_simMatrix.assignColumnInfo(self.subDocumentList, self.subDocumentDict, self.subDocumentIndexDict)
        self.the_simMatrix.assignMatrixData(self.normalizedTargetDocumentMatrix)
        
        self.the_simMatrix.initNewSimMatrix(self.matrixDirectory, "tdSimilarities", self.outputFilename, updateString)
        self.the_simMatrix.calculateAllSimilarities(similarityMetric)
        self.the_simMatrix.outputSimilarityMatrix()
        
    ############################################################################################   
    def outputFullTDMatrix(self):
        
        print "Outputting Full Target x Document Frequency Matrix"
        matrixFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/targetXdocument_counts_full.txt", "w")
        for targetCounter in range(self.numTargets):
            for documentCounter in range(self.numDocuments):
                if self.targetMatrixIndexDict[targetCounter] in self.targetFreqs[documentCounter]:
                    matrixFilehandle.write("%s " % (self.targetFreqs[documentCounter][self.targetMatrixIndexDict[targetCounter]]))
                else:
                    matrixFilehandle.write("0 ")
            matrixFilehandle.write("\n")
        matrixFilehandle.close()
    
    