##############################################################################
# default parameters
similarityFile = 0                      # -s    the file containing the similarity data
targetListIndexFile = 0                 # -t    the file that specifies the labels for each target index 
numNeighbors = 0                        # -n    the number of neighbors you want to output
##############################################################################
# import python libraries
import sys
import sm_libs.simMatrix as simMatrix
import sm_libs.scriptParams as params
##############################################################################

# process script parameters
similarityFile, targetListIndexFile, numNeighbors = params.outputSimNeighbors(sys.argv[1:], similarityFile, targetListIndexFile, numNeighbors)

# import the information
the_simMatrix = simMatrix.simMatrix()
the_simMatrix.initExistingSimMatrix(similarityFile, targetListIndexFile)
the_simMatrix.importTargetInfo()
the_simMatrix.importSimilarityMatrix()
the_simMatrix.outputNeighbors(numNeighbors)


