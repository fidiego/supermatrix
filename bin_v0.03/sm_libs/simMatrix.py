import sys, os, time, datetime, operator
import scipy
import numpy as np
from operator import itemgetter, attrgetter
from scipy import spatial
################################################################################################
################################################################################################
class simMatrix:
    ############################################################################################
    def __init__(self):
        self.matrixDirectory = 0            # the name of the matrix, the folder it is in

        self.targetList = []                # a list of all the targets
        self.targetDict = {}                # a dictionary indexed by the target string, pointing to its index number in the original corpus
        self.targetIndexDict = {}           # a dictionary indexed by the index number in the original corpus, pointing to the target string
        self.numTargets = 0
        self.columnList = []
        self.columnDict = {}
        self.columnIndexDict = {}
        self.numColumns = 0
    
        self.existingTargetList = []
        self.existingTargetDict = {}
        self.existingTargetIndexDict = {}
        self.existingColumnList = []
        self.existingColumnDict = {}
        self.existingColumnIndexDict = {}
        
        self.similarityMatrix = 0

    ############################################################################################
    def assignTargetInfo(self, targetList, targetDict, targetIndexDict):
    
        self.targetList = targetList
        self.targetDict = targetDict
        self.targetIndexDict = targetIndexDict
        self.numTargets = len(self.targetList)

    ############################################################################################
    def assignColumnInfo(self, columnList, columnDict, columnIndexDict):
    
        self.columnList = columnList
        self.columnDict = columnDict
        self.columnIndexDict = columnIndexDict
        self.numColumns = len(self.columnList)

    ############################################################################################
    def assignMatrixData(self, theMatrix):
    
        self.theMatrix = theMatrix
    
    ############################################################################################
    def importTargetInfo(self):
    
        testWordFilehandle = open(self.targetListIndexFile)
        for line in testWordFilehandle:
            data = (line.strip().strip('\n').strip()).split()
            self.targetList.append(data[1])
            self.targetDict[data[1]] = int(data[0])
            self.targetIndexDict[int(data[0])] = data[1]
        testWordFilehandle.close()
        self.numTargets = len(self.targetList)
    
    ############################################################################################
    def initNewSimMatrix(self, matrixDirectory, simDirectory, outputFilename, updateString):
    
        self.matrixDirectory = matrixDirectory
        self.outputFilename = outputFilename
    
        # create the output path and file names
        self.outputPath = self.matrixDirectory+simDirectory
        
        # check to see if the similarity directory exists
        # if not, create it and write the target info file    
        # if it does exist, ask if they want to add to the existing one (y) or exit (n)
        # if yes, read in the target list from the existing one and use that
        if not os.path.isdir(self.outputPath):
            os.mkdir(self.outputPath)
            targetInfoFilehandle = open(self.outputPath+"/target_info.txt", "w")
            for i in range(self.numTargets):
                targetInfoFilehandle.write("%s %s\n" % (self.targetDict[self.targetList[i]], self.targetList[i]))
            targetInfoFilehandle.close()
            columnInfoFilehandle = open(self.outputPath+"/column_info.txt", "w")
            for i in range(self.numColumns):
                columnInfoFilehandle.write("%s %s\n" % (self.columnDict[self.columnList[i]], self.columnList[i]))
            columnInfoFilehandle.close()

        else:
            #print
            #userInput = raw_input("         Similarity files for this this matrix already exist. Would you like to add similarities for these parameter settings? (y/n) -->")
            #if ((userInput == "n") or (userInput == "N")):
            #    sys.exit(1)
            #elif ((userInput == "y") or (userInput == "Y")):
            
            if len(self.targetDict) > 0:
                targetInfoFilehandle = open(self.outputPath+"/target_info.txt")
                for line in targetInfoFilehandle:
                    data = (line.strip('\n').strip()).split()
                    self.existingTargetList.append(data[1])
                    self.existingTargetDict[data[1]] = int(data[0])
                    self.existingTargetIndexDict[int(data[0])] = data[1]
                targetInfoFilehandle.close()
                if not self.targetDict == self.existingTargetDict:
                    print "         Error: the supplied target list and the target list for the existing similarity object are not the same."
                    print
                    sys.exit(1) 
            
            if len(self.columnDict) > 0:
                columnInfoFilehandle = open(self.outputPath+"/column_info.txt")
                for line in columnInfoFilehandle:
                    data = (line.strip('\n').strip()).split()
                    self.existingColumnList.append(data[1])
                    self.existingColumnDict[data[1]] = int(data[0])
                    self.existingColumnIndexDict[int(data[0])] = data[1]
                columnInfoFilehandle.close()
                if not self.columnDict == self.existingColumnDict:
                    print "         Error: the supplied column list and the column list for the existing similarity object are not the same."
                    print
                    sys.exit(1) 
                        
            #else:
            #    print "         Error, %s was not a valid response" % userInput
            #    sys.exit(1)
        
        # check to see if a similarity file with the specified parameters already exists
        # if so, ask if they want to overwrite it
        if os.path.isfile(self.outputPath+"/"+self.outputFilename):
            print
            print "         Warning: A similarity output file with these parameters already exists."
            userInput = raw_input("         Do you want to erase and overwrite this file? (y/n) -->")
            if ((userInput == "n") or (userInput == "N")):
                sys.exit(1)
        else:
            simInfoFilehandle = open(self.outputPath+"/similarity_info.txt", "a")
            simInfoFilehandle.write(updateString)
            simInfoFilehandle.close()

    ############################################################################################
    def calculateAllSimilarities(self, similarityMetric):
        self.similarityMetric = similarityMetric
        
        if self.similarityMetric == 1:
            self.similarityMatrix = self.cosineSimilarity()
        if self.similarityMetric == 2:
            self.similarityMatrix = self.cityBlockDistanceSimilarity()
        if self.similarityMetric == 3:
            self.similarityMatrix = self.euclideanDistanceSimilarity()
        if self.similarityMetric == 4:
            self.similarityMatrix = self.correlationSimilarity()
        if self.similarityMetric == 5:
            self.similarityMatrix = self.dotProductSimilarity()

    ############################################################################################
    def outputSimilarityMatrix(self):
        
        outputFilehandle = open(self.outputPath + "/" + self.outputFilename, "w")
        for i in range(self.numTargets):
            outputFilehandle.write("%s" % self.targetDict[self.targetList[i]])
            for j in range(self.numTargets):
                outputFilehandle.write(" %s:%0.4f" % (self.targetDict[self.targetList[j]], self.similarityMatrix[i,j]))
            outputFilehandle.write("\n")
        outputFilehandle.close()

    ############################################################################################
    def initExistingSimMatrix(self, similarityFile, targetListIndexFile):
        self.similarityFile = similarityFile
        self.targetListIndexFile = targetListIndexFile

    ############################################################################################
    def importSimilarityMatrix(self):
        print "...Importing Similarities"
        self.similarityMatrix = scipy.zeros([self.numTargets, self.numTargets], float)
    
        similarityFilehandle = open(self.similarityFile)
        for line in similarityFilehandle:
            data = (line.strip("\n").strip()).split()
            currentTarget = int(data[0])
            currentSimList = data[1:]
            
            for i in range(len(currentSimList)):
                currentSim = currentSimList[i].split(":")
                self.similarityMatrix[currentTarget, int(currentSim[0])] = float(currentSim[1])
        similarityFilehandle.close()
    
    ############################################################################################
    def outputNeighbors(self, numNeighbors):
        self.numNeighbors = numNeighbors
        print "Sorting and outputting neighborhoods"
        outputFilename = self.similarityFile[:-4] + "_%sneighbors.txt" % self.numNeighbors
        outputFilehandle = open(outputFilename, "w")
        for i in range(self.numTargets):  
            currentSims = self.similarityMatrix[i]
            sortedIndexes = scipy.argsort(currentSims)
            for j in range(self.numNeighbors):
                outputFilehandle.write("%15s %15s %i %7.3f\n" % (self.targetList[i], self.targetList[sortedIndexes[self.numTargets-(j+1)]], j+1, currentSims[sortedIndexes[self.numTargets-(j+1)]]))
        outputFilehandle.close()

    ############################################################################################
    def outputSimNDensities(self, numNeighbors):
        self.numNeighbors = numNeighbors
        print "..Sorting and outputting neighborhoods"
        outputFilename = self.similarityFile[:-4] + "_simNDens_N%s.txt" % self.numNeighbors
        outputFilehandle = open(outputFilename, "w")
        for i in range(self.numTargets):
            currentSims = self.similarityMatrix[i]
            if numNeighbors:
                if numNeighbors < len(currentSims):
                    cutoff = len(currentSims) - numNeighbors
                    sortedSims = currentSims.sort()
                    currentSims = sortedSims[cutoff:]
            simMean = currentSims.mean()
            simStd = currentSims.std()
            outputFilehandle.write("%s %0.4f %0.4f\n" % (self.targetList[i], simMean, simStd))
        outputFilehandle.close()

    ############################################################################################
    def outputTargetSimPairs(self, pairFile):

        pairList = []
        pairFilehandle = open(pairFile)
        for line in pairFilehandle:
            words = (line.strip().strip('\n').strip()).split()
            pairList.append(words)
        pairFilehandle.close()

        print "..Outputting similarities"
        outputFilename = "simPairs.txt"
        outputFilehandle = open(outputFilename, "w")
        outputFilehandle.write("word1 word2 sim | zsim1 zsim2 | psim1 psim2 | nIn1 nIn2\n")
        
        numTargets = len(self.similarityMatrix[0])
        
        for pair in pairList:
            if ((pair[0] in self.targetDict) and (pair[1] in self.targetDict)):
                i = self.targetDict[pair[0]]
                j = self.targetDict[pair[1]]
                
                sim = self.similarityMatrix[i,j]
                
                word0Sims = self.similarityMatrix[i]
                word1Sims = self.similarityMatrix[j]
                
                z0Sim = (sim - word0Sims.mean()) / word0Sims.std()
                z1Sim = (sim - word1Sims.mean()) / word1Sims.std()
                
                sim0min = np.amin(word0Sims)
                sim1min = np.amin(word1Sims)
                adjSim0 = sim + abs(sim0min)
                adjSim1 = sim + abs(sim1min)
                
                adjSimVector0 = word0Sims + abs(sim0min)
                adjSimVector1 = word1Sims + abs(sim1min)
                sim0Sum = adjSimVector0.sum()
                sim1Sum = adjSimVector1.sum()
                
                p0Sim = adjSim0 / sim0Sum
                p1Sim = adjSim1 / sim1Sum
                
                sortedIndexes0 = scipy.argsort(word0Sims)
                sortedIndexes1 = scipy.argsort(word1Sims)
                
                for k in range(numTargets):
                    if sortedIndexes0[k] == j:
                        nIn0 = numTargets - k
                        break
                for k in range(numTargets):
                    if sortedIndexes1[k] == i:
                        nIn1 = numTargets - k
                        break
                
                outputFilehandle.write("%s %s %0.3f | %0.3f %0.3f | %0.5f %0.5f | %0.0f %0.0f\n" % (pair[0], pair[1], sim, z0Sim, z1Sim, p0Sim, p1Sim, nIn0, nIn1))
                
            else:
                outputFilehandle.write("%s %s NA NA NA NA NA NA NA\n" % (pair[0], pair[1]))
        

    ######################################################################################################
    ###### SIMILARITY FUNCTIONS #######
    ######################################################################################################

    ######################################################################################################
    def getSimMetricName(self, simMetricIndex):
    
        similarityMetrixIndexDict = {}
        similarityMetrixIndexDict[1] = "COSINE"
        similarityMetrixIndexDict[2] = "CITYBLOCK"
        similarityMetrixIndexDict[3] = "EUCLIDEAN"
        similarityMetrixIndexDict[4] = "PEARSONR"
        similarityMetrixIndexDict[5] = "DOTPRODUCT"
        
        similarityMetricList = sorted(similarityMetrixIndexDict.items(), key=lambda x: x[1])
                      
        try:
            simMetricName = similarityMetrixIndexDict[simMetricIndex]
            
        except:
            print "Error: Metric %s is not a valid similarity metric." % simMetricIndex
            print "Valid similarity metrics are :"
            for simMetric in similarityMetricList:
                print " %s: %s" % (simMetric[0], simMetric[1])
            sys.exit()
                
        return simMetricName
    
    ######################################################################################################
    # similarity metric 1
    def cosineSimilarity(self):
        print
        print "...Calculating Cosine Similarities"
        numRows = len(self.theMatrix[:,0])
        numCols = len(self.theMatrix[0,:])
        simMatrix = scipy.zeros([numRows, numRows], float)
        for i in range(numRows):
            starttime = time.time()
            for j in range(numRows):
                simMatrix[i,j] = 1 - scipy.spatial.distance.cosine(self.theMatrix[i,:], self.theMatrix[j,:])
            took = time.time() - starttime
            print "     Word %s (%0.2f sec.)" % (str(i+1), took)
        return simMatrix
        
    ######################################################################################################
    # similarity metric 2
    def cityBlockDistanceSimilarity(self):
        print
        print "...Calculating CityBlock Similarities"
        numRows = len(self.theMatrix[:,0])
        numCols = len(self.theMatrix[0,:])
        simMatrix = scipy.zeros([numRows, numRows], float)
        for i in range(numRows):
            starttime = time.time()
            for j in range(numRows):
                simMatrix[i,j] = -1 * scipy.spatial.distance.cityblock(self.theMatrix[i,:], self.theMatrix[j,:])
            took = time.time() - starttime
            print "     Word %s (%0.2f sec.)" % (str(i+1), took)
        return simMatrix
    
    ######################################################################################################
    # similarity metric 3
    def euclideanDistanceSimilarity(self):
        print
        print "...Calculating Euclidean Similarities"
        numRows = len(self.theMatrix[:,0])
        numCols = len(self.theMatrix[0,:])
        simMatrix = scipy.zeros([numRows, numRows], float)
        for i in range(numRows):
            starttime = time.time()
            for j in range(numRows):
                simMatrix[i,j] = -1 * scipy.spatial.distance.euclidean(self.theMatrix[i,:], self.theMatrix[j,:])
            took = time.time() - starttime
            print "     Word %s (%0.2f sec.)" % (str(i+1), took)
        return simMatrix
    
    ######################################################################################################
    # similarity metric 4
    def correlationSimilarity(self):
        print
        print "...Calculating Correlation Similarities"
        numRows = len(self.theMatrix[:,0])
        numCols = len(self.theMatrix[0,:])
        simMatrix = scipy.zeros([numRows, numRows], float)
        for i in range(numRows):
            starttime = time.time()
            for j in range(numRows):
                simMatrix[i,j] = 1 - scipy.spatial.distance.correlation(self.theMatrix[i,:], self.theMatrix[j,:])
            took = time.time() - starttime
            print "     Word %s (%0.2f sec.)" % (str(i+1), took)
        return simMatrix
    
    ######################################################################################################
    # similarity metric 5
    def dotProductSimilarity(self):
        print
        print "...Calculating Dot Product Similarities"
        numRows = len(self.theMatrix[:,0])
        numCols = len(self.theMatrix[0,:])
        simMatrix = scipy.zeros([numRows, numRows], float)
        for i in range(numRows):
            starttime = time.time()
            for j in range(numRows):
                simMatrix[i,j] = np.dot(self.theMatrix[i,:], self.theMatrix[j,:])
            took = time.time() - starttime
            print "     Word %s (%0.2f sec.)" % (str(i+1), took)
        return simMatrix
        
    # spearman rank correlation
    # mutual information
    # projection
    # gaussian kernal
    # tversky
    # KL divergence
        