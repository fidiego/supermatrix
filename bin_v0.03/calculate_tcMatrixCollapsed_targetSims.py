##############################################################################
# default parameters
matrixDirectory = 0                     # -m    the directory containing the matrix data
targetInclusionFile = 0                 # -i    a file containing a list of targets to include, if you dont want to use all targets in the matrix
targetExclusionFile = 0                 # -e    a file containing a list of targets to exclude, if you dont want to use all the targets in the matrix
normalizationMethod = 1                 # -N    how to normalize the vectors. See documentation for choices (1: row sum; 2: row length; 13 PosPMI; 14: Coals)
similarityMetric = 0                    # -M    similarity metric. See documentation for choices (1: cosine, 2: cityblock, 3: euclidean, 4: correlation)
##############################################################################
# import python libraries
import sys
import sm_libs.tcMatrix as tcMatrix
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
matrixDirectory, targetInclusionFile, targetExclusionFile, normalizationMethod, similarityMetric = params.calcTCMatrixCollapsedSims(sys.argv[1:], matrixDirectory, targetInclusionFile, targetExclusionFile, normalizationMethod, similarityMetric)


# import the matrix data
the_tcMatrix = tcMatrix.tcMatrix()

the_tcMatrix.matrixDirectory = matrixDirectory
the_tcMatrix.directionType = 0
the_tcMatrix.subWindowSize = 12
the_tcMatrix.collapseWindow = 1
the_tcMatrix.windowWeighting = 0

the_tcMatrix.importTargetInfo(targetInclusionFile, targetExclusionFile)
the_tcMatrix.subContextList = the_tcMatrix.subTargetList
the_tcMatrix.subContextDict = the_tcMatrix.subTargetDict
the_tcMatrix.subContextIndexDict = the_tcMatrix.subTargetIndexDict

the_tcMatrix.importCollapsedMatrix()

# normalize, calculate, and output similarities
the_tcMatrix.normalizeCoocMatrix(normalizationMethod)
the_tcMatrix.calculateAllSimilarities(similarityMetric)
