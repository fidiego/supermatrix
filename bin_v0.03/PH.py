import sys, os, numpy as np
import sm_libs.scriptParams as params
import sm_libs.tcMatrix as tcMatrix

##############################################################################
corpusDirectory = sys.argv[1]
targetFilename = sys.argv[2]
featureFilename = sys.argv[3]

targetList = []
targetIndexDict = {}
lineCounter = 0
targetFilehandle = open(targetFilename)
for line in targetFilehandle:
    word = line.strip().strip('\n').strip()
    targetList.append(word)
    targetIndexDict[word] = lineCounter
    lineCounter += 1
targetFilehandle.close()

featureList = []
featureIndexDict = {}
featureValenceDict = {}
pFeatureList = []
nFeatureList = []
pFeatureDict = {}
nFeatureDict = {}

lineCounter = 0
pCounter = 0
nCounter = 0
featureFilehandle = open(featureFilename)
for line in featureFilehandle:
    data = (line.strip().strip('\n').strip()).split()
    feature = data[0]
    valenceCat = data[1]
    featureList.append(feature)
    featureIndexDict[feature] = lineCounter
    featureValenceDict[feature] = valenceCat
    if valenceCat == 1:
        pFeatureList.append(feature)
        pFeatureDict[feature] = pCounter
        pCounter += 1
    else:
        nFeatureList.append(feature)
        nFeatureDict[feature] = nCounter
        nCounter += 1    
    lineCounter += 1
featureFilehandle.close()

##############################################################################
# process the script parameters
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.initializeMatrix(corpusDirectory, "tcMatrix", 12, 1)
the_tcMatrix.getTargetList(targetFilename)
the_tcMatrix.getContextList(featureFilename)
the_tcMatrix.getDocumentList(0)
the_tcMatrix.processCorpus()
the_tcMatrix.outputDocumentInfo()
the_tcMatrix.outputTargetInfo()
the_tcMatrix.outputContextInfo()
the_tcMatrix.outputTargetDocumentCountMatrix()
the_tcMatrix.outputContextDocumentCountMatrix()
the_tcMatrix.outputSummedCoocMatrix()
the_tcMatrix.outputMatrixInfo()