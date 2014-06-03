##############################################################################
matrixDirectory = 0                 # -m: location of wdMatrix. can be set at command line using -m
outputDirectory = 0                 # -o: name of output folder to be created. can be set using -o
normalizationMethod = 11            # -N: the normalization method; see documentation for options (11: logentropy)

rowInclusionFilename = 0            # -i: optional file containing a list of targets to use, if you want to use a subset of master list
rowExclusionFilename = 0            # -e: optional file containing a list of targets to NOT use, if you want to exclude them
columnInclusionFilename = 0         # -I: optional file containing a list of documents to use, if you want to use a subset of master list
columnExclusionFilename = 0         # -E: optional file containing a list of documents to NOT use, if you want to use a subset of master list
##############################################################################
import sys, getopt
import sm_libs.scriptParams as params
import sm_libs.normalizations as norm
import sm_libs.tdMatrix as tdMatrix
import sm_libs.svd as svd
##############################################################################

# process the command line arguments
matrixDirectory, outputDirectory, normalizationMethod, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename = params.reduceTDMatrixSVD(sys.argv[1:], matrixDirectory, outputDirectory, normalizationMethod, rowInclusionFilename, rowExclusionFilename, columnInclusionFilename, columnExclusionFilename)

# import the target x document matrix data
the_tdMatrix = tdMatrix.tdMatrix()
the_tdMatrix.importMatrixInfo(matrixDirectory)
the_tdMatrix.importTargetInfo(rowInclusionFilename, rowExclusionFilename)
the_tdMatrix.importDocumentInfo(columnInclusionFilename, columnExclusionFilename)
the_tdMatrix.importTargetDocumentMatrix()

the_tdMatrix.normalizeTargetDocumentMatrix(normalizationMethod)

# run and output the svd
the_svdModel = svd.svdModel()
the_svdModel.initializeModel(matrixDirectory, outputDirectory, the_tdMatrix.normalizedTargetDocumentMatrix, the_tdMatrix.subTargetIndexDict, the_tdMatrix.subDocumentIndexDict)

the_svdModel.computeSVD()
the_svdModel.outputModelInfo()