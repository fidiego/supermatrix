import sys, os, time, datetime, operator, shutil
import numpy as np
from numpy.random import normal as npnorm
import sm_libs.normalizations as norm
import sm_libs.simMatrix as simMatrix
################################################################################################
################################################################################################
class rvaModel:
    ############################################################################################
    def __init__(self):
        # basic parameters

        self.matrixDirectory = 0
        self.rvaDirectory = 0
        self.outputDirectory = 0
        self.outputPath = 0
        
        self.inputMatrix = []
        self.rowIndexDict = {}
        
        self.environmentMatrix = []
        self.memoryMatrix = []
        
        self.randomVectorLength = 0
        self.randomVectorMean = 0
        self.randomVectorSD = 0
        
    ############################################################################################
    def initializeModel(self, matrixDirectory, rvaDirectory, inputMatrix, rowIndexDict, inputColumnIndexDict, randomSeed, vectorLength, vectorMean, vectorSD, normalizationMethod):
    
        self.matrixDirectory = matrixDirectory
        self.rvaDirectory = rvaDirectory
        self.outputPath = self.matrixDirectory + self.rvaDirectory
    
        if os.path.isdir(self.outputPath):
            print
            print "     Warning: The RVA model directory %s already exists in the %s matrix directory." % (matrixDirectory, self.rvaDirectory)
            userInput = raw_input("     Do you want to erase and overwrite this RVA model directory? (y/n) -->")
            if ((userInput == "y") or (userInput == "Y")):
                shutil.rmtree(self.outputPath)
                print
                print "...Overwriting Output Directory"
                os.mkdir(self.outputPath) 
            else:
                print "Quitting..."
                sys.exit(1)
        else:
            print "...Creating New RVA Model Output Directory"
            os.mkdir(self.outputPath)
    
        self.inputMatrix = inputMatrix
        self.rowIndexDict = rowIndexDict
        self.inputColumnIndexDict = inputColumnIndexDict
        self.randomSeed = randomSeed
        self.numRows = len(rowIndexDict)
        self.numCols = vectorLength
        self.numInputCols = len(inputColumnIndexDict)
        self.vectorMean = vectorMean
        self.vectorSD = vectorSD
        self.normalizationMethod = normalizationMethod
    
    ############################################################################################
    def generateRandomVectors(self):
    
        if self.randomSeed:
            np.random.seed(self.randomSeed)
        else:
            np.random.seed(seed=None)
    
        print "...Generating %s Random Normal Enviroment Vectors of length %s with mean and SD of %s,%s" % (self.numInputCols, self.numCols, self.vectorMean, self.vectorSD)
        self.environmentMatrix = npnorm(self.vectorMean, self.vectorSD, [self.numInputCols, self.numCols])
    
    ############################################################################################
    def generateMemoryMatrix(self):
        print "...Building the Memory Vectors from the Enviroment Vectors"
        self.memoryMatrix = np.zeros([self.numRows, self.numCols],float)
        for i in range(self.numRows):
            for j in range(self.numInputCols):
                self.memoryMatrix[i,:] += (self.inputMatrix[i,j]*self.environmentMatrix[j,:])
            if i % 100 == 0:
                print "         Finished %s/%s Rows" % (i, self.numRows)
        
    ############################################################################################
    def outputModelInfo(self):
        print "...Outputting Data"
        outputFilehandle =  open(self.outputPath + "/" + "model_info.txt", "w")
        outputFilehandle.write("num_rows: %s\n" % self.numRows)
        outputFilehandle.write("num_cols: %s\n" % self.numCols)
        outputFilehandle.write("normalization_method: %s\n" % self.normalizationMethod)
        outputFilehandle.write("vector_mean: %s\n" % self.vectorMean)
        outputFilehandle.write("vector_sd: %s\n" % self.vectorSD)
        outputFilehandle.write("random_seed: %s\n" % self.normalizationMethod)
        outputFilehandle.close()

        outputFilehandle = open(self.outputPath+"/"+"row_info.txt", "w")
        for i in range(len(self.rowIndexDict)):
            outputFilehandle.write("%s %s\n" % (str(i), self.rowIndexDict[i]))
        outputFilehandle.close()

        outputFilehandle = open(self.outputPath+"/"+"input_column_info.txt", "w")
        for i in range(len(self.inputColumnIndexDict)):
            outputFilehandle.write("%s %s\n" % (str(i), self.inputColumnIndexDict[i]))
        outputFilehandle.close()

        outputFilehandle = open(self.outputPath+"/"+"enviroment_vectors.txt", "w")
        for i in range(self.numInputCols):
            outputFilehandle.write("%s " % self.inputColumnIndexDict[i])
            for j in range(self.numCols):
                outputFilehandle.write(" %0.6f" % self.environmentMatrix[i,j])
            outputFilehandle.write("\n")
        outputFilehandle.close()
        
        outputFilehandle = open(self.outputPath+"/"+"memory_vectors.txt", "w")
        for i in range(self.numRows):
            outputFilehandle.write("%s " % self.rowIndexDict[i])
            for j in range(self.numCols):
                outputFilehandle.write(" %0.6f" % self.memoryMatrix[i,j])
            outputFilehandle.write("\n")
        outputFilehandle.close()

    ############################################################################################
    def importModelInfo(self, rvaDirectory):
        print "Importing RVA Model Info"
        self.rvaDirectory = rvaDirectory
        
        # Get rva model parameters from text file
        infoFilehandle = open(rvaDirectory+"model_info.txt")
        for line in infoFilehandle:
            data = (line.strip('\n').strip()).split()
            if data[0] == 'num_rows:':
                self.numMasterRows = int(data[1])
            elif data[0] == 'num_cols:':
                self.numCols = int(data[1])
            elif data[0] == 'normalization_method:':
                self.normalizationMethod = int(data[1])
            elif data[0] == 'vector_mean:':
                self.vectorMean = float(data[1])
            elif data[0] == 'vector_sd:':
                self.vectorSD = float(data[1])
            elif data[0] == 'random_seed:':
                self.randomSeed = int(data[1])          
        infoFilehandle.close()
    
    ############################################################################################
    def importRowInfo(self, rowInclusionFilename, rowExclusionFilename):
    
        exclusionDict = {}
        if rowExclusionFilename:
            filehandle = open(rowExclusionFilename)
            for line in filehandle:
                data = (line.strip('\n').strip()).split()
                if len(data) > 0:
                    exclusionDict[data[-1]] = 1
            filehandle.close()
    
        # Create list and dictionaries of rows
        self.rowList = []
        self.rowDict = {}
        self.rowIndexDict = {}
        self.rowSubList = []
        self.rowSubDict = {}
        self.rowSubIndexDict = {}
        
        if rowInclusionFilename:
            inclusionDict = {}
            filehandle = open(rowInclusionFilename)
            for line in filehandle:
                data = (line.strip('\n').strip()).split()
                if len(data) > 0:
                    inclusionDict[data[-1]] = 1
            filehandle.close()
            
            targetInfoFilehandle = open(self.rvaDirectory+"row_info.txt")
            rowCounter = 0
            for line in targetInfoFilehandle:
                data = (line.strip('\n').strip()).split()
                rowIndex = int(data[0])
                rowLabel = data[1]
                if rowLabel in inclusionDict:
                    if not rowLabel in exclusionDict:
                        self.rowList.append(rowLabel)
                        self.rowDict[rowLabel] = rowIndex
                        self.rowIndexDict[rowIndex] = rowLabel
                        self.rowSubList.append(rowLabel)
                        self.rowSubDict[rowLabel] = rowCounter
                        self.rowSubIndexDict[rowCounter] = rowLabel
                        rowCounter += 1
            
        else:
            # go through the file and read rows into the list and dictionaries
            targetInfoFilehandle = open(self.rvaDirectory+"row_info.txt")
            rowCounter = 0
            for line in targetInfoFilehandle:
                data = (line.strip('\n').strip()).split()
                rowIndex = int(data[0])
                rowLabel = data[1]
                if not rowLabel in exclusionDict:
                    self.rowList.append(rowLabel)
                    self.rowDict[rowLabel] = rowIndex
                    self.rowIndexDict[rowIndex] = rowLabel
                    self.rowSubList.append(rowLabel)
                    self.rowSubDict[rowLabel] = rowCounter
                    self.rowSubIndexDict[rowCounter] = rowLabel
                    rowCounter += 1
            targetInfoFilehandle.close()
        self.numRows = len(self.rowList)
        self.numSubRows = len(self.rowSubList)
    
    ############################################################################################
    def importEnvironmentMatrix(self):

        print "Importing RVA Environment Matrix"
        self.environmentMatrix = np.zeros([self.numSubRows, self.numCols], float)
        environmentMatrixFilehandle = open(self.rvaDirectory+"environment_vectors.txt")    
        rowCounter = 0
        for line in environmentMatrixFilehandle:
            data = (line.strip('\n').strip()).split()
            if data[0] in self.rowSubDict:       
                values = data[1:]
                for i in range(len(values)):
                    self.environmentMatrix[rowCounter,i] = float(values[i])
                rowCounter += 1
        environmentMatrixFilehandle.close()

    ############################################################################################
    def importMemoryMatrix(self):
        
        print "Importing RVA Memory Matrix"
        self.memoryMatrix = np.zeros([self.numSubRows, self.numCols], float)
        memoryMatrixFilehandle = open(self.rvaDirectory+"memory_vectors.txt")    
        rowCounter = 0
        for line in memoryMatrixFilehandle:
            data = (line.strip('\n').strip()).split()
            if data[0] in self.rowSubDict:       
                values = data[1:]
                for i in range(len(values)):
                    self.memoryMatrix[rowCounter,i] = float(values[i])
                rowCounter += 1
        memoryMatrixFilehandle.close()
    
    ############################################################################################
    def normalizeMemoryMatrix(self, normalizationMethod):
    
        self.normalizationMethod = normalizationMethod
    
        if self.normalizationMethod == 0:
            self.normMemMatrix = self.memoryMatrix     
        elif self.normalizationMethod == 1:
            self.normMemMatrix = norm.rowProbabilityNormalization(self.memoryMatrix)
        elif self.normalizationMethod == 2:
            self.normMemMatrix = norm.columnProbabilityNormalization(self.memoryMatrix)
        elif self.normalizationMethod == 3:
            self.normMemMatrix = norm.lengthRowNormalization(self.memoryMatrix)
        elif self.normalizationMethod == 4:
            self.normMemMatrix = norm.zscoreRowsNormalization(self.memoryMatrix)
        elif self.normalizationMethod == 5:
            self.normMemMatrix = norm.zscoreColumnsNormalization(self.memoryMatrix)
        elif self.normalizationMethod == 11:
            self.normMemMatrix = norm.logRowEntropyNormalization(self.memoryMatrix)
        elif self.normalizationMethod == 12:
            self.normMemMatrix = norm.pmiNormalization(self.memoryMatrix)
        elif self.normalizationMethod == 13:
            self.normMemMatrix = norm.positivePmiNormalization(self.memoryMatrix)
        elif self.normalizationMethod == 14:
            self.normMemMatrix = norm.coalsCorrelationNormalization(self.memoryMatrix)      
        elif self.normalizationMethod == 15:
            self.normMemMatrix = norm.IntegerizeNormalization(self.memoryMatrix)  
    
    ############################################################################################
    def calculateAllRowSimilarities(self, similarityMetric):
    
        self.similarityMetric = similarityMetric
        self.outputFilename = "rvaSimilarities_N%s_M%s.txt" % (self.normalizationMethod, self.similarityMetric)
        normTypeName = norm.getNormMethodName(self.normalizationMethod)

        self.the_simMatrix = simMatrix.simMatrix()
        simMetricName = self.the_simMatrix.getSimMetricName(similarityMetric)
        updateString = "%s %s %s\n" % (self.outputFilename, normTypeName, simMetricName)

        self.the_simMatrix.assignTargetInfo(self.rowSubList, self.rowSubDict, self.rowSubIndexDict)
        self.the_simMatrix.assignMatrixData(self.normMemMatrix)
        
        self.the_simMatrix.initNewSimMatrix(self.rvaDirectory, self.outputFilename, updateString)
        self.the_simMatrix.calculateAllSimilarities(self.similarityMetric)
        self.the_simMatrix.outputSimilarityMatrix()
    
    
    
    