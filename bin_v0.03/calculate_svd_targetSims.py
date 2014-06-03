##############################################################################
# default parameters
svdDirectory = 0                        # -s    the directory containing the svd model data
numDimensions = 0                       # -n    number of singular value dimensions to retain
rowInclusionList = 0                    # -i    a file containing a list of rows you want to include, if you dont want to use all rows in the svd object
rowExclusionList = 0                    # -e    a file containing a list of rows you want to exclude, if you dont want to use all rows in the svd object
normalizationMethod = 0                 # -N    how to normalize the vectors. See documentation for choices (1: row sum; 2: row length; 13 PosPMI; 14: Coals)
similarityMetric = 0                    # -M    similarity metric. See documentation for choices (1: cosine, 2: cityblock, 3: euclidean, 4: correlation)
##############################################################################
# import python libraries
import sys
import sm_libs.svd as svd
import sm_libs.scriptParams as params
import sm_libs.simMatrix as simMatrix
##############################################################################

# process script parameters
svdDirectory, numDimensions, rowInclusionList, rowExclusionList, normalizationMethod, similarityMetric = params.calcSVDSims(sys.argv[1:], svdDirectory, numDimensions, rowInclusionList, rowExclusionList, normalizationMethod, similarityMetric)

# import the matrix data
the_svdModel = svd.svdModel()
the_svdModel.importModelInfo(svdDirectory)
the_svdModel.importRowInfo(rowInclusionList, rowExclusionList)
the_svdModel.importColumnInfo()
the_svdModel.importRowSingularVectors(numDimensions)

# normalize, calculate, and output similarities
the_svdModel.normalizeRowSingularValues(normalizationMethod)
the_svdModel.calculateAllRowSimilarities(similarityMetric)
