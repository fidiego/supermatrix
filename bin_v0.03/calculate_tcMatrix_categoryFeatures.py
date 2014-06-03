##############################################################################
# default parameters
matrixDirectory = 0                     # -m    the directory containing the matrix data
targetInclusionFile = 0                 # -i    a file containing a list of targets to include, if you dont want to use all targets in the matrix
targetExclusionFile = 0                 # -e    a file containing a list of targets to exclude, if you dont want to use all the targets in the matrix
contextInclusionFile = 0                # -I    a file containing a list of targets to include, if you dont want to use all targets in the matrix
contextExclusionFile = 0                # -E    a file containing a list of targets to exclude, if you dont want to use all the targets in the matrix
normalizationMethod = 1                 # -N    how to normalize the vectors. See documentation for choices (1: row sum; 2: row length; 13 PosPMI; 14: Coals)
categoryFilename = 0                    # -c    the file that contains a list with two columns: 1) the categories, 2) the words
outputDirectory = 0                     # -o    the name of the output directory that will be created
##############################################################################
# import python libraries
import sys
import sm_libs.tcMatrix as tcMatrix
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
matrixDirectory, targetInclusionFile, targetExclusionFile, contextInclusionFile, contextExclusionFile, normalizationMethod, categoryFilename, outputDirectory = params.calcTCMatrixDiagFeats(sys.argv[1:], matrixDirectory, targetInclusionFile, targetExclusionFile, contextInclusionFile, contextExclusionFile, normalizationMethod, categoryFilename, outputDirectory)

# import the matrix data
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.importMatrixInfo(matrixDirectory)
the_tcMatrix.importTargetInfo(targetInclusionFile, targetExclusionFile)
the_tcMatrix.importContextInfo(contextInclusionFile, contextExclusionFile)
the_tcMatrix.importSummedMatrix(1, 0, 1, 0)

# normalize, calculate, and output similarities
the_tcMatrix.normalizeCoocMatrix(normalizationMethod)
the_tcMatrix.calculateCategoryFeatures(categoryFilename, outputDirectory)


