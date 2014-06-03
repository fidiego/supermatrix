##############################################################################
# default parameters
matrixDirectory = 0                     # -m    the directory containing the chain data
targetInclusionFile = 0                 # -i    a file containing a list of targets to include, if you dont want to use all targets in the matrix
targetExclusionFile = 0                 # -e    a file containing a list of targets to exclude, if you dont want to use all the targets in the matrix
documentInclusionFile = 0               # -I    a file containing a list of documents to include, if you dont want to use all documents in the matrix
documentExclusionFile = 0               # -E    a file containing a list of documents to exclude, if you dont want to use all documents in the matrix
normalizationMethod = 1                 # -N    how to normalize the vectors. See documentation for choices (1: row sum; 2: row length; 13 PosPMI; 14: Coals)
similarityMetric = 0                    # -M    similarity metric. See documentation for choices (1: cosine, 2: cityblock, 3: euclidean, 4: correlation)
##############################################################################
# import python libraries
import sys
import sm_libs.tdMatrix as tdMatrix
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
matrixDirectory, targetInclusionFile, targetExclusionFile, documentInclusionFile, documentExclusionFile, normalizationMethod, similarityMetric = params.calcTDMatrixSims(sys.argv[1:], matrixDirectory, targetInclusionFile, targetExclusionFile, documentInclusionFile, documentExclusionFile, normalizationMethod, similarityMetric)

# import the matrix data
the_tdMatrix = tdMatrix.tdMatrix()
the_tdMatrix.importMatrixInfo(matrixDirectory)
the_tdMatrix.importTargetInfo(targetInclusionFile,targetExclusionFile)
the_tdMatrix.importDocumentInfo(documentInclusionFile,documentExclusionFile)
the_tdMatrix.importTargetDocumentMatrix()

# normalize, calculate, and output similarities
the_tdMatrix.normalizeTargetDocumentMatrix(normalizationMethod)
the_tdMatrix.calculateAllSimilarities(similarityMetric)