import sys, os, time, datetime, operator, shutil, copy
import scipy, numpy as np
import sm_libs.normalizations as norm
import sm_libs.simMatrix as simMatrix
#numpy.random
from operator import itemgetter, attrgetter
################################################################################################
################################################################################################
class ldaModel:
    ############################################################################################
    def __init__(self):
        # assign the matrix and model locations and create the initial folder
        self.matrixDirectory = 0
        self.outputPath = 0
    
        # set the basic parameters
        self.alphaList = 0    
        self.betaList = 0
        self.numTopicsList = 0
        self.numIterations = 0
        self.initialRandomSeed = 0
        self.currentRandomSeed = 0
        self.numChains = 0
        self.trackHistories = 0
        
        # set the sizes
        self.numColumns = 0
        self.numRows = 0

        # vectors of length numTokens
        self.tokenTopicAssignment = []
        self.tokenRowIndex = []
        self.tokenColumnIndex = []
        self.tokenUpdateOrder = []
        
        # matrices of size numTopics x numRows, or size numTopics x numColumns
        self.rowTopicCounts = 0
        self.columnTopicCounts = 0

        # vectors of length numTopics
        self.topicCountTotals = []
        self.topicAssignmentProbs = []
    
        # set the output options
        self.numRowOutputs = 0
        self.rowTypeIndexDict = {}
        self.numColumnOutputs = 0
        self.columnTypeIndexDict = {}
        
    ############################################################################################
    def initializeModel(self, matrixDirectory, outputDirectory, alphaList, betaList, numTopicsList, numIterations, initialRandomSeed, numChains, trackHistories, numRowOutputs, numColumnOutputs, countMatrix, rowTypeIndexDict, columnTypeIndexDict):

        # assign the matrix and model locations and create the initial folder
        self.matrixDirectory = matrixDirectory
        self.outputPath = matrixDirectory + outputDirectory
        print "\n\n"#debug ^^^
        print "OUTPUT PATH: \n " + self.outputPath #debug ^^^
        
        # ^^^^^^^^^^^^^^^^^^
        # NOTE: THIS UPDATED NESTED IF-STATEMENT CURRENTLY WORKS, EXCEPT WHEN:
        #		 THE "ADD PARAM SETTINGS" OPTION IS CHOSEN AND A FILE ALREADY EXISTS
        if os.path.isdir(self.outputPath):
            print
            print "Warning: The LDA model directory %s already exists in the %s matrix directory." % (outputDirectory, self.matrixDirectory)
            userInput = raw_input("Do you want to erase and overwrite this LDA model directory? (y/n) -->")
            if ((userInput == "y") or (userInput == "Y")):
				shutil.rmtree(self.outputPath)
				os.mkdir(self.outputPath)  # ^^^ THIS NOW GOES INTO THIS BOOLEAN STATEMENT, SO THAT WE HAVE THIRD OPTION
				os.mkdir(self.outputPath+"/models")
            else:
            	userInput = raw_input("Do you want to add additional parameter settings to existing LDA model directory? (y/n) -->")
            	if (userInput == "y") or (userInput == "Y"):
            		print "--- Adding additional parameter-settings and/or chains to existing directory ---"
            	else:
					print "<<< Quitting reduce_LDA script without running additional LDA sims >>>"
					sys.exit(0)
#             	if ((userInput == "y") or (userInput == "Y")):
#             		print "--- Adding additional parameter-settings and/or chains to existing directory ---"
# 				else:
# 					print "<<< Quitting reduce_LDA script without running additional LDA sims >>>"
# 					sys.exit(0)
        else:
			print "<<< Creating New Model Output Dir >>>"
			os.mkdir(self.outputPath)
			os.mkdir(self.outputPath+"/models")

    
        #os.mkdir(self.outputPath)
        #os.mkdir(self.outputPath+"/models")
    
        # set the basic parameters
        self.alphaList = alphaList    
        self.betaList = betaList
        self.numTopicsList = numTopicsList
        self.numIterations = numIterations
        self.initialRandomSeed = initialRandomSeed
        self.numChains = numChains
        self.trackHistories = trackHistories
        
        # set the sizes
        self.numColumns = len(columnTypeIndexDict)
        self.numRows = len(rowTypeIndexDict)
        self.countMatrix = countMatrix
        self.numTokens = int(self.countMatrix.sum())
        
        # set the output options
        self.numRowOutputs = numRowOutputs
        self.numColumnOutputs = numColumnOutputs
        self.rowTypeIndexDict = rowTypeIndexDict
        self.columnTypeIndexDict = columnTypeIndexDict

    ############################################################################################
    def runModels(self):
        print "Running Models"
        modelNum = 0
        for i in range(len(self.alphaList)):
            for j in range(len(self.betaList)):
                for k in range(len(self.numTopicsList)):
                    modelNum += 1
                    currentModelName = "T-%s_A-%s_B-%s" % (self.numTopicsList[k], self.alphaList[i], self.betaList[j])
                    os.mkdir(self.outputPath+"/models/"+currentModelName)
                    self.currentRandomSeed = copy.copy(self.initialRandomSeed)
                    for currentChain in range(1, self.numChains+1):
                        self.currentOutputDirectory = self.outputPath+"/models/"+currentModelName+"/chain"+str(currentChain)
                        os.mkdir(self.currentOutputDirectory)
                        print "     Model %s (a=%s b=%s T=%s), Chain: %s, Seed: %s" % (modelNum, self.alphaList[i], self.betaList[j], self.numTopicsList[k], currentChain, self.currentRandomSeed)
                        self.outputChainInfo(self.outputPath, self.currentOutputDirectory, currentChain, self.currentRandomSeed, self.alphaList[i], self.betaList[j], self.numTopicsList[k])
                        #######################
                        self.initializeMatrices(self.numTopicsList[k])
                        self.runGibbsSampler(self.alphaList[i], self.betaList[j], self.numTopicsList[k])
                        self.outputRowTopicMatrix(self.currentOutputDirectory+"/rowXtopic_counts.txt", self.numIterations, self.numTopicsList[k])
                        self.outputColumnTopicMatrix(self.currentOutputDirectory+"/columnXtopic_counts.txt", self.numIterations, self.numTopicsList[k])
                        self.outputTopicDistributionsOverRows(self.currentOutputDirectory+"/rowXtopic_distributions.txt", self.numIterations, self.betaList[j], self.numTopicsList[k])


    ############################################################################################
    def initializeMatrices(self, numTopics):
    
        self.currentRandomSeed += 1
        # create the index vector of the random topic assignments for each token
        if self.currentRandomSeed:
            np.random.seed(self.currentRandomSeed)
        else:
            np.random.seed(seed=None)
            print "Warning: No random seed entered, using system clock time"
            
        self.tokenTopicAssignment = np.random.random_integers(0, numTopics-1, self.numTokens)

        # create empty index vectors
        self.tokenRowIndex = [0]*self.numTokens
        self.tokenColumnIndex = [0]*self.numTokens 
        
        # assign the word and document indexes to the index vectors
        tokenCounter = 0
        for i in range(self.numRows):
            for j in range(self.numColumns):
                currentFreqCount = self.countMatrix[i,j]
                
                for k in range(int(currentFreqCount)):
                    self.tokenRowIndex[tokenCounter] = i 
                    self.tokenColumnIndex[tokenCounter] = j      
                    tokenCounter += 1
        
        # create the random token update order
        #self.tokenUpdateOrder = [0]*self.numTokens
        #self.tokenUpdateOrder = numpy.arange(0,self.numTokens)
        #numpy.random.shuffle(self.tokenUpdateOrder)

        # create the empty count matrices of the number of topics assigned to each document and word
        # this creates a numDocuments x numTopics matrix 
        # and a numWords x numTopics matrix
        self.columnTopic_Matrix = scipy.zeros([self.numColumns, numTopics], float)
        self.rowTopic_Matrix = scipy.zeros([self.numRows, numTopics], float)
        
        # loop through the token vectors and increment the corresponding values in the count matrices
        for i in range(self.numTokens):
            self.columnTopic_Matrix[self.tokenColumnIndex[i], self.tokenTopicAssignment[i]] += 1
            self.rowTopic_Matrix[self.tokenRowIndex[i], self.tokenTopicAssignment[i]] += 1

        # get the counts of the number of tokens assigned to each topic
        # this is good for efficient word probability estimation
        self.topicCountTotals = self.rowTopic_Matrix.sum(0)

    ############################################################################################
    def runGibbsSampler(self, alpha, beta, numTopics):
        startTime = time.time()
    
        probsTopicAssignment = scipy.zeros([numTopics])
        probsColumnTopic = scipy.zeros([numTopics])
        probsRowTopic = scipy.zeros([numTopics])
        
        self.tokenUpdateOrder = np.arange(0,self.numTokens)
        
        self.logLikelihoodHistory = scipy.zeros([self.numIterations+1])
        self.generatePosteriorPredictive(alpha, beta)
        self.computeLogLikelihood(numTopics)
        self.logLikelihoodHistory[0] = self.sumLogLikelihood
        self.loglikelihoodChange = []
        
        print "         Finished iteration %5s, took %5.3f, LL = %5.1f, LLC = %s, PPW = %5.2f" % (0, 0, self.logLikelihoodHistory[0], "NA", self.perplexityPerRow)
        outputIterationString =  "Finished iteration %5s, took %5.3f, LL = %5.1f, LLC = %s, PPW = %5.2f\n" % (0, 0, self.logLikelihoodHistory[0], "NA", self.perplexityPerRow)
        self.outputIterationInfo(self.currentOutputDirectory+"/chain_iteration_info.txt",outputIterationString) # ^^^^ OUTPUT ITERATION INFO FOR CHAIN
                                          
        for i in range(self.numIterations):
            self.currentRandomSeed += 1
            np.random.seed(self.currentRandomSeed)
            tokenRandomValues = np.random.rand(self.numTokens)
            np.random.shuffle(self.tokenUpdateOrder)

            if self.trackHistories:
                if ((i % self.trackHistories) == 0):
                    self.outputRowTypeProbDistributions(self.currentOutputDirectory+"/rowXtopic_distribution_histories.txt", i)
                    self.outputRowTopicMatrix(self.currentOutputDirectory+"/rowXtopic_count_histories.txt", i)
                    self.outputColumnTopicMatrix(self.currentOutputDirectory+"/columnXtopic_count_histories.txt", i)

            for j in range(self.numTokens):
            
                currentColumn = self.tokenColumnIndex[self.tokenUpdateOrder[j]]
                currentRow = self.tokenRowIndex[self.tokenUpdateOrder[j]]
                oldTopicAssignment = self.tokenTopicAssignment[self.tokenUpdateOrder[j]]

                self.columnTopic_Matrix[currentColumn,oldTopicAssignment] -= 1
                self.rowTopic_Matrix[currentRow,oldTopicAssignment] -= 1
                self.topicCountTotals[oldTopicAssignment] -= 1
                
                probsColumnTopic = self.columnTopic_Matrix[currentColumn,:]+alpha
                probsRowTopic = (self.rowTopic_Matrix[currentRow,:]+beta) / (self.topicCountTotals + beta*self.numRows)
                probsTopicAssignment = probsColumnTopic * probsRowTopic
                
                cumProbsTopicAssignment = np.cumsum(probsTopicAssignment)
                newTopicAssignment = (np.less_equal(cumProbsTopicAssignment, (tokenRandomValues[j] * cumProbsTopicAssignment[-1]))).sum()
                
                self.columnTopic_Matrix[currentColumn,newTopicAssignment] += 1
                self.rowTopic_Matrix[currentRow,newTopicAssignment] += 1
                self.topicCountTotals[newTopicAssignment] += 1
                
                self.tokenTopicAssignment[self.tokenUpdateOrder[j]] = newTopicAssignment
            
            self.generatePosteriorPredictive(alpha, beta)
            self.computeLogLikelihood(numTopics)
            self.logLikelihoodHistory[i+1] = self.sumLogLikelihood
            
            if ((i % 1) == 0):
                if i > 0:
                    took = time.time() - startTime
                    if i < 10:
                        Last10LL = self.logLikelihoodHistory[:i].mean()
                    else:
                        Last10LL= self.logLikelihoodHistory[i-10:i].mean()
                    
                    print "         Finished iteration %5s, took %5.3f, LL = %5.1f, LLC = %5.2f, PPW = %5.2f" % (i, took/(i+1), self.logLikelihoodHistory[i+1], self.logLikelihoodHistory[i+1] - self.logLikelihoodHistory[i], self.perplexityPerRow)
                    outputIterationString = "Iteration %5s, took %5.3f, LL = %5.1f, LLC = %5.2f, PPW = %5.2f\n" % (i, took/(i+1), self.logLikelihoodHistory[i+1], self.logLikelihoodHistory[i+1] - self.logLikelihoodHistory[i], self.perplexityPerRow)
                    self.outputIterationInfo(self.currentOutputDirectory+"/chain_iteration_info.txt",outputIterationString) # ^^^^ OUTPUT ITERATION INFO FOR CHAIN
        
        
        if self.trackHistories:
            self.outputRowTypeProbDistributions(self.currentOutputDirectory+"/rowXtopic_distribution_histories.txt", i)
            self.outputRowTopicMatrix(self.currentOutputDirectory+"/rowXtopic_count_histories.txt", i)
            self.outputColumnTopicMatrix(self.currentOutputDirectory+"/columnXtopic_count_histories.txt", i)

    ############################################################################################        
    def outputModelInfo(self):

        outputFilehandle = open(self.outputPath+"/"+"row_info.txt", "w")
        for i in range(len(self.rowTypeIndexDict)):
            outputFilehandle.write("%s %s\n" % (str(i), self.rowTypeIndexDict[i]))
        outputFilehandle.close()

        outputFilehandle = open(self.outputPath+"/"+"column_info.txt", "w")
        for i in range(len(self.columnTypeIndexDict)):
            outputFilehandle.write("%s %s\n" % (str(i), self.columnTypeIndexDict[i]))
        outputFilehandle.close()

		#         outputFilehandle =  open(self.outputPath+"/"+"model_info.txt", "w")
		#         outputFilehandle.write("ALPHA:")
		#         for i in range(len(self.alphaList)):
		#             outputFilehandle.write(" %s" % self.alphaList[i])
		#         outputFilehandle.write("\n")
		#         
		#         outputFilehandle.write("BETA:")
		#         for i in range(len(self.betaList)):
		#             outputFilehandle.write(" %s" % self.betaList[i])
		#         outputFilehandle.write("\n")
		# 
		#         outputFilehandle.write("TOPICS:")
		#         for i in range(len(self.numTopicsList)):
		#             outputFilehandle.write(" %s" % self.numTopicsList[i])
		#         outputFilehandle.write("\n")        
		#         
		#         outputFilehandle.write("NUM_CHAINS: %s\n" % self.numChains)
		#         outputFilehandle.write("ITERATIONS: %s\n" % self.numIterations)
		#         outputFilehandle.write("RANDOM_SEED: %s\n" % self.initialRandomSeed)
		#         outputFilehandle.close()

    
    ############################################################################################
    def outputRowTopicMatrix(self, outputPath, iteration, numTopics):
        outputFilehandle = open(outputPath, "a")
        for i in range(self.numRows):
            outputFilehandle.write("i%s %16s" % (iteration, self.rowTypeIndexDict[i]))
            for j in range(numTopics):
                outputFilehandle.write(" %4.0f" % self.rowTopic_Matrix[i,j])
            outputFilehandle.write("\n")
        outputFilehandle.close()
    
    ############################################################################################  
    def outputColumnTopicMatrix(self, outputPath, iteration, numTopics):
        outputFilehandle = open(outputPath, "a")
        for i in range(self.numColumns):
            outputFilehandle.write("i%s %s" % (iteration, i))
            for j in range(numTopics):
                outputFilehandle.write(" %4.0f" % self.columnTopic_Matrix[i,j])
            outputFilehandle.write("\n")
        outputFilehandle.close()

    ############################################################################################
    def outputChainInfo(self, modelOutputPath, chainOutputPath, currentChain, currentRandomSeed, alpha, beta, numTopics):
		#self.outputChainInfo(self.currentOutputDirectory+"/chain_info.txt", currentChain, self.currentRandomSeed, self.alphaList[i], self.betaList[j], self.numTopicsList[k]) # ^^^ New output method for chain info
        #outputFilehandle = open(modelOutputPath+"/all_chainInfo.txt", "a")
        #outputFilehandle.write("ALPHA: %s\n" % alpha)
        #outputFilehandle.write("BETA: %s\n" % beta)
        #outputFilehandle.write("NUM_TOPICS: %s\n" % numTopics)
        #outputFilehandle.write("CHAIN: %s\n" % currentChain)
        #outputFilehandle.write("CURRENT_INIT_RANDOM_SEED: %s\n" % currentRandomSeed)
        #outputFilehandle.write("ITERATIONS: %s\n" % self.numIterations)
        #outputFilehandle.close()
        
        # ^^^ NEW OUTPUT FUNCTION: DO BE USED FOR OUTPUTTING CHAIN INFORMATION TO BOTH:
        # - CHAIN IN DIRECTORY (WILL BE A SINGLE ROW FOR EACH ITERATION RUN
        # - FULL MODEL DIRECTORY (WILL APPEND A NEW LINE FOR EACH CHAIN COMPLETED (WILL NOT REMOVE A DUPLICATE FOR NOW AT LEAST)
		#self.outputChainInfo(self.currentOutputDirectory+"/chain_info.txt", currentChain, self.currentRandomSeed, self.alphaList[i], self.betaList[j], self.numTopicsList[k]) # ^^^ New output method for chain info
        
        outStr=[]
        outStr.append("T:%s" % numTopics)
        outStr.append("A:%s" % alpha)
        outStr.append("B:%s" % beta)
        outStr.append("CHAIN:%s" % currentChain)
        outStr.append("ITERS:%s" % self.numIterations)
        outStr.append("INIT_SEED:%s" % currentRandomSeed)
        
        outputFilehandle = open(chainOutputPath+"/chain_info.txt", "a")
        for i in range(len(outStr)):
        	outputFilehandle.write("%s " % outStr[i].ljust(10))
        outputFilehandle.write("\n")
        outputFilehandle.close()

        outputFilehandle = open(modelOutputPath+"/all_chainInfo.txt", "a")
        for i in range(len(outStr)):
        	outputFilehandle.write("%s " % outStr[i].ljust(10))
        outputFilehandle.write("\n")
        outputFilehandle.close()
        
        outputFilehandle = open(chainOutputPath+"/row_info.txt", "w")
        for i in range(self.numRows):
            outputFilehandle.write("%s %s\n" % (i, self.rowTypeIndexDict[i]))
        outputFilehandle.close()
        
        outputFilehandle = open(chainOutputPath+"/column_info.txt", "w")
        for i in range(self.numColumns):
            outputFilehandle.write("%s %s\n" % (i, self.columnTypeIndexDict[i]))
        outputFilehandle.close()
        
    ############################################################################################
    def outputIterationInfo(self, outputPath, outputIterationString): 
    
        # ^^^ NEW OUTPUT FUNCTION: DO BE USED FOR OUTPUTTING CHAIN INFORMATION TO BOTH:
		#self.outputIterationInfo_Row(self.currentOutputDirectory+"/chain_iter_info.txt",outputIterationString) # ^^^^ OUTPUT ITERATION INFO FOR CHAIN
		outputFilehandle = open(outputPath, "a")
		outputFilehandle.write(outputIterationString)
		outputFilehandle.close()

    ############################################################################################
    def outputTopicDistributionsOverRows(self, outputPath, iteration, beta, numTopics):
        if self.numRowOutputs > self.numRows:
            self.numRowOutputs = self.numRows
    
        outputFilehandle = open(outputPath, "a")
        
        for i in range(numTopics):

            topicProb = self.topicCountTotals[i] / self.topicCountTotals.sum()
            
            currentTopicCounts = self.rowTopic_Matrix[:,i]+beta
            currentTopicProbDistribution = currentTopicCounts / currentTopicCounts.sum()
            outputVector = []
            for j in range(self.numRows):
                outputVector.append((currentTopicProbDistribution[j], self.rowTypeIndexDict[j]))
            sortedOutputVector = sorted(outputVector, reverse=True)
            
            for j in range(self.numRowOutputs):
                outputFilehandle.write("%s %s %0.4f %s %0.4f\n" % (iteration, i+1, topicProb, sortedOutputVector[j][1], sortedOutputVector[j][0]))
            
            outputFilehandle.write("\n")
        outputFilehandle.close()
        
    ############################################################################################
    def generatePosteriorPredictive(self, alpha, beta):
         
         self.pTopicColumn = self.columnTopic_Matrix + alpha
         self.pTopicColumn = self.pTopicColumn.transpose() / self.pTopicColumn.sum(1)
         #print self.pTopicColumn.sum(0)
         self.pRowTopics = self.rowTopic_Matrix + beta
         self.pRowTopics = self.pRowTopics / self.pRowTopics.sum(0)
         #self.pRowTopics = (self.rowTopic_Matrix.transpose() / self.rowTopic_Matrix.sum(0)).transpose()
         #print self.pRowTopics.sum(0)
         self.pRowColumn = np.dot(self.pRowTopics, self.pTopicColumn)
#          
#     	 for i in [1,6]:
#     	 	print self.pRowColumn
#     	 	print "\n\n pRowColumn[i,:] :"
#     	 	print self.pRowColumn[i,:]
#     	 	print np.sum(self.pRowColumn[i,:])
#     	 	print "\n pRowColumn[:,i] :"
#     	 	print self.pRowColumn[:,i]
#     	 	print np.sum(self.pRowColumn[:,i])
#     	 	print self.pRowColumn.sum(0)
#     	 	wait = raw_input("PRESS ENTER TO CONTINUE.")

    ############################################################################################
    def computeLogLikelihood(self, numTopics):
    
        self.sumLogLikelihood = 0
        for i in range(self.numTokens):
            self.sumLogLikelihood += np.log(self.pRowColumn[self.tokenRowIndex[i], self.tokenColumnIndex[i]])
        self.perplexityPerRow = (np.exp(-(self.sumLogLikelihood/self.numTokens)))

    ############################################################################################
    def importChainInfo(self, chainDirectory):
    
        self.chainDirectory = chainDirectory
        
        # Get topic model parameters from text file
        infoFilehandle = open(chainDirectory+"chain_info.txt")

        for line in infoFilehandle:
            data = (line.strip('\n').strip()).split()
        infoFilehandle.close()
            
        for item in data:
            params = item.split(":")
            if params[0] == 'A':
                self.alpha = float(params[1])
            if params[0] == 'B':
                self.beta = float(params[1])
            if params[0] == 'T':
                self.numTopics = float(params[1])
            if params[0] == 'CHAIN':
                self.chain = float(params[1])
            if params[0] == 'ITERS':
                self.iterations = float(params[1])                
            if params[0] == 'INIT_SEED':
                self.initialRandomSeed = float(params[1])                                  
    
    ############################################################################################
    def importRowInfo(self, rowInclusionFile, rowExclusionFile):
    
        exclusionDict = {}
        if rowExclusionFile:
            filehandle = open(rowExclusionFile)
            for line in filehandle:
                data = (line.strip('\n').strip()).split()
                if len(data) > 0:
                    exclusionDict[data[-1]] = 1
            filehandle.close()
    
        # Create list and dictionaries of rows
        self.rowTypeList = []
        self.rowTypeDict = {}
        self.rowTypeIndexDict = {}
        self.rowTypeSubList = []
        self.rowTypeSubDict = {}
        self.rowTypeSubIndexDict = {}
        
        if rowInclusionFile:
            inclusionDict = {}
            filehandle = open(rowInclusionFile)
            for line in filehandle:
                data = (line.strip('\n').strip()).split()
                if len(data) > 0:
                    inclusionDict[data[-1]] = 1
            filehandle.close()
            
            targetInfoFilehandle = open(self.chainDirectory+"row_info.txt")
            rowCounter = 0
            for line in targetInfoFilehandle:
                data = (line.strip('\n').strip()).split()
                rowIndex = int(data[0])
                rowLabel = data[1]
                if rowLabel in inclusionDict:
                    if not rowLabel in exclusionDict:
                        self.rowTypeList.append(rowLabel)
                        self.rowTypeDict[rowLabel] = rowIndex
                        self.rowTypeIndexDict[rowIndex] = rowLabel
                        self.rowTypeSubList.append(rowLabel)
                        self.rowTypeSubDict[rowLabel] = rowCounter
                        self.rowTypeSubIndexDict[rowCounter] = rowLabel
                        rowCounter += 1
            
        else:
            # go through the file and read rows into the list and dictionaries
            targetInfoFilehandle = open(self.chainDirectory+"row_info.txt")
            rowCounter = 0
            for line in targetInfoFilehandle:
                data = (line.strip('\n').strip()).split()
                rowIndex = int(data[0])
                rowLabel = data[1]
                if not rowLabel in exclusionDict:
                    self.rowTypeList.append(rowLabel)
                    self.rowTypeDict[rowLabel] = rowIndex
                    self.rowTypeIndexDict[rowIndex] = rowLabel
                    self.rowTypeSubList.append(rowLabel)
                    self.rowTypeSubDict[rowLabel] = rowCounter
                    self.rowTypeSubIndexDict[rowCounter] = rowLabel
                    rowCounter += 1
                
            targetInfoFilehandle.close()
        self.numRows = len(self.rowTypeList)

    ############################################################################################
    def importColumnList(self):   
        # Create list dictionaries of columns
        self.columnTypeList = []
        self.columnTypeDict = {}
        self.columnTypeIndexDict = {}
        
        # go through the  file and read columns into the list and dictionaries
        targetInfoFilehandle = open(self.modelDirectory + "column_info.txt")
        
        for line in targetInfoFilehandle:
            data = (line.strip('\n').strip()).split()
            columnIndex = int(data[0])
            columnLabel = data[1]
            self.columnTypeList.append(columnLabel)
            self.columnTypeDict[columnLabel] = columnIndex
            self.columnTypeIndexDict[columnIndex] = columnLabel
        targetInfoFilehandle.close()
        self.numColumns = len(self.columnTypeList)

    ############################################################################################
    def importRowTopicMatrix(self):

        # declore the empty matrix
        self.rowTopic_Matrix = scipy.zeros([self.numRows, self.numTopics], float)

        # now go through the row-topic counts file and read in the data into the matrix
        topicCountsFilehandle = open(self.chainDirectory + "rowXtopic_counts.txt")
        lineCounter = 0

        for line in topicCountsFilehandle:
            data = (line.strip('\n').strip()).split()
            if data[1] in self.rowTypeSubDict:          
                for i in range(len(data[2:])):
                    self.rowTopic_Matrix[self.rowTypeSubDict[data[1]],i] = float(data[i+2])
            lineCounter += 1
        topicCountsFilehandle.close()

    ############################################################################################
    def importColumnTopicMatrix(self):   

        # declore the empty matrix
        self.columnTopic_Matrix = scipy.zeros([self.numColumns, self.numTopics], float)

        # now go through the column-topic counts file and read in the data into the matrix
        topicCountsFilehandle = open(self.chainDirectory + "columnXtopic_counts.txt")
        lineCounter = 0
        for line in topicCountsFilehandle:
            data = (line.strip('\n').strip()).split()
            for i in range(len(data[1:])):
                self.columnTopic_Matrix[lineCounter,i] = float(data[i+1])
            lineCounter += 1
        topicCountsFilehandle.close()

    ############################################################################################
    def normalizeRowTopicMatrix(self, normalizationMethod):
    
        print normalizationMethod
    
        self.normalizationMethod = normalizationMethod
        
        self.rowTopic_Matrix = self.rowTopic_Matrix + self.beta
        
        if normalizationMethod == 0:
            pass
        
        if normalizationMethod == 1:
            self.rowTopic_Matrix = norm.rowProbabilityNormalization(self.rowTopic_Matrix)
        
        elif normalizationMethod == 2:
            self.rowTopic_Matrix = norm.columnProbabilityNormalization(self.rowTopic_Matrix)
        
        elif normalizationMethod == 3:
            self.rowTopic_Matrix = norm.lengthRowNormalization(self.rowTopic_Matrix)
        
        elif normalizationMethod == 4:
            self.rowTopic_Matrix = norm.zscoreRowsNormalization(self.rowTopic_Matrix)
        
        elif normalizationMethod == 5:
            self.rowTopic_Matrix = norm.zscoreColumnsNormalization(self.rowTopic_Matrix)
        
        elif normalizationMethod == 11:
            self.rowTopic_Matrix = norm.logRowEntropyNormalization(self.rowTopic_Matrix)
        
        elif normalizationMethod == 12:
            self.rowTopic_Matrix = norm.pmiNormalization(self.rowTopic_Matrix)
        
        elif normalizationMethod == 13:
            self.rowTopic_Matrix = norm.positivePmiNormalization(self.rowTopic_Matrix)
        
        elif normalizationMethod == 14:
            self.rowTopic_Matrix = norm.coalsCorrelationNormalization(self.rowTopic_Matrix)
                    
    ############################################################################################
    def calculateAllSimilarities(self, similarityMetric):
    
        self.similarityMetric = similarityMetric
        
        self.outputFilename = "ldaSimilarities_A%s_B%s_T%s_I%s_S%s_N%s_M%s.txt" % (self.alpha, self.beta, self.numTopics, self.iterations, self.initialRandomSeed, self.normalizationMethod, self.similarityMetric)
        
        normTypeName = norm.getNormMethodName(self.normalizationMethod)

        self.the_simMatrix = simMatrix.simMatrix()
        simMetricName = self.the_simMatrix.getSimMetricName(similarityMetric)
        updateString = "%s %s %s\n" % (self.outputFilename, normTypeName, simMetricName)
        
        self.the_simMatrix.assignTargetInfo(self.rowTypeSubList, self.rowTypeSubDict, self.rowTypeSubIndexDict)
        self.the_simMatrix.assignMatrixData(self.rowTopic_Matrix)
        
        self.the_simMatrix.initNewSimMatrix(self.chainDirectory, self.outputFilename, updateString)
        self.the_simMatrix.calculateAllSimilarities(similarityMetric)
        self.the_simMatrix.outputSimilarityMatrix()
        

