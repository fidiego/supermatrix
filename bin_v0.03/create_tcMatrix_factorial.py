import sys
import sm_libs.scriptParams as params
import sm_libs.tcMatrix as tcMatrix
##############################################################################
corpusDirectory = 0             # -c: the directory containing the corpus information
matrixDirectory = "tcMatrix"    # -m: the directory that will be created and where the matrix info will be stored
targetFilename = 0              # -T: the path of the file containing the list of targets to use
contextFilename = 0             # -C: the path of the file containing the list of contexts to use
documentFilename = 0            # -D: the path of the file containing the (sub)list of documents to use
windowSize = 0                  # -W: the window size over which co-occurrences will be counted
distinctDocs = 0                # -d: whether or not to count co-occurrences separately for each document
##############################################################################

# process the script parameters
corpusDirectory, matrixDirectory, targetFilename, contextFilename, documentFilename, windowSize, distinctDocs = params.createTCMatrix(sys.argv[1:], corpusDirectory, matrixDirectory, targetFilename, contextFilename, documentFilename, windowSize, distinctDocs)

# import corpus info, target list, and document list
the_tcMatrix = tcMatrix.tcMatrix()
the_tcMatrix.initializeMatrix(corpusDirectory, matrixDirectory, windowSize, distinctDocs)
the_tcMatrix.getTargetList(targetFilename)
the_tcMatrix.getContextList(contextFilename)
the_tcMatrix.getDocumentList(documentFilename)

# count the corpus
the_tcMatrix.processCorpus()

# output the data
the_tcMatrix.outputDocumentInfo()
the_tcMatrix.outputTargetInfo()
the_tcMatrix.outputContextInfo()
the_tcMatrix.outputTargetDocumentCountMatrix()
the_tcMatrix.outputContextDocumentCountMatrix()
the_tcMatrix.outputSummedCoocMatrix()
the_tcMatrix.outputMatrixInfo()