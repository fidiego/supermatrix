import sys
import sm_libs.scriptParams as params
import sm_libs.tcMatrix as tcMatrix
##############################################################################
corpusDirectory = 0             # -c: the directory containing the corpus information
matrixDirectory = "tcMatrix"    # -m: the directory that will be created and where the matrix info will be stored
targetFilename = 0              # -T: the path of the file containing the list of targets to use
documentFilename = 0            # -D: the path of the file containing the (sub)list of documents to use
windowSize = 0                  # -W: the window size over which co-occurrences will be counted
##############################################################################

# process the script parameters
corpusDirectory, matrixDirectory, targetFilename, documentFilename, windowSize = params.createCollapsedTCMatrix(sys.argv[1:], corpusDirectory, matrixDirectory, targetFilename, documentFilename, windowSize)

# import corpus info, target list, and document list
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.initializeMatrix(corpusDirectory, matrixDirectory, windowSize, 0)
the_tcMatrix.getTargetList(targetFilename)
the_tcMatrix.getDocumentList(documentFilename)

# count the corpus
the_tcMatrix.processCorpusCollapsed()

# output the data
the_tcMatrix.outputTargetInfo()
the_tcMatrix.outputCollapsedCoocMatrix()
the_tcMatrix.outputCollapsedMatrixInfo()