##############################################################################
# default parameters
matrixDirectory = 0                     # -m    the directory containing the matrix data
pairFile = 0                            # -p    a file containing a list of targets to include, if you dont want to use all targets in the matrix
outputFilename = "assocation_pairs.txt" # -o    name of the output file
directionType = 1                       # -D    how to deal with direction: 1) sum F&B, 2) F only, 3) B only
windowSize = 0                          # -S    how far away to count co-occurrences (0: max - whatever the matrix max was, if S > max, will use max)
windowWeighting = 0                     # -W    the window weighting you want to use: 0) flat, 1) linearly descending
normalizationMethod = 1                 # -N    how to normalize the vectors. See documentation for choices (1: row sum; 2: row length; 13 PosPMI; 14: Coals)
outputAsProbabilityDistribution = 0     # -P    whether to output the value divided by the sum of all that word's possible values
##############################################################################
# import python libraries
import sys
import sm_libs.tcMatrix as tcMatrix
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
matrixDirectory, pairFile, outputFilename, directionType, windowSize, windowWeighting, normalizationMethod, outputAsProbabilityDistribution = params.outputTargetPairAssociations(sys.argv[1:], matrixDirectory, pairFile, outputFilename, directionType, windowSize, windowWeighting, normalizationMethod, outputAsProbabilityDistribution)

# import the matrix data
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.importMatrixInfo(matrixDirectory)
the_tcMatrix.importTargetInfo(0, 0)
the_tcMatrix.importContextInfo(0, 0)
the_tcMatrix.importSummedMatrix(directionType, windowSize, 1, windowWeighting)

# normalize, calculate, and output similarities
the_tcMatrix.normalizeCoocMatrix(normalizationMethod)
if outputAsProbabilityDistribution:
    the_tcMatrix.normalizeCoocMatrix(1)
the_tcMatrix.outputTargetPairAssociations(outputFilename, pairFile)
