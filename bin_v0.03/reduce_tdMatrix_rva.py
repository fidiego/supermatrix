##############################################################################
matrixDirectory = 0                 # -m: location of wdMatrix. can be set at command line using -m
outputDirectory = 0                 # -o: name of output folder to be created. can be set using -o
rowInclusionFilename = 0            # -i: optional file containing a list of targets to use, if you want to use a subset of master list
rowExclusionFilename = 0            # -e: optional file containing a list of targets to NOT use, if you want to exclude them
columnInclusionFilename = 0         # -I: optional file containing a list of documents to use, if you want to use a subset of master list
columnExclusionFilename = 0         # -e: optional file containing a list of documents to NOT use, if you want to use a subset of master list
normalizationMethod = 0             # -N: normalization method of the cooc matrix. Items will be scaled so that lowest value is 1
randomVectorLength = 0              # -L: the length of the random vector that will be generated
randomVectorMean = 0                # -M: mean of the values in the random vector
randomVectorSD = 0                  # -S: standard deviation of the values in the random vector
randomSeed = 0                      # -R: random seed generator. If 0, the current system time will be used.
##############################################################################
import sys, getopt
import sm_libs.scriptParams as params
import sm_libs.normalizations as norm
import sm_libs.tdMatrix as tdMatrix
import sm_libs.rva as rva
##############################################################################

# process the command line arguments
matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, normalizationMethod, randomVectorLength, randomVectorMean, randomVectorSD, randomSeed = params.reduceTDMatrixRVA(sys.argv[1:], matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, normalizationMethod, randomVectorLength, randomVectorMean, randomVectorSD, randomSeed)

# import the target x document matrix data
the_tdMatrix = tdMatrix.tdMatrix()
the_tdMatrix.importMatrixInfo(matrixDirectory)
the_tdMatrix.importTargetInfo(rowInclusionFilename, rowExclusionFilename)
the_tdMatrix.importDocumentInfo(columnInclusionFilename, columnExclusionFilename)
the_tdMatrix.importTargetDocumentMatrix()
the_tdMatrix.normalizeTargetDocumentMatrix(normalizationMethod)

# run and output the svd
the_rvaModel = rva.rvaModel()
the_rvaModel.initializeModel(matrixDirectory, outputDirectory, the_tdMatrix.normalizedTargetDocumentMatrix, the_tdMatrix.subTargetIndexDict, the_tdMatrix.subDocumentIndexDict, randomSeed, randomVectorLength, randomVectorMean, randomVectorSD, normalizationMethod)

the_rvaModel.generateRandomVectors()
the_rvaModel.generateMemoryMatrix()
the_rvaModel.outputModelInfo()