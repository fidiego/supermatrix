##############################################################################
# default parameters
rvaDirectory = 0                        # -r    the directory containing the svd model data
rowInclusionFilename = 0                # -i    a file containing a list of rows you want to include, if you dont want to use all rows in the rva object
rowExclusionFilename = 0                # -e    a file containing a list of rows you want to exclude, if you dont want to use all rows in the rva object
normalizationMethod = 0                 # -N    how to normalize the vectors. See documentation for choices (1: row sum; 2: row length; 13 PosPMI; 14: Coals)
similarityMetric = 1                    # -M    similarity metric. See documentation for choices (1: cosine, 2: cityblock, 3: euclidean, 4: correlation)
##############################################################################
# import python libraries
import sys
import sm_libs.rva as rva
import sm_libs.scriptParams as params
import sm_libs.simMatrix as simMatrix
##############################################################################

# process script parameters
rvaDirectory, rowInclusionFilename, rowExclusionFilename, normalizationMethod, similarityMetric = params.calcRVASims(sys.argv[1:], rvaDirectory, rowInclusionFilename, rowExclusionFilename, normalizationMethod, similarityMetric)

# import the matrix data
the_rvaModel = rva.rvaModel()
the_rvaModel.importModelInfo(rvaDirectory)
the_rvaModel.importRowInfo(rowInclusionFilename, rowExclusionFilename)
the_rvaModel.importMemoryMatrix()

# normalize, calculate, and output similarities
the_rvaModel.normalizeMemoryMatrix(normalizationMethod)
the_rvaModel.calculateAllRowSimilarities(similarityMetric)
