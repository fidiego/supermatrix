##############################################################################
# import python libraries
import sys, os
import sm_libs.tcMatrix as tcMatrix
import sm_libs.simMatrix as simMatrix
import sm_libs.scriptParams as params
##############################################################################
# process script parameters
matrixDirectory = sys.argv[1]
outputDirectory = sys.argv[2]
##############################################################################
ppmiSimFile = matrixDirectory+'tcSims/tcSimilarities_D1_S12_C1_W0_N13_M4.txt'
ppmiSimIndexes = matrixDirectory+'tcSims/target_info.txt'
coalsSimFile = matrixDirectory+'tcSVD/similarities/svdSimilarities_D50_N0_M4.txt'
coalsSimIndexes = matrixDirectory+'tcSVD/similarities/target_info.txt'
rvaSimFile = matrixDirectory+'tcRVA/similarities/rvaSimilarities_N0_M1.txt'
rvaSimIndexes = matrixDirectory+'tcRVA/similarities/target_info.txt'
docSimFile = matrixDirectory+'tdSims/tdSimilarities_N11_M1.txt'
docSimIndexes = matrixDirectory+'tdSims/target_info.txt'
lsaSimFile = matrixDirectory+'tdSVD/similarities/svdSimilarities_D50_N0_M1.txt'
lsaSimIndexes = matrixDirectory+'tdSVD/similarities/target_info.txt'
##############################################################################

the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.importMatrixInfo(matrixDirectory)
the_tcMatrix.importTargetInfo(0, 0)
the_tcMatrix.importContextInfo(0, 0)
the_tcMatrix.importSummedMatrix(1, 0, 1, 0)
the_tcMatrix.normalizeCoocMatrix(12)

the_simMatrix1 = simMatrix.simMatrix()
the_simMatrix1.initExistingSimMatrix(ppmiSimFile, ppmiSimIndexes)
the_simMatrix1.importTargetInfo()
the_simMatrix1.importSimilarityMatrix()

the_simMatrix2 = simMatrix.simMatrix()
the_simMatrix2.initExistingSimMatrix(coalsSimFile, coalsSimIndexes)
the_simMatrix2.importTargetInfo()
the_simMatrix2.importSimilarityMatrix()

the_simMatrix3 = simMatrix.simMatrix()
the_simMatrix3.initExistingSimMatrix(rvaSimFile, rvaSimIndexes)
the_simMatrix3.importTargetInfo()
the_simMatrix3.importSimilarityMatrix()

the_simMatrix4 = simMatrix.simMatrix()
the_simMatrix4.initExistingSimMatrix(docSimFile, docSimIndexes)
the_simMatrix4.importTargetInfo()
the_simMatrix4.importSimilarityMatrix()

the_simMatrix5 = simMatrix.simMatrix()
the_simMatrix5.initExistingSimMatrix(lsaSimFile, lsaSimIndexes)
the_simMatrix5.importTargetInfo()
the_simMatrix5.importSimilarityMatrix()

try:
    os.mkdir(outputDirectory)
except:
    pass

print "Exporting Data"
for i in range(the_tcMatrix.numSubTargets):
    currentTarget = the_tcMatrix.subTargetList[i]
    outputFilehandle = open(outputDirectory+"/"+currentTarget+".txt", "w")
    for j in range(the_tcMatrix.numSubTargets):
        currentContext = the_tcMatrix.subTargetList[j]
    
        pmi = the_tcMatrix.coocMatrix[i,j]
        
        if ((currentTarget in the_simMatrix1.targetDict) and (currentContext in the_simMatrix1.targetDict)):
            x = the_simMatrix1.targetDict[currentTarget]
            y = the_simMatrix1.targetDict[currentContext]
            ppmiSim = the_simMatrix1.similarityMatrix[x,y]
        else:
            ppmiSim = -1

        if ((currentTarget in the_simMatrix2.targetDict) and (currentContext in the_simMatrix2.targetDict)):
            x = the_simMatrix2.targetDict[currentTarget]
            y = the_simMatrix2.targetDict[currentContext]
            coalsSim = the_simMatrix2.similarityMatrix[x,y]
        else:
            coalsSim = -1

        if ((currentTarget in the_simMatrix3.targetDict) and (currentContext in the_simMatrix3.targetDict)):
            x = the_simMatrix3.targetDict[currentTarget]
            y = the_simMatrix3.targetDict[currentContext]
            rvaSim = the_simMatrix3.similarityMatrix[x,y]
        else:
            rvaSim = -1

        if ((currentTarget in the_simMatrix4.targetDict) and (currentContext in the_simMatrix4.targetDict)):
            x = the_simMatrix4.targetDict[currentTarget]
            y = the_simMatrix4.targetDict[currentContext]
            docSim = the_simMatrix4.similarityMatrix[x,y]
        else:
            docSim = -1

        if ((currentTarget in the_simMatrix5.targetDict) and (currentContext in the_simMatrix5.targetDict)):
            x = the_simMatrix5.targetDict[currentTarget]
            y = the_simMatrix5.targetDict[currentContext]
            lsaSim = the_simMatrix5.similarityMatrix[x,y]
        else:
            lsaSim = -1
            
        outputFilehandle.write("%s %s %0.6f %0.6f %0.6f %0.6f %0.6f %0.6f\n" % (currentTarget, currentContext, pmi, ppmiSim, coalsSim, rvaSim, docSim, lsaSim))
    outputFilehandle.close()