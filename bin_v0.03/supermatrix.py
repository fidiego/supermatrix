##############################################################################
# define and set program parameters
documentDirectory = 0           # -d: the path of the directory containing the documents.
corpusDirectory = 0             # -c: the name of the directory that will be created
matrixDirectory1 = "tcMatrix"
inclusionList = 0

windowSize = 1
directionType = 1 # 0 concatenate, 1 summed, 2 forward, 3 backward                      

#alphaList = [.5]                    
#betaList = [.5]                   
#numTopicsList = [2,4,8,12,16]               
#ldaIterations = 100                 
#randomSeed = 10                   

##############################################################################
# import python libraries
import sys
import sm_libs.scriptParams as params
import sm_libs.corpora as corpora
import sm_libs.tdMatrix as tdMatrix
import sm_libs.tcMatrix as tcMatrix
import sm_libs.svd as svd
import sm_libs.lda as lda
##############################################################################

# process command line arguments
documentDirectory, corpusDirectory, inclusionList = params.supermatrix(sys.argv[1:], documentDirectory, corpusDirectory, inclusionList)

# create and corpus
theCorpus = corpora.corpus()
theCorpus.initializeNewCorpus(corpusDirectory, 0, 1)
theCorpus.getSeparateDocumentList(documentDirectory)
theCorpus.countAndMergeSeparateDocuments()
theCorpus.outputCorpusInfo()
theCorpus.outputTargetInfo()
theCorpus.outputDocumentInfo()

# create the tcMatrix
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.initializeMatrix(corpusDirectory+"/", matrixDirectory1, windowSize, 0)
the_tcMatrix.getTargetList(inclusionList)
the_tcMatrix.getContextList(inclusionList)
the_tcMatrix.getDocumentList(0)
the_tcMatrix.processCorpus()
the_tcMatrix.outputDocumentInfo()
the_tcMatrix.outputTargetInfo()
the_tcMatrix.outputContextInfo()
the_tcMatrix.outputTargetDocumentCountMatrix()
the_tcMatrix.outputFullTDMatrix()
the_tcMatrix.outputSummedCoocMatrix()
the_tcMatrix.outputMatrixInfo()

# compute tdMatrix sims
matrixDirectory = corpusDirectory+"/"+matrixDirectory1+"/"
tdSimsDirectory = "tdSimilarities"
the_tdMatrix = tdMatrix.tdMatrix()
the_tdMatrix.importMatrixInfo(matrixDirectory)
the_tdMatrix.importTargetInfo(0,0)
the_tdMatrix.importDocumentInfo(0,0)
the_tdMatrix.importTargetDocumentMatrix()
the_tdMatrix.normalizeTargetDocumentMatrix(0)
the_tdMatrix.calculateAllSimilarities(1)
the_tdMatrix.calculateAllSimilarities(2)
the_tdMatrix.calculateAllSimilarities(4)
the_tdMatrix.importTargetDocumentMatrix()
the_tdMatrix.normalizeTargetDocumentMatrix(1)
the_tdMatrix.calculateAllSimilarities(1)
the_tdMatrix.calculateAllSimilarities(2)
the_tdMatrix.calculateAllSimilarities(4)
the_tdMatrix.importTargetDocumentMatrix()
the_tdMatrix.normalizeTargetDocumentMatrix(11)
the_tdMatrix.calculateAllSimilarities(1)
the_tdMatrix.calculateAllSimilarities(2)
the_tdMatrix.calculateAllSimilarities(4)
the_tdMatrix.importTargetDocumentMatrix()
the_tdMatrix.normalizeTargetDocumentMatrix(13)
the_tdMatrix.calculateAllSimilarities(1)
the_tdMatrix.calculateAllSimilarities(2)
the_tdMatrix.calculateAllSimilarities(4)

# compute tcMatrix sims
matrixDirectory = corpusDirectory+"/"+matrixDirectory1+"/"
tcSimsDirectory = "tcSimilarities"
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.importMatrixInfo(matrixDirectory)
the_tcMatrix.importTargetInfo(0,0)
the_tcMatrix.importContextInfo(0,0)
the_tcMatrix.importSummedMatrix(directionType, 0, 1, 0)
the_tcMatrix.outputFullTCMatrix(matrixDirectory)
the_tcMatrix.normalizeCoocMatrix(0)
the_tcMatrix.calculateAllSimilarities(1)
the_tcMatrix.calculateAllSimilarities(2)
the_tcMatrix.calculateAllSimilarities(4)
the_tcMatrix.importSummedMatrix(directionType, 0, 1, 0)
the_tcMatrix.normalizeCoocMatrix(1)
the_tcMatrix.calculateAllSimilarities(1)
the_tcMatrix.calculateAllSimilarities(2)
the_tcMatrix.calculateAllSimilarities(4)
the_tcMatrix.importSummedMatrix(directionType, 0, 1, 0)
the_tcMatrix.normalizeCoocMatrix(11)
the_tcMatrix.calculateAllSimilarities(1)
the_tcMatrix.calculateAllSimilarities(2)
the_tcMatrix.calculateAllSimilarities(4)
the_tcMatrix.importSummedMatrix(directionType, 0, 1, 0)
the_tcMatrix.normalizeCoocMatrix(13)
the_tcMatrix.calculateAllSimilarities(1)
the_tcMatrix.calculateAllSimilarities(2)
the_tcMatrix.calculateAllSimilarities(4)

# svd the wd matrix
matrixDirectory = corpusDirectory+"/"+matrixDirectory1+"/"
the_tdMatrix = tdMatrix.tdMatrix()
the_tdMatrix.importMatrixInfo(matrixDirectory)
the_tdMatrix.importTargetInfo(0,0)
the_tdMatrix.importDocumentInfo(0,0)
the_tdMatrix.importTargetDocumentMatrix()
the_tdMatrix.normalizeTargetDocumentMatrix(0)
the_svdModel = svd.svdModel()
the_svdModel.initializeModel(matrixDirectory, "tdSVD", the_tdMatrix.normalizedTargetDocumentMatrix, the_tdMatrix.subTargetIndexDict, the_tdMatrix.subDocumentIndexDict)
the_svdModel.computeSVD()
the_svdModel.outputModelInfo()

# svd the ww matrix
matrixDirectory = corpusDirectory+"/"+matrixDirectory1+"/"
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.importMatrixInfo(matrixDirectory)
the_tcMatrix.importTargetInfo(0,0)
the_tcMatrix.importContextInfo(0,0)
the_tcMatrix.importSummedMatrix(0,0,1,0)
the_tcMatrix.normalizeCoocMatrix(0)
the_tcMatrix.getCoocMatrixColumnInfo()
the_svdModel = svd.svdModel()
the_svdModel.initializeModel(matrixDirectory, "tcSVD", the_tcMatrix.coocMatrix, the_tcMatrix.subTargetIndexDict, the_tcMatrix.columnIndexDict)
the_svdModel.computeSVD()
the_svdModel.outputModelInfo()

# lda the wd matrix
#matrixDirectory = corpusDirectory+"/"+matrixDirectory1+"/"
#the_tdMatrix = tdMatrix.tdMatrix()
#the_tdMatrix.importMatrixInfo(matrixDirectory)
#the_tdMatrix.importTargetInfo(0,0)
#the_tdMatrix.importDocumentInfo(0,0)
#the_tdMatrix.importTargetDocumentMatrix()
#the_ldaModel = lda.ldaModel()
#the_ldaModel.initializeModel(matrixDirectory, "tdLDA", alphaList, betaList, numTopicsList, ldaIterations, randomSeed, 1, 0, 8, 8, the_tdMatrix.subTargetFreqs, the_tdMatrix.subTargetIndexDict, the_tdMatrix.subDocumentIndexDict)
#the_ldaModel.runModels()
#the_ldaModel.outputModelInfo()

# compute the wd svd similarities
svdDirectory = corpusDirectory+"/"+matrixDirectory1+"/"+"tdSVD/"
the_svdModel = svd.svdModel()
the_svdModel.importModelInfo(svdDirectory)
the_svdModel.importRowInfo(0,0)
the_svdModel.importColumnInfo()
for i in range(the_tdMatrix.numSubTargets-1):
    numDimensions = i+2
    the_svdModel.importRowSingularVectors(numDimensions)
    the_svdModel.normalizeRowSingularValues(0)
    the_svdModel.calculateAllRowSimilarities(1)
    the_svdModel.calculateAllRowSimilarities(2)
    the_svdModel.calculateAllRowSimilarities(4)

# compuate the ww svd similarities
svdDirectory = corpusDirectory+"/"+matrixDirectory1+"/"+"tcSVD/"
the_svdModel = svd.svdModel()
the_svdModel.importModelInfo(svdDirectory)
the_svdModel.importRowInfo(0,0)
the_svdModel.importColumnInfo()
for i in range(the_tcMatrix.numSubTargets-1):
    numDimensions = i+2
    the_svdModel.importRowSingularVectors(numDimensions)
    the_svdModel.normalizeRowSingularValues(0)
    the_svdModel.calculateAllRowSimilarities(1)
    the_svdModel.calculateAllRowSimilarities(2)
    the_svdModel.calculateAllRowSimilarities(4)
    
# compute all four neighborhoods