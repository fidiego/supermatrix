import sys, getopt
import sm_libs.scriptParams as params
import sm_libs.tdMatrix as tdMatrix
import sm_libs.lda as lda
##############################################################################
matrixDirectory = 0                 # -m: location of wdMatrix. can be set at command line using -m
outputDirectory = 0                 # -o: name of output folder to be created. can be set using -o

alphaList = [.05]                    # -A: if you want to test a range of alpha values, use a comma separated list, e.g. [0.01,0.1,1]
betaList = [.1]                    # -B: if you want to test a range of beta values, use a comma separated list, e.g. [0.01,0.1]
numTopicsList = [1000]                 # -T: if you want to test a range of topic values, use a comma separated list, e.g. [5,10,15]

numIterations = 500                 # -N: number of passes through the corpus
randomSeed = 10                     # -S: initial random number generator seed value. If zero, will use the system clock
numChains = 1                       # -C: number of different randomly initialized runs

rowInclusionFilename = 0            # -i: optional file containing a list of targets to use, if you want to use a subset of master list
rowExclusionFilename = 0            # -e: optional file containing a list of targets to NOT use, if you want to exclude them
columnInclusionFilename = 0         # -I: optional file containing a list of documents to use, if you want to use a subset of master list
columnExclusionFilename = 0         # -E: optional file containing a list of documents to NOT use, if you want to use a subset of master list

trackHistories = 0                  # -h: whether to print topic assignments every n iterations. if n = zero: no; if n > 0: will output each n iterations
numRowAssignmentOutputs = 30        # -x: number of targets to output in the topic Assignments file
numColumnAssignmentOutputs = 30		# -y: nonfunctioning

# process the command line arguments
matrixDirectory, outputDirectory, alphaList, betaList, numTopicsList, numIterations, randomSeed, numChains, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, trackHistories, numRowAssignmentOutputs = params.reduceTDMatrixLDA(sys.argv[1:], matrixDirectory, outputDirectory, alphaList, betaList, numTopicsList, numIterations, randomSeed, numChains, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, trackHistories, numRowAssignmentOutputs)

# import the target x document matrix data
the_tdMatrix = tdMatrix.tdMatrix()
the_tdMatrix.importMatrixInfo(matrixDirectory)
the_tdMatrix.importTargetInfo(rowInclusionFilename, rowExclusionFilename)
the_tdMatrix.importDocumentInfo(columnInclusionFilename, columnExclusionFilename)
the_tdMatrix.importTargetDocumentMatrix()

# run and output the lda
the_ldaModel = lda.ldaModel()
the_ldaModel.initializeModel(matrixDirectory, outputDirectory, alphaList, betaList, numTopicsList, numIterations, randomSeed, numChains, trackHistories, numRowAssignmentOutputs, numColumnAssignmentOutputs, the_tdMatrix.subTargetFreqs, the_tdMatrix.subTargetIndexDict, the_tdMatrix.subDocumentIndexDict)
the_ldaModel.runModels()
the_ldaModel.outputModelInfo()