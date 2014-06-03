##############################################################################
# default parameters
matrixDirectory = 0                     # -m    the directory containing the matrix data
outputDirectory = "sentiments"          # -o    the name of the output directory that will be created
targetFilename = 0                      # -T
featureFilename = 0                     # -F
documentFilename = 0                    # -D
normalizationMethod = 1                 # -N    how to normalize the vectors. See documentation for choices (1: row sum; 2: row length; 13 PosPMI; 14: Coals)

##############################################################################
# import python libraries
import sys
import sm_libs.tcMatrix as tcMatrix
import sm_libs.sentiments as sent
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
matrixDirectory, outputDirectory, targetFilename, featureFilename, documentFilename, normalizationMethod = params.calcSentiments(sys.argv[1:], matrixDirectory, outputDirectory, targetFilename, featureFilename, documentFilename, normalizationMethod)

# import the matrix data
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.importMatrixInfo(matrixDirectory)
the_tcMatrix.importTargetInfo(0, 0)
the_tcMatrix.importContextInfo(0, 0)


# import the matrix data
the_sentiments = sent.sentimentModel()
the_sentiments.initializeModel(matrixDirectory, outputDirectory, targetFilename, featureFilename, documentFilename, normalizationMethod)
the_sentiments.getTargetList(the_tcMatrix)
the_sentiments.getFeatureList(the_tcMatrix)

