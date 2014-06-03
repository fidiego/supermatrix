##############################################################################
# default parameters
matrixDirectory = 0                     # -m    the directory containing the matrix data
targetInclusionFile = 0                 # -i    a file containing a list of targets to include, if you dont want to use all targets in the matrix
targetExclusionFile = 0                 # -e    a file containing a list of targets to exclude, if you dont want to use all the targets in the matrix
contextInclusionFile = 0                # -I    a file containing a list of targets to include, if you dont want to use all targets in the matrix
contextExclusionFile = 0                # -E    a file containing a list of targets to exclude, if you dont want to use all the targets in the matrix
directionType = 1                       # -D    how to deal with direction: 0) concatenate F&B, 1) sum F&B, 2) F only, 3) B only
windowSize = 0                          # -S    how far away to count co-occurrences (0: max - whatever the matrix max was, if S > max, will use max)
collapseWindow = 1                      # -C    the window type you want to use: 0) 
windowWeighting = 0                     # -W    the window weighting you want to use: 0) flat, 1) linearly descending
normalizationMethod = 1                 # -N    how to normalize the vectors. See documentation for choices (1: row sum; 2: row length; 13 PosPMI; 14: Coals)
similarityMetric = 0                    # -M    similarity metric. See documentation for choices (1: cosine, 2: cityblock, 3: euclidean, 4: correlation)
##############################################################################
# import python libraries
import sys
import sm_libs.tcMatrix as tcMatrix
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
matrixDirectory, targetInclusionFile, targetExclusionFile, contextInclusionFile, contextExclusionFile, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod, similarityMetric = params.calcTCMatrixSims(sys.argv[1:], matrixDirectory, targetInclusionFile, targetExclusionFile, contextInclusionFile, contextExclusionFile, directionType, windowSize, collapseWindow, windowWeighting, normalizationMethod, similarityMetric)

# import the matrix data
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.importMatrixInfo(matrixDirectory)
the_tcMatrix.importTargetInfo(targetInclusionFile, targetExclusionFile)
the_tcMatrix.importContextInfo(contextInclusionFile, contextExclusionFile)
the_tcMatrix.importSummedMatrix(directionType, windowSize, collapseWindow, windowWeighting)

# normalize, calculate, and output similarities
the_tcMatrix.normalizeCoocMatrix(normalizationMethod)
the_tcMatrix.calculateAllSimilarities(similarityMetric)
