##############################################################################
# define and set program parameters
corpusDirectory = 0                 # -c: the path of the directory containing the corpus.
outputFilename = 0                  # -o: the name of the document list file that will be created
typeThreshold = 0                   # -t: the type frequency threshold; documents with less than this many word types will be excluded
tokenThreshold = 0                  # -T: the token frequency threshold; documents with less than this many word tokens will be excluded
numDocumentsThreshold = 0           # -n: the maximum number of documents to be retained (in frequency order)
includeListFilename = 0             # -i: the path of the file that is a list of targets to force include
excludeListFilename = 0             # -e: the path of the file that is a list of targets to force exclude
##############################################################################
# import python libraries
import sys, getopt
import sm_libs.scriptParams as params
import sm_libs.corpora as corpora
##############################################################################

# process command line arguments
corpusDirectory, outputFilename, typeThreshold, tokenThreshold, numDocumentsThreshold, includeListFilename, excludeListFilename = params.corpGetSubDocuments(sys.argv[1:], corpusDirectory, outputFilename, typeThreshold, tokenThreshold, numDocumentsThreshold, includeListFilename, excludeListFilename)

# create and initialize a corpus object, import corpus info
theCorpus = corpora.corpus()
theCorpus.importCorpusInfo(corpusDirectory)
theCorpus.importTargetInfo()
theCorpus.importDocumentInfo()

# create and initialize a corpus object, import corpus info
theCorpus.outputDocumentSubList(outputFilename, typeThreshold, tokenThreshold, numDocumentsThreshold, includeListFilename, excludeListFilename)
