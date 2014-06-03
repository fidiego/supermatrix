import sys, os, time, datetime, shutil, math, operator
import scipy
import sm_libs.normalizations as norm
import sm_libs.simMatrix as simMatrix
import scipy.stats
import numpy
################################################################################################
################################################################################################
class tcMatrix:
    ############################################################################################
    def __init__(self):
        
        self.corpusDirectory = 0
        self.matrixDirectory = 0
        self.windowSize = 0
        self.distinctDocs = 0
        
        self.targetList = []                # a list of all the targets
        self.targetCorpusDict = {}          # a dictionary indexed by the target string, pointing to its index number in the original corpus
        self.targetCorpusIndexDict = {}     # a dictionary indexed by the index number in the original corpus, pointing to the target string
        self.targetMatrixDict = {}          # a dictionary indexed by the target string, pointing to its index number in the original corpus
        self.targetMatrixIndexDict = {}     # a dictionary indexed by the index number in the original corpus, pointing to the target string
        self.numTargets = 0                 # the number of target words
        self.targetFreqs = []               # a list of dictionaries, with the frequency of each target in each document, summed across documents
        self.targetSumFreqs = []            # a list containing the frequency of each target, summed across documents
        
        self.contextList = []                # a list of all the contexts
        self.contextCorpusDict = {}          # a dictionary indexed by the context string, pointing to its index number in the original corpus
        self.contextCorpusIndexDict = {}     # a dictionary indexed by the index number in the original corpus, pointing to the context string
        self.contextMatrixDict = {}          # a dictionary indexed by the context string, pointing to its index number in the original corpus
        self.contextMatrixIndexDict = {}     # a dictionary indexed by the index number in the original corpus, pointing to the context string
        self.numContexts = 0                 # the number of context words
        self.contextFreqs = []               # a list of dictionaries, with the frequency of each context in each document, summed across documents
        self.contextSumFreqs = []            # a list containing the frequency of each context, summed across documents        
        
        self.documentList = []              # a list of all the document labels
        self.documentCorpusDict = {}        # a dictionary of docnames pointing to the original index numbers in the corpus
        self.documentMatrixDict = {}        # a dictionary of original corpus indexes pointing to doc names
        self.documentCorpusIndexDict = {}   # a dictionary of docnames pointing to matrix index numbers (e.g. included docs only)
        self.documentMatrixIndexDict = {}   # a dictionary of matrix indexes pointing to doc names
        self.numDocuments = 0               # the number of documents
        self.documentSizes = []             # a list of the number of tokens in each file
        self.documentTargetSums = []        # a list of the number of counted targets in each file
        self.documentContextSums = []        # a list of the number of counted contexts in each file

        self.summed_fMatrix = {}            # the sparse matrix containing forward target->context co-occurrences, summed across documents
        self.summed_bMatrix = {}            # the sparse matrix containing forward context<-target co-occurrences, summed across documents
        self.last_fMatrix = {}              # the sparse matrix containing forward target->context co-occurrences, for the most recent document
        self.last_bMatrix = {}              # the sparse matrix containing forward context<-target co-occurrences, for the most recent document
        self.collapsed_matrix = {}
        
    ############################################################################################
    ############################################################################################
    def initializeMatrix(self, corpusDirectory, matrixDirectory, windowSize, distinctDocs):
        self.ST = (datetime.datetime.now()).timetuple()
        
        self.corpusDirectory = corpusDirectory
        self.matrixDirectory = matrixDirectory
        self.windowSize = windowSize
        self.distinctDocs = distinctDocs
    
        if os.path.isdir(self.corpusDirectory+self.matrixDirectory):
        
            print
            print "Warning: The matrix directory %s already exists in the %s corpus directory." % (self.matrixDirectory, self.corpusDirectory)
            userInput = raw_input("Do you want to erase and overwrite this directory? (y/n) -->")
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
    def getContextList(self, contextListFilename):
    
        if contextListFilename:
            contextListFilehandle = open(contextListFilename)
        else:
            contextListFilehandle = open(self.corpusDirectory+"target_info.txt")
    
        for line in contextListFilehandle:
            data = (line.strip("\n").strip()).split()
            if len(data) > 0:
                newContext = data[0]
                
                if len(newContext) > 0:
                    if not newContext in self.contextMatrixDict:
                        self.contextList.append(newContext)
                        self.contextMatrixDict[newContext] = self.numContexts
                        self.contextMatrixIndexDict[self.numContexts] = newContext
                        self.numContexts += 1
        contextListFilehandle.close()
        
        self.contextSumFreqs = [0]*self.numContexts
        
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
        self.documentTargetSums = [0]*self.numDocuments
        self.documentContextSums = [0]*self.numDocuments

    ############################################################################################
    def processCorpusCollapsed(self):
    
        linecounter = 0
        documentIndex = 0
        corpusFilehandle = open(self.corpusDirectory+"corpus.txt")

        window = []
        for line in corpusFilehandle:    
            if linecounter in self.documentCorpusIndexDict:
                startTime = time.time()
                currentTotalTokens = 0
                currentCountedTargets = 0
                currentTargetFreqDict = {}
                
                data = (line.strip('\n').strip()).split()
                
                for token in data:
                    
                    currentTotalTokens += 1
                    window.append(token)
                    
                    if len(window) >= self.windowSize+1:
                    
                        if window[0] in self.targetMatrixDict:
                            currentCountedTargets += 1
                            self.targetSumFreqs[self.targetMatrixDict[window[0]]] += 1
                            if window[0] in currentTargetFreqDict:
                                currentTargetFreqDict[window[0]] += 1
                            else:
                                currentTargetFreqDict[window[0]] = 1
                
                            for wordRange in range(len(window)-1):
                                if window[wordRange+1] in self.targetMatrixDict:
                                    if (window[0], window[wordRange+1]) in self.collapsed_matrix:
                                        self.collapsed_matrix[(window[0], window[wordRange+1])] += 1
                                    else:
                                        self.collapsed_matrix[(window[0], window[wordRange+1])] = 1                                      

                        # we're done with word1, remove it from the window
                        window = window[1:]
                
                # flush the remainder of the window, same code as above
                while len(window) > 0:
                        if window[0] in self.targetMatrixDict:
                            currentCountedTargets += 1
                            self.targetSumFreqs[self.targetMatrixDict[window[0]]] += 1
                            if window[0] in currentTargetFreqDict:
                                currentTargetFreqDict[window[0]] += 1
                            else:
                                currentTargetFreqDict[window[0]] = 1
                
                            for wordRange in range(len(window)-1):
                                if window[wordRange+1] in self.targetMatrixDict:
                                    if (window[0], window[wordRange+1]) in self.collapsed_matrix:
                                        self.collapsed_matrix[(window[0], window[wordRange+1])] += 1
                                    else:
                                        self.collapsed_matrix[(window[0], window[wordRange+1])] = 1                                      

                        # we're done with word1, remove it from the window
                        window = window[1:]
                    
                self.targetFreqs.append(currentTargetFreqDict)
                self.documentSizes[documentIndex] = currentTotalTokens
                self.documentTargetSums[documentIndex] = currentCountedTargets
                
                took = time.time() - startTime
                print "         Finished Document %s. Counted %s of %s Tokens (%6.4f sec.)" % (self.documentList[documentIndex], currentCountedTargets, currentTotalTokens, took)
                documentIndex += 1
            linecounter += 1
    
        corpusFilehandle.close()
        
    ############################################################################################
    def processCorpus(self):

        linecounter = 0
        documentIndex = 0
        corpusFilehandle = open(self.corpusDirectory+"corpus.txt")

        window = []
        for line in corpusFilehandle:    
            if linecounter in self.documentCorpusIndexDict:
                startTime = time.time()
                currentTotalTokens = 0
                currentCountedTargets = 0
                currentCountedContexts = 0
                currentTargetFreqDict = {}
                currentContextFreqDict = {}
                
                data = (line.strip('\n').strip()).split()
                
                for token in data:
                    
                    currentTotalTokens += 1
                    window.append(token)
                    
                    if len(window) >= self.windowSize+1:
                    
                        if ((window[0] in self.targetMatrixDict) or (window[0] in self.contextMatrixDict)):
                    
                            if window[0] in self.targetMatrixDict:
                                currentCountedTargets += 1
                                self.targetSumFreqs[self.targetMatrixDict[window[0]]] += 1
                                if window[0] in currentTargetFreqDict:
                                    currentTargetFreqDict[window[0]] += 1
                                else:
                                    currentTargetFreqDict[window[0]] = 1
                                    
                            if window[0] in self.contextMatrixDict:
                                currentCountedContexts += 1
                                self.contextSumFreqs[self.contextMatrixDict[window[0]]] += 1
                                if window[0] in currentContextFreqDict:
                                    currentContextFreqDict[window[0]] += 1
                                else:
                                    currentContextFreqDict[window[0]] = 1
                                    
                            for wordRange in range(len(window)-1):
                                # if token1 is a target and token2 is a context, increment the count in the fMatrix dict
                                if ((window[0] in self.targetMatrixDict) and (window[wordRange+1] in self.contextMatrixDict)):
                                    if (window[0], window[wordRange+1], wordRange+1) in self.summed_fMatrix:
                                        self.summed_fMatrix[(window[0], window[wordRange+1], wordRange+1)] += 1
                                    else:
                                        self.summed_fMatrix[(window[0], window[wordRange+1], wordRange+1)] = 1
                                    if self.distinctDocs:
                                        if (window[0], window[wordRange+1], wordRange+1) in self.last_fMatrix:
                                            self.last_fMatrix[(window[0], window[wordRange+1], wordRange+1)] += 1
                                        else:
                                            self.last_fMatrix[(window[0], window[wordRange+1], wordRange+1)] = 1                                    
                                        
                                # if token1 is a context and token2 is a target, increment the count in the bMatrix dict
                                if ((window[0] in self.contextMatrixDict) and (window[wordRange+1] in self.targetMatrixDict)):
                                    if (window[wordRange+1], window[0], wordRange+1) in self.summed_bMatrix:
                                        self.summed_bMatrix[(window[wordRange+1], window[0], wordRange+1)] += 1
                                    else:
                                        self.summed_bMatrix[(window[wordRange+1], window[0], wordRange+1)] = 1                                        
                                    if self.distinctDocs:
                                        if (window[wordRange+1], window[0], wordRange+1) in self.last_bMatrix:
                                            self.last_bMatrix[(window[wordRange+1], window[0], wordRange+1)] += 1
                                        else:
                                            self.last_bMatrix[(window[wordRange+1], window[0], wordRange+1)] = 1
                    
                        # we're done with word1, remove it from the window
                        window = window[1:]
                
                # flush the remainder of the window, same code as above
                while len(window) > 0:
                    if ((window[0] in self.targetMatrixDict) or (window[0] in self.contextMatrixDict)):                    
                        if window[0] in self.targetMatrixDict:
                            currentCountedTargets += 1
                            self.targetSumFreqs[self.targetMatrixDict[window[0]]] += 1
                            if window[0] in currentTargetFreqDict:
                                currentTargetFreqDict[window[0]] += 1
                            else:
                                currentTargetFreqDict[window[0]] = 1
                                
                        if window[0] in self.contextMatrixDict:
                            currentCountedContexts += 1
                            self.contextSumFreqs[self.contextMatrixDict[window[0]]] += 1
                            if window[0] in currentContextFreqDict:
                                currentContextFreqDict[window[0]] += 1
                            else:
                                currentContextFreqDict[window[0]] = 1
                                
                        for wordRange in range(len(window)-1):
                            # if token1 is a target and token2 is a context, increment the count in the fMatrix dict
                            if ((window[0] in self.targetMatrixDict) and (window[wordRange+1] in self.contextMatrixDict)):
                                if (window[0], window[wordRange+1], wordRange+1) in self.summed_fMatrix:
                                    self.summed_fMatrix[(window[0], window[wordRange+1], wordRange+1)] += 1
                                else:
                                    self.summed_fMatrix[(window[0], window[wordRange+1], wordRange+1)] = 1
                                if self.distinctDocs:
                                    if (window[0], window[wordRange+1], wordRange+1) in self.last_fMatrix:
                                        self.last_fMatrix[(window[0], window[wordRange+1], wordRange+1)] += 1
                                    else:
                                        self.last_fMatrix[(window[0], window[wordRange+1], wordRange+1)] = 1                                    
                                    
                            # if token1 is a context and token2 is a target, increment the count in the bMatrix dict
                            if ((window[0] in self.contextMatrixDict) and (window[wordRange+1] in self.targetMatrixDict)):
                                if (window[wordRange+1], window[0], wordRange+1) in self.summed_bMatrix:
                                    self.summed_bMatrix[(window[wordRange+1], window[0], wordRange+1)] += 1
                                else:
                                    self.summed_bMatrix[(window[wordRange+1], window[0], wordRange+1)] = 1
                                if self.distinctDocs:
                                    if (window[wordRange+1], window[0], wordRange+1) in self.last_bMatrix:
                                        self.last_bMatrix[(window[wordRange+1], window[0], wordRange+1)] += 1
                                    else:
                                        self.last_bMatrix[(window[wordRange+1], window[0], wordRange+1)] = 1
                
                    # we're done with word1, remove it from the window
                    window = window[1:]
                    
                self.targetFreqs.append(currentTargetFreqDict)
                self.contextFreqs.append(currentContextFreqDict)
                self.documentSizes[documentIndex] = currentTotalTokens
                self.documentTargetSums[documentIndex] = currentCountedTargets
                self.documentContextSums[documentIndex] = currentCountedContexts
                
                if self.distinctDocs:
                    self.outputLastCoocMatrix(documentIndex)
                    self.last_fMatrix = {}
                    self.last_bMatrix = {}
                
                took = time.time() - startTime
                print "         Finished Document %s. Counted %s/%s of %s Tokens (%6.4f sec.)" % (self.documentList[documentIndex], currentCountedTargets, currentCountedContexts, currentTotalTokens, took)
                documentIndex += 1
            linecounter += 1
    
        corpusFilehandle.close()
    ############################################################################################
    def outputCollapsedCoocMatrix(self):
    
        print "Outputting Target x Context Co-occurrence Matrix" 
        collapsedCoocsFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/target_coocs_collapsed.txt", "w")
        
        for targetCounter1 in range(self.numTargets):
            collapsedCoocsFilehandle.write("%s " % targetCounter1)
            
            for targetCounter2 in range(self.numTargets):
                if (self.targetMatrixIndexDict[targetCounter1], self.targetMatrixIndexDict[targetCounter2]) in self.collapsed_matrix:
                
                    collapsedCoocsFilehandle.write(" %s:%s" % (targetCounter2, self.collapsed_matrix[(self.targetMatrixIndexDict[targetCounter1], self.targetMatrixIndexDict[targetCounter2])]))
            collapsedCoocsFilehandle.write("\n")
        collapsedCoocsFilehandle.close()
    
    ############################################################################################
    def outputSummedCoocMatrix(self):
        print "Outputting Target x Context Co-occurrence Matrix" 
        summedCoocsFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/targetXcontext_coocs_summed.txt", "w")
        
        for targetCounter in range(self.numTargets):
            summedCoocsFilehandle.write("%s " % targetCounter)
            
            for contextCounter in range(self.numContexts):
                for windowCounter in range(self.windowSize):
                    if (self.targetMatrixIndexDict[targetCounter], self.contextMatrixIndexDict[contextCounter], windowCounter+1) in self.summed_fMatrix:
                        summedCoocsFilehandle.write(" %s:%s:%s" % (contextCounter, windowCounter+1, self.summed_fMatrix[(self.targetMatrixIndexDict[targetCounter], self.contextMatrixIndexDict[contextCounter], windowCounter+1)]))
                    if (self.targetMatrixIndexDict[targetCounter], self.contextMatrixIndexDict[contextCounter], windowCounter+1) in self.summed_bMatrix:
                        summedCoocsFilehandle.write(" %s:%s:%s" % (contextCounter, -1*(windowCounter+1), self.summed_bMatrix[(self.targetMatrixIndexDict[targetCounter], self.contextMatrixIndexDict[contextCounter], windowCounter+1)]))
            summedCoocsFilehandle.write("\n")
        summedCoocsFilehandle.close()

    ############################################################################################
    def outputLastCoocMatrix(self, documentIndex):
        summedCoocsFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/targetXcontext_coocs_perDocument.txt", "a")
    
        for targetCounter in range(self.numTargets):
            summedCoocsFilehandle.write("%s:%s " % (documentIndex, targetCounter))
            
            for contextCounter in range(self.numContexts):
                for windowCounter in range(self.windowSize):
                    if (self.targetMatrixIndexDict[targetCounter], self.contextMatrixIndexDict[contextCounter], windowCounter+1) in self.last_fMatrix:
                        summedCoocsFilehandle.write(" %s:%s:%s" % (contextCounter, windowCounter+1, self.last_fMatrix[(self.targetMatrixIndexDict[targetCounter], self.contextMatrixIndexDict[contextCounter], windowCounter+1)]))
                    if (self.targetMatrixIndexDict[targetCounter], self.contextMatrixIndexDict[contextCounter], windowCounter+1) in self.last_bMatrix:
                        summedCoocsFilehandle.write(" %s:%s:%s" % (contextCounter, -1*(windowCounter+1), self.last_bMatrix[(self.targetMatrixIndexDict[targetCounter], self.contextMatrixIndexDict[contextCounter], windowCounter+1)]))
            summedCoocsFilehandle.write("\n")
        summedCoocsFilehandle.close()

    ############################################################################################
    def outputCollapsedMatrixInfo(self):
        summaryFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/collapsed_matrix_summary.txt", "w")
        summaryFilehandle.write("num_documents: %s\n" % self.numDocuments)
        summaryFilehandle.write("num_targets: %s\n" % self.numTargets)
        summaryFilehandle.write("window_size: %s\n" % self.windowSize)
        summaryFilehandle.write("datetime_started: %s-%s-%s_%s:%s:%s\n" % (self.ST[0],self.ST[1],self.ST[2],self.ST[3],self.ST[4],self.ST[5]))
        DT = (datetime.datetime.now()).timetuple()
        summaryFilehandle.write("datetime_finished: %s-%s-%s_%s:%s:%s\n" % (DT[0],DT[1],DT[2],DT[3],DT[4],DT[5]))
        summaryFilehandle.close()
        
    ############################################################################################
    def outputMatrixInfo(self):
        summaryFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/matrix_summary.txt", "w")
        summaryFilehandle.write("num_documents: %s\n" % self.numDocuments)
        summaryFilehandle.write("num_targets: %s\n" % self.numTargets)
        summaryFilehandle.write("num_context: %s\n" % self.numContexts)
        summaryFilehandle.write("window_size: %s\n" % self.windowSize)
        summaryFilehandle.write("datetime_started: %s-%s-%s_%s:%s:%s\n" % (self.ST[0],self.ST[1],self.ST[2],self.ST[3],self.ST[4],self.ST[5]))
        DT = (datetime.datetime.now()).timetuple()
        summaryFilehandle.write("datetime_finished: %s-%s-%s_%s:%s:%s\n" % (DT[0],DT[1],DT[2],DT[3],DT[4],DT[5]))
        summaryFilehandle.close()
    
    ############################################################################################
    def outputCollapsedMatrixInfo(self):
        summaryFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/matrix_summary.txt", "w")
        summaryFilehandle.write("num_documents: %s\n" % self.numDocuments)
        summaryFilehandle.write("num_targets: %s\n" % self.numTargets)
        summaryFilehandle.write("window_size: %s\n" % self.windowSize)
        summaryFilehandle.write("datetime_started: %s-%s-%s_%s:%s:%s\n" % (self.ST[0],self.ST[1],self.ST[2],self.ST[3],self.ST[4],self.ST[5]))
        DT = (datetime.datetime.now()).timetuple()
        summaryFilehandle.write("datetime_finished: %s-%s-%s_%s:%s:%s\n" % (DT[0],DT[1],DT[2],DT[3],DT[4],DT[5]))
        summaryFilehandle.close()
    
    ############################################################################################
    def outputDocumentInfo(self):
        infoFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/document_info.txt", "w")
        for documentCounter in range(self.numDocuments):
            infoFilehandle.write("%s %s %s %s %s %s\n" % (documentCounter, self.documentList[documentCounter], self.documentSizes[documentCounter], self.documentTargetSums[documentCounter], self.documentContextSums[documentCounter], self.documentCorpusDict[self.documentMatrixIndexDict[documentCounter]]))
        infoFilehandle.close()
        
    ############################################################################################
    def outputTargetInfo(self):
        targetInfoFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/target_info.txt", "w")
        for i in range(self.numTargets):
            targetInfoFilehandle.write("%s %s %s\n" % (self.targetMatrixDict[self.targetList[i]], self.targetList[i], self.targetSumFreqs[i]))    
        targetInfoFilehandle.close()

    ############################################################################################
    def outputContextInfo(self):
        contextInfoFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/context_info.txt", "w")
        for i in range(self.numContexts):
            contextInfoFilehandle.write("%s %s %s\n" % (self.contextMatrixDict[self.contextList[i]], self.contextList[i], self.contextSumFreqs[i]))    
        contextInfoFilehandle.close()

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
    def outputContextDocumentCountMatrix(self):
        print "Outputting Context x Document Frequency Matrix"
        matrixFilehandle = open(self.corpusDirectory+self.matrixDirectory+"/contextXdocument_counts.txt", "w")
        for documentCounter in range(self.numDocuments):
            matrixFilehandle.write("%s " % documentCounter)
            for contextCounter in range(self.numContexts):
                if self.contextMatrixIndexDict[contextCounter] in self.contextFreqs[documentCounter]:
                    matrixFilehandle.write(" %s:%s" % (contextCounter, self.contextFreqs[documentCounter][self.contextMatrixIndexDict[contextCounter]]))
            matrixFilehandle.write("\n")
        matrixFilehandle.close()
            
    ############################################################################################
    def importMatrixInfo(self, matrixDirectory):
        self.matrixDirectory = matrixDirectory
        matrixInfoFilehandle = open(self.matrixDirectory+"matrix_summary.txt")
        for line in matrixInfoFilehandle:
            data = (line.strip('\n').strip()).split()
            if data[0] == "window_size:":
                self.windowSize = int(data[1])
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
        
        documentFilehandle = open(self.matrixDirectory + "/document_info.txt")
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

    ###########################################################################################
    def importContextInfo(self, contextInclusionFile, contextExclusionFile):
    
        # if there is an exclusion list, add those items to a dictionary
        excludeDict = {}
        if contextExclusionFile:
            contextExclusionFilehandle = open(contextExclusionFile)
            for line in contextExclusionFilehandle:
                data = (line.strip('\n').strip()).split()
                if len(data) > 0:
                    context = data[-1]
                    excludeDict[context] = 1
            contextExclusionFilehandle.close()   
        
        contextFilehandle = open(self.matrixDirectory + "/context_info.txt")
        self.subContextList = []
        self.subContextDict = {}
        self.subContextIndexDict = {}
        
        # if the user specified that only a subset of documents are to be used
        # then add only those items to the matrix, excluding any in the exclude dict
        if contextInclusionFile:
            # read in that subset from the file
            includeDict = {}
            self.contextInclusionList = []
            contextInclusionFilehandle = open(contextInclusionFile)
            for line in contextInclusionFilehandle:
                data = (line.strip('\n').strip()).split()
                if len(data) > 0:
                    context = data[-1]
                    self.contextInclusionList.append(context)
                    includeDict[context] = 1
            contextInclusionFilehandle.close()
            
            # then read in the master list of documents but only keep the ones that were in the sublist
            contextCounter = 0
            lineCounter = 1
            for line in contextFilehandle:
                data = (line.strip('\n').strip()).split()
                if data[1] in includeDict:
                    if not data[1] in excludeDict:
                        self.contextList.append(data[1])
                        self.contextFreqs.append(int(data[2]))
                        self.contextMatrixDict[data[1]] = int(data[0])
                        self.contextMatrixIndexDict[int(data[0])] = data[1]
                        self.subContextList.append(data[1])
                        self.subContextDict[data[1]] = contextCounter
                        self.subContextIndexDict[contextCounter] = data[1]
                        contextCounter += 1
                lineCounter += 1

        else:
            # otherwise, just read in the master list, excluding any in the exclude dict
            lineCounter = 1
            contextCounter = 0
            for line in contextFilehandle:
                data = (line.strip('\n').strip()).split()
                if not data[1] in excludeDict:
                    self.contextList.append(data[1])
                    self.contextFreqs.append(int(data[2]))
                    self.contextMatrixDict[data[1]] = int(data[0])
                    self.contextMatrixIndexDict[int(data[0])] = data[1]
                    self.subContextList.append(data[1])
                    self.subContextDict[data[1]] = contextCounter
                    self.subContextIndexDict[contextCounter] = data[1]
                    contextCounter += 1
                lineCounter += 1
                
        contextFilehandle.close()
        self.numContexts = lineCounter - 1
        self.numSubContexts = len(self.subContextDict)
        
    ############################################################################################
    def importTargetDocumentMatrix(self):
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
                print "     Warning! Target %s has a frequency of zero for this set of documents" % (self.subTargetIndexDict[i])
                wereThereZeros += 1
        if wereThereZeros:
            response = raw_input("     There were %s targets with frequencies of zero. Are you sure you want to continue? (y/n)" % wereThereZeros)
            if ((response == "N") or (response == "n")):
                sys.exit(0)

        self.documentSums = self.subTargetFreqs.sum(0)
        for j in range(self.numSubDocuments):
            if self.documentSums[j] == 0:
                print "     Warning! Document %s has zero targets for this set of targets" % (self.subDocumentIndexDict[j])
                wereThereZeros += 1
        if wereThereZeros:
            response = raw_input("     There were %s documents with target counts of zero. Are you sure you want to continue? (y/n)" % wereThereZeros)
            if ((response == "N") or (response == "n")):
                sys.exit()

    ############################################################################################
    def importContextDocumentMatrix(self):
        self.subContextFreqs = scipy.zeros([self.numSubContexts, self.numSubDocuments], float)

        contextFilehandle = open(self.matrixDirectory + "contextXdocument_counts.txt")
        lineCounter = 1
        for line in contextFilehandle:
            data = (line.strip('\n').strip()).split()
            if int(data[0]) in self.documentMatrixIndexDict:
                for i in range(len(data[1:])):
                    currentPair = data[i+1].split(":")
                    
                    if int(currentPair[0]) in self.contextMatrixIndexDict:
                        self.subContextFreqs[self.subContextDict[self.contextMatrixIndexDict[int(currentPair[0])]], self.subDocumentDict[self.documentMatrixIndexDict[int(data[0])]]] = int(currentPair[1])
            lineCounter += 1
        contextFilehandle.close()
        
        wereThereZeros = 0
        self.contextSums = self.subContextFreqs.sum(1)
        for i in range(self.numSubContexts):
            if self.contextSums[i] == 0:
                print "     Warning! Context %s has a frequency of zero for this set of documents" % (self.subContextIndexDict[i])
                wereThereZeros += 1
        if wereThereZeros:
            response = raw_input("     There were %s contexts with frequencies of zero. Are you sure you want to continue? (y/n)" % wereThereZeros)
            if ((response == "N") or (response == "n")):
                sys.exit(0)

        self.documentSums = self.subContextFreqs.sum(0)
        for j in range(self.numSubDocuments):
            if self.documentSums[j] == 0:
                print "     Warning! Document %s has zero contexts for this set of contexts" % (self.subDocumentIndexDict[j])
                wereThereZeros += 1
        if wereThereZeros:
            response = raw_input("     There were %s documents with context counts of zero. Are you sure you want to continue? (y/n)" % wereThereZeros)
            if ((response == "N") or (response == "n")):
                sys.exit()
        
    ############################################################################################
    def importCollapsedMatrix(self):
        self.coocMatrix = scipy.zeros([self.numSubTargets, self.numSubTargets], float)
    
        inputFilehandle = open(self.matrixDirectory+"target_coocs_collapsed.txt")
        for line in inputFilehandle:
            data = (line.strip('\n').strip()).split()
            currentTargetIndex1 = int(data[0])
            
            if currentTargetIndex1 in self.targetMatrixIndexDict:
                currentTargetSubIndex1 = self.subTargetDict[self.targetMatrixIndexDict[currentTargetIndex1]]
                        
                for i in range(len(data[1:])):
                    currentCooc = data[i+1].split(":")
                    currentTargetIndex2 = int(currentCooc[0])
                    currentCount = float(currentCooc[1])
                    
                    if currentTargetIndex2 in self.targetMatrixIndexDict:
                        currentTargetSubIndex2 = self.subTargetDict[self.targetMatrixIndexDict[currentTargetIndex2]]
                        self.coocMatrix[currentTargetSubIndex1, currentTargetSubIndex2] += currentCount
    


    ############################################################################################
    def importSummedMatrix(self, directionType, windowSize, collapseWindow, windowWeighting):
        
        # assign the variables
        self.directionType = directionType
        self.collapseWindow = collapseWindow
        self.windowWeighting = windowWeighting    
        
        # if window size parameter is 0 or greater than that of the matrix, set it to the size of the matrix
        if windowSize == 0:
            self.subWindowSize = self.windowSize
        elif windowSize > self.windowSize:
            self.subWindowSize = self.windowSize
        else:
            self.subWindowSize = windowSize
    
        print "...Importing Co-occurrence Matrix"
        if self.collapseWindow:
            if self.directionType == 0:
                self.coocMatrix = scipy.zeros([self.numSubTargets, self.numSubContexts*2], float)
            else:
                self.coocMatrix = scipy.zeros([self.numSubTargets, self.numSubContexts], float)
        else:
            if self.directionType == 0:
                self.coocMatrix = scipy.zeros([self.numSubTargets, self.numSubContexts*self.subWindowSize*2], float)
            else:
                self.coocMatrix = scipy.zeros([self.numSubTargets, self.numSubContexts*self.subWindowSize], float)

        inputFilehandle = open(self.matrixDirectory+"targetXcontext_coocs_summed.txt")
        for line in inputFilehandle:
            data = (line.strip('\n').strip()).split()
            
            currentTargetIndex = int(data[0])
        
            if currentTargetIndex in self.targetMatrixIndexDict:
                currentTargetSubIndex = self.subTargetDict[self.targetMatrixIndexDict[currentTargetIndex]]
            
                for i in range(len(data[1:])):
                    currentCooc = data[i+1].split(":")

                    currentContextIndex = int(currentCooc[0])
                    
                    currentWindow = int(currentCooc[1])
                    currentDistance = int(math.fabs(currentWindow))
                    currentCount = float(currentCooc[2])
                    
                    if currentContextIndex in self.contextMatrixIndexDict:
                        currentContextSubIndex = self.subContextDict[self.contextMatrixIndexDict[currentContextIndex]]
                        
                    
                        if currentDistance <= self.subWindowSize:
                        
                            if self.collapseWindow:
                                if self.windowWeighting:
                                    currentCount = currentCount * (self.subWindowSize - currentDistance + 1)
                            
                                if currentWindow < 0:
                                    if self.directionType == 0:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 1:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 2:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                
                                else:                                   
                                    if self.directionType == 0:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex+self.numSubContexts] += currentCount
                                    
                                    elif self.directionType == 1:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 3:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                
                            else:
                                if self.windowWeighting:
                                    currentCount = currentCount * (self.subWindowSize - currentDistance + 1)
                            
                                if currentWindow < 0:
                                    if self.directionType == 0:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 1:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 2:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                
                                else:                                   
                                    if self.directionType == 0:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts) + (self.numSubContexts*self.subWindowSize)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 1:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 3:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount

    ############################################################################################
    def importSummedMatrix(self, directionType, windowSize, collapseWindow, windowWeighting):
        
        # assign the variables
        self.directionType = directionType
        self.collapseWindow = collapseWindow
        self.windowWeighting = windowWeighting    
        
        # if window size parameter is 0 or greater than that of the matrix, set it to the size of the matrix
        if windowSize == 0:
            self.subWindowSize = self.windowSize
        elif windowSize > self.windowSize:
            self.subWindowSize = self.windowSize
        else:
            self.subWindowSize = windowSize
    
        print "...Importing Co-occurrence Matrix"
        if self.collapseWindow:
            if self.directionType == 0:
                self.coocMatrix = scipy.zeros([self.numSubTargets, self.numSubContexts*2], float)
            else:
                self.coocMatrix = scipy.zeros([self.numSubTargets, self.numSubContexts], float)
        else:
            if self.directionType == 0:
                self.coocMatrix = scipy.zeros([self.numSubTargets, self.numSubContexts*self.subWindowSize*2], float)
            else:
                self.coocMatrix = scipy.zeros([self.numSubTargets, self.numSubContexts*self.subWindowSize], float)

        inputFilehandle = open(self.matrixDirectory+"targetXcontext_coocs_summed.txt")
        for line in inputFilehandle:
            data = (line.strip('\n').strip()).split()
            
            currentTargetIndex = int(data[0])
        
            if currentTargetIndex in self.targetMatrixIndexDict:
                currentTargetSubIndex = self.subTargetDict[self.targetMatrixIndexDict[currentTargetIndex]]
            
                for i in range(len(data[1:])):
                    currentCooc = data[i+1].split(":")

                    currentContextIndex = int(currentCooc[0])
                    
                    currentWindow = int(currentCooc[1])
                    currentDistance = int(math.fabs(currentWindow))
                    currentCount = float(currentCooc[2])
                    
                    if currentContextIndex in self.contextMatrixIndexDict:
                        currentContextSubIndex = self.subContextDict[self.contextMatrixIndexDict[currentContextIndex]]
                        
                    
                        if currentDistance <= self.subWindowSize:
                        
                            if self.collapseWindow:
                                if self.windowWeighting:
                                    currentCount = currentCount * (self.subWindowSize - currentDistance + 1)
                            
                                if currentWindow < 0:
                                    if self.directionType == 0:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 1:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 2:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                
                                else:                                   
                                    if self.directionType == 0:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex+self.numSubContexts] += currentCount
                                    
                                    elif self.directionType == 1:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 3:
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                
                            else:
                                if self.windowWeighting:
                                    currentCount = currentCount * (self.subWindowSize - currentDistance + 1)
                            
                                if currentWindow < 0:
                                    if self.directionType == 0:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 1:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 2:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                
                                else:                                   
                                    if self.directionType == 0:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts) + (self.numSubContexts*self.subWindowSize)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 1:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount
                                    
                                    elif self.directionType == 3:
                                        currentContextSubIndex = currentContextSubIndex + ((currentDistance-1)*self.numSubContexts)
                                        self.coocMatrix[currentTargetSubIndex, currentContextSubIndex] += currentCount



    ############################################################################################
    def getCoocMatrixColumnInfo(self):
        self.columnList = []
        self.columnDict = {}
        self.columnIndexDict = {}

        for i in range(len(self.coocMatrix[0,:])):
            columnLabel = "C"+str(i+1)
            self.columnList.append(columnLabel)
            self.columnDict[columnLabel] = i
            self.columnIndexDict[i] = columnLabel

    ############################################################################################
    def normalizeCoocMatrix(self, normalizationMethod):
    
        self.normalizationMethod = normalizationMethod
        
        if normalizationMethod == 0:
            pass
        
        if normalizationMethod == 1:
            self.coocMatrix = norm.rowProbabilityNormalization(self.coocMatrix)
        
        elif normalizationMethod == 2:
            self.coocMatrix = norm.columnProbabilityNormalization(self.coocMatrix)
        
        elif normalizationMethod == 3:
            self.coocMatrix = norm.lengthRowNormalization(self.coocMatrix)
        
        elif normalizationMethod == 4:
            self.coocMatrix = norm.zscoreRowsNormalization(self.coocMatrix)
        
        elif normalizationMethod == 5:
            self.coocMatrix = norm.zscoreColumnsNormalization(self.coocMatrix)
        
        elif normalizationMethod == 11:
            self.coocMatrix = norm.logRowEntropyNormalization(self.coocMatrix)
        
        elif normalizationMethod == 12:
            self.coocMatrix = norm.pmiNormalization(self.coocMatrix)
        
        elif normalizationMethod == 13:
            self.coocMatrix = norm.positivePmiNormalization(self.coocMatrix)
        
        elif normalizationMethod == 14:
            self.coocMatrix = norm.coalsCorrelationNormalization(self.coocMatrix)

        elif normalizationMethod == 15:
            self.coocMatrix = norm.integerizeNormalization(self.coocMatrix)
                    
    ############################################################################################
    def calculateAllSimilarities(self, similarityMetric):
    
        self.similarityMetric = similarityMetric
        
        self.outputFilename = "tcSimilarities_D%s_S%s_C%s_W%s_N%s_M%s.txt" % (self.directionType, self.subWindowSize, self.collapseWindow, self.windowWeighting, self.normalizationMethod, self.similarityMetric)
        
        directionTypeName, collapseWindowName, windowWeightingName = self.getMatrixParameterNames()
        normTypeName = norm.getNormMethodName(self.normalizationMethod)
        windowSizeName = "WINDOW_SIZE=%s" % self.subWindowSize

        self.the_simMatrix = simMatrix.simMatrix()
        simMetricName = self.the_simMatrix.getSimMetricName(similarityMetric)
        updateString = "%s %s %s %s %s %s %s\n" % (self.outputFilename, directionTypeName, windowSizeName, collapseWindowName, windowWeightingName, normTypeName, simMetricName)
        
        self.the_simMatrix.assignTargetInfo(self.subTargetList, self.subTargetDict, self.subTargetIndexDict)
        self.the_simMatrix.assignColumnInfo(self.subContextList, self.subContextDict, self.subContextIndexDict)
        
        self.the_simMatrix.assignMatrixData(self.coocMatrix)
        
        self.the_simMatrix.initNewSimMatrix(self.matrixDirectory, "tcSimilarities", self.outputFilename, updateString)
        self.the_simMatrix.calculateAllSimilarities(similarityMetric)
        self.the_simMatrix.outputSimilarityMatrix()
    
    ######################################################################################################
    def calculateCategoryFeatures(self, categoryFileName, outputDirectory):
    
        os.mkdir(self.matrixDirectory+outputDirectory)
        
        categoryList = []
        categoryDict = {}
        wordToCategoryDict = {}
        f = open(categoryFileName)
        for line in f:
            data = (line.strip().strip('\n').strip()).split()
            category = data[0]
            word = data[1]
            if not category in categoryDict:
                categoryList.append(category)
                categoryDict[category] = []
            wordToCategoryDict[word] = category
            categoryDict[category].append(word)
        f.close()
        
        print "Computing Diagnostic Features for Each Category"
        for category in categoryList:
            
            fileName = self.matrixDirectory+outputDirectory+"/"+category+".txt"
            filehandle = open(fileName, "w")
        
            print "     %s" % category
            categoryWordList = categoryDict[category]
            wordDict = {}
            for word in categoryWordList:
                wordDict[word] = 1
            
            categoryVector = numpy.zeros([self.numSubTargets], float)
            for i in range(self.numSubTargets):
                if self.subTargetList[i] in wordDict:
                    categoryVector[i] = 1
            
            correlationTupleList = []
            filehandle.write("%s\n" % category)
            for i in range(self.numSubContexts):
                correlation = scipy.stats.pearsonr(categoryVector, self.coocMatrix[:,i])[0]
                correlationTupleList.append((self.subContextList[i], correlation))
            correlationTupleList.sort(key=operator.itemgetter(1), reverse=True)
            for i in range(self.numSubContexts):
                if correlationTupleList[i][0] in wordDict:
                    inCat = 1
                else:
                    inCat = 0
                filehandle.write("%s %0.3f %s\n" % (correlationTupleList[i][0], correlationTupleList[i][1], inCat))
            filehandle.close

    ######################################################################################################
    def getMatrixParameterNames(self):
    
        directionTypeIndexDict = {}
        directionTypeIndexDict[0] = "FORWARD_BACWARD_CONCAT"
        directionTypeIndexDict[1] = "FORWARD_BACWARD_SUMMED"
        directionTypeIndexDict[2] = "BACKWARD_ONLY"
        directionTypeIndexDict[3] = "FORWARD_ONLY"
        directionTypeList = sorted(directionTypeIndexDict.items(), key=lambda x: x[1])

        collapseWindowIndexDict = {}
        collapseWindowIndexDict[0] = "UNCOLLAPSED_WINDOW"
        collapseWindowIndexDict[1] = "COLLAPSED_WINDOW"
        collapseWindowList = sorted(collapseWindowIndexDict.items(), key=lambda x: x[1])

        windowWeightingIndexDict = {}
        windowWeightingIndexDict[0] = "NO_WEIGHTING"
        windowWeightingIndexDict[1] = "LINEARLY_DESCENDING_WEIGHTING"
        windowWeightingList = sorted(windowWeightingIndexDict.items(), key=lambda x: x[1])
        
        try:
            directionTypeName = directionTypeIndexDict[self.directionType]  
        except:
            print "Error: Direction Type Setting %s is not a valid setting." % self.directionType
            print "Valid settings are :"
            for setting in directionTypeList:
                print " %s: %s" % (setting[0], setting[1])
            sys.exit()

        try:
            collapseWindowName = collapseWindowIndexDict[self.collapseWindow]  
        except:
            print "Error: Collapse Window Setting %s is not a valid setting." % self.collapseWindow
            print "Valid settings are :"
            for setting in collapseWindowList:
                print " %s: %s" % (setting[0], setting[1])
            sys.exit()

        try:
            windowWeightingName = windowWeightingIndexDict[self.windowWeighting]  
        except:
            print "Error: Window Weighting Setting %s is not a valid setting." % self.windowWeighting
            print "Valid settings are :"
            for setting in windowWeightingList:
                print " %s: %s" % (setting[0], setting[1])
            sys.exit()
                
        return directionTypeName, collapseWindowName, windowWeightingName

    ############################################################################################
    def outputRepetitions(self, outputFilename):
        print "...Outputting Repetitions"
        outputFilehandle = open(outputFilename, "w")
    
        for i in range(len(self.subTargetList)):
            currentTarget = self.subTargetList[i]
            currentRowIndex = self.subTargetDict[currentTarget]
            currentContextIndex = self.subContextDict[currentTarget]
            currentCount = self.coocMatrix[currentRowIndex,currentContextIndex]
            currentRowSum = self.coocMatrix[currentRowIndex,:].sum()
            if currentRowSum > 0:
                currentProp = float(currentCount) / currentRowSum
            else:
                currentProp = "NA"
            outputFilehandle.write("%s %s\n" % (currentTarget, currentProp))
            
        outputFilehandle.close()
        
    ############################################################################################
    def outputSquareAssociations(self, outputFilename):
        print "Outputting Associations"
        outputFilehandle = open(self.matrixDirectory+outputFilename, "w")
        
        for i in range(self.numSubTargets):
            outputFilehandle.write("%s" % self.subTargetList[i])
            for j in range(self.numSubTargets):
                currentAssocation = self.coocMatrix[i,j]
                outputFilehandle.write(" %0.6f" % currentAssocation)
            outputFilehandle.write("\n")
        outputFilehandle.close()

    ############################################################################################
    def outputWordDiversities(self, outputFilename, targetInclusionFile):
    
        targetList = []
        inputListFilehandle = open(targetInclusionFile)
        for line in inputListFilehandle:
            word = line.strip().strip('\n').strip()
            targetList.append(word)
        inputListFilehandle.close()
    
        print "Outputting Word Diversities"
        outputFilehandle = open(self.matrixDirectory+outputFilename, "w")
        
        numCols = len(self.coocMatrix[0,:])
        
        for target in targetList:
            currentCount = 0
            if target in self.subTargetDict:
                i = self.subTargetDict[target]
                for j in range(numCols):
                    if self.coocMatrix[i,j] > 0:
                        currentCount += 1
                currentDiversity = currentCount / float(numCols)
                outputFilehandle.write("%s %0.4f\n" % (target, currentDiversity))
            
            else:
                outputFilehandle.write("%s NA\n" % (target))
            
        outputFilehandle.close()

    ############################################################################################
    def outputTargetPairAssociations(self, outputFilename, pairFile):
    
        pairList = []
        pairFilehandle = open(pairFile)
        for line in pairFilehandle:
            words = (line.strip().strip('\n').strip()).split()
            pairList.append(words)
        pairFilehandle.close()
    
        print "Outputting Pair Associations"
        outputFilehandle = open(outputFilename, "w")
        
        for pair in pairList:
            if ((pair[0] in self.subTargetDict) and (pair[1] in self.subContextDict)):
                i = self.subTargetDict[pair[0]]
                j = self.subTargetDict[pair[1]]
                association = self.coocMatrix[i,j]
                outputFilehandle.write("%s %s %0.5f \n" % (pair[0], pair[1], association))
            
            else:
                outputFilehandle.write("%s %s NA\n" % (pair[0], pair[1]))
            
        outputFilehandle.close()

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
        
    ############################################################################################   
    def outputFullTCMatrix(self, outputPath):
        
        print "Outputting Full Target x Target Cooc Matrix"
        summedCoocsFilehandle = open(outputPath + "/targetXcontext_coocs_summed_full.txt", "w")

        for i in range(len(self.coocMatrix[:,0])):
            for j in range(len(self.coocMatrix[0,:])):
                summedCoocsFilehandle.write("%0.0f " % self.coocMatrix[i,j])
            summedCoocsFilehandle.write("\n")
        summedCoocsFilehandle.close()
        
