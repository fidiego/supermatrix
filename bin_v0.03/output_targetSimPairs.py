##############################################################################
# default parameters
pairFile = 0                            # -p    the file containing the list of word pairs
similarityFile = 0                      # -s    the file containing the similarity data
targetListIndexFile = 0                 # -t    the file that specifies the labels for each target index 
##############################################################################
# import python libraries
import sys
import sm_libs.simMatrix as simMatrix
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
pairFile, similarityFile, targetListIndexFile = params.outputTargetSimPairs(sys.argv[1:], pairFile, similarityFile, targetListIndexFile)

# import the information
the_simMatrix = simMatrix.simMatrix()
the_simMatrix.initExistingSimMatrix(similarityFile, targetListIndexFile)
the_simMatrix.importTargetInfo()
the_simMatrix.importSimilarityMatrix()
the_simMatrix.outputTargetSimPairs(pairFile)


