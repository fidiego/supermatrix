##############################################################################
corpusDirectory = 0             # -c: the directory containing the corpus information
matrixDirectory = "tdMatrix"    # -m: the directory that will be created and where the matrix info will be stored
targetFilename = 0              # -T: the path of the file containing the list of targets to use
documentFilename = 0            # -D: the path of the file containing the list of documents to use
##############################################################################
import sys
import sm_libs.scriptParams as params
import sm_libs.tdMatrix as tdMatrix
##############################################################################

# process the script parameters
corpusDirectory, matrixDirectory, targetFilename, documentFilename = params.createTDMatrix(sys.argv[1:], corpusDirectory, matrixDirectory, targetFilename, documentFilename)

# import corpus info, target list, and document list
the_tdMatrix = tdMatrix.tdMatrix()
the_tdMatrix.initializeMatrix(corpusDirectory, matrixDirectory)
the_tdMatrix.getTargetList(targetFilename)
the_tdMatrix.getDocumentList(documentFilename)

# count the corpus
the_tdMatrix.processCorpus()

# output the data
the_tdMatrix.outputDocumentInfo()
the_tdMatrix.outputTargetInfo()
the_tdMatrix.outputTargetDocumentCountMatrix()
the_tdMatrix.outputMatrixInfo()

