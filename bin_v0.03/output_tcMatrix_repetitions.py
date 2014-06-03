##############################################################################
matrixDirectory = 0                 # -m: path of the matrix directory
outputFile = "repetitions.txt"      # -o: name of the output file you want to create
targetInclusionFilename = 0         # -i: a file with a list of targets you want to include (all others in matrix will be excluded)
targetExclusionFilename = 0         # -e: a file with a list of targets you want to exclude (all others in matrix will be included)
windowSize = 0                      # -w: window size you want to use, if you want it to be smaller than the matrix's window size
##############################################################################
import sys
import sm_libs.scriptParams as params
import sm_libs.tcMatrix as tcMatrix

# process the script parameters
matrixDirectory, outputFile, targetInclusionFilename, targetExclusionFilename, windowSize = params.outputTCMatrixRepetitions(sys.argv[1:], matrixDirectory, outputFile, targetInclusionFilename, targetExclusionFilename, windowSize)

# import the matrix data
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.importMatrixInfo(matrixDirectory)
the_tcMatrix.importTargetInfo(targetInclusionFilename, targetExclusionFilename)
the_tcMatrix.importContextInfo(0, 0)
the_tcMatrix.importSummedMatrix(2, windowSize, 1, 0)

# calculate and output the repetitions
the_tcMatrix.outputRepetitions(outputFile)

