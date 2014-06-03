##############################################################################
# default parameters
chainDirectory = 0                      # -c    the directory containing the chain data
normalizationMethod = 1                 # -N    how to normalize the vectors. See documentation for choices (1: row sum; 2: row length; 13 PosPMI; 14: Coals)
similarityMetric = 0                    # -M    similarity metric. See documentation for choices (1: cosine, 2: cityblock, 3: euclidean, 4: correlation)
rowInclusionFile = 0                    # -i    file containing a list of subtargets to include, if you dont want to use the entire list
rowExclusionFile = 0                    # -e    file containing a list of subtargets to exclude, if you dont want to use the entire list
##############################################################################
# import python libraries
import sys
import sm_libs.lda as lda
import sm_libs.scriptParams as params
import sm_libs.simMatrix as simMatrix
##############################################################################

# process script parameters
chainDirectory, normalizationMethod, similarityMetric, rowInclusionFile, rowExclusionFile = params.calcLDASims(sys.argv[1:], chainDirectory, normalizationMethod, similarityMetric, rowInclusionFile, rowExclusionFile)

# import the matrix data
the_ldaModel = lda.ldaModel()
the_ldaModel.importChainInfo(chainDirectory)
the_ldaModel.importRowInfo(rowInclusionFile, rowExclusionFile)
the_ldaModel.importRowTopicMatrix()

# normalize, calculate, and output similarities
the_ldaModel.normalizeRowTopicMatrix(normalizationMethod)
the_ldaModel.calculateAllSimilarities(similarityMetric)