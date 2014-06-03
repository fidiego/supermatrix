import sys, os, time, datetime, operator, shutil
import numpy as np
import sm_libs.normalizations as norm
################################################################################################
################################################################################################
class sentimentModel:
    ############################################################################################
    def __init__(self):
        # basic parameters

        self.matrixDirectory = 0
        self.outputDirectory = 0
        self.outputPath = 0

        self.targetFilename = 0
        self.targetList = []
        self.targetIndexDict = []
        self.numTargets = 0
        
        self.featureFilename = 0
        self.featureList = []
        self.featureIndexDict = {}
        self.featureValenceCatDict = {}
        self.featureValenceRatingDict = {}
        self.pFeatureList = []
        self.nFeatureList = []
        self.pFeatureDict = {}
        self.nFeatureDict = {}
        self.numFeatures = 0
        self.numPFeatures = 0
        self.numNFeatures = 0
        
        self.documentFilename = 0
        self.documentList = []
        self.documentIndexDict = {}
        self.numDocuments = 0
        
        self.normalizationMethod = 0
        
    ############################################################################################
    def initializeModel(self, matrixDirectory, outputDirectory, targetFilename, featureFilename, documentFilename, normalizationMethod):
    
        self.matrixDirectory = matrixDirectory
        self.outputDirectory = outputDirectory
        self.outputPath = self.matrixDirectory + self.outputDirectory
    
        if os.path.isdir(self.outputPath):
            print
            print "     Warning: The Sentiment model directory %s already exists in the %s matrix directory." % (matrixDirectory, self.outputDirectory)
            userInput = raw_input("     Do you want to erase and overwrite this Sentiment model directory? (y/n) -->")
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
    
        self.targetFilename = targetFilename
        self.featureFilename = featureFilename
        self.documentFilename = documentFilename
        self.normalizationMethod = normalizationMethod
    
    ############################################################################################
    def getTargetList(self, the_tcMatrix):
    
        lineCounter = 0
        targetFilehandle = open(self.targetFilename)
        for line in targetFilehandle:
            word = line.strip().strip('\n').strip()
            self.targetList.append(word)
            self.targetIndexDict[word] = lineCounter
            if not word in the_tcMatrix.subTargetDict:
                print "Warning: %s is not in this matrix's target list" % word
            lineCounter += 1
        targetFilehandle.close()
        self.numTargets = lineCounter
    
    ############################################################################################
    def getFeatureList(self, the_tcMatrix):
        lineCounter = 0
        pCounter = 0
        nCounter = 0
        featureFilehandle = open(self.featureFilename)
        for line in featureFilehandle:
            data = (line.strip().strip('\n').strip()).split()
            feature = data[0]
            valenceCat = int(data[1])
            if not feature in the_tcMatrix.subContextDict:
                print "Warning: %s is not in this matrix's context list" % feature
            self.featureList.append(feature)
            self.featureIndexDict[feature] = lineCounter
            self.featureValenceCatDict[feature] = valenceCat
            if len(data) == 3:
                self.featureValenceRatingDict[feature] = float(data[2])
            if valenceCat == 1:
                self.pFeatureList.append(feature)
                self.pFeatureDict[feature] = pCounter
                pCounter += 1
            else:
                self.nFeatureList.append(feature)
                self.nFeatureDict[feature] = nCounter
                nCounter += 1    
            lineCounter += 1
        featureFilehandle.close()
        self.numFeatures = lineCounter
        self.numPFeatures = pCounter
        self.numNFeatures = nCounter        
    ############################################################################################
    
    