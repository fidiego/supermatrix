##############################################################################
matrixDirectory = 0                 # -m  location of Matrix. can be set at command line using -m
outputDirectory = 0                 # -o  name of output folder to be created. can be set using -o
rowInclusionFilename = 0            # -i  optional file containing a list of targets to use, if you want to use a subset of master list
rowExclusionFilename = 0            # -e  optional file containing a list of targets to NOT use, if you want to exclude them
columnInclusionFilename = 0         # -I  optional file containing a list of documents to use, if you want to use a subset of master list
columnExclusionFilename = 0         # -E  optional file containing a list of documents to NOT use, if you want to use a subset of master list
directionType = 0                   # -D  how to deal with direction: 0) concatenate F&B, 1) sum F&B, 2) F only, 3) B only
windowSize = 0                      # -S  how far away to count co-occurrences (0: max - whatever the matrix max was, if S > max, will use max)
collapseWindow = 1                  # -C  the window type you want to use: 0) Don't collapse window 1) CollapseWindow
windowWeighting = 0                 # -W  the window weighting you want to use: 0) flat, 1) linearly descending
normalizationMethod = 1             # -N: the normalization method; see documentation for options (13: posPMI)
##############################################################################
import sys
import sm_libs.scriptParams as params
import sm_libs.normalizations as norm
import sm_libs.tcMatrix as tcMatrix
import sm_libs.svd as svd
##############################################################################

# process the command line arguments
matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod = params.reduceTCMatrixSVD(sys.argv[1:], matrixDirectory, outputDirectory, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod)

# import the target x document matrix data
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.importMatrixInfo(matrixDirectory)
the_tcMatrix.importTargetInfo(rowInclusionFilename, rowExclusionFilename)
the_tcMatrix.importContextInfo(columnInclusionFilename, columnExclusionFilename)
the_tcMatrix.importSummedMatrix(directionType, windowSize, collapseWindow, windowWeighting)

# normalize the matrix
the_tcMatrix.normalizeCoocMatrix(normalizationMethod)

# run and output the svd
the_tcMatrix.getCoocMatrixColumnInfo()
the_svdModel = svd.svdModel()
the_svdModel.initializeModel(matrixDirectory, outputDirectory, the_tcMatrix.coocMatrix, the_tcMatrix.subTargetIndexDict, the_tcMatrix.columnIndexDict)
the_svdModel.computeSVD()
the_svdModel.outputModelInfo()