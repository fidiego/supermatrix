import sys, numpy as np, scipy, time, operator
from scipy import stats
from scipy.stats import distributions
######################################################################################################
###### OUTPUT DEFINITIONS #######
######################################################################################################
def getNormMethodName(normMethodIndex):
    
    normalizationMethodsIndexDict = {}
    normalizationMethodsIndexDict[0] = "NO_NORM"
    normalizationMethodsIndexDict[1] = "ROW_SUM"
    normalizationMethodsIndexDict[2] = "COL_SUM"
    normalizationMethodsIndexDict[3] = "ROW_LENGTH"
    normalizationMethodsIndexDict[4] = "ROW_ZSCORE"
    normalizationMethodsIndexDict[5] = "COL_ZSCORE"
    normalizationMethodsIndexDict[6] = "ROWCOL_ZSCORE"
    normalizationMethodsIndexDict[7] = "COLROW_ZSCORE"
    normalizationMethodsIndexDict[8] = "ALL_ZSCORE"
    normalizationMethodsIndexDict[10] = "LOG10"
    normalizationMethodsIndexDict[11] = "LOGENTROPY"
    normalizationMethodsIndexDict[12] = "PMI"
    normalizationMethodsIndexDict[13] = "POSPMI"
    normalizationMethodsIndexDict[14] = "COALS"
    
    normalizationMethodList = sorted(normalizationMethodsIndexDict.items(), key=lambda x: x[1])
                  
    try:
        normMethodName = normalizationMethodsIndexDict[normMethodIndex]
        
    except:
        print "Error: Method %s is not a valid normalization method." % normMethodIndex
        print "Valid normalization methods are :"
        for normMethod in normalizationMethodList:
            print " %s: %s" % (normMethod[0], normMethod[1])
        sys.exit()
            
    return normMethodName
    
######################################################################################################
###### NORMALIZATION FUNCTIONS #######
######################################################################################################
# normalization 1
def rowProbabilityNormalization(theMatrix):
    print "...Normalizing Matrix by Row Sums"
    rowSums = theMatrix.sum(1)
    
    for i in range(len(rowSums)):
        if rowSums[i] == 0:
            print "     Warning! Row %s has sum of zero. Setting all norm values for this row to 0." % str(i)
            rowSums[i] = 1
    normMatrix = (theMatrix.transpose() / rowSums).transpose()
    return normMatrix

######################################################################################################
# normalization 2
def columnProbabilityNormalization(theMatrix):
    print "...Normalizing Matrix by Column Sums"
    columnSums = theMatrix.sum(0)
    for i in range(len(columnSums)):
        if columnSums[i] == 0:
            print "     Warning! Column %s has sum of zero. Setting all norm values for this column to 0." % str(i)
            columnSums[i] = 1
    normMatrix = (theMatrix.transpose() / columnSums).transpose()
    return normMatrix

######################################################################################################
# normalization 3
def lengthRowNormalization(theMatrix):
    print "...Normalizing Matrix by Row Lengths"
    
    rowLengths = np.sum(np.abs(theMatrix)**2,axis=1)**(1./2)
    for i in range(len(rowLengths)):
        if rowLengths[i] == 0:
            print "     Warning! Row %s has length of zero. Setting all norm values for this row to 0." % str(i)
            rowLengths[i] = 1
    normMatrix = theMatrix / rowLengths
    return normMatrix

######################################################################################################
# normalization 4
def zscoreRowsNormalization(theMatrix):
    print "...Normalizing Matrix by Row Z-Score"
    normMatrix = (theMatrix - theMatrix.mean(1)) - theMatrix.std(1, ddof=1)
    return normMatrix

######################################################################################################
# normalization 5
def zscoreColumnsNormalization(theMatrix):
    print "...Normalizing Matrix by Column Z-Score"
    normMatrix = (theMatrix - theMatrix.mean(0)) - theMatrix.std(0, ddof=1)
    return normMatrix
    
######################################################################################################
# normalization 6    
def zscoreBoth(theMatrix):
    print "...Normalizing Matrix by Row Z-Score"
    normMatrix1 = (theMatrix - theMatrix.mean(1)) - theMatrix.std(1, ddof=1)
    print "...Normalizing Matrix by Column Z-Score"
    normMatrix = (normMatrix1 - normMatrix1.mean(0)) - normMatrix1.std(0, ddof=1)
    return normMatrix

######################################################################################################
# normalization 7
def zscoreAll(theMatrix):
    print "...Normalizing Matrix by Row Z-Score"
    normMatrix = (theMatrix - theMatrix.mean()) - theMatrix.std(ddof=1)
    return normMatrix
    
######################################################################################################
# normalization 10
def log10(theMatrix):
    print "...Normalizing Matrix by Converting to Log10 Scores"
    normMatrix = np.log10(theMatrix+1)

######################################################################################################
# normalization 11
def logRowEntropyNormalization(theMatrix):
    print "...Normalizing Matrix Into LSA-style Log Entropy Values"
    
    numRows = len(theMatrix[:,0])
    numCols = len(theMatrix[0,:])
    normMatrix = scipy.zeros([numRows, numCols], float)
    rowEntropies = scipy.zeros([numRows],float)
    for i in range(numRows):
        currentVector = theMatrix[i,:]
        rowEntropies[i] = distributions.entropy(currentVector[np.nonzero(currentVector)])
        if rowEntropies[i] == 0:
            print "Warning: row %s had entropy of 0: Setting to 1."
            rowEntropies[i] = 1
    
    theMatrix = theMatrix + 1
    normMatrix = np.log10((theMatrix.transpose() / rowEntropies).transpose())

    return normMatrix

######################################################################################################
# normalization 12
def pmiNormalization(theMatrix):
    print "...Normalizing Matrix into Pointwise Mutual Information Values"
    numRows = len(theMatrix[:,0])
    numCols = len(theMatrix[0,:])
    colSums = theMatrix.sum(0)
    rowSums = theMatrix.sum(1)
    matrixSum = rowSums.sum()
 
    normMatrix = scipy.zeros([numRows, numCols], float)
    startTime = time.time()
    for i in range(numRows):
        for j in range(numCols):
            if rowSums[i] == 0:
                print "     Warning! Row %s has Sum of zero. Setting norm values for this item to 0." % str(i)
                normMatrix[i,j] = 0
            elif colSums[j] == 0:
                print "     Warning! Column %s has Sum of zero. Setting norm values for this item to 0." % str(i)
                normMatrix[i,j] = 0
            elif theMatrix[i,j] == 0:
                normMatrix[i,j] = 0
            else:
                normMatrix[i,j] = np.log((theMatrix[i,j] / matrixSum) / ((rowSums[i]/matrixSum) * (colSums[j]/matrixSum)))
        if ((i+1) % 100 == 0):
            took = time.time() - startTime
            print "     Finished %s/%s rows. Took %0.2f sec." % (i+1, numRows, took)
            startTime = time.time()
    return normMatrix

######################################################################################################
# normalization 13
def positivePmiNormalization(theMatrix):
    print "...Normalizing Matrix into Pointwise Mutual Information Values"
    numRows = len(theMatrix[:,0])
    numCols = len(theMatrix[0,:])
    colSums = theMatrix.sum(0)
    rowSums = theMatrix.sum(1)
    matrixSum = rowSums.sum()
    
    normMatrix = scipy.zeros([numRows, numCols], float)
    startTime = time.time()
    for i in range(numRows):
        for j in range(numCols):
            if rowSums[i] == 0:
                #print "     Warning! Row %s has Sum of zero. Setting norm values for this item to 0." % str(i)
                normMatrix[i,j] = 0
            elif colSums[j] == 0:
                #print "     Warning! Column %s has Sum of zero. Setting norm values for this item to 0." % str(i)
                normMatrix[i,j] = 0
            elif theMatrix[i,j] == 0:
                normMatrix[i,j] = 0
            else:
                normMatrix[i,j] = np.log((theMatrix[i,j] / matrixSum) / ((rowSums[i]/matrixSum) * (colSums[j]/matrixSum)))
                if normMatrix[i,j] < 0:
                    normMatrix[i,j] = 0
        if ((i+1) % 100 == 0):
            took = time.time() - startTime
            print "     Finished %s/%s rows. Took %0.2f sec." % (i+1, numRows, took)
            startTime = time.time()
    return normMatrix

######################################################################################################
# normalization 14
def coalsCorrelationNormalization(theMatrix):
    print "...Normalizing Matrix into COALS Correlation Values"
    numRows = len(theMatrix[:,0])
    numCols = len(theMatrix[0,:])
    rowSums = theMatrix.sum(1)
    colSums = theMatrix.sum(0)
    matrixSum = rowSums.sum()

    normMatrix = scipy.zeros([numRows, numCols], float)
    startTime = time.time()
    for i in range(numRows):
        for j in range(numCols):
            if rowSums[i] == 0:
                print "     Warning! Row %s has Sum of zero. Setting norm values for this item to 0." % str(i)
                pass
            elif colSums[j] == 0:
                print "     Warning! Column %s has Sum of zero. Setting norm values for this item to 0." % str(i)
                pass
            else:
                normMatrix = (matrixSum*theMatrix[i,j] - rowSums[i]*colSums[j]) / (((rowSums[i]*(matrixSum-rowSums[i])) * (colSums[j]*(matrixSum-colSums[j])))**0.5)
        if ((i+1) % 100 == 0):
            took = time.time() - startTime
            print "     Finished %s/%s rows. Took %0.2f sec." % (i+1, numRows, took)
            startTime = time.time()
    return normMatrix

######################################################################################################
def integerizeNormalization(theMatrix):
    print "...Normlizing the matrix into values where smallest is 1 and all other values are proportional multiples"
    multiplier = 1/(theMatrix[theMatrix != 0].min())
    return normMatrix*multiplier
