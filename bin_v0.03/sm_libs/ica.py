import sys, os, time, datetime, operator, shutil
import scipy
import numpy as np
from scipy import linalg
from operator import itemgetter, attrgetter
import sm_libs.normalizations as norm
import sm_libs.simMatrix as simMatrix
import sklearn
from sklearn.decomposition import FastICA, PCA
import sklearn.decomposition
################################################################################################
################################################################################################
class icaModel:
    ############################################################################################
    def __init__(self):
        # basic parameters

        self.matrixDirectory = 0
        self.icaDirectory = 0
        self.outputDirectory = 0
        self.outputPath = 0
        
        self.rowList = []
        self.rowDict = {}
        self.rowIndexDict = {}
        self.columnList = []
        self.columnDict = {}
        self.columnIndexDict = {}
        
        self.theMatrix = []
        self.rowSingularVectors = []
        self.singularValues = []
        self.columnSingularVectors = []
        
        self.normalizationMethod = 0
        
    ############################################################################################
    def initializeModel(self, matrixDirectory, icaDirectory, theMatrix, rowIndexDict, columnIndexDict):
    
        self.matrixDirectory = matrixDirectory
        self.icaDirectory = icaDirectory

        self.outputPath = self.matrixDirectory + self.icaDirectory
    
        if os.path.isdir(self.outputPath):
            print
            print "     Warning: The ICA model directory %s already exists in the %s matrix directory." % (matrixDirectory, self.icaDirectory)
            userInput = raw_input("     Do you want to erase and overwrite this ICA model directory? (y/n) -->")
            if ((userInput == "y") or (userInput == "Y")):
                shutil.rmtree(self.outputPath)
                print
                print "...Overwriting Output Directory"
                os.mkdir(self.outputPath) 
            else:
                print "Quitting..."
                sys.exit(1)
        else:
            print "...Creating New Model Output Directory"
            os.mkdir(self.outputPath)
    
        self.theMatrix = theMatrix
        self.rowIndexDict = rowIndexDict
        self.columnIndexDict = columnIndexDict
    
    ############################################################################################
    def computeICA(self):
        print "...Computing ICA"
        ica = sklearn.decomposition.FastICA()
        resultsMatrix = ica.fit_transform(self.theMatrix)
        self.rowSingularVectors = ica.fit_transform(X)
    
    ############################################################################################        
    def outputModelInfo(self):
        print "...Outputting Data"
        outputFilehandle =  open(self.outputPath + "/" + "model_info.txt", "w")
        outputFilehandle.write("normalization_method: %s\n" % self.normalizationMethod)
        outputFilehandle.close()

        outputFilehandle = open(self.outputPath+"/"+"row_info.txt", "w")
        for i in range(len(self.rowIndexDict)):
            outputFilehandle.write("%s %s\n" % (str(i), self.rowIndexDict[i]))
        outputFilehandle.close()

        outputFilehandle = open(self.outputPath+"/"+"column_info.txt", "w")
        for i in range(len(self.columnIndexDict)):
            outputFilehandle.write("%s %s\n" % (str(i), self.columnIndexDict[i]))
        outputFilehandle.close()
        
        outputFilehandle = open(self.outputPath+"/"+"row_singular_vectors.txt", "w")
        for i in range(len(self.rowIndexDict)):
            outputFilehandle.write("%s " % self.rowIndexDict[i])
            for j in range(len(self.rowIndexDict)):
                outputFilehandle.write(" %0.6f" % self.rowSingularVectors[i,j])
            outputFilehandle.write("\n")
        outputFilehandle.close()

        #outputFilehandle = open(self.outputPath+"/"+"column_singular_vectors.txt", "w")
        #for i in range(len(self.columnIndexDict)):
        #    outputFilehandle.write("%s " % self.columnIndexDict[i])
        #    for j in range(len(self.columnIndexDict)):
        #        outputFilehandle.write(" %0.6f" % self.columnSingularVectors[i,j])
        #    outputFilehandle.write("\n")
        #outputFilehandle.close()
        
    ############################################################################################        
    def importModelInfo(self, icaDirectory):
        self.icaDirectory = icaDirectory
        
        # Get ica model parameters from text file
        infoFilehandle = open(icaDirectory+"model_info.txt")
        for line in infoFilehandle:
            data = (line.strip('\n').strip()).split()
            if data[0] == 'normalization_method:':
                self.normalizationMethod = int(data[1])
        infoFilehandle.close()

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
        self.rowList = []
        self.rowDict = {}
        self.rowIndexDict = {}
        self.rowSubList = []
        self.rowSubDict = {}
        self.rowSubIndexDict = {}
        
        if rowInclusionFile:
            inclusionDict = {}
            filehandle = open(rowInclusionFile)
            for line in filehandle:
                data = (line.strip('\n').strip()).split()
                if len(data) > 0:
                    inclusionDict[data[-1]] = 1
            filehandle.close()
            
            targetInfoFilehandle = open(self.icaDirectory+"row_info.txt")
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
            targetInfoFilehandle = open(self.icaDirectory+"row_info.txt")
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

    ############################################################################################        
    def importColumnInfo(self):

        # Create list and dictionaries of columns
        self.columnList = []
        self.columnDict = {}
        self.columnIndexDict = {}
        
        # go through the file and read columns into the list and dictionaries
        columnInfoFilehandle = open(self.icaDirectory+"column_info.txt")
        
        for line in columnInfoFilehandle:
            data = (line.strip('\n').strip()).split()
            columnIndex = int(data[0])
            columnLabel = data[1]
            self.columnList.append(columnLabel)
            self.columnDict[columnLabel] = columnIndex
            self.columnIndexDict[columnIndex] = columnLabel
        columnInfoFilehandle.close()
        self.numColumns = len(self.columnList)
        
    ############################################################################################        
    def importRowSingularVectors(self, numDimensions):
    
        if numDimensions == 0:
            self.numDimensions = self.numRows
        elif numDimensions > self.numColumns:
            self.numDimensions = self.numColumns
        else:
            self.numDimensions = numDimensions
    
        self.rowSingularValues = scipy.zeros([self.numRows, self.numDimensions], float)
    
        rowSingularVectorsFilehandle = open(self.icaDirectory+"row_singular_vectors.txt")
        
        rowCounter = 0
        for line in rowSingularVectorsFilehandle:
            data = (line.strip('\n').strip()).split()
            if data[0] in self.rowSubDict:       
                values = data[1:]
                for dimensionCounter in range(self.numDimensions):
                    self.rowSingularValues[rowCounter, dimensionCounter] = values[dimensionCounter]
                rowCounter += 1
        rowSingularVectorsFilehandle.close()
        
    ############################################################################################        
    def normalizeRowSingularValues(self, normalizationMethod):
        self.normalizationMethod = normalizationMethod
    
        if self.normalizationMethod == 0:
            self.normRowMatrix = self.rowSingularValues     
        elif self.normalizationMethod == 1:
            self.normRowMatrix = norm.rowProbabilityNormalization(self.rowSingularValues)
        elif self.normalizationMethod == 2:
            self.normRowMatrix = norm.columnProbabilityNormalization(self.rowSingularValues)
        elif self.normalizationMethod == 3:
            self.normRowMatrix = norm.lengthRowNormalization(self.rowSingularValues)
        elif self.normalizationMethod == 4:
            self.normRowMatrix = norm.zscoreRowsNormalization(self.rowSingularValues)
        elif self.normalizationMethod == 5:
            self.normRowMatrix = norm.zscoreColumnsNormalization(self.rowSingularValues)
        elif self.normalizationMethod == 11:
            self.normRowMatrix = norm.logRowEntropyNormalization(self.rowSingularValues)
        elif self.normalizationMethod == 12:
            self.normRowMatrix = norm.pmiNormalization(self.rowSingularValues)
        elif self.normalizationMethod == 13:
            self.normRowMatrix = norm.positivePmiNormalization(self.rowSingularValues)
        elif self.normalizationMethod == 14:
            self.normRowMatrix = norm.coalsCorrelationNormalization(self.rowSingularValues)      
        elif self.normalizationMethod == 15:
            self.normRowMatrix = norm.IntegerizeNormalization(self.rowSingularValues)    
            
    ############################################################################################        
    def calculateAllRowSimilarities(self, similarityMetric):
    
        self.similarityMetric = similarityMetric
        self.outputFilename = "icaSimilarities_D%s_N%s_M%s.txt" % (self.numDimensions, self.normalizationMethod, self.similarityMetric)
        normTypeName = norm.getNormMethodName(self.normalizationMethod)

        self.the_simMatrix = simMatrix.simMatrix()
        simMetricName = self.the_simMatrix.getSimMetricName(similarityMetric)
        updateString = "%s %s %s\n" % (self.outputFilename, normTypeName, simMetricName)

        self.the_simMatrix.assignTargetInfo(self.rowSubList, self.rowSubDict, self.rowSubIndexDict)
        self.the_simMatrix.assignMatrixData(self.normRowMatrix)
        
        self.the_simMatrix.initNewSimMatrix(self.icaDirectory, "icaSimilarities", self.outputFilename, updateString)
        self.the_simMatrix.calculateAllSimilarities(self.similarityMetric)
        self.the_simMatrix.outputSimilarityMatrix()
    